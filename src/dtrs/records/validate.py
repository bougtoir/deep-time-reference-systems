"""Structural (JSON Schema subset) and semantic validation of relation records."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .encode import coordinate_values_hash, coordinates_hash, declared_recoverability, relations_hash
from .schema import JSON_SCHEMA

_TYPES = {
    "object": dict,
    "array": list,
    "string": str,
    "integer": int,
    "number": (int, float),
}


@dataclass(frozen=True)
class Issue:
    code: str
    path: str
    severity: str
    message: str


def _check(value, schema: dict, path: str, issues: list[Issue]) -> None:
    expected = schema.get("type")
    if expected is not None:
        python_type = _TYPES[expected]
        if isinstance(value, bool) or not isinstance(value, python_type):
            issues.append(Issue("type", path, "fatal", f"expected {expected}"))
            return
    if "enum" in schema and value not in schema["enum"]:
        issues.append(Issue("enum", path, "fatal", f"{value!r} not in {schema['enum']}"))
    if isinstance(value, dict):
        for key in schema.get("required", []):
            if key not in value:
                issues.append(Issue("required", f"{path}/{key}", "fatal", "missing required field"))
        for key, subschema in schema.get("properties", {}).items():
            if key in value:
                _check(value[key], subschema, f"{path}/{key}", issues)
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            issues.append(Issue("minItems", path, "fatal", "too few items"))
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            issues.append(Issue("maxItems", path, "fatal", "too many items"))
        if "items" in schema:
            for index, item in enumerate(value):
                _check(item, schema["items"], f"{path}/{index}", issues)


def validate_structure(record: dict) -> list[Issue]:
    issues: list[Issue] = []
    _check(record, JSON_SCHEMA, "", issues)
    return issues


def validate(record: dict) -> list[Issue]:
    """Return all structural and semantic issues; severity fatal|component|warning."""
    issues = validate_structure(record)
    if any(issue.severity == "fatal" for issue in issues):
        return issues
    n = len(record["entities"])
    ids = [entity["id"] for entity in record["entities"]]
    duplicates = sorted({identifier for identifier in ids if ids.count(identifier) > 1})
    for identifier in duplicates:
        issues.append(Issue("entity_collision", "/entities", "component", identifier))
    coordinates = record.get("coordinates")
    if coordinates is not None:
        for key in ("values", "velocities", "standard_uncertainty_m"):
            if key in coordinates and len(coordinates[key]) != n:
                issues.append(Issue("length", f"/coordinates/{key}", "component", "length != entities"))
    reference_system = record.get("reference_system")
    if reference_system is not None and "axes" in reference_system:
        from .encode import axes_matrix

        matrix = axes_matrix(reference_system["axes"])
        if abs(abs(np.linalg.det(matrix)) - 1.0) > 1e-9:
            issues.append(Issue("axes_degenerate", "/reference_system/axes", "component", "repeated axis"))
    relations = record.get("relations")
    if relations is not None:
        for index, edge in enumerate(relations["edges"]):
            i, j, distance = edge
            if not (0 <= int(i) < n and 0 <= int(j) < n) or i == j or distance < 0:
                issues.append(Issue("edge", f"/relations/edges/{index}", "component", "invalid edge"))
    anchors = record.get("anchors") or {}
    for name in ("origin", "axis"):
        if name in anchors and len(anchors[name]["values"]) != n:
            issues.append(Issue("anchor_length", f"/anchors/{name}", "component", "length != entities"))
    if "chirality" in anchors:
        triple = anchors["chirality"]["triple"]
        if len(set(triple)) != 3 or any(not isinstance(k, int) or not 0 <= k < n for k in triple):
            issues.append(Issue("chirality_invalid", "/anchors/chirality", "component", "invalid triple"))
    if "meridian" in anchors and not 0 <= anchors["meridian"]["entity"] < n:
        issues.append(Issue("meridian_invalid", "/anchors/meridian", "component", "invalid entity"))
    fixity = record.get("fixity")
    if fixity is not None and "coordinates" in record:
        stored = fixity.get("coordinate_values_sha256")
        if stored is not None and stored != coordinate_values_hash(record):
            issues.append(Issue("fixity_mismatch", "/fixity/coordinate_values_sha256", "component", "coordinate values altered"))
    provenance = record.get("provenance")
    if provenance is not None:
        if "coordinates" in record:
            stored = provenance.get("coordinates_sha256")
            if stored is None:
                issues.append(Issue("hash_missing", "/provenance/coordinates_sha256", "warning", "absent"))
            elif stored != coordinates_hash(record):
                issues.append(Issue("hash_mismatch", "/provenance/coordinates_sha256", "component", "coordinates altered"))
        if "relations" in record:
            stored = provenance.get("relations_sha256")
            if stored is not None and stored != relations_hash(record):
                issues.append(Issue("hash_mismatch_relations", "/provenance/relations_sha256", "component", "relations altered"))
    declared = record.get("declared_recoverability")
    if declared is not None and relations is not None:
        if declared != declared_recoverability(record):
            issues.append(Issue("declared_state_mismatch", "/declared_recoverability", "warning", "recomputed differs"))
    return issues
