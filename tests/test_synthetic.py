"""The generator must obey its declared design without source data."""

import numpy as np
import pandas as pd
import pytest

from retail_case.schema import ATTITUDE_COLUMNS, BEHAVIOR_COLUMNS
from retail_case.synthetic import generate_data
from retail_case.validation import validate_data


def test_generation_is_seeded_and_changes_with_seed():
    first = generate_data(n=81, seed=12, missing_rate=0.05)
    pd.testing.assert_frame_equal(first, generate_data(n=81, seed=12, missing_rate=0.05))
    assert not first.equals(generate_data(n=81, seed=13, missing_rate=0.05))


def test_generated_schema_ids_bounds_and_provenance():
    frame = generate_data(n=81, seed=12, missing_rate=0.05)
    assert set(frame.columns) == {
        "participant_id",
        "data_status",
        *ATTITUDE_COLUMNS,
        *BEHAVIOR_COLUMNS,
    }
    assert frame["participant_id"].is_unique
    assert frame["participant_id"].str.fullmatch(r"SYN\d{6,}").all()
    assert frame["data_status"].eq("SYNTHETIC").all()
    for feature in ATTITUDE_COLUMNS:
        nonmissing = frame[feature].dropna().to_numpy(dtype=float)
        assert np.isfinite(nonmissing).all()
        assert (nonmissing == np.floor(nonmissing)).all()
        assert np.logical_and(nonmissing >= 1, nonmissing <= 5).all()
        assert frame[feature].isna().sum() == 4
    assert frame["monthly_store_visits"].between(0, 30).all()
    assert frame["weekly_other_channel_visits"].between(0, 21).all()
    assert not frame[list(BEHAVIOR_COLUMNS)].isna().any().any()
    assert validate_data(frame)["n_rows"] == 81


@pytest.mark.parametrize("n", [1, 2, 5])
def test_small_cohorts_remain_valid_without_forced_clusters(n):
    frame = generate_data(n=n, seed=5, missing_rate=0)
    assert len(frame) == n
    assert not frame.isna().any().any()
    validate_data(frame)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"n": 0},
        {"n": -1},
        {"n": 2.5},
        {"missing_rate": -0.01},
        {"missing_rate": 0.21},
        {"missing_rate": float("nan")},
    ],
)
def test_generator_rejects_invalid_design_arguments(kwargs):
    with pytest.raises((ValueError, TypeError)):
        generate_data(**kwargs)
