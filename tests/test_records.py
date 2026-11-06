import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from dtrs.records import JSON_SCHEMA, SCHEMA_VERSION, build_record, decode, validate
from dtrs.records.benchmark import (
    ground_truth,
    make_query,
    scenario_record,
    score,
    site_arrays,
)

ROOT = Path(__file__).resolve().parents[1]
SETTINGS = {
    "seed": 7,
    "reference_epoch": 2015.0,
    "comparison_epoch": 2025.0,
    "sparse_edge_probability": 0.5,
    "perturbed_sites": [1, 5, 9],
    "perturbation_m": 0.05,
}


@pytest.fixture(scope="module")
def setup():
    sites = pd.read_csv(ROOT / "data/processed/itrf_selected_sites.csv")
    arrays = site_arrays(sites)
    query = make_query(arrays, 2015.0, 2025.0)
    return arrays, query, ground_truth(arrays, query)


def _categories(record, query, truth):
    return score(decode(record, query), truth)["category"].value_counts(normalize=True)


def test_schema_version_and_examples_validate(setup):
    arrays, _, _ = setup
    assert JSON_SCHEMA["properties"]["schema_version"]["enum"] == [SCHEMA_VERSION]
    for representation in ("A", "B", "BR", "C", "D", "E"):
        record = build_record(arrays["points"], arrays["velocities"], arrays["ids"], arrays["labels"],
                              arrays["sigma"], representation)
        assert not [i for i in validate(record) if i.severity != "warning"], representation
        json.loads(json.dumps(record))


def test_intact_strong_baseline_fully_recovers(setup):
    arrays, query, truth = setup
    record = scenario_record("S0_intact", "B", arrays, SETTINGS)
    assert _categories(record, query, truth).get("correct_unique") == 1.0


def test_relational_only_never_claims_orientation(setup):
    arrays, query, truth = setup
    scored = score(decode(scenario_record("S0_intact", "C", arrays, SETTINGS), query), truth)
    directional = scored[scored["task"].isin(["T2", "T3", "T4"])]
    assert set(directional["state"]) == {"non_identifiable"}
    assert (scored["category"] != "false_certainty").all()


def test_missing_witness_returns_group_not_coordinates(setup):
    arrays, query, truth = setup
    scored = score(decode(scenario_record("S7_chirality_witness_absent", "D", arrays, SETTINGS), query), truth)
    assert set(scored.loc[scored["task"] == "T3", "state"]) == {"unique_up_to_group"}
    assert set(scored.loc[scored["task"] == "T4", "state"]) == {"unique_up_to_group"}


@pytest.mark.parametrize("scenario", ["S4_silent_left_handed_export", "S13_epoch_mislabelled_at_export",
                                      "S11_unflagged_coordinate_error"])
def test_hybrid_has_no_false_certainty_where_baseline_fails(setup, scenario):
    arrays, query, truth = setup
    baseline = _categories(scenario_record(scenario, "B", arrays, SETTINGS), query, truth)
    hybrid = _categories(scenario_record(scenario, "E", arrays, SETTINGS), query, truth)
    assert baseline.get("false_certainty", 0) > 0
    assert hybrid.get("false_certainty", 0) == 0


def test_baseline_fixity_flags_post_export_corruption(setup):
    arrays, query, truth = setup
    record = scenario_record("S10_epoch_mislabelled_coordinates", "B", arrays, SETTINGS)
    assert _categories(record, query, truth).get("flagged_invalid") == 1.0


def test_redundant_copy_repairs_field_missing_from_primary(setup):
    arrays, query, truth = setup
    from dtrs.records.benchmark import _build_base
    from dtrs.records.encode import refresh_derived

    record = _build_base(arrays, "BR", convention_name="plate_fixed_rotated")
    record["reference_system"].pop("transformation_to_frame")
    refresh_derived(record)
    assert _categories(record, query, truth).get("correct_unique") == 1.0


def test_digital_copy_witness_does_not_protect_common_mode(setup):
    arrays, query, truth = setup
    record = scenario_record("S4_silent_left_handed_export", "E", arrays, SETTINGS,
                             chirality_evidence="digital_copy")
    assert _categories(record, query, truth).get("false_certainty", 0) > 0


def test_invalid_witness_is_flagged(setup):
    arrays, _, _ = setup
    record = scenario_record("S8_chirality_witness_invalid", "E", arrays, SETTINGS)
    assert "chirality_invalid" in {i.code for i in validate(record)}


def test_structural_error_is_invalid_record(setup):
    arrays, query, truth = setup
    record = scenario_record("S0_intact", "E", arrays, SETTINGS)
    record["schema_version"] = "0.0"
    assert set(score(decode(record, query), truth)["state"]) == {"invalid_record"}


def test_results_registry_contains_record_benchmark():
    values = pd.read_csv(ROOT / "results/manuscript_values.csv")
    assert (values["source"] == "record_benchmark").sum() > 100
    assert np.isfinite(values.loc[values["source"] == "record_benchmark", "value"].dropna()).all()
