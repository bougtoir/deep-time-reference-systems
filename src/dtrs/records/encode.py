"""Encoders for the five benchmark representations (A, B, BR, C, D, E)."""

from __future__ import annotations

import copy
import hashlib
import json

import numpy as np

from .schema import SCHEMA_NAME, SCHEMA_VERSION

REPRESENTATIONS = ("A", "B", "BR", "C", "D", "E")

AXIS_VECTORS = {
    "geocentricX": np.array([1.0, 0.0, 0.0]),
    "geocentricY": np.array([0.0, 1.0, 0.0]),
    "geocentricZ": np.array([0.0, 0.0, 1.0]),
}


def axis_vector(direction: str) -> np.ndarray:
    if direction.startswith("-"):
        return -AXIS_VECTORS[direction[1:]]
    return AXIS_VECTORS[direction]


def rotation_about(axis: np.ndarray, angle_radians: float) -> np.ndarray:
    axis = axis / np.linalg.norm(axis)
    k = np.array([[0, -axis[2], axis[1]], [axis[2], 0, -axis[0]], [-axis[1], axis[0], 0]])
    return np.eye(3) + np.sin(angle_radians) * k + (1 - np.cos(angle_radians)) * k @ k


def convention(name: str) -> tuple[list[str], np.ndarray]:
    """Return (axes, storage matrix S) such that stored = frame @ S.T."""
    if name == "standard":
        return ["geocentricX", "geocentricY", "geocentricZ"], np.eye(3)
    if name == "left_handed":
        return ["geocentricX", "-geocentricY", "geocentricZ"], np.diag([1.0, -1.0, 1.0])
    if name == "axis_swapped":
        return ["geocentricY", "geocentricX", "geocentricZ"], np.array(
            [[0.0, 1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0]]
        )
    if name == "plate_fixed_rotated":
        pole = np.array([np.cos(np.radians(50.0)) * np.cos(np.radians(-100.0)),
                         np.cos(np.radians(50.0)) * np.sin(np.radians(-100.0)),
                         np.sin(np.radians(50.0))])
        return ["geocentricX", "geocentricY", "geocentricZ"], rotation_about(pole, np.radians(30.0))
    raise ValueError(f"unknown convention {name}")


def axes_matrix(axes: list[str]) -> np.ndarray:
    """Matrix A with stored = frame @ A.T for a signed-permutation axis list."""
    return np.vstack([axis_vector(direction) for direction in axes])


def canonical_hash(payload: object) -> str:
    text = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def coordinates_hash(record: dict) -> str:
    return canonical_hash(
        {
            "coordinates": record.get("coordinates"),
            "reference_system": record.get("reference_system"),
        }
    )


def coordinate_values_hash(record: dict) -> str:
    return canonical_hash({"values": (record.get("coordinates") or {}).get("values")})


def relations_hash(record: dict) -> str:
    return canonical_hash({"relations": record.get("relations")})


