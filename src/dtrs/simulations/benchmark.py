import numpy as np
import pandas as pd

from dtrs.frames import axial_reflection
from dtrs.geodesy import ellipsoid_surface, relation_signs
from dtrs.geometry import classical_mds, pairwise_distances, procrustes_align, random_rotation
from dtrs.uncertainty import corruption_experiment


def wilson_interval(success_probability: float, trials: int) -> tuple[float, float]:
    z = 1.959963984540054
    denominator = 1.0 + z**2 / trials
    center = (success_probability + z**2 / (2 * trials)) / denominator
    half_width = (
        z
        * np.sqrt(
            success_probability * (1.0 - success_probability) / trials
            + z**2 / (4 * trials**2)
        )
        / denominator
    )
    return center - half_width, center + half_width


def generate_ellipsoid_points(
    n_points: int,
    semi_major_axis_m: float,
    inverse_flattening: float,
    rng: np.random.Generator,
) -> np.ndarray:
    latitude = np.arcsin(rng.uniform(-0.95, 0.95, size=n_points))
    longitude = rng.uniform(-np.pi, np.pi, size=n_points)
    return ellipsoid_surface(
        latitude,
        longitude,
        semi_major_axis_m,
        inverse_flattening,
    )


def run_ellipsoid_sensitivity(config: dict) -> pd.DataFrame:
    rng = np.random.default_rng(config["seed"])
    synthetic = config["synthetic"]
    baseline = synthetic["ellipsoid"]
    comparison = synthetic["ellipsoid_sensitivity"]
    latitude = np.arcsin(rng.uniform(-0.95, 0.95, size=synthetic["n_points"]))
    longitude = rng.uniform(-np.pi, np.pi, size=synthetic["n_points"])
    baseline_points = ellipsoid_surface(
        latitude,
        longitude,
        baseline["semi_major_axis_m"],
        baseline["inverse_flattening"],
    )
    comparison_points = ellipsoid_surface(
        latitude,
        longitude,
        comparison["semi_major_axis_m"],
        comparison["inverse_flattening"],
    )
    coordinate_displacement = np.linalg.norm(
        comparison_points - baseline_points,
        axis=1,
    )
    distance_difference = pairwise_distances(comparison_points) - pairwise_distances(
        baseline_points
    )
    upper_triangle = np.triu_indices(synthetic["n_points"], 1)
    axis = np.array([0.0, 0.0, 1.0])
    pairs = [(first, second) for first in range(len(baseline_points)) for second in range(first)]
    baseline_relations = np.array(
        [
            relation_signs(baseline_points[first], baseline_points[second], axis)
            for first, second in pairs
        ]
    )
    comparison_relations = np.array(
        [
            relation_signs(comparison_points[first], comparison_points[second], axis)
            for first, second in pairs
        ]
    )
    return pd.DataFrame(
        [
            {
                "metric": "ellipsoid_maximum_coordinate_difference_m",
                "value": np.max(coordinate_displacement),
                "unit": "m",
            },
            {
                "metric": "ellipsoid_median_coordinate_difference_m",
                "value": np.median(coordinate_displacement),
                "unit": "m",
            },
            {
                "metric": "ellipsoid_maximum_chord_distance_difference_m",
                "value": np.max(np.abs(distance_difference[upper_triangle])),
                "unit": "m",
            },
            {
                "metric": "ellipsoid_median_chord_distance_difference_m",
                "value": np.median(np.abs(distance_difference[upper_triangle])),
                "unit": "m",
            },
            {
                "metric": "ellipsoid_axial_ordering_agreement",
                "value": np.mean(
                    baseline_relations[:, 0] == comparison_relations[:, 0]
                ),
                "unit": "proportion",
            },
            {
                "metric": "ellipsoid_signed_longitude_agreement",
                "value": np.mean(
                    baseline_relations[:, 1] == comparison_relations[:, 1]
                ),
                "unit": "proportion",
            },
        ]
    )


