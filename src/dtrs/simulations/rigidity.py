import numpy as np
import pandas as pd


def rigidity_matrix(points: np.ndarray, edges: np.ndarray) -> np.ndarray:
    matrix = np.zeros((len(edges), 3 * len(points)))
    for row, (first, second) in enumerate(edges):
        difference = points[first] - points[second]
        matrix[row, 3 * first : 3 * first + 3] = difference
        matrix[row, 3 * second : 3 * second + 3] = -difference
    return matrix


def rigidity_rank(points: np.ndarray, edges: np.ndarray) -> int:
    matrix = rigidity_matrix(points, edges)
    if matrix.size == 0:
        return 0
    singular_values = np.linalg.svd(matrix, compute_uv=False)
    tolerance = max(matrix.shape) * np.finfo(float).eps * singular_values[0]
    return int(np.count_nonzero(singular_values > tolerance))


def complete_graph_edges(n_points: int) -> np.ndarray:
    return np.array(
        [(first, second) for first in range(n_points) for second in range(first)],
        dtype=int,
    )


def sample_graph_edges(
    n_points: int,
    edge_probability: float,
    rng: np.random.Generator,
) -> np.ndarray:
    candidates = complete_graph_edges(n_points)
    included = rng.random(len(candidates)) < edge_probability
    return candidates[included]


def _wilson_interval(successes: int, trials: int) -> tuple[float, float]:
    probability = successes / trials
    z = 1.959963984540054
    denominator = 1.0 + z**2 / trials
    center = (probability + z**2 / (2 * trials)) / denominator
    half_width = (
        z
        * np.sqrt(
            probability * (1.0 - probability) / trials
            + z**2 / (4 * trials**2)
        )
        / denominator
    )
    return center - half_width, center + half_width


def run_rigidity_phase_diagram(config: dict) -> pd.DataFrame:
    settings = config["rigidity"]
    rng = np.random.default_rng(config["seed"] + settings.get("seed_offset", 1000))
    rows = []
    for n_points in settings["n_points"]:
        target_rank = 3 * n_points - 6
        for edge_probability in settings["edge_probabilities"]:
            ranks = []
            edge_counts = []
            for _ in range(settings["trials"]):
                points = rng.normal(size=(n_points, 3))
                edges = sample_graph_edges(n_points, edge_probability, rng)
                ranks.append(rigidity_rank(points, edges))
                edge_counts.append(len(edges))
            ranks_array = np.array(ranks)
            excess_nullity = 3 * n_points - ranks_array - 6
            successes = int(np.count_nonzero(ranks_array == target_rank))
            lower, upper = _wilson_interval(successes, settings["trials"])
            rows.append(
                {
                    "n_points": n_points,
                    "edge_probability": edge_probability,
                    "trials": settings["trials"],
                    "mean_edge_count": float(np.mean(edge_counts)),
                    "full_local_rigidity_probability": successes
                    / settings["trials"],
                    "full_local_rigidity_95ci_lower": lower,
                    "full_local_rigidity_95ci_upper": upper,
                    "mean_excess_nullity": float(np.mean(excess_nullity)),
                    "median_excess_nullity": float(np.median(excess_nullity)),
                }
            )
    return pd.DataFrame(rows)
