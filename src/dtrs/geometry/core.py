import numpy as np


def pairwise_distances(points: np.ndarray) -> np.ndarray:
    differences = points[:, None, :] - points[None, :, :]
    return np.linalg.norm(differences, axis=-1)


def classical_mds(distances: np.ndarray, dimension: int = 3) -> np.ndarray:
    n_points = distances.shape[0]
    centering = np.eye(n_points) - np.ones((n_points, n_points)) / n_points
    gram = -0.5 * centering @ (distances**2) @ centering
    eigenvalues, eigenvectors = np.linalg.eigh(gram)
    order = np.argsort(eigenvalues)[::-1]
    eigenvalues = np.maximum(eigenvalues[order][:dimension], 0.0)
    eigenvectors = eigenvectors[:, order][:, :dimension]
    return eigenvectors * np.sqrt(eigenvalues)


def random_rotation(rng: np.random.Generator) -> np.ndarray:
    matrix = rng.normal(size=(3, 3))
    q, _ = np.linalg.qr(matrix)
    if np.linalg.det(q) < 0:
        q[:, 0] *= -1
    return q


def procrustes_align(
    source: np.ndarray,
    target: np.ndarray,
    allow_reflection: bool = False,
) -> tuple[np.ndarray, np.ndarray, float]:
    source_centered = source - source.mean(axis=0)
    target_centered = target - target.mean(axis=0)
    u, _, vt = np.linalg.svd(source_centered.T @ target_centered)
    transform = u @ vt
    if not allow_reflection and np.linalg.det(transform) < 0:
        u[:, -1] *= -1
        transform = u @ vt
    aligned = source_centered @ transform + target.mean(axis=0)
    rmse = float(np.sqrt(np.mean(np.sum((aligned - target) ** 2, axis=1))))
    return aligned, transform, rmse


def oriented_volume(points: np.ndarray) -> float:
    if points.shape != (4, 3):
        raise ValueError("oriented_volume requires four three-dimensional points")
    return float(
        np.linalg.det(
            np.stack(
                [
                    points[1] - points[0],
                    points[2] - points[0],
                    points[3] - points[0],
                ],
                axis=1,
            )
        )
        / 6.0
    )
