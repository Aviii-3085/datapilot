"""
Tests for insight generation.
"""

import pandas as pd

from datapilot.analysis.insights import (
    generate_insight_summary,
)


def test_generate_insight_summary() -> None:
    dataframe = pd.DataFrame(
        {
            "Age": [
                20,
                21,
                None,
                22,
                150,
            ],
            "Salary": [
                100,
                200,
                300,
                400,
                500,
            ],
        }
    )

    summary = generate_insight_summary(
        dataframe
    )

    assert len(summary.insights) > 0
    assert len(summary.recommendations) > 0