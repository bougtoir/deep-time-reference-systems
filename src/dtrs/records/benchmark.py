"""Metadata-loss benchmark for representations A, B, BR, C, D and E."""

from __future__ import annotations

import copy
import json
import time

import numpy as np
import pandas as pd

from .decode import Query, decode
from .encode import (
    REPRESENTATIONS,
    build_record,
    chirality_sign,
    declared_recoverability,
    refresh_derived,
    relations_hash,
    to_frame,
)

DISTANCE_TOLERANCE_M = 0.01
LONGITUDE_TOLERANCE_DEGREES = 1e-5
CATEGORIES = (
    "correct_unique",
    "false_certainty",
    "informative_ambiguity",
    "non_identifiable",
    "flagged_invalid",
)


def site_arrays(sites: pd.DataFrame) -> dict:
    return {
        "points": sites[["x_m", "y_m", "z_m"]].to_numpy(dtype=float),
        "velocities": sites[["vx_m_per_year", "vy_m_per_year", "vz_m_per_year"]].to_numpy(dtype=float),
        "sigma": sites[["sigma_x_m", "sigma_y_m", "sigma_z_m"]].to_numpy(dtype=float),
        "ids": sites["domes"].astype(str).tolist(),
        "labels": sites["site_name"].astype(str).tolist(),
    }


def make_query(arrays: dict, reference_epoch: float, comparison_epoch: float) -> Query:
    ids = arrays["ids"]
    pairs = [(ids[i], ids[j]) for i in range(len(ids)) for j in range(i)]
    return Query(reference_epoch, comparison_epoch, pairs, list(ids))


def ground_truth(arrays: dict, query: Query) -> dict[tuple[str, str], float]:
    points, velocities = arrays["points"], arrays["velocities"]
    index = {identifier: k for k, identifier in enumerate(arrays["ids"])}
    latitude = np.arcsin(points[:, 2] / np.linalg.norm(points, axis=1))
    longitude = np.arctan2(points[:, 1], points[:, 0])
    moved = points + velocities * (query.comparison_epoch - query.reference_epoch)
    truth = {}
    for a, b in query.pairs:
        i, j = index[a], index[b]
        item = f"{a}|{b}"
        truth[("T1", item)] = float(np.linalg.norm(points[i] - points[j]))
        truth[("T5", item)] = float(np.linalg.norm(moved[i] - moved[j]))
        truth[("T2", item)] = float(np.sign(latitude[i] - latitude[j]))
        delta = (longitude[i] - longitude[j] + np.pi) % (2 * np.pi) - np.pi
        truth[("T3", item)] = float(np.sign(delta))
    for site in query.sites:
        truth[("T4", site)] = float(np.degrees(longitude[index[site]]))
    return truth


def _correct(task: str, value: float, truth: float) -> bool:
    if not np.isfinite(value):
        return False
    if task in ("T1", "T5"):
        return abs(value - truth) <= DISTANCE_TOLERANCE_M
    if task == "T4":
        return abs((value - truth + 180.0) % 360.0 - 180.0) <= LONGITUDE_TOLERANCE_DEGREES
    return value == truth


def score(answers, truth) -> pd.DataFrame:
    rows = []
    for answer in answers:
        expected = truth[(answer.task, answer.item)]
        if answer.state == "unique":
            category = "correct_unique" if _correct(answer.task, answer.value, expected) else "false_certainty"
        elif answer.state == "invalid_record":
            category = "flagged_invalid"
        elif answer.state == "non_identifiable":
            category = "non_identifiable"
        else:
            category = "informative_ambiguity"
        contains_truth = True
        if answer.state == "set_valued" and answer.candidates:
            contains_truth = any(_correct(answer.task, c, expected) for c in answer.candidates)
        if answer.state == "probabilistic":
            contains_truth = _correct(answer.task, answer.value, expected)
        rows.append(
            {
                "task": answer.task,
                "item": answer.item,
                "state": answer.state,
                "category": category,
                "probability": answer.probability,
                "truth_consistent": contains_truth,
            }
        )
    return pd.DataFrame(rows)


