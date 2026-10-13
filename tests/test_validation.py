"""Fail early on malformed synthetic inputs and impossible values."""

import numpy as np
import pandas as pd
import pytest

from retail_case.schema import ATTITUDE_COLUMNS
from retail_case.validation import DataValidationError, validate_data


def test_validation_reports_actual_missingness(cohort):
    result = validate_data(cohort)
    assert result["data_status"] == "SYNTHETIC"
    assert result["n_rows"] == len(cohort)
    assert set(result["columns"]) == set(cohort.columns)
    for feature in ATTITUDE_COLUMNS:
        assert result["missingness"][feature] == pytest.approx(cohort[feature].isna().mean())


@pytest.mark.parametrize("change", ["missing", "extra", "empty", "duplicate_columns"])
def test_exact_nonempty_schema(cohort, change):
    if change == "missing":
        bad = cohort.drop(columns=[ATTITUDE_COLUMNS[0]])
    elif change == "extra":
        bad = cohort.assign(unapproved_outcome=0)
    elif change == "duplicate_columns":
        bad = cohort.copy()
        bad.columns = ["participant_id"] + list(cohort.columns[1:-1]) + ["participant_id"]
    else:
        bad = cohort.iloc[:0]
    with pytest.raises(DataValidationError):
        validate_data(bad)


@pytest.mark.parametrize("bad_id", [None, "SYN1", "REAL000001", "SYN000001 extra"])
def test_ids_require_synthetic_namespace(cohort, bad_id):
    cohort.loc[0, "participant_id"] = bad_id
    with pytest.raises(DataValidationError):
        validate_data(cohort)


def test_duplicate_ids_and_unmarked_data_are_rejected(cohort):
    duplicate = cohort.copy()
    duplicate.loc[1, "participant_id"] = duplicate.loc[0, "participant_id"]
    with pytest.raises(DataValidationError):
        validate_data(duplicate)
    cohort.loc[0, "data_status"] = "OBSERVED"
    with pytest.raises(DataValidationError):
        validate_data(cohort)


@pytest.mark.parametrize(
    "column,value",
    [
        (ATTITUDE_COLUMNS[0], 0),
        (ATTITUDE_COLUMNS[0], 6),
        (ATTITUDE_COLUMNS[0], 2.5),
        (ATTITUDE_COLUMNS[0], np.inf),
        ("monthly_store_visits", -1),
        ("monthly_store_visits", 31),
        ("weekly_other_channel_visits", 22),
        ("monthly_store_visits", np.nan),
    ],
)
def test_numeric_finite_integer_and_range_constraints(cohort, column, value):
    bad = cohort.copy()
    # Use float so malformed non-integral inputs remain representable under pandas 3.
    bad[column] = bad[column].astype(float)
    bad.loc[0, column] = value
    with pytest.raises(DataValidationError):
        validate_data(bad)


def test_string_and_boolean_values_are_not_numeric_responses(cohort):
    for value in ["3", True]:
        bad = cohort.copy()
        bad[ATTITUDE_COLUMNS[0]] = bad[ATTITUDE_COLUMNS[0]].astype(object)
        bad.loc[0, ATTITUDE_COLUMNS[0]] = value
        with pytest.raises(DataValidationError):
            validate_data(bad)


def test_complex_numeric_values_are_not_real_integer_responses(cohort):
    cohort[ATTITUDE_COLUMNS[0]] = cohort[ATTITUDE_COLUMNS[0]].astype(complex)
    cohort.loc[0, ATTITUDE_COLUMNS[0]] = 3 + 2j
    with pytest.raises(DataValidationError):
        validate_data(cohort)


def test_nullable_provenance_marker_cannot_skip_missing_status(cohort):
    cohort["data_status"] = cohort["data_status"].astype("string")
    cohort.loc[0, "data_status"] = pd.NA
    with pytest.raises(DataValidationError):
        validate_data(cohort)


def test_excessive_missingness_is_rejected(cohort):
    cohort.loc[:16, ATTITUDE_COLUMNS[0]] = np.nan
    assert cohort[ATTITUDE_COLUMNS[0]].isna().mean() > 0.20
    with pytest.raises(DataValidationError):
        validate_data(cohort)
