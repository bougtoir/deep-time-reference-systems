"""Decoders mapping a (possibly damaged) record to per-task recoverability states."""

from __future__ import annotations

from dataclasses import dataclass, field
from math import erf, sqrt

import numpy as np

from dtrs.geometry.core import classical_mds

from .encode import chirality_sign, to_frame
from .validate import validate

DISTANCE_TASKS = ("T1", "T5")
DIRECTION_TASKS = ("T2", "T3", "T4")


@dataclass
class Query:
    reference_epoch: float
    comparison_epoch: float
    pairs: list[tuple[str, str]]
    sites: list[str]


@dataclass
class Answer:
    task: str
    item: str
    state: str
    value: float = float("nan")
    probability: float = float("nan")
    group: str = ""
    candidates: tuple = field(default_factory=tuple)


def _wrap(angle: np.ndarray | float) -> np.ndarray | float:
    return (np.asarray(angle) + np.pi) % (2 * np.pi) - np.pi


def _items(query: Query):
    for task in ("T1", "T2", "T3", "T5"):
        for a, b in query.pairs:
            yield task, f"{a}|{b}", (a, b)
    for site in query.sites:
        yield "T4", site, (site,)


def _all(query: Query, state: str) -> list[Answer]:
    return [Answer(task, item, state) for task, item, _ in _items(query)]


def _index_map(record: dict, first_match: bool) -> tuple[dict[str, int], set[str]]:
    ids = [entity["id"] for entity in record.get("entities", [])]
    mapping: dict[str, int] = {}
    for index, identifier in enumerate(ids):
        mapping.setdefault(identifier, index)
    duplicates = set() if first_match else {i for i in ids if ids.count(i) > 1}
    return mapping, duplicates


def _point_answers(points, velocities, mapping, query, *, distance_ok, velocity_ok, direction_ok):
    out: dict[tuple[str, str], tuple[str, float]] = {}
    latitude = np.arcsin(points[:, 2] / np.linalg.norm(points, axis=1))
    longitude = np.arctan2(points[:, 1], points[:, 0])
    dt = query.comparison_epoch - query.reference_epoch
    for task, item, keys in _items(query):
        if any(key not in mapping for key in keys):
            out[(task, item)] = ("non_identifiable", np.nan)
            continue
        idx = [mapping[key] for key in keys]
        if task == "T1":
            value = float(np.linalg.norm(points[idx[0]] - points[idx[1]]))
            out[(task, item)] = ("unique", value) if distance_ok else ("non_identifiable", np.nan)
        elif task == "T5":
            if distance_ok and velocity_ok:
                moved = points + velocities * dt
                out[(task, item)] = ("unique", float(np.linalg.norm(moved[idx[0]] - moved[idx[1]])))
            else:
                out[(task, item)] = ("non_identifiable", np.nan)
        elif not direction_ok:
            out[(task, item)] = ("non_identifiable", np.nan)
        elif task == "T2":
            out[(task, item)] = ("unique", float(np.sign(latitude[idx[0]] - latitude[idx[1]])))
        elif task == "T3":
            out[(task, item)] = ("unique", float(np.sign(_wrap(longitude[idx[0]] - longitude[idx[1]]))))
        else:
            out[(task, item)] = ("unique", float(np.degrees(longitude[idx[0]])))
    return out


def _finalise(query, table, duplicates, group_for=None, probability_for=None, candidates_for=None):
    answers = []
    for task, item, keys in _items(query):
        state, value = table[(task, item)]
        if any(key in duplicates for key in keys) and state not in ("invalid_record",):
            answers.append(Answer(task, item, "set_valued", group="entity_collision"))
            continue
        answer = Answer(task, item, state, value)
        if group_for and (task, item) in group_for:
            answer.group = group_for[(task, item)]
        if probability_for and (task, item) in probability_for:
            answer.probability = probability_for[(task, item)]
        if candidates_for and (task, item) in candidates_for:
            answer.candidates = candidates_for[(task, item)]
        answers.append(answer)
    return answers


