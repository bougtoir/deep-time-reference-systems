"""Figures for the relation-record benchmark."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .figures import BLUE, GRAY, GREEN, ORANGE, RED, _save

REPRESENTATION_COLORS = {"A": GRAY, "B": BLUE, "BR": "#6b8fb3", "C": "#9b7bb5", "D": ORANGE, "E": GREEN}
SCENARIO_LABELS = {
    "S0_intact": "S0 intact",
    "S1_crs_block_deleted:standard": "S1a CRS block lost (standard)",
    "S1_crs_block_deleted:left_handed": "S1b CRS block lost (left-handed)",
    "S1_crs_block_deleted:plate_fixed_rotated": "S1c CRS block lost (rotated)",
    "S2_crs_id_missing_params_retained": "S2 CRS id lost, parameters kept",
    "S3_coordinate_epoch_missing": "S3 coordinate epoch lost",
    "S4_silent_left_handed_export": "S4 silent handedness flip",
    "S5_axis_swap_labelled": "S5 labelled axis swap",
    "S6_entity_collision": "S6 identifier collision",
    "S7_chirality_witness_absent": "S7 chiral witness absent",
    "S8_chirality_witness_invalid": "S8 chiral witness invalid",
    "S9_crs_and_witness_lost": "S9 CRS and witness lost",
    "S10_epoch_mislabelled_coordinates": "S10 epoch-mislabelled values",
    "S11_unflagged_coordinate_error": "S11 unflagged 5 cm error",
    "S12_sparse_relations_crs_lost": "S12 sparse relations, CRS lost",
    "S13_epoch_mislabelled_at_export": "S13 epoch mislabel, hash re-issued",
}


def figure_record_architecture(path: Path) -> None:
    figure, axis = plt.subplots(figsize=(7.4, 4.4))
    axis.axis("off")
    boxes = [
        (0.02, 0.62, "Record (JSON)\nentities, coordinates,\nreference system, relations,\nanchors, uncertainty,\nprovenance, hashes", BLUE),
        (0.36, 0.62, "Validator\nstructure + semantics\nfatal / component /\nwarning issues", ORANGE),
        (0.70, 0.62, "Decoder\ncoordinate path\nrelational path\ncross-checks", GREEN),
        (0.36, 0.08, "Independent anchors\norigin, axis, chirality,\nmeridian (evidence type)", GRAY),
        (0.70, 0.08, "Per-task state\nunique | up to group |\nset-valued | probabilistic |\nnon-identifiable | invalid", RED),
    ]
    for x, y, text, color in boxes:
        axis.add_patch(plt.Rectangle((x, y), 0.28, 0.3, facecolor=color, alpha=0.13, edgecolor=color, linewidth=1.5))
        axis.text(x + 0.14, y + 0.15, text, ha="center", va="center", fontsize=7.8)
    arrow = {"arrowstyle": "->", "color": "#374151", "linewidth": 1.4}
    axis.annotate("", xy=(0.36, 0.77), xytext=(0.30, 0.77), arrowprops=arrow)
    axis.annotate("", xy=(0.70, 0.77), xytext=(0.64, 0.77), arrowprops=arrow)
    axis.annotate("", xy=(0.84, 0.38), xytext=(0.84, 0.62), arrowprops=arrow)
    axis.annotate("", xy=(0.74, 0.62), xytext=(0.58, 0.38), arrowprops=arrow)
    axis.set_xlim(0, 1)
    axis.set_ylim(0, 1)
    axis.set_title("Recoverability-aware relation record: data flow", weight="bold", fontsize=12)
    _save(figure, path)


def figure_scenario_outcomes(scenarios: pd.DataFrame, path: Path) -> None:
    order = [name for name in SCENARIO_LABELS if name in set(scenarios["scenario"])]
    representations = ["A", "B", "BR", "C", "D", "E"]
    figure, axes = plt.subplots(1, 2, figsize=(10.5, 6.2), sharey=True)
    for axis, column, title, cmap in (
        (axes[0], "false_certainty", "False-certainty proportion", "Reds"),
        (axes[1], "correct_unique", "Correct unique-answer proportion", "Greens"),
    ):
        matrix = scenarios.pivot(index="scenario", columns="representation", values=column).loc[order, representations]
        image = axis.imshow(matrix.to_numpy(), cmap=cmap, vmin=0, vmax=1, aspect="auto")
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                value = matrix.iat[i, j]
                axis.text(j, i, f"{value:.2f}", ha="center", va="center", fontsize=7,
                          color="white" if value > 0.6 else "black")
        axis.set_xticks(range(len(representations)), representations)
        axis.set_yticks(range(len(order)), [SCENARIO_LABELS[name] for name in order], fontsize=8)
        axis.set_title(title, fontsize=10, weight="bold")
        axis.set_xlabel("Representation")
        figure.colorbar(image, ax=axis, fraction=0.046, pad=0.03)
    _save(figure, path)


def figure_missingness(missingness: pd.DataFrame, path: Path) -> None:
    figure, axes = plt.subplots(2, 2, figsize=(9.0, 6.6), sharex=True)
    mechanisms = [("field_mcar", "Independent field deletion"), ("metadata_block", "Correlated metadata-block loss")]
    for row, (mechanism, label) in enumerate(mechanisms):
        frame = missingness[missingness["mechanism"] == mechanism]
        for representation, color in REPRESENTATION_COLORS.items():
            subset = frame[frame["representation"] == representation].sort_values("rate")
            rate = subset["rate"].to_numpy()
            axes[row, 0].plot(rate, subset["records_with_false_certainty"], marker="o", color=color, label=representation)
            axes[row, 0].fill_between(rate, subset["records_with_false_certainty_95ci_low"],
                                      subset["records_with_false_certainty_95ci_high"], color=color, alpha=0.15)
            axes[row, 1].errorbar(rate, subset["mean_coverage"], yerr=subset["mean_coverage_95ci_halfwidth"],
                                  marker="o", color=color, label=representation, capsize=2)
        axes[row, 0].set_ylabel(f"{label}\nrecords with false certainty")
        axes[row, 1].set_ylabel("Mean correct-unique coverage")
        axes[row, 0].set_yscale("symlog", linthresh=0.01)
        axes[row, 1].set_ylim(0, 1.02)
    for axis in axes[1]:
        axis.set_xlabel("Deletion probability")
    axes[0, 1].legend(ncol=3, fontsize=8, frameon=False)
    _save(figure, path)


def figure_ablation_calibration(ablation: pd.DataFrame, reliability: pd.DataFrame, path: Path) -> None:
    figure, axes = plt.subplots(1, 2, figsize=(10.0, 4.2), gridspec_kw={"width_ratios": [1.5, 1]})
    frame = ablation.set_index("ablation")
    labels = list(frame.index)
    y = np.arange(len(labels))
    left = np.zeros(len(labels))
    for column, color, name in (
        ("correct_unique", GREEN, "correct unique"),
        ("informative_ambiguity", BLUE, "honest ambiguity"),
        ("non_identifiable", GRAY, "non-identifiable"),
        ("false_certainty", RED, "false certainty"),
    ):
        axes[0].barh(y, frame[column], left=left, color=color, label=name)
        left += frame[column].to_numpy()
    for index, value in enumerate(frame["false_certainty"]):
        axes[0].text(1.01, index, f"FC {value:.4f}", va="center", fontsize=7)
    axes[0].set_yticks(y, [label.replace("_", " ") for label in labels], fontsize=8)
    axes[0].invert_yaxis()
    axes[0].set_xlim(0, 1.18)
    axes[0].set_xlabel("Proportion of task items (representation E)")
    axes[0].legend(fontsize=7, loc="upper center", bbox_to_anchor=(0.5, -0.16), ncol=4, frameon=False)
    axes[0].set_title("Field ablation", fontsize=10, weight="bold")
    valid = reliability[reliability["n"] > 0]
    axes[1].plot([0.5, 1.0], [0.5, 1.0], color=GRAY, linestyle="--", linewidth=1)
    axes[1].scatter(valid["mean_predicted"], valid["observed_accuracy"], s=np.sqrt(valid["n"]) * 4, color=ORANGE)
    axes[1].set_xlim(0.48, 1.0)
    axes[1].set_ylim(0.48, 1.0)
    axes[1].set_xlabel("Mean predicted probability")
    axes[1].set_ylabel("Observed accuracy")
    axes[1].set_title("Probabilistic N/S calibration", fontsize=10, weight="bold")
    _save(figure, path)


def generate_record_figures(outputs: dict, sites_figure_source, output_directory: Path) -> None:
    output_directory.mkdir(parents=True, exist_ok=True)
    figure_record_architecture(output_directory / "figure_2_record_architecture.png")
    figure_scenario_outcomes(outputs["scenarios"], output_directory / "figure_4_scenario_outcomes.png")
    figure_missingness(outputs["missingness"], output_directory / "figure_5_missingness.png")
    figure_ablation_calibration(outputs["ablation"], outputs["reliability"],
                                output_directory / "figure_6_ablation_calibration.png")