def _build_base(arrays, representation, **kwargs):
    return build_record(
        arrays["points"], arrays["velocities"], arrays["ids"], arrays["labels"], arrays["sigma"],
        representation, **kwargs,
    )


def _delete(record: dict, path: str) -> None:
    parts = path.split(".")
    node = record
    for part in parts[:-1]:
        node = node.get(part)
        if node is None:
            return
    node.pop(parts[-1], None)


def scenario_record(name: str, representation: str, arrays: dict, settings: dict, **build_kwargs) -> dict:
    """Return the damaged record for one deterministic scenario."""
    def _build(arrays_, representation_, **kwargs):
        return _build_base(arrays_, representation_, **{**build_kwargs, **kwargs})

    if name.startswith("S1_crs_block_deleted:"):
        record = _build(arrays, representation, convention_name=name.split(":")[1])
        record.pop("reference_system", None)
        return record
    if name == "S9_crs_and_witness_lost":
        record = _build(arrays, representation, convention_name="left_handed")
        record.pop("reference_system", None)
        _delete(record, "anchors.chirality")
        return record
    if name == "S12_sparse_relations_crs_lost":
        record = _build(arrays, representation, convention_name="left_handed")
        record.pop("reference_system", None)
        if "relations" in record:
            rng = np.random.default_rng(settings["seed"])
            keep = rng.random(len(record["relations"]["edges"])) < settings["sparse_edge_probability"]
            for key in ("edges", "rates_m_per_year"):
                record["relations"][key] = [e for e, k in zip(record["relations"][key], keep) if k]
            refresh_derived(record)
        return record
    convention_name = {"S2_crs_id_missing_params_retained": "plate_fixed_rotated",
                       "S5_axis_swap_labelled": "axis_swapped"}.get(name, "standard")
    record = _build(arrays, representation, convention_name=convention_name)
    if name == "S0_intact" or name == "S5_axis_swap_labelled":
        return record
    if name == "S2_crs_id_missing_params_retained":
        _delete(record, "reference_system.crs_id")
        return record
    if name == "S3_coordinate_epoch_missing":
        _delete(record, "reference_system.coordinate_epoch")
        _delete(record, "redundant_reference_system.coordinate_epoch")
        return record
    if name == "S4_silent_left_handed_export":
        _common_mode_flip(record)
        return record
    if name == "S6_entity_collision":
        record["entities"][2]["id"] = record["entities"][7]["id"]
        refresh_derived(record)
        return record
    if name == "S7_chirality_witness_absent":
        _delete(record, "anchors.chirality")
        refresh_derived(record)
        return record
    if name == "S8_chirality_witness_invalid":
        if "anchors" in record:
            record["anchors"]["chirality"]["triple"] = [0, 0, 99]
        refresh_derived(record)
        return record
    if name in ("S10_epoch_mislabelled_coordinates", "S13_epoch_mislabelled_at_export"):
        if "coordinates" in record:
            dt = settings["comparison_epoch"] - settings["reference_epoch"]
            frame = arrays["points"] + arrays["velocities"] * dt
            _, storage = _convention_storage(convention_name)
            record["coordinates"]["values"] = np.round(frame @ storage.T, 4).tolist()
            if name == "S13_epoch_mislabelled_at_export":
                refresh_derived(record)
        return record
    if name == "S11_unflagged_coordinate_error":
        if "coordinates" in record:
            rng = np.random.default_rng(settings["seed"] + 11)
            values = np.array(record["coordinates"]["values"])
            for k in settings["perturbed_sites"]:
                direction = rng.normal(size=3)
                values[k] += settings["perturbation_m"] * direction / np.linalg.norm(direction)
            record["coordinates"]["values"] = np.round(values, 4).tolist()
            refresh_derived(record)
        return record
    raise ValueError(name)


def _convention_storage(name):
    from .encode import convention

    return convention(name)