def decode_naive(record: dict, query: Query) -> list[Answer]:
    """Representation A consumer: assumes conventional ECEF metres at the reference epoch."""
    coordinates = record.get("coordinates")
    if coordinates is None:
        return _all(query, "non_identifiable")
    points = np.array(coordinates["values"], dtype=float)
    velocities = np.array(coordinates.get("velocities", np.zeros_like(points)), dtype=float)
    mapping, _ = _index_map(record, first_match=True)
    table = _point_answers(points, velocities, mapping, query, distance_ok=True, velocity_ok=True, direction_ok=True)
    return _finalise(query, table, set())


def _usable_reference_system(record: dict) -> tuple[dict | None, str]:
    """Reconcile primary and redundant copies over the union of their keys.

    A key present in only one copy is repaired from that copy; a key present in both
    with different values is a conflict.
    """
    primary = record.get("reference_system")
    secondary = record.get("redundant_reference_system")
    copies = [rs for rs in (primary, secondary) if rs]
    if not copies:
        return None, "missing"
    merged: dict = {}
    for rs in copies:
        for key, value in rs.items():
            if key in merged and key != "crs_id" and merged[key] != value:
                return None, "conflict"
            merged.setdefault(key, value)
    if "axes" in merged and "unit" in merged:
        return merged, "ok"
    return None, "missing"


def _coordinate_path(record, query):
    coordinates = record.get("coordinates")
    reference_system, status = _usable_reference_system(record)
    if coordinates is None or reference_system is None:
        return None, status
    stored = np.array(coordinates["values"], dtype=float)
    points = to_frame(stored, reference_system)
    velocities = None
    if "velocities" in coordinates:
        velocities = to_frame(np.array(coordinates["velocities"], dtype=float), reference_system)
    epoch = reference_system.get("coordinate_epoch")
    epoch_ok = epoch is not None and (epoch == query.reference_epoch or velocities is not None)
    if epoch is not None and velocities is not None:
        points = points - velocities * (epoch - query.reference_epoch)
    return {"points": points, "velocities": velocities, "epoch_ok": epoch_ok}, "ok"


def decode_strict(record: dict, query: Query) -> list[Answer]:
    """Representations B and BR: ISO 19111-style consumer that never assumes defaults."""
    if any(issue.code in ("fixity_mismatch", "length") for issue in validate(record)):
        return _all(query, "invalid_record")
    path, status = _coordinate_path(record, query)
    if status == "conflict":
        return _all(query, "invalid_record")
    if path is None:
        return _all(query, "non_identifiable")
    mapping, duplicates = _index_map(record, first_match=False)
    direction_ok = True
    if "digital_chirality" in record:
        witness = record["digital_chirality"]
        if chirality_sign(path["points"], tuple(witness["triple"]), np.array([0.0, 0.0, 1.0])) != witness["sign"]:
            direction_ok = False
    table = _point_answers(
        path["points"],
        path["velocities"],
        mapping,
        query,
        distance_ok=path["epoch_ok"],
        velocity_ok=path["velocities"] is not None,
        direction_ok=direction_ok,
    )
    if not direction_ok:
        for key, (state, value) in table.items():
            if key[0] in ("T3", "T4"):
                table[key] = ("invalid_record", np.nan)
    return _finalise(query, table, duplicates)


