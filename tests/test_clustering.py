"""Reported diagnostics must be computed from the fitted synthetic partitions."""

import json

import numpy as np
import pytest
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, silhouette_score

from retail_case.clustering import analyze_data
from retail_case.evaluation import (
    check_cluster_count,
    initialization_stability,
    partition_agreement,
    summarize_partition,
)
from retail_case.preprocess import prepare_features
from retail_case.schema import ATTITUDE_COLUMNS, BEHAVIOR_COLUMNS
from retail_case.synthetic import generate_data


@pytest.fixture
def analysis(cohort):
    return analyze_data(cohort, seed=77, k_values=(2, 3), initialization_runs=3)


def test_analysis_is_repeatable_and_strictly_json_serializable(cohort, analysis):
    repeated = analyze_data(cohort, seed=77, k_values=(2, 3), initialization_runs=3)
    assert repeated == analysis
    json.dumps(analysis, allow_nan=False)
    assert analysis["data_status"] == "SYNTHETIC"
    assert "synthetic" in analysis["notice"].lower()
    assert "survey" in analysis["notice"].lower()
    assert analysis["exploratory_k"] in {2, 3}
    assert len(analysis["labels"]) == len(cohort)
    assert any("validity" in warning for warning in analysis["warnings"])


def test_candidate_metrics_match_actual_partitions(cohort, analysis):
    matrix, _ = prepare_features(cohort)
    for candidate in analysis["candidates"]:
        fitted = KMeans(n_clusters=candidate["k"], n_init=10, random_state=77).fit_predict(matrix)
        assert candidate["silhouette"] == pytest.approx(silhouette_score(matrix, fitted))
        _, sizes = np.unique(fitted, return_counts=True)
        assert candidate["min_cluster_share"] == pytest.approx(sizes.min() / len(cohort))
        assert candidate["max_cluster_share"] == pytest.approx(sizes.max() / len(cohort))
        assert (
            -1 <= candidate["initialization_ari_min"] <= candidate["initialization_ari_mean"] <= 1
        )
    reference = next(row for row in analysis["candidates"] if row["k"] == analysis["exploratory_k"])
    assert reference["silhouette"] == pytest.approx(silhouette_score(matrix, analysis["labels"]))
    assert reference["silhouette"] == max(row["silhouette"] for row in analysis["candidates"])


def test_profiles_and_baselines_summarize_observed_cells(cohort, analysis):
    labels = np.asarray(analysis["labels"])
    assert sum(row["count"] for row in analysis["profiles"]) == len(cohort)
    assert sum(row["share"] for row in analysis["profiles"]) == pytest.approx(1)
    for row in analysis["profiles"]:
        subset = cohort.loc[labels == row["cluster"]]
        assert row["count"] == len(subset)
        for feature in (*ATTITUDE_COLUMNS, *BEHAVIOR_COLUMNS):
            assert row[feature] == pytest.approx(subset[feature].mean())
    baseline = analysis["baseline"]
    assert baseline["unsegmented"]["count"] == len(cohort)
    assert sum(row["count"] for row in baseline["descriptive_strata"]) == len(cohort)
    for feature in (*ATTITUDE_COLUMNS, *BEHAVIOR_COLUMNS):
        assert baseline["unsegmented"][feature] == pytest.approx(cohort[feature].mean())


def test_sensitivity_reports_actual_no_pca_partition(cohort, analysis):
    row = next(item for item in analysis["sensitivity"] if item["variant"] == "no_pca")
    matrix, _ = prepare_features(cohort, use_pca=False)
    labels = KMeans(n_clusters=analysis["exploratory_k"], n_init=10, random_state=77).fit_predict(
        matrix
    )
    assert row["k"] == analysis["exploratory_k"]
    assert row["ari_vs_reference"] == pytest.approx(adjusted_rand_score(analysis["labels"], labels))
    assert row["silhouette"] == pytest.approx(silhouette_score(matrix, labels))
    assert {item["variant"] for item in analysis["sensitivity"]} >= {
        "no_pca",
        "omit_shopping_time_pressure",
    }


def test_behavioral_outcomes_do_not_determine_assignments(cohort, analysis):
    changed = cohort.copy()
    changed["monthly_store_visits"] = 30 - changed["monthly_store_visits"]
    changed["weekly_other_channel_visits"] = 21 - changed["weekly_other_channel_visits"]
    second = analyze_data(changed, seed=77, k_values=(2, 3), initialization_runs=3)
    assert second["labels"] == analysis["labels"]
    for left, right in zip(second["candidates"], analysis["candidates"], strict=True):
        assert left == pytest.approx(right)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"k_values": ()},
        {"k_values": (1,)},
        {"k_values": (2, 2)},
        {"k_values": (80,)},
        {"initialization_runs": 1},
        {"seed": -1},
    ],
)
def test_invalid_clustering_requests_fail(cohort, kwargs):
    with pytest.raises(ValueError):
        analyze_data(cohort, **kwargs)


def test_constant_and_insufficient_distinct_feature_rows_fail():
    constant = generate_data(n=12, missing_rate=0)
    constant.loc[:, list(ATTITUDE_COLUMNS)] = 3
    with pytest.raises(ValueError):
        analyze_data(constant, k_values=(2,), initialization_runs=2)
    with pytest.raises(ValueError):
        check_cluster_count(np.array([[0.0], [0.0], [1.0], [1.0]]), 3)
    with pytest.raises(ValueError):
        analyze_data(generate_data(n=3, missing_rate=0), k_values=(3,), initialization_runs=2)


def test_unestimable_sensitivity_is_reported_without_invented_metrics():
    frame = generate_data(n=20, missing_rate=0)
    frame.loc[:, list(ATTITUDE_COLUMNS)] = 3
    frame["shopping_time_pressure"] = np.tile([1, 2, 3, 4, 5], 4)
    result = analyze_data(frame, k_values=(2,), initialization_runs=2)
    omitted = next(
        row for row in result["sensitivity"] if row["variant"] == "omit_shopping_time_pressure"
    )
    assert omitted["silhouette"] is None
    assert omitted["ari_vs_reference"] is None
    assert any("could not be evaluated" in warning for warning in result["warnings"])
    json.dumps(result, allow_nan=False)


def test_partition_agreement_ignores_arbitrary_cluster_numbers():
    assert partition_agreement(np.array([0, 0, 1, 1]), np.array([9, 9, 4, 4])) == 1
    with pytest.raises(ValueError):
        partition_agreement(np.array([0, 1]), np.array([0]))


def test_diagnostics_reject_degenerate_and_unaligned_labels():
    matrix = np.array([[0.0], [0.1], [2.0], [2.1]])
    for labels in [np.zeros(4), np.arange(4), np.array([0, 1])]:
        with pytest.raises(ValueError):
            summarize_partition(matrix, labels)
    with pytest.raises(ValueError):
        initialization_stability(matrix, 2, seed=1, runs=1)
