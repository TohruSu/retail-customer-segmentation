"""Technical checks for exploratory clustering of fictional retail records.

These diagnostics compare algorithmic partitions. Neither silhouette nor adjusted
Rand agreement establishes real customer segments or a business target.
"""

from __future__ import annotations

from itertools import combinations
from numbers import Integral

import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, silhouette_score


def _check_matrix(matrix: np.ndarray) -> np.ndarray:
    """Require usable, finite feature rows before computing model diagnostics."""
    values = np.asarray(matrix, dtype=float)
    if values.ndim != 2 or values.shape[1] == 0:
        raise ValueError("Clustering requires a two-dimensional, nonempty feature matrix.")
    if values.shape[0] < 3:
        raise ValueError("Clustering diagnostics require at least three records.")
    if not np.isfinite(values).all():
        raise ValueError("Prepared clustering features must all be finite.")
    return values


def check_cluster_count(matrix: np.ndarray, k: int) -> np.ndarray:
    """Validate that a k-means partition and its silhouette can be evaluated."""
    values = _check_matrix(matrix)
    if isinstance(k, bool) or not isinstance(k, Integral) or int(k) < 2:
        raise ValueError("Each candidate k must be an integer of at least 2.")
    if int(k) >= len(values):
        raise ValueError(f"Candidate k={k} requires more than {k} records to evaluate silhouette.")
    distinct = len(np.unique(values, axis=0))
    if distinct < int(k):
        raise ValueError(
            f"Candidate k={k} needs at least {k} distinct prepared feature rows; "
            f"only {distinct} are available."
        )
    return values


def summarize_partition(matrix: np.ndarray, labels: np.ndarray) -> dict[str, float]:
    """Return silhouette and size balance for an actually fitted partition."""
    values = _check_matrix(matrix)
    assignments = np.asarray(labels)
    if assignments.ndim != 1 or len(assignments) != len(values):
        raise ValueError("Cluster labels must contain one assignment per feature row.")
    unique, counts = np.unique(assignments, return_counts=True)
    if not 2 <= len(unique) < len(values):
        raise ValueError("Silhouette requires between 2 and n_records - 1 nonempty clusters.")
    shares = counts / len(values)
    return {
        "silhouette": float(silhouette_score(values, assignments)),
        "min_cluster_share": float(shares.min()),
        "max_cluster_share": float(shares.max()),
    }


def initialization_stability(
    matrix: np.ndarray,
    k: int,
    *,
    seed: int,
    runs: int = 5,
) -> dict[str, float]:
    """Compare every pair of single-initialization fits with adjusted Rand index.

    Separate seeds are drawn deterministically. ``n_init=1`` deliberately measures
    sensitivity to initialization, whereas the main comparison uses ``n_init=10``.
    Cluster-number permutations do not affect adjusted Rand agreement.
    """
    values = check_cluster_count(matrix, k)
    if isinstance(runs, bool) or not isinstance(runs, Integral) or int(runs) < 2:
        raise ValueError("Initialization stability requires at least two integer runs.")
    if isinstance(seed, bool) or not isinstance(seed, Integral) or not 0 <= int(seed) < 2**32:
        raise ValueError("Seed must be an integer between 0 and 2**32 - 1.")
    generator = np.random.default_rng(int(seed))
    seeds = generator.integers(0, 2**32 - 1, size=int(runs), dtype=np.uint32)
    partitions = [
        KMeans(n_clusters=int(k), n_init=1, random_state=int(run_seed)).fit_predict(values)
        for run_seed in seeds
    ]
    agreement = [
        float(adjusted_rand_score(left, right)) for left, right in combinations(partitions, 2)
    ]
    return {
        "initialization_ari_mean": float(np.mean(agreement)),
        "initialization_ari_min": float(np.min(agreement)),
    }


def partition_agreement(reference: np.ndarray, comparison: np.ndarray) -> float:
    """Compare aligned records in two partitions without comparing label numbers."""
    left, right = np.asarray(reference), np.asarray(comparison)
    if left.ndim != 1 or right.ndim != 1 or len(left) != len(right) or not len(left):
        raise ValueError("Partition comparison requires nonempty, aligned label vectors.")
    return float(adjusted_rand_score(left, right))


def candidate_warnings(candidates: list[dict[str, float | int]]) -> list[str]:
    """Flag transparent heuristic diagnostics, without treating them as a target rule."""
    warnings = []
    for candidate in candidates:
        k = candidate["k"]
        if candidate["silhouette"] < 0.25:
            warnings.append(
                f"k={k}: silhouette is below the illustrative 0.25 diagnostic threshold; "
                "separation is weak and the unsegmented baseline remains relevant."
            )
        if candidate["min_cluster_share"] < 0.10 or candidate["max_cluster_share"] > 0.70:
            warnings.append(
                f"k={k}: cluster sizes cross an illustrative imbalance threshold "
                "(smallest share < 0.10 or largest share > 0.70)."
            )
        if (
            candidate["initialization_ari_mean"] < 0.80
            or candidate["initialization_ari_min"] < 0.60
        ):
            warnings.append(
                f"k={k}: initialization agreement crosses an illustrative instability "
                "threshold (mean ARI < 0.80 or minimum ARI < 0.60)."
            )
    return warnings
