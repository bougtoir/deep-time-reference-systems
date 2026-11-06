import numpy as np

from dtrs.frames import axial_reflection
from dtrs.geodesy import (
    LongitudeRelationStatus,
    axial_latitude_ordering,
    ellipsoid_surface,
    local_enu_basis,
    relation_signs,
    signed_longitude_relation,
)
from dtrs.geometry import random_rotation


def test_local_enu_basis_is_orthonormal() -> None:
    basis = local_enu_basis(np.deg2rad(35.0), np.deg2rad(140.0))
    np.testing.assert_allclose(basis @ basis.T, np.eye(3), atol=1e-12)
    assert np.linalg.det(basis) > 0


def test_direction_signs_survive_proper_rotation() -> None:
    rng = np.random.default_rng(12)
    points = ellipsoid_surface(
        np.deg2rad(np.array([20.0, 35.0])),
        np.deg2rad(np.array([15.0, 70.0])),
        6378137.0,
        298.257223563,
    )
    axis = np.array([0.0, 0.0, 1.0])
    expected = relation_signs(points[1], points[0], axis)
    rotation = random_rotation(rng)
    observed = relation_signs(
        rotation @ points[1],
        rotation @ points[0],
        rotation @ axis,
    )
    assert observed == expected


def test_axial_reflection_preserves_ns_and_reverses_ew() -> None:
    points = ellipsoid_surface(
        np.deg2rad(np.array([20.0, 35.0])),
        np.deg2rad(np.array([15.0, 70.0])),
        6378137.0,
        298.257223563,
    )
    axis = np.array([0.0, 0.0, 1.0])
    expected = relation_signs(points[1], points[0], axis)
    reflection = axial_reflection()
    observed = relation_signs(
        reflection @ points[1],
        reflection @ points[0],
        reflection @ axis,
    )
    assert observed[0] == expected[0]
    assert observed[1] == -expected[1]


def test_pole_is_singular_for_east_direction() -> None:
    pole = np.array([0.0, 0.0, 1.0])
    equator = np.array([1.0, 0.0, 0.0])
    _, east_west = relation_signs(pole, equator, np.array([0.0, 0.0, 1.0]))
    assert east_west == 0


def test_antipodal_points_have_undefined_east_direction() -> None:
    axis = np.array([0.0, 0.0, 1.0])
    point_a = np.array([1.0, 0.0, 0.0])
    point_b = np.array([-1.0, 0.0, 0.0])
    assert relation_signs(point_a, point_b, axis)[1] == 0
    assert relation_signs(point_b, point_a, axis)[1] == 0


def test_exact_and_near_antipodal_relations_are_distinguished() -> None:
    axis = np.array([0.0, 0.0, 1.0])
    point = np.array([1.0, 0.0, 0.0])
    exact = signed_longitude_relation(point, -point, axis)
    near = signed_longitude_relation(
        point,
        np.array([-np.cos(5e-9), np.sin(5e-9), 0.0]),
        axis,
    )
    assert exact.status == LongitudeRelationStatus.ANTIPODAL
    assert near.status == LongitudeRelationStatus.NEAR_ANTIPODAL
    assert np.isnan(exact.difference_radians)
    assert np.isnan(near.difference_radians)


def test_same_meridian_tie_is_not_reported_as_undefined() -> None:
    axis = np.array([0.0, 0.0, 1.0])
    point_a = np.array([1.0, 0.0, 0.2])
    point_b = np.array([2.0, 0.0, -0.1])
    relation = signed_longitude_relation(point_a, point_b, axis)
    assert relation.status == LongitudeRelationStatus.SAME_MERIDIAN
    assert relation.is_defined
    assert relation.sign == 0


def test_signed_longitude_uses_wrapped_principal_branch() -> None:
    axis = np.array([0.0, 0.0, 1.0])
    longitude_a = np.deg2rad(179.0)
    longitude_b = np.deg2rad(-179.0)
    point_a = np.array([np.cos(longitude_a), np.sin(longitude_a), 0.0])
    point_b = np.array([np.cos(longitude_b), np.sin(longitude_b), 0.0])
    relation = signed_longitude_relation(point_a, point_b, axis)
    np.testing.assert_allclose(relation.difference_radians, np.deg2rad(-2.0))
    assert relation.sign == -1


def test_signed_relative_longitude_is_not_transitive() -> None:
    axis = np.array([0.0, 0.0, 1.0])

    def equatorial_point(longitude_degrees: float) -> np.ndarray:
        longitude = np.deg2rad(longitude_degrees)
        return np.array([np.cos(longitude), np.sin(longitude), 0.0])

    point_a = equatorial_point(0.0)
    point_b = equatorial_point(-120.0)
    point_c = equatorial_point(120.0)
    assert signed_longitude_relation(point_a, point_b, axis).sign == 1
    assert signed_longitude_relation(point_b, point_c, axis).sign == 1
    assert signed_longitude_relation(point_c, point_a, axis).sign == 1


def test_axial_ordering_reports_ties_explicitly() -> None:
    axis = np.array([0.0, 0.0, 1.0])
    point_a = np.array([1.0, 0.0, 1.0])
    point_b = np.array([0.0, 1.0, 1.0])
    ordering = axial_latitude_ordering(point_a, point_b, axis)
    assert ordering.is_tie
    assert ordering.sign == 0
