import argparse
from pathlib import Path

import pandas as pd
import yaml

from dtrs.plotting import generate_all_figures
from dtrs.simulations.benchmark import (
    run_ellipsoid_sensitivity,
    run_synthetic_benchmark,
)
from dtrs.simulations.itrf import run_itrf_demonstration
from dtrs.simulations.rigidity import run_rigidity_phase_diagram


ROOT = Path(__file__).resolve().parents[1]


def read_config(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        config = yaml.safe_load(handle)
    config["real_data"]["source"] = str(ROOT / config["real_data"]["source"])
    return config


def model_hierarchy() -> pd.DataFrame:
    return pd.DataFrame(
        [
            [
                "M0",
                "labeled entities only",
                "entity identity only",
                "unconstrained geometry",
            ],
            ["M1", "+ selected chord distances", "recorded edge lengths", "graph-dependent"],
            [
                "M2",
                "+ locally rigid distance graph with known metric scale",
                "local Euclidean shape",
                "Euclidean isometry E(3); possibly discrete noncongruent embeddings",
            ],
            [
                "M3",
                "+ complete labeled Euclidean chord-distance matrix",
                "global Euclidean shape for a generic full-dimensional configuration",
                "translation and O(3)",
            ],
            [
                "M4",
                "+ fixed origin or centered coordinates",
                "origin-referenced shape",
                "O(3)",
            ],
            [
                "M5",
                "+ independently interpreted directed axis",
                "axial latitude ordering",
                "residual invariance group O(2)",
            ],
            [
                "M6",
                "+ physically recoverable chiral witness",
                "signed relative longitude away from degeneracies",
                "proper axial rotations SO(2)",
            ],
            [
                "M7",
                "+ independently recoverable directed meridian",
                "absolute angular origin about the axis",
                "identity",
            ],
            [
                "Metadata",
                "+ observation epoch, entity continuity, units, and model provenance",
                "time-indexed physical interpretation",
                "model and measurement uncertainty remain",
            ],
        ],
        columns=[
            "model",
            "stored_information",
            "identifiable_quantities",
            "remaining_ambiguity",
        ],
    )


def reference_frame_taxonomy() -> pd.DataFrame:
    return pd.DataFrame(
        [
            [
                "Terrestrial reference frame",
                "realized station coordinates and velocities",
                "time-dependent Euclidean/Helmert mapping",
                "high for modern epochs",
                "network/model discontinuity",
                "yes",
                "yes",
            ],
            [
                "Celestial reference frame",
                "extragalactic source directions",
                "celestial rotations",
                "high",
                "source structure and realization change",
                "with Earth orientation",
                "with Earth orientation",
            ],
            [
                "Spin-axis frame",
                "directed angular-momentum/rotation axis",
                "rotation about axis and axial reflection",
                "medium",
                "polar motion and true polar wander",
                "yes",
                "only with physical chirality",
            ],
            [
                "Plate-fixed frame",
                "rigid plate model",
                "plate Euler rotation",
                "medium",
                "deformation and plate reorganization",
                "model-dependent",
                "model-dependent",
            ],
            [
                "Paleomagnetic frame",
                "remanent field direction under field assumptions",
                "axial rotations",
                "geological",
                "remagnetization and GAD violations",
                "paleolatitude",
                "not from paleomagnetism alone",
            ],
            [
                "Hotspot/mantle frame",
                "hotspot tracks or mantle structures",
                "model-specific plate rotations",
                "geological",
                "mantle motion and sparse anchors",
                "model-dependent",
                "model-dependent",
            ],
            [
                "Relative tectonic network",
                "distances/rotations among blocks",
                "network gauge transformations",
                "geological",
                "topology loss and deformation",
                "only with axial anchor",
                "only with orientation anchor",
            ],
            [
                "Hybrid redundant frame",
                "independent geometric, axial, and physical anchors",
                "intersection of preserved symmetries",
                "highest conditional robustness",
                "correlated anchor failure",
                "yes",
                "yes",
            ],
        ],
        columns=[
            "frame",
            "physical_anchor",
            "preserving_transformations",
            "temporal_durability",
            "principal_failure_mode",
            "north_south_support",
            "east_west_support",
        ],
    )


def rigidity_thresholds(rigidity: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for n_points, group in rigidity.groupby("n_points"):
        ordered = group.sort_values("edge_probability")
        probability_50 = ordered[
            ordered["full_local_rigidity_probability"] >= 0.50
        ]
        probability_95 = ordered[
            ordered["full_local_rigidity_probability"] >= 0.95
        ]
        rows.append(
            {
                "n_points": n_points,
                "first_tested_edge_probability_at_or_above_50pct": (
                    probability_50.iloc[0]["edge_probability"]
                    if not probability_50.empty
                    else float("nan")
                ),
                "first_tested_edge_probability_at_or_above_95pct": (
                    probability_95.iloc[0]["edge_probability"]
                    if not probability_95.empty
                    else float("nan")
                ),
                "complete_graph_local_rigidity_probability": ordered.iloc[-1][
                    "full_local_rigidity_probability"
                ],
            }
        )
    return pd.DataFrame(rows)


def write_manuscript_values(
    synthetic: pd.DataFrame,
    itrf: pd.DataFrame,
    uncertainty: pd.DataFrame,
    ellipsoid_sensitivity: pd.DataFrame | None = None,
    rigidity: pd.DataFrame | None = None,
    config: dict | None = None,
) -> pd.DataFrame:
    values = pd.concat(
        [
            synthetic.assign(source="synthetic_benchmark", unit="proportion_or_m"),
            itrf.assign(source="itrf2020_demonstration"),
        ],
        ignore_index=True,
    )
    if config is not None:
        values = pd.concat(
            [
                values,
                pd.DataFrame(
                    [
                        {
                            "metric": "random_seed",
                            "value": config["seed"],
                            "source": "configuration",
                            "unit": "integer",
                        }
                    ]
                ),
            ],
            ignore_index=True,
        )
    if ellipsoid_sensitivity is not None:
        values = pd.concat(
            [
                values,
                ellipsoid_sensitivity.assign(source="ellipsoid_sensitivity"),
            ],
            ignore_index=True,
        )
    if rigidity is not None and not rigidity.empty:
        largest_network = rigidity["n_points"].max()
        largest_rows = rigidity[rigidity["n_points"] == largest_network].sort_values(
            "edge_probability"
        )
        values = pd.concat(
            [
                values,
                pd.DataFrame(
                    [
                        {
                            "metric": "rigidity_largest_network_n_points",
                            "value": largest_network,
                            "source": "rigidity_phase_diagram",
                            "unit": "count",
                        },
                        {
                            "metric": "rigidity_trials_per_cell",
                            "value": largest_rows.iloc[0]["trials"],
                            "source": "rigidity_phase_diagram",
                            "unit": "count",
                        },
                    ]
                ),
            ],
            ignore_index=True,
        )
        threshold_rows = largest_rows[
            largest_rows["full_local_rigidity_probability"] >= 0.95
        ]
        if not threshold_rows.empty:
            threshold_row = threshold_rows.iloc[0]
            preceding_rows = largest_rows[
                largest_rows["edge_probability"] < threshold_row["edge_probability"]
            ]
            threshold_values = [
                {
                    "metric": "rigidity_95pct_threshold_edge_probability",
                    "value": threshold_row["edge_probability"],
                    "source": "rigidity_phase_diagram",
                    "unit": "probability",
                },
                {
                    "metric": "rigidity_probability_at_95pct_threshold",
                    "value": threshold_row["full_local_rigidity_probability"],
                    "source": "rigidity_phase_diagram",
                    "unit": "proportion",
                },
                {
                    "metric": "rigidity_95pct_threshold_95ci_lower",
                    "value": threshold_row["full_local_rigidity_95ci_lower"],
                    "source": "rigidity_phase_diagram",
                    "unit": "proportion",
                },
                {
                    "metric": "rigidity_95pct_threshold_95ci_upper",
                    "value": threshold_row["full_local_rigidity_95ci_upper"],
                    "source": "rigidity_phase_diagram",
                    "unit": "proportion",
                },
            ]
            if not preceding_rows.empty:
                preceding_row = preceding_rows.iloc[-1]
                threshold_values.extend(
                    [
                        {
                            "metric": "rigidity_edge_probability_before_95pct_threshold",
                            "value": preceding_row["edge_probability"],
                            "source": "rigidity_phase_diagram",
                            "unit": "probability",
                        },
                        {
                            "metric": "rigidity_probability_before_95pct_threshold",
                            "value": preceding_row[
                                "full_local_rigidity_probability"
                            ],
                            "source": "rigidity_phase_diagram",
                            "unit": "proportion",
                        },
                        {
                            "metric": (
                                "rigidity_probability_before_95pct_threshold_95ci_lower"
                            ),
                            "value": preceding_row[
                                "full_local_rigidity_95ci_lower"
                            ],
                            "source": "rigidity_phase_diagram",
                            "unit": "proportion",
                        },
                        {
                            "metric": (
                                "rigidity_probability_before_95pct_threshold_95ci_upper"
                            ),
                            "value": preceding_row[
                                "full_local_rigidity_95ci_upper"
                            ],
                            "source": "rigidity_phase_diagram",
                            "unit": "proportion",
                        },
                    ]
                )
            values = pd.concat(
                [
                    values,
                    pd.DataFrame(threshold_values),
                ],
                ignore_index=True,
            )
    zero_noise = uncertainty[uncertainty["angular_noise_degrees"] == 0.0]
    for corruption in [0.1, 0.4]:
        rows = zero_noise[
            zero_noise["chirality_corruption_probability"] == corruption
        ]
        if rows.empty:
            continue
        row = rows.iloc[0]
        values = pd.concat(
            [
                values,
                pd.DataFrame(
                    [
                        {
                            "metric": f"north_south_accuracy_at_{corruption:g}_chirality_corruption",
                            "value": row["north_south_accuracy"],
                            "source": "uncertainty_benchmark",
                            "unit": "proportion",
                        },
                        {
                            "metric": f"east_west_accuracy_at_{corruption:g}_chirality_corruption",
                            "value": row["east_west_accuracy"],
                            "source": "uncertainty_benchmark",
                            "unit": "proportion",
                        },
                        {
                            "metric": f"east_west_accuracy_at_{corruption:g}_chirality_corruption_95ci_lower",
                            "value": row["east_west_95ci_lower"],
                            "source": "uncertainty_benchmark",
                            "unit": "proportion",
                        },
                        {
                            "metric": f"east_west_accuracy_at_{corruption:g}_chirality_corruption_95ci_upper",
                            "value": row["east_west_95ci_upper"],
                            "source": "uncertainty_benchmark",
                            "unit": "proportion",
                        },
                    ]
                ),
            ],
            ignore_index=True,
        )
    return values


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/default.yml")
    arguments = parser.parse_args()
    config = read_config(ROOT / arguments.config)
    synthetic, uncertainty = run_synthetic_benchmark(config)
    ellipsoid_sensitivity = run_ellipsoid_sensitivity(config)
    rigidity = run_rigidity_phase_diagram(config)
    itrf, sites = run_itrf_demonstration(config)
    for directory in ["results", "data/processed", "tables", "figures"]:
        (ROOT / directory).mkdir(parents=True, exist_ok=True)
    synthetic.to_csv(ROOT / "results/synthetic_summary.csv", index=False)
    uncertainty.to_csv(ROOT / "results/uncertainty_results.csv", index=False)
    ellipsoid_sensitivity.to_csv(
        ROOT / "results/ellipsoid_sensitivity.csv",
        index=False,
    )
    rigidity.to_csv(ROOT / "results/rigidity_phase_diagram.csv", index=False)
    itrf.to_csv(ROOT / "results/itrf_summary.csv", index=False)
    sites.to_csv(ROOT / "data/processed/itrf_selected_sites.csv", index=False)
    hierarchy = model_hierarchy()
    taxonomy = reference_frame_taxonomy()
    rigidity_summary = rigidity_thresholds(rigidity)
    hierarchy.to_csv(ROOT / "tables/table_1_identifiability_hierarchy.csv", index=False)
    taxonomy.to_csv(ROOT / "tables/table_2_reference_frame_taxonomy.csv", index=False)
    rigidity_summary.to_csv(
        ROOT / "tables/table_3_rigidity_thresholds.csv",
        index=False,
    )
    ellipsoid_sensitivity.to_csv(
        ROOT / "tables/table_s1_ellipsoid_sensitivity.csv",
        index=False,
    )
    values = write_manuscript_values(
        synthetic,
        itrf,
        uncertainty,
        ellipsoid_sensitivity,
        rigidity,
        config,
    )
    values.to_csv(ROOT / "results/manuscript_values.csv", index=False)
    generate_all_figures(synthetic, uncertainty, sites, rigidity, ROOT / "figures")
    traceability = pd.DataFrame(
        [
            [
                "C1",
                "Results: synthetic benchmark",
                "Complete distances reconstruct shape modulo Euclidean isometry",
                "synthetic ellipsoid points",
                "distance_reconstruction_rmse_allow_reflection_m",
                "scripts/run_pipeline.py",
                arguments.config,
                "Supplementary Fig. S1",
                "verified_by_test",
            ],
            [
                "C2",
                "Results: symmetry experiment",
                "Axial reflection preserves N/S and reverses E/W",
                "synthetic ellipsoid points",
                "reflection_*_accuracy",
                "scripts/run_pipeline.py",
                arguments.config,
                "Fig. 3; Supplementary Fig. S1",
                "verified_by_test",
            ],
            [
                "C3",
                "Results: uncertainty",
                "Handedness corruption selectively degrades E/W",
                "Monte Carlo simulation",
                "*_accuracy",
                "scripts/run_pipeline.py",
                arguments.config,
                "Supplementary Fig. S2",
                "verified_by_seeded_run",
            ],
            [
                "C4",
                "Results: ITRF2020",
                "The frame-loss ambiguity occurs in realized geodetic coordinates",
                "ITRF2020 SLR station file",
                "axial_reflection_*_accuracy",
                "scripts/run_pipeline.py",
                arguments.config,
                "Fig. 5",
                "verified_by_checksum",
            ],
            [
                "C5",
                "Results: incomplete distance networks",
                "Local rigidity emerges as graph density increases",
                "Seeded generic three-dimensional frameworks",
                "full_local_rigidity_probability; full_local_rigidity_95ci_*; "
                "mean_excess_nullity",
                "src/dtrs/simulations/rigidity.py",
                arguments.config,
                "Fig. 4; Table 3",
                "verified_by_seeded_run_and_rank_tests",
            ],
            [
                "C6",
                "Results: ellipsoid sensitivity",
                "WGS84 versus GRS80 does not change directional classifications",
                "Common seeded geodetic latitude/longitude sample",
                "ellipsoid_*",
                "src/dtrs/simulations/benchmark.py",
                arguments.config,
                "Supplementary Table S1",
                "verified_by_seeded_run",
            ],
        ],
        columns=[
            "claim_id",
            "manuscript_section",
            "reported_value_or_claim",
            "source_dataset",
            "source_field",
            "generating_script",
            "config",
            "figure_or_table",
            "verification_status",
        ],
    )
    traceability.to_csv(ROOT / "result_traceability.csv", index=False)
    print(values.to_string(index=False))


if __name__ == "__main__":
    main()