def _common_mode_flip(record: dict) -> None:
    """Export bug negating Y; every digitally derived field is recomputed after the bug."""
    if "coordinates" in record:
        flip = np.diag([1.0, -1.0, 1.0])
        for key in ("values", "velocities"):
            if key in record["coordinates"]:
                record["coordinates"][key] = (np.array(record["coordinates"][key]) @ flip).round(5).tolist()
    if "digital_chirality" in record:
        witness = record["digital_chirality"]
        frame = to_frame(np.array(record["coordinates"]["values"]), record["reference_system"])
        witness["sign"] = chirality_sign(frame, tuple(witness["triple"]), np.array([0.0, 0.0, 1.0]))
    anchors = record.get("anchors") or {}
    if anchors.get("chirality", {}).get("evidence") == "digital_copy" and "coordinates" in record:
        frame = to_frame(np.array(record["coordinates"]["values"]), record["reference_system"])
        anchors["chirality"]["sign"] = chirality_sign(frame, tuple(anchors["chirality"]["triple"]), np.array([0.0, 0.0, 1.0]))
    refresh_derived(record)


SCENARIOS = (
    "S0_intact",
    "S1_crs_block_deleted:standard",
    "S1_crs_block_deleted:left_handed",
    "S1_crs_block_deleted:plate_fixed_rotated",
    "S2_crs_id_missing_params_retained",
    "S3_coordinate_epoch_missing",
    "S4_silent_left_handed_export",
    "S5_axis_swap_labelled",
    "S6_entity_collision",
    "S7_chirality_witness_absent",
    "S8_chirality_witness_invalid",
    "S9_crs_and_witness_lost",
    "S10_epoch_mislabelled_coordinates",
    "S11_unflagged_coordinate_error",
    "S12_sparse_relations_crs_lost",
    "S13_epoch_mislabelled_at_export",
)


def wilson(successes: int, trials: int) -> tuple[float, float]:
    if trials == 0:
        return float("nan"), float("nan")
    z = 1.959963984540054
    p = successes / trials
    denominator = 1 + z**2 / trials
    centre = (p + z**2 / (2 * trials)) / denominator
    half = z * np.sqrt(p * (1 - p) / trials + z**2 / (4 * trials**2)) / denominator
    return float(centre - half), float(centre + half)


def summarise(scored: pd.DataFrame, keys: list[str]) -> pd.DataFrame:
    rows = []
    for group, frame in scored.groupby(keys, sort=False):
        group = group if isinstance(group, tuple) else (group,)
        row = dict(zip(keys, group))
        row["n_items"] = len(frame)
        for category in CATEGORIES:
            row[category] = float((frame["category"] == category).mean())
        row["truth_inconsistent_ambiguity"] = float(
            ((frame["category"] == "informative_ambiguity") & ~frame["truth_consistent"]).mean()
        )
        rows.append(row)
    return pd.DataFrame(rows)


def run_scenarios(arrays, query, truth, settings, representations=REPRESENTATIONS) -> pd.DataFrame:
    frames = []
    for name in SCENARIOS:
        for representation in representations:
            record = scenario_record(name, representation, arrays, settings)
            scored = score(decode(record, query), truth)
            frames.append(scored.assign(scenario=name, representation=representation))
    return pd.concat(frames, ignore_index=True)


MCAR_FIELDS = (
    "reference_system.crs_id",
    "reference_system.axes",
    "reference_system.unit",
    "reference_system.coordinate_epoch",
    "reference_system.transformation_to_frame",
    "redundant_reference_system",
    "coordinates.velocities",
    "digital_chirality",
    "relations.rates_m_per_year",
    "anchors.origin",
    "anchors.axis",
    "anchors.chirality",
    "anchors.meridian",
    "uncertainty",
)


def _has(record: dict, path: str) -> bool:
    node = record
    for part in path.split("."):
        if not isinstance(node, dict) or part not in node:
            return False
        node = node[part]
    return True