def _relational_reconstruction(record: dict, flags: set[str]):
    relations = record["relations"]
    n = len(record["entities"])
    anchors = record.get("anchors") or {}
    if len(relations["edges"]) != n * (n - 1) // 2 or "origin" not in anchors or "origin" in flags:
        return None
    matrix = np.zeros((n + 1, n + 1))
    for i, j, distance in relations["edges"]:
        matrix[int(i), int(j)] = matrix[int(j), int(i)] = distance
    radii = np.array(anchors["origin"]["values"], dtype=float)
    matrix[n, :n] = matrix[:n, n] = radii
    q = classical_mds(matrix)
    q = q[:n] - q[n]
    result = {"points": q, "group": "O(3)"}
    if "axis" not in anchors or "axis" in flags:
        return result
    latitude = np.array(anchors["axis"]["values"], dtype=float)
    axis, *_ = np.linalg.lstsq(q, radii * np.sin(latitude), rcond=None)
    axis = axis / np.linalg.norm(axis)
    result.update(axis=axis, latitude=latitude, group="O(2)")
    if "chirality" not in anchors or "chirality" in flags:
        e1 = np.cross(axis, [1.0, 0.0, 0.0] if abs(axis[0]) < 0.9 else [0.0, 1.0, 0.0])
        e1 /= np.linalg.norm(e1)
    else:
        witness = anchors["chirality"]
        if chirality_sign(q, tuple(witness["triple"]), axis) != witness["sign"]:
            u = np.cross(axis, [1.0, 0.0, 0.0] if abs(axis[0]) < 0.9 else [0.0, 1.0, 0.0])
            u /= np.linalg.norm(u)
            q = q - 2.0 * np.outer(q @ u, u)
        e1 = np.cross(axis, [1.0, 0.0, 0.0] if abs(axis[0]) < 0.9 else [0.0, 1.0, 0.0])
        e1 /= np.linalg.norm(e1)
        result["group"] = "SO(2)"
    e2 = np.cross(axis, e1)
    longitude = np.arctan2(q @ e2, q @ e1)
    if "meridian" in anchors and "meridian" not in flags and result["group"] == "SO(2)":
        meridian = anchors["meridian"]
        longitude = _wrap(longitude - longitude[meridian["entity"]] + np.radians(meridian["longitude_degrees"]))
        result["group"] = "I"
    result.update(points=q, longitude=longitude)
    return result


