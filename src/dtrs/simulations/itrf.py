from pathlib import Path

import numpy as np
import pandas as pd

from dtrs.frames import axial_reflection
from dtrs.geodesy import ecef_to_geocentric, relation_signs
from dtrs.geometry import pairwise_distances
from dtrs.reconstruction import reconstruct_from_distances


def parse_itrf_slr(path: str | Path) -> pd.DataFrame:
    records = []
    pending = None
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if " SLR " in line:
            fields = line.split()
            slr_index = fields.index("SLR")
            if slr_index < 2:
                continue
            try:
                pending = {
                    "domes": fields[0],
                    "site_name": " ".join(fields[1:slr_index]),
                    "technique_id": fields[slr_index + 1],
                    "x_m": float(fields[slr_index + 2]),
                    "y_m": float(fields[slr_index + 3]),
                    "z_m": float(fields[slr_index + 4]),
                    "sigma_x_m": float(fields[slr_index + 5]),
                    "sigma_y_m": float(fields[slr_index + 6]),
                    "sigma_z_m": float(fields[slr_index + 7]),
                }
            except (ValueError, IndexError):
                pending = None
        elif pending is not None and line.split() and line.split()[0] == pending["domes"]:
            fields = line.split()
            try:
                pending["vx_m_per_year"] = float(fields[1])
                pending["vy_m_per_year"] = float(fields[2])
                pending["vz_m_per_year"] = float(fields[3])
            except (ValueError, IndexError):
                pending = None
                continue
            records.append(pending)
            pending = None
    frame = pd.DataFrame(records)
    return frame.drop_duplicates("domes", keep="last").reset_index(drop=True)


def select_global_sites(frame: pd.DataFrame, n_sites: int, max_sigma: float) -> pd.DataFrame:
    filtered = frame[
        frame[["sigma_x_m", "sigma_y_m", "sigma_z_m"]].max(axis=1) <= max_sigma
    ].copy()
    points = filtered[["x_m", "y_m", "z_m"]].to_numpy()
    latitude, longitude = ecef_to_geocentric(points)
    filtered["latitude_degrees"] = np.rad2deg(latitude)
    filtered["longitude_degrees"] = np.rad2deg(longitude)
    filtered["maximum_coordinate_sigma_m"] = filtered[
        ["sigma_x_m", "sigma_y_m", "sigma_z_m"]
    ].max(axis=1)
    longitude_bins = pd.cut(
        filtered["longitude_degrees"],
        bins=np.linspace(-180.0, 180.0, n_sites + 1),
        labels=False,
        include_lowest=True,
    )
    selected = (
        filtered.assign(longitude_bin=longitude_bins)
        .sort_values(["longitude_bin", "maximum_coordinate_sigma_m"])
        .groupby("longitude_bin", observed=True)
        .head(1)
        .head(n_sites)
    )
    if len(selected) < n_sites:
        remaining = filtered[~filtered["domes"].isin(selected["domes"])].sort_values(
            ["maximum_coordinate_sigma_m", "sigma_x_m", "sigma_y_m", "sigma_z_m"]
        )
        selected = pd.concat(
            [selected, remaining.head(n_sites - len(selected))],
            ignore_index=True,
        )
    return selected.reset_index(drop=True)


def run_itrf_demonstration(config: dict) -> tuple[pd.DataFrame, pd.DataFrame]:
    settings = config["real_data"]
    sites = select_global_sites(
        parse_itrf_slr(settings["source"]),
        settings["n_sites"],
        settings["max_coordinate_sigma_m"],
    )
    coordinates = sites[["x_m", "y_m", "z_m"]].to_numpy()
    velocities = sites[
        ["vx_m_per_year", "vy_m_per_year", "vz_m_per_year"]
    ].to_numpy()
    distances = pairwise_distances(coordinates)
    _, reconstruction_rmse = reconstruct_from_distances(
        distances,
        coordinates,
        allow_reflection=True,
    )
    reflection = axial_reflection()
    reflected_coordinates = coordinates @ reflection.T
    axis = np.array([0.0, 0.0, 1.0])
    reflected_axis = reflection @ axis
    pairs = [(i, j) for i in range(len(sites)) for j in range(i)]
    original_relations = np.array(
        [relation_signs(coordinates[i], coordinates[j], axis) for i, j in pairs]
    )
    reflected_relations = np.array(
        [
            relation_signs(reflected_coordinates[i], reflected_coordinates[j], reflected_axis)
            for i, j in pairs
        ]
    )
    delta_years = settings["comparison_epoch"] - settings["reference_epoch"]
    future_coordinates = coordinates + velocities * delta_years
    future_distances = pairwise_distances(future_coordinates)
    distance_change = future_distances - distances
    summary = pd.DataFrame(
        [
            {"metric": "n_selected_sites", "value": len(sites), "unit": "count"},
            {
                "metric": "maximum_coordinate_standard_uncertainty_m",
                "value": settings["max_coordinate_sigma_m"],
                "unit": "m",
            },
            {
                "metric": "distance_reconstruction_rmse_m",
                "value": reconstruction_rmse,
                "unit": "m",
            },
            {
                "metric": "axial_reflection_north_south_accuracy",
                "value": (reflected_relations[:, 0] == original_relations[:, 0]).mean(),
                "unit": "proportion",
            },
            {
                "metric": "axial_reflection_east_west_accuracy",
                "value": (reflected_relations[:, 1] == original_relations[:, 1]).mean(),
                "unit": "proportion",
            },
            {
                "metric": "maximum_pairwise_distance_change_m",
                "value": np.max(np.abs(distance_change)),
                "unit": "m",
            },
            {
                "metric": "median_pairwise_distance_change_m",
                "value": np.median(np.abs(distance_change[np.triu_indices(len(sites), 1)])),
                "unit": "m",
            },
            {
                "metric": "reference_epoch",
                "value": settings["reference_epoch"],
                "unit": "decimal_year",
            },
            {
                "metric": "comparison_epoch",
                "value": settings["comparison_epoch"],
                "unit": "decimal_year",
            },
        ]
    )
    sites["reference_epoch"] = settings["reference_epoch"]
    sites["comparison_epoch"] = settings["comparison_epoch"]
    sites["x_comparison_epoch_m"] = future_coordinates[:, 0]
    sites["y_comparison_epoch_m"] = future_coordinates[:, 1]
    sites["z_comparison_epoch_m"] = future_coordinates[:, 2]
    return summary, sites
