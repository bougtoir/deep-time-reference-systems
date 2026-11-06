import numpy as np

from dtrs.simulations.benchmark import (
    run_ellipsoid_sensitivity,
    run_synthetic_benchmark,
    wilson_interval,
)
from dtrs.uncertainty import axis_perturbation
from scripts.run_pipeline import write_manuscript_values


CONFIG = {
    "seed": 11,
    "synthetic": {
        "n_points": 12,
        "n_frame_trials": 10,
        "monte_carlo_trials": 100,
        "ellipsoid": {
            "semi_major_axis_m": 6378137.0,
            "inverse_flattening": 298.257223563,
        },
        "ellipsoid_sensitivity": {
            "semi_major_axis_m": 6378137.0,
            "inverse_flattening": 298.257222101,
        },
        "anchor_corruption_probabilities": [0.0, 0.1],
        "angular_noise_degrees": [0.0, 0.1],
    },
}


def test_seeded_benchmark_is_reproducible() -> None:
    summary_a, uncertainty_a = run_synthetic_benchmark(CONFIG)
    summary_b, uncertainty_b = run_synthetic_benchmark(CONFIG)
    np.testing.assert_allclose(summary_a["value"], summary_b["value"])
    np.testing.assert_allclose(
        uncertainty_a.select_dtypes(include=[float]),
        uncertainty_b.select_dtypes(include=[float]),
    )


def test_proper_alignment_exposes_reflection_ambiguity() -> None:
    summary, _ = run_synthetic_benchmark(CONFIG)
    metrics = summary.set_index("metric")["value"]
    assert (
        metrics["distance_reconstruction_rmse_proper_only_m"]
        > metrics["distance_reconstruction_rmse_allow_reflection_m"]
    )


def test_wgs84_grs80_sensitivity_preserves_directional_relations() -> None:
    sensitivity = run_ellipsoid_sensitivity(CONFIG).set_index("metric")["value"]
    assert sensitivity["ellipsoid_maximum_coordinate_difference_m"] > 0
    assert sensitivity["ellipsoid_axial_ordering_agreement"] == 1.0
    assert sensitivity["ellipsoid_signed_longitude_agreement"] == 1.0


def test_manuscript_values_allow_non_default_uncertainty_grid() -> None:
    summary, uncertainty = run_synthetic_benchmark(
        {
            **CONFIG,
            "synthetic": {
                **CONFIG["synthetic"],
                "anchor_corruption_probabilities": [0.2],
                "angular_noise_degrees": [0.05],
            },
        }
    )
    itrf = summary.iloc[:1].assign(unit="m")
    values = write_manuscript_values(summary, itrf, uncertainty)
    assert not values.empty


def test_axis_perturbation_preserves_axis_norm() -> None:
    axis = np.array([0.0, 0.0, 2.0])
    perturbed = axis_perturbation(axis, 0.2, np.random.default_rng(5))
    np.testing.assert_allclose(np.linalg.norm(perturbed), np.linalg.norm(axis))


def test_wilson_interval_contains_estimate() -> None:
    lower, upper = wilson_interval(0.6, 4000)
    assert lower < 0.6 < upper
    assert upper - lower < 0.04
