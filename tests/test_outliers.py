"""
Tests for outlier detection.
"""

import pandas as pd

from datapilot.analysis.outliers import (
    generate_outlier_summary,
)


def test_generate_outlier_summary() -> None:
    """
    Test standard IQR outlier detection.
    """

    dataframe = pd.DataFrame(
        {
            "Age": [
                20,
                21,
                22,
                23,
                24,
                150,
            ],
            "Salary": [
                10,
                20,
                30,
                40,
                50,
                60,
            ],
        }
    )

    summary = generate_outlier_summary(
        dataframe
    )

    assert summary.total_outliers == 1

    assert (
        summary.columns_with_outliers["Age"]
        == 1
    )

    assert "Salary" in (
        summary.columns_without_outliers
    )


def test_missing_values_are_ignored() -> None:
    """
    Missing numeric values should not be counted
    as outliers.
    """

    dataframe = pd.DataFrame(
        {
            "Age": [
                20,
                21,
                None,
                22,
                23,
                150,
            ],
        }
    )

    summary = generate_outlier_summary(
        dataframe
    )

    assert summary.total_outliers == 1
    assert (
        summary.columns_with_outliers["Age"]
        == 1
    )


def test_constant_column_has_no_outliers() -> None:
    """
    A constant numeric column should not produce
    false outliers when its IQR is zero.
    """

    dataframe = pd.DataFrame(
        {
            "Age": [25, 25, 25, 25, 25],
        }
    )

    summary = generate_outlier_summary(
        dataframe
    )

    assert summary.total_outliers == 0
    assert summary.columns_with_outliers == {}
    assert summary.columns_without_outliers == [
        "Age"
    ]
    assert summary.outlier_percentage == 0.0


def test_all_missing_numeric_column() -> None:
    """
    An entirely missing numeric column should not
    produce outliers.
    """

    dataframe = pd.DataFrame(
        {
            "Age": pd.Series(
                [None, None, None],
                dtype="float64",
            ),
        }
    )

    summary = generate_outlier_summary(
        dataframe
    )

    assert summary.total_outliers == 0
    assert summary.columns_with_outliers == {}
    assert summary.columns_without_outliers == [
        "Age"
    ]
    assert summary.outlier_percentage == 0.0


def test_outlier_percentage_uses_non_missing_numeric_values() -> None:
    """
    Outlier percentage should use the number of observed
    numeric values as its denominator.
    """

    dataframe = pd.DataFrame(
        {
            "Age": [
                20,
                21,
                22,
                23,
                24,
                150,
                None,
            ],
        }
    )

    summary = generate_outlier_summary(
        dataframe
    )

    assert summary.total_outliers == 1
    assert summary.outlier_percentage == 16.67