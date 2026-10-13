"""Median imputation, standardization, and variance-based optional PCA."""

from numbers import Real

import numpy as np
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from retail_case.schema import ATTITUDE_COLUMNS
from retail_case.validation import validate_data


def prepare_features(
    frame,
    features=ATTITUDE_COLUMNS,
    variance_target: float = 0.9,
    use_pca: bool = True,
) -> tuple[np.ndarray, dict]:
    """Fit only invented attitude proxies; visit measures are excluded from clustering."""
    validate_data(frame)
    features = tuple(features)
    if len(features) < 2 or len(set(features)) != len(features):
        raise ValueError("features must contain at least two distinct attitude columns")
    if any(feature not in ATTITUDE_COLUMNS for feature in features):
        raise ValueError(
            "only declared attitude features may enter clustering; exclude visit outcomes"
        )
    if len(frame) < 2:
        raise ValueError("preprocessing requires at least two rows")
    if (
        isinstance(variance_target, bool)
        or not isinstance(variance_target, Real)
        or not np.isfinite(variance_target)
        or not 0 < variance_target < 1
    ):
        raise ValueError("variance_target must be strictly between 0 and 1")
    if not isinstance(use_pca, bool):
        raise ValueError("use_pca must be a boolean")
    selected = frame.loc[:, features]
    if not any(selected[column].nunique(dropna=True) > 1 for column in features):
        raise ValueError(
            "attitude features have no variation; a descriptive baseline is appropriate"
        )

    steps = [("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]
    if use_pca:
        steps.append(("pca", PCA(n_components=variance_target, svd_solver="full")))
    pipeline = Pipeline(steps)
    transformed = pipeline.fit_transform(selected)
    pca = pipeline.named_steps.get("pca")
    metadata = {
        "features": list(features),
        "imputation": "per-feature median fitted on this exploratory synthetic cohort",
        "imputation_values": {
            feature: float(value)
            for feature, value in zip(
                features, pipeline.named_steps["imputer"].statistics_, strict=True
            )
        },
        "scaling": "StandardScaler fitted on this exploratory synthetic cohort",
        "use_pca": use_pca,
        "variance_target": float(variance_target),
        "component_count": int(transformed.shape[1]),
        "explained_variance_ratio": [] if pca is None else pca.explained_variance_ratio_.tolist(),
        "retained_variance": 1.0 if pca is None else float(pca.explained_variance_ratio_.sum()),
    }
    return transformed, metadata
