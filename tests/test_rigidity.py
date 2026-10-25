from pathlib import Path

import numpy as np
import pandas as pd

from dtrs.simulations.rigidity import (
    complete_graph_edges,
    rigidity_rank,
    run_rigidity_phase_diagram,
)


def test_generic_complete_graph_has_only_euclidean_gauge_nullity() -> None:
    points = np.random.default_rng(17).normal(size=(8, 3))
    assert rigidity_rank(points, complete_graph_edges(len(points))) == 3 * len(points) - 6


def test_tree_distance_graph_is_not_locally_rigid_in_three_dimensions() -> None:
    points = np.random.default_rng(19).normal(size=(8, 3))
    tree_edges = np.array([(index, index - 1) for index in range(1, len(points))])
    assert rigidity_rank(points, tree_edges) < 3 * len(points) - 6


def test_phase_diagram_is_seeded_and_complete_graph_is_rigid() -> None:
    config = {
        "seed": 23,
        "rigidity": {
            "n_points": [6],
            "edge_probabilities": [0.2, 1.0],
            "trials": 10,
            "seed_offset": 50,
        },
    }
    first = run_rigidity_phase_diagram(config)
    second = run_rigidity_phase_diagram(config)
    np.testing.assert_allclose(
        first.select_dtypes(include=[float, int]),
        second.select_dtypes(include=[float, int]),
    )
    complete = first[first["edge_probability"] == 1.0].iloc[0]
    assert complete["full_local_rigidity_probability"] == 1.0
    assert complete["mean_excess_nullity"] == 0.0


def test_canonical_phase_diagram_uses_at_least_1000_trials_per_cell() -> None:
    results = pd.read_csv(
        Path(__file__).parents[1] / "results/rigidity_phase_diagram.csv"
    )
    assert results["trials"].min() >= 1000
