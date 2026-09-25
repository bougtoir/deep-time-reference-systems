from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


BLUE = "#1f5a7a"
ORANGE = "#d97706"
GREEN = "#39734d"
RED = "#a33a3a"
GRAY = "#5b6573"


def _save(figure: plt.Figure, path: Path) -> None:
    figure.savefig(path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(figure)


def figure_1_hierarchy(path: Path) -> None:
    figure, axis = plt.subplots(figsize=(7.2, 4.8))
    axis.axis("off")
    rows = [
        ("Labeled entities + epoch", "identity and time index", RED),
        ("+ Euclidean chord distances", "shape modulo Euclidean isometry", BLUE),
        ("+ origin and metric scale", "orthogonal ambiguity O(3)", ORANGE),
        ("+ directed physical axis", "axial ordering; residual O(2)", GREEN),
        ("+ physical chiral witness", "signed relative longitude; residual SO(2)", GREEN),
        ("+ directed meridian", "angular origin; residual {I}", GRAY),
    ]
    for index, (title, subtitle, color) in enumerate(rows):
        y = 0.9 - index * 0.155
        axis.add_patch(
            plt.Rectangle(
                (0.08, y - 0.055),
                0.84,
                0.1,
                facecolor=color,
                alpha=0.14,
                edgecolor=color,
                linewidth=1.5,
            )
        )
        axis.text(0.11, y + 0.012, title, weight="bold", fontsize=10.5, va="center")
        axis.text(0.89, y - 0.018, subtitle, fontsize=9, ha="right", va="center")
        if index < len(rows) - 1:
            axis.annotate(
                "",
                xy=(0.5, y - 0.095),
                xytext=(0.5, y - 0.06),
                arrowprops={"arrowstyle": "->", "color": GRAY},
            )
    axis.set_title(
        "Preserved observables and the spatial meaning they support",
        fontsize=12,
        weight="bold",
    )
    _save(figure, path)


def figure_2_residual_invariance(path: Path) -> None:
    figure, axis = plt.subplots(figsize=(7.2, 4.2))
    axis.axis("off")
    groups = [
        ("O(3)", "centered complete\nchord distances", BLUE),
        ("O(2)", "+ directed axis", GREEN),
        ("SO(2)", "+ physical\nchiral witness", ORANGE),
        ("{I}", "+ directed\nmeridian", GRAY),
    ]
    x_positions = np.linspace(0.12, 0.88, len(groups))
    for index, ((group, condition, color), x_position) in enumerate(
        zip(groups, x_positions)
    ):
        axis.add_patch(
            plt.Circle(
                (x_position, 0.57),
                0.09,
                facecolor=color,
                edgecolor=color,
                alpha=0.17,
                linewidth=2,
            )
        )
        axis.text(
            x_position,
            0.57,
            group,
            ha="center",
            va="center",
            fontsize=14,
            weight="bold",
        )
        axis.text(
            x_position,
            0.31,
            condition,
            ha="center",
            va="center",
            fontsize=9,
        )
        if index < len(groups) - 1:
            axis.annotate(
                "",
                xy=(x_positions[index + 1] - 0.1, 0.57),
                xytext=(x_position + 0.1, 0.57),
                arrowprops={"arrowstyle": "->", "color": "#374151", "linewidth": 1.5},
            )
    axis.text(
        0.5,
        0.1,
        "Known metric scale assumed; otherwise a similarity-scale ambiguity remains",
        ha="center",
        fontsize=9,
        color=RED,
    )
    axis.set_title(
        "Residual invariance group after successive physical anchors",
        weight="bold",
        fontsize=12,
    )
    _save(figure, path)


def figure_3_direction_asymmetry(path: Path) -> None:
    theta = np.linspace(0, 2 * np.pi, 500)
    figure, axes = plt.subplots(1, 2, figsize=(7.2, 3.5))
    for axis, reflected in zip(axes, [False, True]):
        axis.plot(np.cos(theta), np.sin(theta), color=GRAY)
        axis.axhline(0, color="#c7cbd1", linewidth=0.8)
        axis.axvline(0, color="#c7cbd1", linewidth=0.8)
        points = np.array([[0.72, 0.45], [0.72, -0.25]])
        if reflected:
            points[:, 0] *= -1
        axis.scatter(points[:, 0], points[:, 1], color=[BLUE, ORANGE], s=50)
        axis.text(points[0, 0], points[0, 1] + 0.1, "A", ha="center", weight="bold")
        axis.text(points[1, 0], points[1, 1] - 0.14, "B", ha="center", weight="bold")
        axis.annotate(
            "spin axis",
            xy=(0, 1),
            xytext=(0.15, 0.72),
            arrowprops={"arrowstyle": "->", "color": GREEN},
            color=GREEN,
        )
        axis.set_aspect("equal")
        axis.set_xlim(-1.15, 1.15)
        axis.set_ylim(-1.15, 1.15)
        axis.axis("off")
        axis.set_title(
            "Original orientation" if not reflected else "Mirror ambiguity",
            fontsize=10,
        )
    figure.suptitle(
        "Axial reflection preserves axial ordering but reverses signed longitude",
        weight="bold",
    )
    figure.text(
        0.5,
        0.01,
        "Signed longitude is pairwise on the principal branch; poles and antipodes are undefined",
        ha="center",
        fontsize=8,
        color=GRAY,
    )
    _save(figure, path)


def figure_4_benchmark(summary: pd.DataFrame, path: Path) -> None:
    metrics = summary.set_index("metric")["value"]
    labels = ["N/S\nproper", "E/W\nproper", "N/S\nreflection", "E/W\nreflection"]
    values = [
        metrics["proper_rotation_north_south_accuracy"],
        metrics["proper_rotation_east_west_accuracy"],
        metrics["reflection_north_south_accuracy"],
        metrics["reflection_east_west_accuracy"],
    ]
    figure, axis = plt.subplots(figsize=(6.2, 4.0))
    bars = axis.bar(labels, values, color=[GREEN, BLUE, GREEN, ORANGE])
    axis.set_ylim(0, 1.05)
    axis.set_ylabel("Directional sign accuracy")
    axis.set_title("Synthetic recovery under frame change", weight="bold")
    for bar, value in zip(bars, values):
        axis.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.025,
            f"{value:.3f}",
            ha="center",
            fontsize=9,
        )
    _save(figure, path)


