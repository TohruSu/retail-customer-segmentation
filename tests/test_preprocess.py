"""Check fitted preprocessing, variance rationale, and leakage boundaries."""

import numpy as np
import pytest

from retail_case.preprocess import prepare_features
from retail_case.schema import ATTITUDE_COLUMNS
from retail_case.synthetic import generate_data


def test_imputation_scaling_and_pca_are_finite_and_repeatable(cohort):
    transformed, metadata = prepare_features(cohort, variance_target=0.9)
    repeated, repeated_metadata = prepare_features(cohort, variance_target=0.9)
    np.testing.assert_allclose(transformed, repeated)
    assert repeated_metadata == metadata
    assert transformed.shape == (len(cohort), metadata["component_count"])
    assert np.isfinite(transformed).all()
    assert metadata["features"] == list(ATTITUDE_COLUMNS)
    assert metadata["component_count"] <= len(ATTITUDE_COLUMNS)
    assert metadata["retained_variance"] == pytest.approx(sum(metadata["explained_variance_ratio"]))
    assert metadata["retained_variance"] >= 0.9


def test_no_pca_preserves_selected_feature_count_and_standardization(cohort):
    matrix, metadata = prepare_features(cohort, use_pca=False)
    assert matrix.shape == (len(cohort), len(ATTITUDE_COLUMNS))
    assert metadata["component_count"] == len(ATTITUDE_COLUMNS)
    np.testing.assert_allclose(matrix.mean(axis=0), 0, atol=1e-12)
    np.testing.assert_allclose(matrix.std(axis=0), 1, atol=1e-12)


def test_behavioral_outcomes_do_not_change_clustering_features(cohort):
    changed = cohort.copy()
    changed["monthly_store_visits"] = 30 - changed["monthly_store_visits"]
    changed["weekly_other_channel_visits"] = 21 - changed["weekly_other_channel_visits"]
    baseline, _ = prepare_features(cohort)
    changed_matrix, _ = prepare_features(changed)
    np.testing.assert_allclose(baseline, changed_matrix)
    with pytest.raises(ValueError):
        prepare_features(cohort, features=[ATTITUDE_COLUMNS[0], "monthly_store_visits"])


@pytest.mark.parametrize("target", [0, 1, -0.1, float("nan"), True, "0.9", None])
def test_invalid_variance_targets_fail(cohort, target):
    with pytest.raises(ValueError):
        prepare_features(cohort, variance_target=target)


@pytest.mark.parametrize(
    "features", [[], [ATTITUDE_COLUMNS[0]], [ATTITUDE_COLUMNS[0], ATTITUDE_COLUMNS[0]]]
)
def test_features_must_include_two_distinct_allowed_proxies(cohort, features):
    with pytest.raises(ValueError):
        prepare_features(cohort, features=features)


def test_too_small_and_all_constant_cohorts_fail():
    with pytest.raises(ValueError):
        prepare_features(generate_data(n=1, missing_rate=0))
    constant = generate_data(n=20, missing_rate=0)
    constant.loc[:, list(ATTITUDE_COLUMNS)] = 3
    with pytest.raises(ValueError):
        prepare_features(constant)


def test_two_rows_fit_a_finite_rank_limited_pca():
    matrix, metadata = prepare_features(generate_data(n=2, seed=5, missing_rate=0))
    assert matrix.shape == (2, 1)
    assert np.isfinite(matrix).all()
    assert metadata["retained_variance"] == pytest.approx(1)
