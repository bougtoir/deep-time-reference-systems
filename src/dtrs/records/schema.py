"""Versioned record model for time-indexed spatial relations."""

from __future__ import annotations

import json
from pathlib import Path

SCHEMA_NAME = "dtrs-relation-record"
SCHEMA_VERSION = "1.1.0"

STATES = (
    "unique",
    "unique_up_to_group",
    "set_valued",
    "probabilistic",
    "non_identifiable",
    "invalid_record",
)

EVIDENCE_TYPES = ("independent_physical", "digital_copy", "conventional_definition")

AXIS_DIRECTIONS = (
    "geocentricX",
    "geocentricY",
    "geocentricZ",
    "-geocentricX",
    "-geocentricY",
    "-geocentricZ",
)

TASKS = {
    "T1": "Euclidean distance at the reference epoch",
    "T2": "north-south ordering along the directed spin axis",
    "T3": "signed east-west longitude relation",
    "T4": "absolute longitude from a meridian origin",
    "T5": "Euclidean distance at the comparison epoch",
}

_NUMBER = {"type": "number"}
_VECTOR = {"type": "array", "items": _NUMBER, "minItems": 3, "maxItems": 3}
_ANCHOR_EVIDENCE = {"type": "string", "enum": list(EVIDENCE_TYPES)}

JSON_SCHEMA: dict = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": f"https://github.com/bougtoir/deep-time-reference-systems/schema/{SCHEMA_VERSION}",
    "title": "Recoverability-aware record of time-indexed spatial relations",
    "type": "object",
    "required": ["schema", "schema_version", "record_id", "entities"],
    "properties": {
        "schema": {"type": "string", "enum": [SCHEMA_NAME]},
        "schema_version": {"type": "string", "enum": [SCHEMA_VERSION]},
        "record_id": {"type": "string"},
        "representation": {"type": "string"},
        "entities": {
            "type": "array",
            "minItems": 2,
            "items": {
                "type": "object",
                "required": ["id"],
                "properties": {
                    "id": {"type": "string"},
                    "label": {"type": "string"},
                    "identifier_scheme": {"type": "string"},
                },
            },
        },
        "coordinates": {
            "type": "object",
            "required": ["values"],
            "properties": {
                "values": {"type": "array", "items": _VECTOR},
                "velocities": {"type": "array", "items": _VECTOR},
                "standard_uncertainty_m": {"type": "array", "items": _VECTOR},
            },
        },
        "reference_system": {
            "type": "object",
            "properties": {
                "crs_id": {"type": "string"},
                "frame": {"type": "string"},
                "axes": {
                    "type": "array",
                    "minItems": 3,
                    "maxItems": 3,
                    "items": {"type": "string", "enum": list(AXIS_DIRECTIONS)},
                },
                "unit": {"type": "string", "enum": ["metre"]},
                "frame_reference_epoch": _NUMBER,
                "coordinate_epoch": _NUMBER,
                "transformation_to_frame": {
                    "type": "object",
                    "required": ["method", "matrix"],
                    "properties": {
                        "method": {"type": "string"},
                        "matrix": {"type": "array", "items": _VECTOR, "minItems": 3, "maxItems": 3},
                    },
                },
            },
        },
        "relations": {
            "type": "object",
            "required": ["kind", "unit", "epoch", "edges"],
            "properties": {
                "kind": {"type": "string", "enum": ["euclidean_distance"]},
                "unit": {"type": "string", "enum": ["metre"]},
                "epoch": _NUMBER,
                "edges": {"type": "array", "items": {"type": "array", "minItems": 3, "maxItems": 3}},
                "rates_m_per_year": {"type": "array", "items": {"type": "array", "minItems": 3, "maxItems": 3}},
            },
        },
        "anchors": {
            "type": "object",
            "properties": {
                "origin": {
                    "type": "object",
                    "required": ["observable", "values", "evidence"],
                    "properties": {
                        "observable": {"type": "string", "enum": ["geocentric_distance_m"]},
                        "values": {"type": "array", "items": _NUMBER},
                        "evidence": _ANCHOR_EVIDENCE,
                    },
                },
                "axis": {
                    "type": "object",
                    "required": ["observable", "values", "evidence"],
                    "properties": {
                        "observable": {"type": "string", "enum": ["geocentric_latitude_radians"]},
                        "values": {"type": "array", "items": _NUMBER},
                        "standard_uncertainty_radians": _NUMBER,
                        "evidence": _ANCHOR_EVIDENCE,
                    },
                },
                "chirality": {
                    "type": "object",
                    "required": ["triple", "sign", "evidence"],
                    "properties": {
                        "triple": {"type": "array", "minItems": 3, "maxItems": 3},
                        "sign": {"type": "integer", "enum": [-1, 1]},
                        "evidence": _ANCHOR_EVIDENCE,
                    },
                },
                "meridian": {
                    "type": "object",
                    "required": ["entity", "longitude_degrees", "evidence"],
                    "properties": {
                        "entity": {"type": "integer"},
                        "longitude_degrees": _NUMBER,
                        "evidence": _ANCHOR_EVIDENCE,
                    },
                },
            },
        },
        "uncertainty": {
            "type": "object",
            "properties": {
                "distance_standard_uncertainty_m": _NUMBER,
                "coverage_factor": _NUMBER,
            },
        },
        "provenance": {
            "type": "object",
            "properties": {
                "sources": {"type": "array"},
                "software": {"type": "string"},
                "coordinates_sha256": {"type": "string"},
                "relations_sha256": {"type": "string"},
            },
        },
        "declared_recoverability": {
            "type": "object",
            "properties": {
                "residual_group": {"type": "string", "enum": ["O(3)", "O(2)", "SO(2)", "I", "undetermined"]},
                "tasks": {"type": "object"},
            },
        },
        "fixity": {
            "type": "object",
            "properties": {
                "algorithm": {"type": "string"},
                "scope": {"type": "string"},
                "coordinate_values_sha256": {"type": "string"},
            },
        },
        "redundant_reference_system": {"type": "object"},
        "digital_chirality": {"type": "object"},
    },
}


