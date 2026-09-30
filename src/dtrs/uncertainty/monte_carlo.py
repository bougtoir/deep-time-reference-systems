import numpy as np
from scipy.spatial.transform import Rotation

from dtrs.frames import axial_reflection
from dtrs.geodesy import relation_signs


def axis_perturbation(
    axis: np.ndarray,
    standard_deviation_degrees: float,
    rng: np.random.Generator,
) -> np.ndarray:
    normalized_axis = axis / np.linalg.norm(axis)
    tangent = rng.normal(size=3)
    tangent -= normalized_axis * np.dot(normalized_axis, tangent)
    tangent_norm = np.linalg.norm(tangent)
    if tangent_norm <= np.finfo(float).eps:
        tangent = np.cross(normalized_axis, np.array([1.0, 0.0, 0.0]))
        if np.linalg.norm(tangent) <= np.finfo(float).eps:
            tangent = np.cross(normalized_axis, np.array([0.0, 1.0, 0.0]))
    tangent /= np.linalg.norm(tangent)
    angle = rng.normal(scale=np.deg2rad(standard_deviation_degrees))
    perturbation = Rotation.from_rotvec(tangent * angle).as_matrix()
    return perturbation @ axis


def corruption_experiment(
    point_a: np.ndarray,
    point_b: np.ndarray,
    axis: np.ndarray,
    corruption_probability: float,
    angular_noise_degrees: float,
    trials: int,
    rng: np.random.Generator,
) -> tuple[float, float]:
    expected = relation_signs(point_a, point_b, axis)
    north_south_correct = 0
    east_west_correct = 0
    reflection = axial_reflection()
    for _ in range(trials):
        perturbed_axis = axis_perturbation(axis, angular_noise_degrees, rng)
        a = point_a
        b = point_b
        if rng.random() < corruption_probability:
            a = reflection @ a
            b = reflection @ b
            perturbed_axis = reflection @ perturbed_axis
        observed = relation_signs(a, b, perturbed_axis)
        north_south_correct += observed[0] == expected[0]
        east_west_correct += observed[1] == expected[1]
    return (
        north_south_correct / trials,
        east_west_correct / trials,
    )
