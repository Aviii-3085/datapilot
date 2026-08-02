"""
Tests for correlation analysis.
"""

import pandas as pd

from datapilot.analysis.correlation import (
    generate_correlation_summary,
)


def test_generate_correlation_summary() -> None:
    dataframe = pd.DataFrame(
        {
            "A": [1, 2, 3, 4, 5],
            "B": [2, 4, 6, 8, 10],
            "C": [5, 4, 3, 2, 1],
        }
    )

    summary = generate_correlation_summary(
        dataframe
    )

    assert summary.correlation_matrix.shape == (
        3,
        3,
    )

    assert (
        "A ↔ B"
        in summary.strong_positive_pairs
    )

    assert (
        "A ↔ C"
        in summary.strong_negative_pairs
    )