def write_schema(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(JSON_SCHEMA, indent=2) + "\n", encoding="utf-8")


FIELD_ROWS = (
    ("entities", "Identifier, label, namespace; collisions are reported", "Entity identity (T6)"),
    ("coordinates", "Values, optional velocities, unit", "Original representation; precise answers when metadata are intact"),
    ("reference_system", "CRS id, axes, unit, frame, coordinate and frame epochs, transformation", "Interprets coordinates (ISO 19111 / PROJJSON role)"),
    ("relations", "Labelled chord distances, rates, epoch, completeness", "Frame-free metric evidence (T1, T5); rigidity check"),
    ("anchors.origin", "Geocentric radii with evidence type", "Removes translation; enables axial projection"),
    ("anchors.axis", "Axial latitudes with standard uncertainty", "Reduces O(3) to O(2); N/S ordering (T2)"),
    ("anchors.chirality", "Oriented entity triple, sign, evidence type", "Reduces O(2) to SO(2) only if independent physical evidence (T3)"),
    ("anchors.meridian", "Entity and longitude of the directed meridian", "Reduces SO(2) to identity (T4)"),
    ("uncertainty", "Coordinate and distance standard uncertainty, coverage factor", "Consistency tolerances; probabilistic states"),
    ("provenance", "Source ids and SHA-256, software version, coordinate and relation hashes", "Detects stale or edited components"),
    ("declared_recoverability", "Residual group and per-task state computed at export", "Machine-readable ambiguity class; stale declarations rejected"),
)


def record_field_table():
    import pandas as pd

    return pd.DataFrame(FIELD_ROWS, columns=["Field", "Content", "Role in recovery"])