def figure_5_uncertainty(uncertainty: pd.DataFrame, path: Path) -> None:
    figure, axes = plt.subplots(1, 2, figsize=(7.2, 3.7), sharey=True)
    for noise, group in uncertainty.groupby("angular_noise_degrees"):
        axes[0].errorbar(
            group["chirality_corruption_probability"],
            group["north_south_accuracy"],
            yerr=np.vstack(
                [
                    group["north_south_accuracy"] - group["north_south_95ci_lower"],
                    group["north_south_95ci_upper"] - group["north_south_accuracy"],
                ]
            ),
            marker="o",
            capsize=2,
            label=f"{noise:g}°",
        )
        axes[1].errorbar(
            group["chirality_corruption_probability"],
            group["east_west_accuracy"],
            yerr=np.vstack(
                [
                    group["east_west_accuracy"] - group["east_west_95ci_lower"],
                    group["east_west_95ci_upper"] - group["east_west_accuracy"],
                ]
            ),
            marker="o",
            capsize=2,
            label=f"{noise:g}°",
        )
    axes[0].set_title("North/south")
    axes[1].set_title("East/west")
    for axis in axes:
        axis.set_xlabel("Handedness corruption probability")
        axis.set_ylim(0.45, 1.02)
        axis.grid(alpha=0.25)
    axes[0].set_ylabel("Classification accuracy")
    axes[1].legend(title="Axis noise", fontsize=7, title_fontsize=8)
    figure.suptitle("Uncertainty and anchor corruption", weight="bold")
    _save(figure, path)


def figure_4_rigidity(rigidity: pd.DataFrame, path: Path) -> None:
    probability = rigidity.pivot(
        index="n_points",
        columns="edge_probability",
        values="full_local_rigidity_probability",
    )
    figure, axis = plt.subplots(figsize=(7.2, 4.1))
    image = axis.imshow(probability, cmap="viridis", vmin=0, vmax=1, aspect="auto")
    axis.set_xticks(
        range(len(probability.columns)),
        [f"{value:.1f}" for value in probability.columns],
    )
    axis.set_yticks(range(len(probability.index)), probability.index)
    axis.set_xlabel("Independent edge-retention probability")
    axis.set_ylabel("Number of points")
    for row in range(probability.shape[0]):
        for column in range(probability.shape[1]):
            value = probability.iloc[row, column]
            axis.text(
                column,
                row,
                f"{value:.2f}",
                ha="center",
                va="center",
                fontsize=7,
                color="white" if value < 0.35 or value > 0.8 else "black",
            )
    axis.set_title(
        "Probability of full local rigidity after removing six Euclidean gauge modes",
        weight="bold",
    )
    figure.colorbar(image, ax=axis, label="Full local-rigidity probability")
    _save(figure, path)


