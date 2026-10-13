"""Reproducible exploratory partitions, baselines, and sensitivity diagnostics.

Only independently generated synthetic inputs belong in this portfolio workflow.
Behavioral visit variables describe partitions but never enter their fit.
"""

from __future__ import annotations

import platform
from collections.abc import Iterable
from importlib.metadata import version
from numbers import Integral
from typing import Any

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from threadpoolctl import threadpool_limits

from .evaluation import (
    candidate_warnings,
    check_cluster_count,
    initialization_stability,
    partition_agreement,
    summarize_partition,
)
from .preprocess import prepare_features
from .schema import ATTITUDE_COLUMNS, BEHAVIOR_COLUMNS, SYNTHETIC_NOTICE
from .validation import validate_data


def _observed_means(frame: pd.DataFrame) -> dict[str, float | None]:
    """Summarize observed cells; do not present imputed values as observed profiles."""
    summary = {}
    for column in (*ATTITUDE_COLUMNS, *BEHAVIOR_COLUMNS):
        mean = frame[column].mean()
        summary[column] = None if pd.isna(mean) else float(mean)
    return summary


def _profile_rows(frame: pd.DataFrame, labels: np.ndarray) -> list[dict[str, Any]]:
    return [
        {
            "cluster": int(cluster),
            "count": int((labels == cluster).sum()),
            "share": float((labels == cluster).mean()),
            **_observed_means(frame.loc[labels == cluster]),
        }
        for cluster in np.unique(labels)
    ]


def _baselines(frame: pd.DataFrame) -> dict[str, Any]:
    convenience = frame["convenience_preference"]
    strata = [
        ("convenience_proxy_at_least_4", convenience.ge(4)),
        ("convenience_proxy_below_4", convenience.lt(4)),
        ("convenience_proxy_missing", convenience.isna()),
    ]
    return {
        "unsegmented": {"count": int(len(frame)), **_observed_means(frame)},
        "descriptive_strata": [
            {
                "stratum": name,
                "count": int(mask.sum()),
                "share": float(mask.mean()),
                **_observed_means(frame.loc[mask]),
            }
            for name, mask in strata
            if mask.any()
        ],
        "stratification_rule": (
            "A predeclared illustrative convenience_preference threshold of 4: "
            "observed values >= 4 versus < 4, with missing values kept separate. "
            "This descriptive grouping is neither a learned segment nor a managerial target."
        ),
    }


def _json_native(value: Any) -> Any:
    """Keep strict JSON writers usable even if preprocessing returns NumPy metadata."""
    if isinstance(value, dict):
        return {str(key): _json_native(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, np.ndarray)):
        return [_json_native(item) for item in value]
    if isinstance(value, np.generic):
        return _json_native(value.item())
    if isinstance(value, float) and not np.isfinite(value):
        raise ValueError("Analysis produced a nonfinite number; a strict JSON report is required.")
    return value


