import numpy as np

from dtrs.geometry import (
    classical_mds,
    oriented_volume,
    pairwise_distances,
    procrustes_align,
    random_rotation,
)


def test_distances_are_invariant_to_rigid_transform() -> None:
    rng = np.random.default_rng(4)
    points = rng.normal(size=(12, 3))
    rotation = random_rotation(rng)
    transformed = points @ rotation.T + np.array([4.0, -2.0, 8.0])
    np.testing.assert_allclose(
        pairwise_distances(points),
        pairwise_distances(transformed),
        atol=1e-12,
    )


def test_complete_distances_reconstruct_up_to_reflection() -> None:
    rng = np.random.default_rng(8)
    points = rng.normal(size=(10, 3))
    reconstructed = classical_mds(pairwise_distances(points))
    _, _, rmse = procrustes_align(reconstructed, points, allow_reflection=True)
    assert rmse < 1e-10


def test_oriented_volume_changes_sign_under_reflection() -> None:
    tetrahedron = np.array(
        [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    )
    reflection = np.diag([1.0, -1.0, 1.0])
    assert np.sign(oriented_volume(tetrahedron)) == -np.sign(
        oriented_volume(tetrahedron @ reflection.T)
    )