def run_missingness(arrays, query, truth, settings) -> pd.DataFrame:
    rng = np.random.default_rng(settings["seed"] + 101)
    templates = {
        (convention_name, representation): _build_base(arrays, representation, convention_name=convention_name)
        for convention_name in settings["missingness_conventions"]
        for representation in REPRESENTATIONS
    }
    rows = []
    for mechanism in ("field_mcar", "metadata_block"):
        for rate in settings["missingness_rates"]:
            for convention_name in settings["missingness_conventions"]:
                for replicate in range(settings["missingness_replicates"]):
                    uniforms = rng.random(len(MCAR_FIELDS) + 1)
                    for representation in REPRESENTATIONS:
                        record = copy.deepcopy(templates[(convention_name, representation)])
                        if mechanism == "field_mcar":
                            for path, u in zip(MCAR_FIELDS, uniforms):
                                if u < rate and _has(record, path):
                                    _delete(record, path)
                        elif uniforms[-1] < rate:
                            record.pop("reference_system", None)
                            record.pop("redundant_reference_system", None)
                        scored = score(decode(record, query), truth)
                        rows.append(
                            {
                                "mechanism": mechanism,
                                "rate": rate,
                                "convention": convention_name,
                                "replicate": replicate,
                                "representation": representation,
                                "any_false_certainty": bool((scored["category"] == "false_certainty").any()),
                                "false_certainty_rate": float((scored["category"] == "false_certainty").mean()),
                                "coverage": float((scored["category"] == "correct_unique").mean()),
                            }
                        )
    return pd.DataFrame(rows)


