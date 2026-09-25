import numpy as np


def transform_frame(
    points: np.ndarray,
    transform: np.ndarray,
    translation: np.ndarray | None = None,
) -> np.ndarray:
    shifted = points @ transform.T
    if translation is not None:
        shifted = shifted + translation
    return shifted


def axial_reflection() -> np.ndarray:
    return np.diag([1.0, -1.0, 1.0])
