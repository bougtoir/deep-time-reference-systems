import numpy as np


def classification_accuracy(observed: np.ndarray, expected: np.ndarray) -> float:
    return float(np.mean(observed == expected))


def reconstruction_rmse(observed: np.ndarray, expected: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.sum((observed - expected) ** 2, axis=1))))