def summarise_missingness(raw: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (mechanism, rate, representation), frame in raw.groupby(
        ["mechanism", "rate", "representation"], sort=False
    ):
        n = len(frame)
        k = int(frame["any_false_certainty"].sum())
        low, high = wilson(k, n)
        coverage = frame["coverage"].to_numpy()
        rows.append(
            {
                "mechanism": mechanism,
                "rate": rate,
                "representation": representation,
                "n_records": n,
                "records_with_false_certainty": k / n,
                "records_with_false_certainty_95ci_low": low,
                "records_with_false_certainty_95ci_high": high,
                "mean_item_false_certainty": float(frame["false_certainty_rate"].mean()),
                "mean_coverage": float(coverage.mean()),
                "mean_coverage_95ci_halfwidth": float(1.959963984540054 * coverage.std(ddof=1) / np.sqrt(n)),
            }
        )
    return pd.DataFrame(rows)


ABLATIONS = {
    "full": [],
    "no_relations": ["relations"],
    "no_origin_anchor": ["anchors.origin"],
    "no_axis_anchor": ["anchors.axis"],
    "no_chirality_anchor": ["anchors.chirality"],
    "no_meridian_anchor": ["anchors.meridian"],
    "no_uncertainty": ["uncertainty"],
    "no_provenance": ["provenance"],
    "chirality_digital_copy": [],
}


def run_ablation(arrays, query, truth, settings) -> pd.DataFrame:
    frames = []
    for ablation, removed in ABLATIONS.items():
        evidence = "digital_copy" if ablation == "chirality_digital_copy" else "independent_physical"
        for name in SCENARIOS:
            record = scenario_record(name, "E", arrays, settings, chirality_evidence=evidence)
            for path in removed:
                _delete(record, path)
            if removed and "provenance" in record and "relations" in record:
                record["provenance"]["relations_sha256"] = relations_hash(record)
            if removed and "relations" in record:
                record["declared_recoverability"] = declared_recoverability(record)
            scored = score(decode(record, query), truth)
            frames.append(scored.assign(scenario=name, ablation=ablation))
    raw = pd.concat(frames, ignore_index=True)
    return summarise(raw, ["ablation"])


def run_calibration(arrays, query, truth, settings) -> tuple[pd.DataFrame, pd.DataFrame]:
    rng = np.random.default_rng(settings["seed"] + 202)
    rows = []
    for noise in settings["calibration_axis_noise_radians"]:
        for replicate in range(settings["calibration_replicates"]):
            record = _build_base(arrays, "D")
            latitude = np.array(record["anchors"]["axis"]["values"])
            record["anchors"]["axis"]["values"] = (latitude + rng.normal(0.0, noise, latitude.shape)).tolist()
            record["anchors"]["axis"]["standard_uncertainty_radians"] = noise
            refresh_derived(record)
            for answer in decode(record, query):
                if answer.task != "T2":
                    continue
                expected = truth[("T2", answer.item)]
                correct = answer.value == expected
                probability = answer.probability if answer.state == "probabilistic" else 1.0
                rows.append({"noise_radians": noise, "replicate": replicate, "state": answer.state,
                             "predicted_probability": probability, "correct": correct})
    raw = pd.DataFrame(rows)
    summary_rows = []
    for noise, frame in raw.groupby("noise_radians"):
        unique = frame[frame["state"] == "unique"]
        probabilistic = frame[frame["state"] == "probabilistic"]
        brier = float(((frame["predicted_probability"] - frame["correct"].astype(float)) ** 2).mean())
        summary_rows.append(
            {
                "noise_radians": noise,
                "n_items": len(frame),
                "share_unique": len(unique) / len(frame),
                "unique_error_rate": float(1 - unique["correct"].mean()) if len(unique) else float("nan"),
                "share_probabilistic": len(probabilistic) / len(frame),
                "probabilistic_mean_predicted": float(probabilistic["predicted_probability"].mean()) if len(probabilistic) else float("nan"),
                "probabilistic_observed_accuracy": float(probabilistic["correct"].mean()) if len(probabilistic) else float("nan"),
                "brier_score": brier,
            }
        )
    bins = np.array([0.5, 0.6, 0.7, 0.8, 0.9, 0.975])
    reliability = []
    probabilistic = raw[raw["state"] == "probabilistic"]
    for low, high in zip(bins[:-1], bins[1:]):
        frame = probabilistic[(probabilistic["predicted_probability"] >= low) & (probabilistic["predicted_probability"] < high)]
        reliability.append({"bin_low": low, "bin_high": high, "n": len(frame),
                            "mean_predicted": float(frame["predicted_probability"].mean()) if len(frame) else float("nan"),
                            "observed_accuracy": float(frame["correct"].mean()) if len(frame) else float("nan")})
    return pd.DataFrame(summary_rows), pd.DataFrame(reliability)


def run_cost(arrays, query, settings) -> pd.DataFrame:
    rows = []
    baseline = None
    for representation in REPRESENTATIONS:
        record = _build_base(arrays, representation)
        size = len(json.dumps(record, separators=(",", ":")).encode("utf-8"))
        baseline = size if representation == "A" else baseline
        timings = []
        for _ in range(settings["timing_repeats"]):
            start = time.perf_counter()
            decode(record, query)
            timings.append(time.perf_counter() - start)
        rows.append({"representation": representation, "json_bytes": size,
                     "bytes_per_entity": size / len(arrays["ids"]),
                     "size_ratio_to_A": size / baseline,
                     "median_decode_ms": 1000 * float(np.median(timings))})
    return pd.DataFrame(rows)


def write_examples(arrays, settings, directory) -> list:
    directory.mkdir(parents=True, exist_ok=True)
    written = []
    for representation in REPRESENTATIONS:
        record = _build_base(arrays, representation)
        path = directory / f"intact_{representation}.json"
        path.write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8")
        written.append(path)
    for name in ("S4_silent_left_handed_export", "S10_epoch_mislabelled_coordinates", "S9_crs_and_witness_lost"):
        record = scenario_record(name, "E", arrays, settings)
        path = directory / f"{name.split('_')[0]}_E.json"
        path.write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8")
        written.append(path)
    return written


def run_record_benchmark(config: dict, sites: pd.DataFrame) -> dict[str, pd.DataFrame]:
    settings = dict(config["records"])
    settings["seed"] = config["seed"] + settings.get("seed_offset", 0)
    arrays = site_arrays(sites)
    query = make_query(arrays, settings["reference_epoch"], settings["comparison_epoch"])
    truth = ground_truth(arrays, query)
    scenarios = summarise(run_scenarios(arrays, query, truth, settings), ["scenario", "representation"])
    missingness = summarise_missingness(run_missingness(arrays, query, truth, settings))
    ablation = run_ablation(arrays, query, truth, settings)
    calibration, reliability = run_calibration(arrays, query, truth, settings)
    cost = run_cost(arrays, query, settings)
    stress = run_stress(arrays, query, truth, settings)
    return {
        "stress": stress,
        "scenarios": scenarios,
        "missingness": missingness,
        "ablation": ablation,
        "calibration": calibration,
        "reliability": reliability,
        "cost": cost,
        "arrays": arrays,
        "settings": settings,
    }


def record_values(outputs: dict[str, pd.DataFrame]) -> pd.DataFrame:
    def key(text: str) -> str:
        return str(text).replace(":", "_").replace(".", "p")

    rows = []
    for _, row in outputs["scenarios"].iterrows():
        for category in CATEGORIES:
            rows.append((f"rec_{key(row['scenario'])}_{row['representation']}_{category}", row[category], "proportion"))
    for _, row in outputs["stress"].iterrows():
        for category in CATEGORIES:
            rows.append((f"rec_stress_{row['scenario']}_{row['representation']}_{category}", row[category], "proportion"))
    for _, row in outputs["missingness"].iterrows():
        stem = f"rec_{row['mechanism']}_r{key(row['rate'])}_{row['representation']}"
        for column, unit in (
            ("records_with_false_certainty", "proportion"),
            ("records_with_false_certainty_95ci_low", "proportion"),
            ("records_with_false_certainty_95ci_high", "proportion"),
            ("mean_coverage", "proportion"),
            ("mean_coverage_95ci_halfwidth", "proportion"),
            ("n_records", "count"),
        ):
            rows.append((f"{stem}_{column}", row[column], unit))
    for _, row in outputs["ablation"].iterrows():
        for category in ("correct_unique", "false_certainty", "informative_ambiguity", "non_identifiable"):
            rows.append((f"rec_ablation_{row['ablation']}_{category}", row[category], "proportion"))
        rows.append((f"rec_ablation_{row['ablation']}_n_items", row["n_items"], "count"))
    for _, row in outputs["calibration"].iterrows():
        stem = f"rec_calibration_noise{key(row['noise_radians'])}"
        rows.append((f"{stem}_axis_noise_radians", row["noise_radians"], "radian"))
        for column in ("share_unique", "unique_error_rate", "share_probabilistic",
                       "probabilistic_mean_predicted", "probabilistic_observed_accuracy", "brier_score", "n_items"):
            rows.append((f"{stem}_{column}", row[column], "proportion" if column != "n_items" else "count"))
    for _, row in outputs["cost"].iterrows():
        for column, unit in (("json_bytes", "byte"), ("size_ratio_to_A", "ratio"), ("median_decode_ms", "ms")):
            rows.append((f"rec_cost_{row['representation']}_{column}", row[column], unit))
    settings = outputs["settings"]
    rows.extend(
        [
            ("rec_n_items_per_scenario", float(outputs["scenarios"]["n_items"].iloc[0]), "count"),
            ("rec_n_scenarios", float(outputs["scenarios"]["scenario"].nunique()), "count"),
            ("rec_missingness_replicates", float(settings["missingness_replicates"]), "count"),
            ("rec_calibration_replicates", float(settings["calibration_replicates"]), "count"),
            ("rec_distance_tolerance_m", DISTANCE_TOLERANCE_M, "m"),
            ("rec_longitude_tolerance_degrees", LONGITUDE_TOLERANCE_DEGREES, "degree"),
            ("rec_perturbation_m", float(settings["perturbation_m"]), "m"),
            ("rec_sparse_edge_probability", float(settings["sparse_edge_probability"]), "proportion"),
            ("rec_seed", float(settings["seed"]), "integer"),
        ]
    )
    return pd.DataFrame(
        [{"metric": m, "value": float(v), "source": "record_benchmark", "unit": u} for m, v, u in rows]
    )


STRESS_LABELS = {
    "X1_handedness_flip_including_anchor": "X1 handedness flip also reverses chirality anchor",
    "X2_agreeing_wrong_coordinates_and_relations": "X2 coordinates and relations share a 5 cm error",
    "X3_consistent_identifier_swap": "X3 two identifiers swapped in every field",
    "X4_chirality_anchor_mislabelled": "X4 chirality anchor mislabelled, data correct",
    "X5_consistent_wrong_epoch": "X5 all fields at wrong epoch, labels consistent",
}


def stress_outcome_table(stress: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for name, label in STRESS_LABELS.items():
        frame = stress[stress["scenario"] == name].set_index("representation")
        rows.append(
            {
                "Scenario": label,
                "B false certainty": round(float(frame.loc["B", "false_certainty"]), 3),
                "BR false certainty": round(float(frame.loc["BR", "false_certainty"]), 3),
                "D false certainty": round(float(frame.loc["D", "false_certainty"]), 3),
                "E false certainty": round(float(frame.loc["E", "false_certainty"]), 3),
                "E correct unique": round(float(frame.loc["E", "correct_unique"]), 3),
                "E honest ambiguity": round(float(frame.loc["E", "informative_ambiguity"]), 3),
            }
        )
    return pd.DataFrame(rows)


def scenario_outcome_table(scenarios: pd.DataFrame) -> pd.DataFrame:
    from dtrs.plotting.records_figures import SCENARIO_LABELS

    rows = []
    for name, label in SCENARIO_LABELS.items():
        frame = scenarios[scenarios["scenario"] == name].set_index("representation")
        if frame.empty:
            continue
        rows.append(
            {
                "Scenario": label,
                "B false certainty": round(float(frame.loc["B", "false_certainty"]), 3),
                "B correct unique": round(float(frame.loc["B", "correct_unique"]), 3),
                "BR false certainty": round(float(frame.loc["BR", "false_certainty"]), 3),
                "BR correct unique": round(float(frame.loc["BR", "correct_unique"]), 3),
                "E false certainty": round(float(frame.loc["E", "false_certainty"]), 3),
                "E correct unique": round(float(frame.loc["E", "correct_unique"]), 3),
                "E honest ambiguity": round(float(frame.loc["E", "informative_ambiguity"]), 3),
                "B flagged invalid": round(float(frame.loc["B", "flagged_invalid"]), 3),
                "D correct unique": round(float(frame.loc["D", "correct_unique"]), 3),
            }
        )
    return pd.DataFrame(rows)


STRESS_SCENARIOS = (
    "X1_handedness_flip_including_anchor",
    "X2_agreeing_wrong_coordinates_and_relations",
    "X3_consistent_identifier_swap",
    "X4_chirality_anchor_mislabelled",
    "X5_consistent_wrong_epoch",
)
STRESS_REPRESENTATIONS = ("B", "BR", "D", "E")


def stress_record(name: str, representation: str, arrays: dict, settings: dict) -> dict:
    """Corruptions that also reach the independent evidence; all derived fields are re-issued."""
    if name in ("X2_agreeing_wrong_coordinates_and_relations", "X5_consistent_wrong_epoch"):
        damaged = dict(arrays)
        points = np.array(arrays["points"], dtype=float)
        if name == "X2_agreeing_wrong_coordinates_and_relations":
            rng = np.random.default_rng(settings["seed"] + 11)
            for k in settings["perturbed_sites"]:
                direction = rng.normal(size=3)
                points[k] += settings["perturbation_m"] * direction / np.linalg.norm(direction)
        else:
            dt = settings["comparison_epoch"] - settings["reference_epoch"]
            points = points + np.asarray(arrays["velocities"]) * dt
        damaged["points"] = points
        return _build_base(damaged, representation)
    record = _build_base(arrays, representation)
    if name == "X1_handedness_flip_including_anchor":
        _common_mode_flip(record)
        if "anchors" in record:
            record["anchors"]["chirality"]["sign"] *= -1
    elif name == "X3_consistent_identifier_swap":
        entities = record["entities"]
        entities[2], entities[7] = entities[7], entities[2]
    elif name == "X4_chirality_anchor_mislabelled":
        if "anchors" in record:
            record["anchors"]["chirality"]["sign"] *= -1
    refresh_derived(record)
    return record


def run_stress(arrays, query, truth, settings) -> pd.DataFrame:
    frames = []
    for name in STRESS_SCENARIOS:
        for representation in STRESS_REPRESENTATIONS:
            record = stress_record(name, representation, arrays, settings)
            scored = score(decode(record, query), truth)
            frames.append(scored.assign(scenario=name, representation=representation))
    return summarise(pd.concat(frames, ignore_index=True), ["scenario", "representation"])