def geocentric_latitude_longitude(points: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    radius = np.linalg.norm(points, axis=1)
    return np.arcsin(points[:, 2] / radius), np.arctan2(points[:, 1], points[:, 0])


def chirality_sign(points: np.ndarray, triple: tuple[int, int, int], axis: np.ndarray) -> int:
    i, j, k = triple
    value = np.linalg.det(np.vstack([points[j] - points[i], points[k] - points[i], axis]))
    return 1 if value > 0 else -1


def choose_triple(points: np.ndarray) -> tuple[int, int, int]:
    axis = np.array([0.0, 0.0, 1.0])
    best, best_value = (0, 1, 2), 0.0
    n = len(points)
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                value = abs(np.linalg.det(np.vstack([points[j] - points[i], points[k] - points[i], axis])))
                if value > best_value:
                    best, best_value = (i, j, k), value
    return best


def residual_group(anchors: dict | None, complete: bool) -> str | None:
    if not complete:
        return None
    anchors = anchors or {}
    if "origin" not in anchors:
        return None
    if "axis" not in anchors:
        return "O(3)"
    if "chirality" not in anchors:
        return "O(2)"
    if "meridian" not in anchors:
        return "SO(2)"
    return "I"


def declared_recoverability(record: dict) -> dict:
    relations = record.get("relations")
    n = len(record["entities"])
    complete = relations is not None and len(relations["edges"]) == n * (n - 1) // 2
    group = residual_group(record.get("anchors"), complete)
    has_rates = relations is not None and "rates_m_per_year" in relations
    task_states = {
        "T1": "unique" if relations is not None else "not_encoded_relationally",
        "T5": "unique" if has_rates else "not_encoded_relationally",
        "T2": {"O(2)": "unique", "SO(2)": "unique", "I": "unique"}.get(group, "non_identifiable"),
        "T3": {"O(2)": "unique_up_to_group", "SO(2)": "unique", "I": "unique"}.get(
            group, "non_identifiable"
        ),
        "T4": {"O(2)": "unique_up_to_group", "SO(2)": "unique_up_to_group", "I": "unique"}.get(
            group, "non_identifiable"
        ),
    }
    return {"residual_group": group or "undetermined", "tasks": task_states}


def build_record(
    frame_points: np.ndarray,
    velocities: np.ndarray,
    ids: list[str],
    labels: list[str],
    sigma: np.ndarray,
    representation: str,
    *,
    convention_name: str = "standard",
    reference_epoch: float = 2015.0,
    chirality_evidence: str = "independent_physical",
    meridian_entity: int | None = None,
    sources: list[dict] | None = None,
    software: str = "dtrs",
) -> dict:
    if representation not in REPRESENTATIONS:
        raise ValueError(representation)
    n = len(frame_points)
    record: dict = {
        "schema": SCHEMA_NAME,
        "schema_version": SCHEMA_VERSION,
        "record_id": f"itrf2020-slr-{n}-{representation}-{convention_name}",
        "representation": representation,
        "entities": [
            {"id": ids[i], "label": labels[i], "identifier_scheme": "IERS DOMES"} for i in range(n)
        ],
    }
    axes, storage = convention(convention_name)
    if representation in ("A", "B", "BR", "E"):
        stored = frame_points @ storage.T
        stored_velocity = velocities @ storage.T
        record["coordinates"] = {
            "values": np.round(stored, 4).tolist(),
            "velocities": np.round(stored_velocity, 5).tolist(),
            "standard_uncertainty_m": np.round(np.abs(sigma), 4).tolist(),
        }
        if representation == "A":
            record["coordinates"].pop("velocities")
    if representation in ("B", "BR", "E"):
        reference_system: dict = {
            "crs_id": f"ITRF2020 geocentric Cartesian ({convention_name} storage axes)",
            "frame": "ITRF2020",
            "axes": axes,
            "unit": "metre",
            "frame_reference_epoch": 2015.0,
            "coordinate_epoch": reference_epoch,
        }
        signed_permutation = axes_matrix(axes)
        residual = storage @ np.linalg.inv(signed_permutation)
        if not np.allclose(residual, np.eye(3)):
            reference_system["transformation_to_frame"] = {
                "method": "finite rotation (plate-fixed to ITRF2020)",
                "matrix": np.linalg.inv(residual).round(12).tolist(),
            }
        record["reference_system"] = reference_system
    if representation in ("C", "D", "E"):
        edges, rates = [], []
        for i in range(n):
            for j in range(i):
                difference = frame_points[i] - frame_points[j]
                distance = float(np.linalg.norm(difference))
                rate = float(difference @ (velocities[i] - velocities[j]) / distance)
                edges.append([i, j, round(distance, 4)])
                rates.append([i, j, round(rate, 6)])
        record["relations"] = {
            "kind": "euclidean_distance",
            "unit": "metre",
            "epoch": reference_epoch,
            "edges": edges,
            "rates_m_per_year": rates,
        }
        record["uncertainty"] = {
            "distance_standard_uncertainty_m": round(float(np.sqrt(2) * np.max(np.abs(sigma))), 4),
            "coverage_factor": 3.0,
        }
    if representation in ("D", "E"):
        latitude, longitude = geocentric_latitude_longitude(frame_points)
        triple = choose_triple(frame_points)
        meridian = int(np.argmin(np.abs(longitude))) if meridian_entity is None else meridian_entity
        record["anchors"] = {
            "origin": {
                "observable": "geocentric_distance_m",
                "values": np.round(np.linalg.norm(frame_points, axis=1), 4).tolist(),
                "evidence": "independent_physical",
            },
            "axis": {
                "observable": "geocentric_latitude_radians",
                "values": np.round(latitude, 12).tolist(),
                "standard_uncertainty_radians": 1e-9,
                "evidence": "independent_physical",
            },
            "chirality": {
                "triple": list(triple),
                "sign": chirality_sign(frame_points, triple, np.array([0.0, 0.0, 1.0])),
                "evidence": chirality_evidence,
            },
            "meridian": {
                "entity": meridian,
                "longitude_degrees": round(float(np.degrees(longitude[meridian])), 10),
                "evidence": "conventional_definition",
            },
        }
    if representation == "BR":
        record["redundant_reference_system"] = copy.deepcopy(record["reference_system"])
        stored_points = np.array(record["coordinates"]["values"])
        triple = choose_triple(frame_points)
        frame_view = to_frame(stored_points, record["reference_system"])
        record["digital_chirality"] = {
            "triple": list(triple),
            "sign": chirality_sign(frame_view, triple, np.array([0.0, 0.0, 1.0])),
            "evidence": "digital_copy",
        }
    if representation == "E":
        record["provenance"] = {
            "sources": sources or [],
            "software": software,
        }
    elif representation in ("B", "BR"):
        record["fixity"] = {"algorithm": "sha256", "scope": "coordinates.values"}
    refresh_derived(record)
    return record


def to_frame(stored: np.ndarray, reference_system: dict) -> np.ndarray:
    frame = stored @ axes_matrix(reference_system["axes"])
    transformation = reference_system.get("transformation_to_frame")
    if transformation is not None:
        frame = frame @ np.array(transformation["matrix"]).T
    return frame


def refresh_derived(record: dict) -> None:
    """Recompute hashes and declared recoverability as an exporting system would."""
    if record.get("representation") in ("C", "D", "E"):
        record["declared_recoverability"] = declared_recoverability(record)
    if "fixity" in record and "coordinates" in record:
        record["fixity"]["coordinate_values_sha256"] = coordinate_values_hash(record)
    if "provenance" in record:
        if "coordinates" in record:
            record["provenance"]["coordinates_sha256"] = coordinates_hash(record)
        if "relations" in record:
            record["provenance"]["relations_sha256"] = relations_hash(record)
