"""Deterministic toy simulation with overlapping continuous factors and no true groups."""

import numpy as np
import pandas as pd

from retail_case.schema import ATTITUDE_COLUMNS, REQUIRED_COLUMNS, SYNTHETIC_NOTICE


def generate_data(n: int = 720, seed: int = 2026, missing_rate: float = 0.03) -> pd.DataFrame:
    """Generate newly invented proxies without reading external data.

    The coefficients are declared simulation assumptions, not fitted parameters.
    Missing entries are sampled independently per feature, with floor(n * rate) entries.
    """
    if isinstance(n, bool) or not isinstance(n, (int, np.integer)) or n < 1:
        raise ValueError("n must be a positive integer")
    if isinstance(seed, bool) or not isinstance(seed, (int, np.integer)) or seed < 0:
        raise ValueError("seed must be a non-negative integer")
    if isinstance(missing_rate, bool) or not isinstance(missing_rate, (int, float)):
        raise ValueError("missing_rate must be a number between 0 and 0.20")
    if not np.isfinite(missing_rate) or not 0 <= missing_rate <= 0.20:
        raise ValueError("missing_rate must be between 0 and 0.20")

    rng = np.random.default_rng(seed)
    factors = rng.normal(size=(n, 3))  # budget attention, time pressure, exploration
    weights = np.array(
        [
            [0.70, 0.05, -0.10],
            [0.10, -0.55, 0.25],
            [-0.10, 0.75, 0.15],
            [-0.15, 0.10, 0.75],
            [0.15, -0.65, 0.20],
            [0.05, 0.85, -0.05],
            [0.05, 0.10, 0.60],
        ]
    )
    attitudes = np.clip(np.rint(3 + factors @ weights.T + rng.normal(0, 0.9, (n, 7))), 1, 5)
    budget, time_pressure, exploration = factors.T
    store_rate = np.clip(5 - 0.6 * time_pressure + 0.4 * exploration, 0.8, 12)
    other_rate = np.clip(2.5 + 0.7 * time_pressure - 0.3 * budget, 0.3, 7)
    visits = np.clip(rng.poisson(store_rate), 0, 30)
    other_visits = np.clip(rng.poisson(other_rate), 0, 21)
    missing_count = int(n * missing_rate)
    for column in range(len(ATTITUDE_COLUMNS)):
        if missing_count:
            attitudes[rng.choice(n, size=missing_count, replace=False), column] = np.nan

    frame = pd.DataFrame(attitudes, columns=ATTITUDE_COLUMNS)
    frame.insert(0, "weekly_other_channel_visits", other_visits)
    frame.insert(0, "monthly_store_visits", visits)
    frame.insert(0, "data_status", "SYNTHETIC")
    frame.insert(0, "participant_id", [f"SYN{i + 1:06d}" for i in range(n)])
    frame = frame.loc[:, REQUIRED_COLUMNS]
    frame.attrs.update(data_status="SYNTHETIC", notice=SYNTHETIC_NOTICE, seed=int(seed))
    return frame
