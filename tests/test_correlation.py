"""
Tests for correlation analysis.
"""

import pandas as pd

from datapilot.analysis.correlation import (
    generate_correlation_summary,
)


def test_generate_correlation_summary() -> None:
    """
    Test strong positive and negative correlations.
    """

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


def test_non_numeric_columns_are_excluded() -> None:
    """
    Non-numeric columns should not participate in
    correlation analysis.
    """

    dataframe = pd.DataFrame(
        {
            "Age": [20, 21, 22, 23],
            "Name": ["A", "B", "C", "D"],
        }
    )

    summary = generate_correlation_summary(
        dataframe
    )

    assert list(
        summary.correlation_matrix.columns
    ) == ["Age"]


def test_weak_correlations_are_not_reported() -> None:
    """
    Correlations below the 0.70 threshold should not
    appear in strong correlation findings.
    """

    dataframe = pd.DataFrame(
        {
            "A": [1, 2, 3, 4, 5],
            "B": [3, 1, 4, 2, 5],
        }
    )

    summary = generate_correlation_summary(
        dataframe
    )

    assert summary.strong_positive_pairs == {}
    assert summary.strong_negative_pairs == {}

def test_constant_columns_do_not_create_false_correlations() -> None:
    """
    Constant columns produce undefined correlations and
    should not be reported as strong correlations.
    """

    dataframe = pd.DataFrame(
        {
            "A": [1, 1, 1, 1, 1],
            "B": [1, 2, 3, 4, 5],
        }
    )

    summary = generate_correlation_summary(
        dataframe
    )

    assert summary.strong_positive_pairs == {}
    assert summary.strong_negative_pairs == {}


def test_single_numeric_column() -> None:
    """
    A single numeric column should produce a valid
    one-column correlation matrix with no pairs.
    """

    dataframe = pd.DataFrame(
        {
            "Age": [20, 21, 22, 23, 24],
        }
    )

    summary = generate_correlation_summary(
        dataframe
    )

    assert summary.correlation_matrix.shape == (
        1,
        1,
    )

    assert summary.strong_positive_pairs == {}
    assert summary.strong_negative_pairs == {}


def test_no_numeric_columns() -> None:
    """
    A dataset with no numeric columns should produce
    an empty correlation matrix and no findings.
    """

    dataframe = pd.DataFrame(
        {
            "Name": ["A", "B", "C"],
            "Department": ["IT", "HR", "Sales"],
        }
    )

    summary = generate_correlation_summary(
        dataframe
    )

    assert summary.correlation_matrix.empty
    assert summary.strong_positive_pairs == {}
    assert summary.strong_negative_pairs == {}