def run_synthetic_benchmark(config: dict) -> tuple[pd.DataFrame, pd.DataFrame]:
    rng = np.random.default_rng(config["seed"])
    synthetic = config["synthetic"]
    ellipsoid = synthetic["ellipsoid"]
    points = generate_ellipsoid_points(
        synthetic["n_points"],
        ellipsoid["semi_major_axis_m"],
        ellipsoid["inverse_flattening"],
        rng,
    )
    distances = pairwise_distances(points)
    reconstructed = classical_mds(distances)
    _, _, reflected_rmse = procrustes_align(
        reconstructed,
        points,
        allow_reflection=True,
    )
    _, _, proper_rmse = procrustes_align(
        reconstructed,
        points,
        allow_reflection=False,
    )
    axis = np.array([0.0, 0.0, 1.0])
    expected = np.array(
        [relation_signs(points[i], points[j], axis) for i in range(len(points)) for j in range(i)]
    )
    proper_matches = []
    reflected_matches = []
    reflection = axial_reflection()
    for _ in range(synthetic["n_frame_trials"]):
        rotation = random_rotation(rng)
        rotated_points = points @ rotation.T
        rotated_axis = rotation @ axis
        proper = np.array(
            [
                relation_signs(rotated_points[i], rotated_points[j], rotated_axis)
                for i in range(len(points))
                for j in range(i)
            ]
        )
        reflected_points = rotated_points @ reflection.T
        reflected_axis = reflection @ rotated_axis
        reflected = np.array(
            [
                relation_signs(reflected_points[i], reflected_points[j], reflected_axis)
                for i in range(len(points))
                for j in range(i)
            ]
        )
        proper_matches.append((proper == expected).mean(axis=0))
        reflected_matches.append((reflected == expected).mean(axis=0))
    proper_matches_array = np.array(proper_matches)
    reflected_matches_array = np.array(reflected_matches)
    summary = pd.DataFrame(
        [
            {
                "metric": "synthetic_number_of_points",
                "value": synthetic["n_points"],
            },
            {
                "metric": "synthetic_frame_trials",
                "value": synthetic["n_frame_trials"],
            },
            {
                "metric": "synthetic_monte_carlo_trials_per_condition",
                "value": synthetic["monte_carlo_trials"],
            },
            {
                "metric": "distance_reconstruction_rmse_allow_reflection_m",
                "value": reflected_rmse,
            },
            {
                "metric": "distance_reconstruction_rmse_proper_only_m",
                "value": proper_rmse,
            },
            {
                "metric": "proper_rotation_north_south_accuracy",
                "value": proper_matches_array[:, 0].mean(),
            },
            {
                "metric": "proper_rotation_east_west_accuracy",
                "value": proper_matches_array[:, 1].mean(),
            },
            {
                "metric": "reflection_north_south_accuracy",
                "value": reflected_matches_array[:, 0].mean(),
            },
            {
                "metric": "reflection_east_west_accuracy",
                "value": reflected_matches_array[:, 1].mean(),
            },
        ]
    )
    pair = ellipsoid_surface(
        np.deg2rad(np.array([20.0, 20.4])),
        np.deg2rad(np.array([10.0, 10.4])),
        ellipsoid["semi_major_axis_m"],
        ellipsoid["inverse_flattening"],
    )
    uncertainty_rows = []
    for noise in synthetic["angular_noise_degrees"]:
        for corruption in synthetic["anchor_corruption_probabilities"]:
            north_south, east_west = corruption_experiment(
                pair[1],
                pair[0],
                axis,
                corruption,
                noise,
                synthetic["monte_carlo_trials"],
                rng,
            )
            north_south_lower, north_south_upper = wilson_interval(
                north_south,
                synthetic["monte_carlo_trials"],
            )
            east_west_lower, east_west_upper = wilson_interval(
                east_west,
                synthetic["monte_carlo_trials"],
            )
            uncertainty_rows.append(
                {
                    "angular_noise_degrees": noise,
                    "chirality_corruption_probability": corruption,
                    "north_south_accuracy": north_south,
                    "north_south_95ci_lower": north_south_lower,
                    "north_south_95ci_upper": north_south_upper,
                    "east_west_accuracy": east_west,
                    "east_west_95ci_lower": east_west_lower,
                    "east_west_95ci_upper": east_west_upper,
                }
            )
    return summary, pd.DataFrame(uncertainty_rows)
