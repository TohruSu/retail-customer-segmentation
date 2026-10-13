"""Reject malformed inputs without echoing records into error messages."""

import numpy as np
import pandas as pd
from pandas.api.types import is_bool_dtype, is_complex_dtype, is_numeric_dtype

from retail_case.schema import (
    ATTITUDE_COLUMNS,
    BEHAVIOR_COLUMNS,
    REQUIRED_COLUMNS,
    SYNTHETIC_NOTICE,
)


class DataValidationError(ValueError):
    """The independently synthetic input fails its declared schema."""


def validate_data(frame: pd.DataFrame) -> dict:
    """Validate schema, provenance marker, finite integer bounds, IDs, and missingness.

    A marker documents intended input scope; it cannot prove provenance on its own.
    """
    if not isinstance(frame, pd.DataFrame) or frame.empty:
        raise DataValidationError("input must be a nonempty pandas DataFrame")
    if frame.columns.has_duplicates or set(frame.columns) != set(REQUIRED_COLUMNS):
        raise DataValidationError("columns must match the independently synthetic schema exactly")
    ids = frame["participant_id"]
    if ids.isna().any() or not ids.map(lambda value: isinstance(value, str)).all():
        raise DataValidationError("participant_id must contain synthetic string identifiers")
    if not ids.str.fullmatch(r"SYN\d{6,}").all() or ids.duplicated().any():
        raise DataValidationError("participant_id must be unique SYN-prefixed identifiers")
    if frame["data_status"].isna().any() or not frame["data_status"].eq("SYNTHETIC").all():
        raise DataValidationError("data_status must be SYNTHETIC on every row")

    missingness = {}
    bounds = {
        **dict.fromkeys(ATTITUDE_COLUMNS, (1, 5)),
        **dict(zip(BEHAVIOR_COLUMNS, [(0, 30), (0, 21)], strict=True)),
    }
    for column, (minimum, maximum) in bounds.items():
        values = frame[column]
        if (
            is_bool_dtype(values.dtype)
            or is_complex_dtype(values.dtype)
            or not is_numeric_dtype(values.dtype)
        ):
            raise DataValidationError(
                f"{column} must have a real numeric dtype, excluding booleans"
            )
        missing_fraction = float(values.isna().mean())
        missingness[column] = missing_fraction
        if column in BEHAVIOR_COLUMNS and missing_fraction:
            raise DataValidationError(f"{column} cannot contain missing values")
        if column in ATTITUDE_COLUMNS and missing_fraction > 0.20:
            raise DataValidationError(f"{column} missingness exceeds the 20% limit")
        observed = values.dropna().to_numpy(dtype=float)
        if not np.isfinite(observed).all():
            raise DataValidationError(f"{column} must contain only finite observed values")
        if ((observed < minimum) | (observed > maximum)).any():
            raise DataValidationError(f"{column} must be between {minimum} and {maximum}")
        if not np.equal(observed, np.floor(observed)).all():
            raise DataValidationError(f"{column} must contain integer-valued proxies or counts")
    return {
        "data_status": "SYNTHETIC",
        "notice": SYNTHETIC_NOTICE,
        "n_rows": int(len(frame)),
        "columns": list(REQUIRED_COLUMNS),
        "missingness": missingness,
    }