def figure_5_itrf(sites: pd.DataFrame, path: Path) -> None:
    figure, axes = plt.subplots(1, 2, figsize=(7.2, 3.8))
    map_axis, change_axis = axes
    velocities = (
        np.linalg.norm(
            sites[["vx_m_per_year", "vy_m_per_year", "vz_m_per_year"]].to_numpy(),
            axis=1,
        )
        * 1000
    )
    scatter = map_axis.scatter(
        sites["longitude_degrees"],
        sites["latitude_degrees"],
        c=velocities,
        cmap="viridis",
        s=45,
        edgecolor="black",
        linewidth=0.4,
    )
    for _, row in sites.iterrows():
        map_axis.text(
            row["longitude_degrees"] + 2,
            row["latitude_degrees"] + 1,
            row["technique_id"],
            fontsize=6,
        )
    map_axis.set_xlim(-180, 180)
    map_axis.set_ylim(-90, 90)
    map_axis.set_xlabel("Geocentric longitude (degrees)")
    map_axis.set_ylabel("Geocentric latitude (degrees)")
    map_axis.set_title("Selected ITRF2020 SLR sites", fontsize=10)
    map_axis.grid(alpha=0.25)
    figure.colorbar(scatter, ax=map_axis, label="Velocity magnitude (mm yr^-1)")

    present = sites[["x_m", "y_m", "z_m"]].to_numpy()
    comparison = sites[
        ["x_comparison_epoch_m", "y_comparison_epoch_m", "z_comparison_epoch_m"]
    ].to_numpy()
    present_distances = np.linalg.norm(
        present[:, None, :] - present[None, :, :],
        axis=-1,
    )
    comparison_distances = np.linalg.norm(
        comparison[:, None, :] - comparison[None, :, :],
        axis=-1,
    )
    upper_triangle = np.triu_indices(len(sites), 1)
    changes = np.abs(
        comparison_distances[upper_triangle] - present_distances[upper_triangle]
    )
    change_axis.hist(changes, bins=12, color=BLUE, alpha=0.8, edgecolor="white")
    change_axis.axvline(
        np.median(changes),
        color=ORANGE,
        linewidth=2,
        label=f"median = {np.median(changes):.3f} m",
    )
    change_axis.set_xlabel("Absolute pairwise chord-distance change (m)")
    change_axis.set_ylabel("Station pairs")
    change_axis.set_title(
        "Epoch dependence, 2015.0 to 2025.0",
        fontsize=10,
    )
    change_axis.legend(fontsize=8)
    figure.suptitle(
        "ITRF2020 demonstration: realized coordinates and time-indexed relations",
        weight="bold",
    )
    _save(figure, path)


def generate_all_figures(
    synthetic_summary: pd.DataFrame,
    uncertainty: pd.DataFrame,
    itrf_sites: pd.DataFrame,
    rigidity: pd.DataFrame,
    output_directory: str | Path,
) -> None:
    output = Path(output_directory)
    output.mkdir(parents=True, exist_ok=True)
    figure_1_hierarchy(output / "figure_1_representation_hierarchy.png")
    figure_2_residual_invariance(
        output / "figure_2_residual_invariance_hierarchy.png"
    )
    figure_3_direction_asymmetry(output / "figure_3_direction_asymmetry.png")
    figure_4_rigidity(rigidity, output / "figure_4_rigidity_phase_diagram.png")
    figure_5_itrf(itrf_sites, output / "figure_5_itrf_demonstration.png")
    figure_4_benchmark(
        synthetic_summary,
        output / "supplementary_figure_s1_synthetic_benchmark.png",
    )
    figure_5_uncertainty(
        uncertainty,
        output / "supplementary_figure_s2_anchor_sensitivity.png",
    )
