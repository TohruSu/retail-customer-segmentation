"""Small independent synthetic cohorts keep analytical checks inexpensive."""

import pytest

from retail_case.synthetic import generate_data


@pytest.fixture
def cohort():
    return generate_data(n=80, seed=314, missing_rate=0.05)