def analyze_data(
    df: pd.DataFrame,
    seed: int = 2026,
    variance_target: float = 0.9,
    k_values: Iterable[int] = (2, 3, 4, 5),
    initialization_runs: int = 5,
) -> dict[str, Any]:
    """Compare k candidates and return synthetic diagnostics, never a target decision.

    ``exploratory_k`` maximizes silhouette only to select one technical reference
    partition for profiles and sensitivity comparisons; ties prefer the smaller k.
    It does not determine a meaningful real-world number of customer segments.
    Profile and baseline means use observed cells, excluding missing values.
    """
    validate_data(df)
    if isinstance(seed, bool) or not isinstance(seed, Integral) or not 0 <= int(seed) < 2**32:
        raise ValueError("Seed must be an integer between 0 and 2**32 - 1.")
    if (
        isinstance(initialization_runs, bool)
        or not isinstance(initialization_runs, Integral)
        or int(initialization_runs) < 2
    ):
        raise ValueError("Initialization stability requires at least two integer runs.")
    try:
        cluster_counts = tuple(k_values)
    except TypeError as exc:
        raise ValueError(
            "k_values must be a nonempty iterable of distinct integer candidates."
        ) from exc
    if not cluster_counts:
        raise ValueError("At least one candidate cluster count is required.")
    if any(
        isinstance(k, bool) or not isinstance(k, Integral) or int(k) < 2 for k in cluster_counts
    ):
        raise ValueError("Each candidate k must be an integer of at least 2.")
    cluster_counts = tuple(int(k) for k in cluster_counts)
    if len(set(cluster_counts)) != len(cluster_counts):
        raise ValueError("Candidate cluster counts must be distinct.")
    if len(df) <= max(cluster_counts):
        raise ValueError(
            f"At least {max(cluster_counts) + 1} records are required for the requested "
            "candidate silhouette comparisons."
        )

    # Small matrices need bounded BLAS/OpenMP pools rather than hundreds of threads.
    with threadpool_limits(limits=2):
        matrix, preprocessing = prepare_features(
            df, features=ATTITUDE_COLUMNS, variance_target=variance_target, use_pca=True
        )
        for k in cluster_counts:
            check_cluster_count(matrix, k)
        candidates, partitions = [], {}
        for k in cluster_counts:
            labels = KMeans(n_clusters=k, n_init=10, random_state=int(seed)).fit_predict(matrix)
            partitions[k] = labels
            candidates.append(
                {
                    "k": k,
                    **summarize_partition(matrix, labels),
                    **initialization_stability(
                        matrix, k, seed=int(seed), runs=int(initialization_runs)
                    ),
                }
            )
        exploratory_k = int(max(candidates, key=lambda row: (row["silhouette"], -row["k"]))["k"])
        reference_labels = partitions[exploratory_k]
        warnings = [
            "All numeric results describe independently generated synthetic records; "
            "they are not consumer-survey findings or evidence of real customer segments.",
            "exploratory_k maximizes silhouette for a technical comparison only; "
            "no real segment count or managerial target is recommended.",
            "Adjusted Rand stability measures algorithm agreement, "
            "not real-world segment validity.",
            "Cluster profile and baseline means exclude missing cells; model fitting uses "
            "the preprocessing imputation recorded in metadata.",
            *candidate_warnings(candidates),
        ]
        sensitivity = []
        variants = [
            ("no_pca", ATTITUDE_COLUMNS, False),
            (
                "omit_shopping_time_pressure",
                tuple(column for column in ATTITUDE_COLUMNS if column != "shopping_time_pressure"),
                True,
            ),
        ]
        for name, features, use_pca in variants:
            try:
                alternative, _ = prepare_features(
                    df, features=features, variance_target=variance_target, use_pca=use_pca
                )
                check_cluster_count(alternative, exploratory_k)
                labels = KMeans(
                    n_clusters=exploratory_k, n_init=10, random_state=int(seed)
                ).fit_predict(alternative)
                diagnostics = summarize_partition(alternative, labels)
            except ValueError as exc:
                # An omission can remove the sole varying feature. Preserve the main
                # analysis and explicitly report that this check is not estimable.
                sensitivity.append(
                    {
                        "variant": name,
                        "k": exploratory_k,
                        "ari_vs_reference": None,
                        "silhouette": None,
                    }
                )
                warnings.append(f"Sensitivity variant {name} could not be evaluated: {exc}")
                continue
            agreement = partition_agreement(reference_labels, labels)
            sensitivity.append(
                {
                    "variant": name,
                    "k": exploratory_k,
                    "ari_vs_reference": agreement,
                    "silhouette": diagnostics["silhouette"],
                }
            )
            if agreement < 0.80:
                warnings.append(
                    f"Sensitivity variant {name}: ARI against the reference is below "
                    "the illustrative 0.80 threshold; assignments depend on "
                    "the feature representation."
                )

    return _json_native(
        {
            "data_status": "SYNTHETIC",
            "notice": SYNTHETIC_NOTICE,
            "n_rows": int(len(df)),
            "runtime": {
                "python": platform.python_version(),
                **{
                    package: version(package)
                    for package in (
                        "numpy",
                        "pandas",
                        "scikit-learn",
                        "matplotlib",
                        "threadpoolctl",
                    )
                },
            },
            "analysis_settings": {
                "seed": int(seed),
                "variance_target": float(variance_target),
                "k_values": list(cluster_counts),
                "initialization_runs": int(initialization_runs),
                "n_init_reference": 10,
                "n_init_stability": 1,
            },
            "preprocessing": preprocessing,
            "candidates": candidates,
            "exploratory_k": exploratory_k,
            "labels": reference_labels.tolist(),
            "profiles": _profile_rows(df, reference_labels),
            "sensitivity": sensitivity,
            "baseline": _baselines(df),
            "warnings": warnings,
        }
    )
