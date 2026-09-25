from dataclasses import dataclass
from enum import Enum

import numpy as np


class LongitudeRelationStatus(str, Enum):
    DEFINED = "defined"
    SAME_MERIDIAN = "same_meridian"
    AXIS_DEGENERACY = "axis_degeneracy"
    ANTIPODAL = "antipodal"
    NEAR_ANTIPODAL = "near_antipodal"


@dataclass(frozen=True)
class AxialOrdering:
    latitude_difference_radians: float
    sign: int
    is_tie: bool


@dataclass(frozen=True)
class SignedLongitudeRelation:
    difference_radians: float
    sign: int
    status: LongitudeRelationStatus

    @property
    def is_defined(self) -> bool:
        return self.status in {
            LongitudeRelationStatus.DEFINED,
            LongitudeRelationStatus.SAME_MERIDIAN,
        }


def ellipsoid_surface(
    latitude_radians: np.ndarray,
    longitude_radians: np.ndarray,
    semi_major_axis_m: float,
    inverse_flattening: float,
) -> np.ndarray:
    flattening = 1.0 / inverse_flattening
    eccentricity_squared = flattening * (2.0 - flattening)
    prime_vertical = semi_major_axis_m / np.sqrt(
        1.0 - eccentricity_squared * np.sin(latitude_radians) ** 2
    )
    x = prime_vertical * np.cos(latitude_radians) * np.cos(longitude_radians)
    y = prime_vertical * np.cos(latitude_radians) * np.sin(longitude_radians)
    z = (
        prime_vertical
        * (1.0 - eccentricity_squared)
        * np.sin(latitude_radians)
    )
    return np.column_stack([x, y, z])


def ecef_to_geocentric(points: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    norms = np.linalg.norm(points, axis=1)
    latitude = np.arcsin(points[:, 2] / norms)
    longitude = np.arctan2(points[:, 1], points[:, 0])
    return latitude, longitude


def _unit_vector(vector: np.ndarray, name: str) -> np.ndarray:
    norm = np.linalg.norm(vector)
    if norm <= np.finfo(float).eps:
        raise ValueError(f"{name} must have nonzero norm")
    return vector / norm


def axial_latitude(point: np.ndarray, directed_axis: np.ndarray) -> float:
    axis = _unit_vector(directed_axis, "directed_axis")
    point_unit = _unit_vector(point, "point")
    return float(np.arcsin(np.clip(np.dot(axis, point_unit), -1.0, 1.0)))


def axial_latitude_ordering(
    point_a: np.ndarray,
    point_b: np.ndarray,
    directed_axis: np.ndarray,
    angular_tolerance_radians: float = 1e-12,
) -> AxialOrdering:
    difference = axial_latitude(point_a, directed_axis) - axial_latitude(
        point_b,
        directed_axis,
    )
    is_tie = abs(difference) <= angular_tolerance_radians
    return AxialOrdering(
        latitude_difference_radians=difference,
        sign=0 if is_tie else int(np.sign(difference)),
        is_tie=is_tie,
    )


def signed_longitude_relation(
    point_a: np.ndarray,
    point_b: np.ndarray,
    directed_axis: np.ndarray,
    *,
    axial_tolerance: float = 1e-12,
    angular_tolerance_radians: float = 1e-12,
    antipodal_tolerance_radians: float = 1e-8,
) -> SignedLongitudeRelation:
    axis = _unit_vector(directed_axis, "directed_axis")
    point_a_norm = np.linalg.norm(point_a)
    point_b_norm = np.linalg.norm(point_b)
    if point_a_norm <= np.finfo(float).eps or point_b_norm <= np.finfo(float).eps:
        raise ValueError("points must have nonzero norm")
    a = point_a - axis * np.dot(axis, point_a)
    b = point_b - axis * np.dot(axis, point_b)
    if (
        np.linalg.norm(a) <= axial_tolerance * point_a_norm
        or np.linalg.norm(b) <= axial_tolerance * point_b_norm
    ):
        return SignedLongitudeRelation(
            difference_radians=float("nan"),
            sign=0,
            status=LongitudeRelationStatus.AXIS_DEGENERACY,
        )
    a /= np.linalg.norm(a)
    b /= np.linalg.norm(b)
    sine = float(np.dot(axis, np.cross(b, a)))
    cosine = float(np.clip(np.dot(a, b), -1.0, 1.0))
    absolute_angle = float(np.arctan2(abs(sine), cosine))
    if np.pi - absolute_angle <= angular_tolerance_radians:
        return SignedLongitudeRelation(
            difference_radians=float("nan"),
            sign=0,
            status=LongitudeRelationStatus.ANTIPODAL,
        )
    if np.pi - absolute_angle <= antipodal_tolerance_radians:
        return SignedLongitudeRelation(
            difference_radians=float("nan"),
            sign=0,
            status=LongitudeRelationStatus.NEAR_ANTIPODAL,
        )
    difference = float(np.arctan2(sine, cosine))
    if abs(difference) <= angular_tolerance_radians:
        return SignedLongitudeRelation(
            difference_radians=0.0,
            sign=0,
            status=LongitudeRelationStatus.SAME_MERIDIAN,
        )
    return SignedLongitudeRelation(
        difference_radians=difference,
        sign=int(np.sign(difference)),
        status=LongitudeRelationStatus.DEFINED,
    )


def signed_longitude_difference(
    point_a: np.ndarray,
    point_b: np.ndarray,
    spin_axis: np.ndarray,
) -> float:
    relation = signed_longitude_relation(point_a, point_b, spin_axis)
    if not relation.is_defined:
        return float("nan")
    return relation.difference_radians


def relation_signs(
    point_a: np.ndarray,
    point_b: np.ndarray,
    spin_axis: np.ndarray,
) -> tuple[int, int]:
    axial = axial_latitude_ordering(point_a, point_b, spin_axis)
    longitude = signed_longitude_relation(point_a, point_b, spin_axis)
    return axial.sign, longitude.sign


def local_enu_basis(
    geodetic_latitude_radians: float,
    longitude_radians: float,
) -> np.ndarray:
    sin_latitude = np.sin(geodetic_latitude_radians)
    cos_latitude = np.cos(geodetic_latitude_radians)
    sin_longitude = np.sin(longitude_radians)
    cos_longitude = np.cos(longitude_radians)
    east = np.array([-sin_longitude, cos_longitude, 0.0])
    north = np.array(
        [
            -sin_latitude * cos_longitude,
            -sin_latitude * sin_longitude,
            cos_latitude,
        ]
    )
    up = np.array(
        [
            cos_latitude * cos_longitude,
            cos_latitude * sin_longitude,
            sin_latitude,
        ]
    )
    return np.vstack([east, north, up])
