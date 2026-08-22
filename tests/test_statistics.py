"""
Tests for statistical analysis.
"""

import math

import pandas as pd

from datapilot.analysis.statistics import (
    generate_statistics_summary,
)


def test_generate_statistics_summary() -> None:
    """
    Test descriptive statistics for numeric columns.
    """

    dataframe = pd.DataFrame(
        {
            "Age": [20, 25, 30, 35],
            "Salary": [100, 200, 300, 400],
            "Department": [
                "IT",
                "HR",
                "IT",
                "Sales",
            ],
        }
    )

    summary = generate_statistics_summary(
        dataframe
    )

    assert "Age" in summary.column_statistics
    assert "Salary" in summary.column_statistics

    assert (
        summary.column_statistics["Age"]["mean"]
        == 27.5
    )

    assert (
        summary.column_statistics["Salary"]["max"]
        == 400.0
    )


def test_non_numeric_columns_are_excluded() -> None:
    """
    Non-numeric columns should not appear in statistics.
    """

    dataframe = pd.DataFrame(
        {
            "Name": ["A", "B", "C"],
            "Age": [20, 21, 22],
        }
    )

    summary = generate_statistics_summary(
        dataframe
    )

    assert list(
        summary.column_statistics.keys()
    ) == ["Age"]


def test_missing_numeric_values_are_ignored() -> None:
    """
    Missing values should not prevent numeric statistics
    from being generated.
    """

    dataframe = pd.DataFrame(
        {
            "Age": [20, None, 30, 40],
        }
    )

    summary = generate_statistics_summary(
        dataframe
    )

    statistics = summary.column_statistics["Age"]

    assert statistics["count"] == 3.0
    assert statistics["mean"] == 30.0
    assert statistics["median"] == 30.0
    assert statistics["min"] == 20.0
    assert statistics["max"] == 40.0


def test_single_value_numeric_column() -> None:
    """
    A single-value numeric column should still produce
    a complete statistics record.
    """

    dataframe = pd.DataFrame(
        {
            "Age": [25],
        }
    )

    summary = generate_statistics_summary(
        dataframe
    )

    statistics = summary.column_statistics["Age"]

    assert statistics["count"] == 1.0
    assert statistics["mean"] == 25.0
    assert statistics["median"] == 25.0
    assert statistics["min"] == 25.0
    assert statistics["max"] == 25.0

    assert math.isnan(statistics["std"])
    assert math.isnan(statistics["variance"])


def test_all_missing_numeric_column() -> None:
    """
    An entirely missing numeric column should not crash
    statistical analysis.
    """

    dataframe = pd.DataFrame(
        {
            "Age": pd.Series(
                [None, None, None],
                dtype="float64",
            ),
        }
    )

    summary = generate_statistics_summary(
        dataframe
    )

    statistics = summary.column_statistics["Age"]

    assert statistics["count"] == 0.0
    assert math.isnan(statistics["mean"])
    assert math.isnan(statistics["median"])
    assert math.isnan(statistics["std"])
    assert math.isnan(statistics["variance"])
    assert math.isnan(statistics["min"])
    assert math.isnan(statistics["q1"])
    assert math.isnan(statistics["q3"])
    assert math.isnan(statistics["max"])
    assert math.isnan(statistics["skewness"])
    assert math.isnan(statistics["kurtosis"])