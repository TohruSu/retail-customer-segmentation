"""Keep unlike visit time bases separate without changing plotted diagnostics."""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest

from retail_case.figures import make_diagnostics_figure
from retail_case.schema import SYNTHETIC_NOTICE


@pytest.fixture(scope="module")
def diagnostics_figure():
    # Independently invented plot inputs: no clustering fit or survey fixture.
    result = {
        "n_rows": 4,
        "exploratory_k": 2,
        "candidates": [
            {
                "k": 2,
                "silhouette": 0.12,
                "min_cluster_share": 0.25,
                "max_cluster_share": 0.75,
                "initialization_ari_mean": 0.5,
                "initialization_ari_min": 0.1,
            },
            {
                "k": 3,
                "silhouette": 0.09,
                "min_cluster_share": 0.2,
                "max_cluster_share": 0.5,
                "initialization_ari_mean": 0.6,
                "initialization_ari_min": 0.2,
            },
        ],
    }
    visits = pd.DataFrame(
        {"monthly_store_visits": [12, 3, 0, 3], "weekly_other_channel_visits": [2, 0, 2, 1]}
    )
    figure = make_diagnostics_figure(result, visits)
    yield figure
    plt.close(figure)


def test_visit_ecdfs_have_independent_time_specific_axes(diagnostics_figure):
    axes = {axis.get_xlabel(): axis for axis in diagnostics_figure.axes}
    monthly = axes["Store visits / month"]
    weekly = axes["Other-channel visits / week"]
    assert monthly is not weekly
    assert not monthly.get_shared_x_axes().joined(monthly, weekly)
    assert len(diagnostics_figure.axes) == 5  # No old shared-time-base overlay remains.

    for axis, expected_visits in ((monthly, [0, 3, 3, 12]), (weekly, [0, 1, 2, 2])):
        assert "SYNTHETIC" in axis.get_title()
        assert len(axis.lines) == 1
        line = axis.lines[0]
        np.testing.assert_array_equal(line.get_xdata(), expected_visits)
        np.testing.assert_array_equal(line.get_ydata(), [0.25, 0.5, 0.75, 1.0])
        assert line.get_drawstyle() == "steps-post"
    assert SYNTHETIC_NOTICE in "\n".join(text.get_text() for text in diagnostics_figure.texts)


def test_existing_diagnostic_panel_values_are_preserved(diagnostics_figure):
    axes = {axis.get_title(): axis for axis in diagnostics_figure.axes}
    expected_panels = {
        "SYNTHETIC silhouette by candidate k": [[0.12, 0.09]],
        "SYNTHETIC cluster-size range": [[25, 20], [75, 50]],
        "SYNTHETIC initialization sensitivity": [[0.5, 0.6], [0.1, 0.2]],
    }
    for title, expected_lines in expected_panels.items():
        lines = axes[title].lines
        assert len(lines) == len(expected_lines)
        for line, expected_values in zip(lines, expected_lines, strict=True):
            np.testing.assert_array_equal(line.get_xdata(), [2, 3])
            np.testing.assert_array_equal(line.get_ydata(), expected_values)
