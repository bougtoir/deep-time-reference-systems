from pathlib import Path

import numpy as np

from dtrs.simulations.itrf import parse_itrf_slr, select_global_sites


ROOT = Path(__file__).resolve().parents[1]


def test_itrf_parser_reads_positions_and_velocities() -> None:
    frame = parse_itrf_slr(ROOT / "data/raw/itrf2020/ITRF2020_SLR.SSC.txt")
    assert len(frame) > 50
    assert frame["domes"].is_unique
    assert np.isfinite(
        frame[
            ["x_m", "y_m", "z_m", "vx_m_per_year", "vy_m_per_year", "vz_m_per_year"]
        ].to_numpy()
    ).all()


def test_global_selection_is_deterministic() -> None:
    frame = parse_itrf_slr(ROOT / "data/raw/itrf2020/ITRF2020_SLR.SSC.txt")
    first = select_global_sites(frame, 12, 0.02)
    second = select_global_sites(frame, 12, 0.02)
    assert first["domes"].tolist() == second["domes"].tolist()
    assert len(first) == 12
    assert first["longitude_degrees"].max() - first["longitude_degrees"].min() > 250


def test_comparison_epoch_is_recorded_without_fixed_year_labels() -> None:
    from dtrs.simulations.itrf import run_itrf_demonstration

    summary, sites = run_itrf_demonstration(
        {
            "real_data": {
                "source": str(ROOT / "data/raw/itrf2020/ITRF2020_SLR.SSC.txt"),
                "reference_epoch": 2015.0,
                "comparison_epoch": 2035.0,
                "max_coordinate_sigma_m": 0.02,
                "n_sites": 10,
            }
        }
    )
    metrics = summary.set_index("metric")["value"]
    assert metrics["comparison_epoch"] == 2035.0
    assert "x_comparison_epoch_m" in sites
    assert "x_2025_m" not in sites
