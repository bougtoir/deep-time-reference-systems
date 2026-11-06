import numpy as np

from dtrs.geometry import classical_mds, procrustes_align


def reconstruct_from_distances(
    distances: np.ndarray,
    reference_points: np.ndarray | None = None,
    allow_reflection: bool = True,
) -> tuple[np.ndarray, float | None]:
    reconstructed = classical_mds(distances)
    if reference_points is None:
        return reconstructed, None
    aligned, _, rmse = procrustes_align(
        reconstructed,
        reference_points,
        allow_reflection=allow_reflection,
    )
    return aligned, rmse