def decode_recoverability(record: dict, query: Query) -> list[Answer]:
    """Representations C, D and E: validator-gated, never coerces ambiguity to coordinates."""
    issues = validate(record)
    if any(issue.severity == "fatal" for issue in issues):
        return _all(query, "invalid_record")
    codes = {issue.code for issue in issues}
    flags: set[str] = set()
    if "chirality_invalid" in codes:
        flags.add("chirality")
    if "meridian_invalid" in codes:
        flags.add("meridian")
    mapping, duplicates = _index_map(record, first_match=False)
    coordinate = None
    if "hash_mismatch" not in codes and "length" not in codes:
        coordinate, status = _coordinate_path(record, query)
        if status == "conflict":
            coordinate = None
    relational = None
    if record.get("relations") is not None and "hash_mismatch_relations" not in codes and "edge" not in codes:
        relational = _relational_reconstruction(record, flags)
    anchors = record.get("anchors") or {}
    dt = query.comparison_epoch - query.reference_epoch

    edge_distance: dict[tuple[int, int], tuple[float, float]] = {}
    if record.get("relations") is not None and "hash_mismatch_relations" not in codes and "edge" not in codes:
        relations = record["relations"]
        rates = {(int(i), int(j)): r for i, j, r in relations.get("rates_m_per_year", [])}
        offset = query.reference_epoch - relations["epoch"]
        for i, j, distance in relations["edges"]:
            key = (int(i), int(j))
            rate = rates.get(key)
            base = distance + (rate * offset if rate is not None else (0.0 if offset == 0 else np.nan))
            edge_distance[key] = (base, base + rate * dt if rate is not None else np.nan)
            edge_distance[(key[1], key[0])] = edge_distance[key]

    sigma = (record.get("uncertainty") or {}).get("distance_standard_uncertainty_m")
    k = (record.get("uncertainty") or {}).get("coverage_factor", 3.0)
    coordinate_orientation_ok = coordinate is not None
    if coordinate is not None:
        pts = coordinate["points"]
        z = np.array([0.0, 0.0, 1.0])
        witness = anchors.get("chirality")
        if witness is not None and "chirality" not in flags:
            if chirality_sign(pts, tuple(witness["triple"]), z) != witness["sign"]:
                coordinate_orientation_ok = False
        if "axis" in anchors:
            latitude = np.arcsin(pts[:, 2] / np.linalg.norm(pts, axis=1))
            if np.max(np.abs(latitude - np.array(anchors["axis"]["values"]))) > 1e-6:
                coordinate_orientation_ok = False

    table: dict[tuple[str, str], tuple[str, float]] = {}
    groups: dict[tuple[str, str], str] = {}
    probabilities: dict[tuple[str, str], float] = {}
    candidates: dict[tuple[str, str], tuple] = {}
    coordinate_table = None
    if coordinate is not None:
        coordinate_table = _point_answers(
            coordinate["points"], coordinate["velocities"], mapping, query,
            distance_ok=coordinate["epoch_ok"], velocity_ok=coordinate["velocities"] is not None,
            direction_ok=coordinate_orientation_ok,
        )
    for task, item, keys in _items(query):
        if any(key not in mapping for key in keys):
            table[(task, item)] = ("non_identifiable", np.nan)
            continue
        idx = [mapping[key] for key in keys]
        from_coordinates = coordinate_table[(task, item)] if coordinate_table else ("non_identifiable", np.nan)
        if task in DISTANCE_TASKS:
            relational_value = np.nan
            if (idx[0], idx[1]) in edge_distance:
                relational_value = edge_distance[(idx[0], idx[1])][0 if task == "T1" else 1]
            has_relational = np.isfinite(relational_value)
            if from_coordinates[0] == "unique" and has_relational and sigma is not None:
                if abs(from_coordinates[1] - relational_value) > k * sigma:
                    table[(task, item)] = ("set_valued", np.nan)
                    candidates[(task, item)] = (from_coordinates[1], relational_value)
                    continue
            if has_relational:
                table[(task, item)] = ("unique", float(relational_value))
            else:
                table[(task, item)] = from_coordinates
            continue
        if from_coordinates[0] == "unique":
            table[(task, item)] = from_coordinates
            continue
        if relational is None or "axis" not in relational:
            table[(task, item)] = ("non_identifiable", np.nan)
            continue
        group = relational["group"]
        if task == "T2":
            latitude = relational["latitude"]
            delta = latitude[idx[0]] - latitude[idx[1]]
            table[(task, item)] = ("unique", float(np.sign(delta)))
            noise = anchors["axis"].get("standard_uncertainty_radians")
            if noise:
                probability = 0.5 * (1 + erf(abs(delta) / (2 * noise)))
                if probability < 0.975:
                    table[(task, item)] = ("probabilistic", float(np.sign(delta)))
                    probabilities[(task, item)] = probability
        elif task == "T3":
            value = float(np.sign(_wrap(relational["longitude"][idx[0]] - relational["longitude"][idx[1]])))
            table[(task, item)] = ("unique", value) if group in ("SO(2)", "I") else ("unique_up_to_group", value)
            if group == "O(2)":
                groups[(task, item)] = "O(2)"
        else:
            value = float(np.degrees(relational["longitude"][idx[0]]))
            table[(task, item)] = ("unique", value) if group == "I" else ("unique_up_to_group", value)
            if group != "I":
                groups[(task, item)] = group
    return _finalise(query, table, duplicates, groups, probabilities, candidates)


DECODERS = {
    "A": decode_naive,
    "B": decode_strict,
    "BR": decode_strict,
    "C": decode_recoverability,
    "D": decode_recoverability,
    "E": decode_recoverability,
}


def decode(record: dict, query: Query) -> list[Answer]:
    return DECODERS[record.get("representation", "A")](record, query)
