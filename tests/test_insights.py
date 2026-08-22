"""
Tests for insight generation.
"""

import pandas as pd

from datapilot.analysis.insights import (
    generate_insight_summary,
)


def test_missing_values_generate_insight_and_recommendation() -> None:
    """
    Missing values should produce a corresponding insight
    and recommendation.
    """

    dataframe = pd.DataFrame(
        {
            "Age": [20, 21, None, 22],
            "Salary": [100, 200, 300, 400],
        }
    )

    summary = generate_insight_summary(
        dataframe
    )

    assert "Dataset contains 1 missing values." in (
        summary.insights
    )

    assert (
        "Handle missing values before "
        "training machine learning models."
        in summary.recommendations
    )


def test_duplicate_rows_generate_insight_and_recommendation() -> None:
    """
    Duplicate rows should produce a corresponding insight
    and recommendation.
    """

    dataframe = pd.DataFrame(
        {
            "Age": [20, 20, 21, 22],
            "Salary": [100, 100, 200, 300],
        }
    )

    summary = generate_insight_summary(
        dataframe
    )

    assert "Dataset contains 1 duplicate rows." in (
        summary.insights
    )

    assert "Remove duplicate rows." in (
        summary.recommendations
    )


def test_outliers_generate_insight_and_recommendation() -> None:
    """
    Statistical outliers should produce a corresponding
    insight and recommendation.
    """

    dataframe = pd.DataFrame(
        {
            "Age": [20, 21, 22, 23, 150],
            "Salary": [100, 200, 300, 400, 500],
        }
    )

    summary = generate_insight_summary(
        dataframe
    )

    assert any(
        "statistical outliers" in insight
        for insight in summary.insights
    )

    assert "Review outliers before modelling." in (
        summary.recommendations
    )


def test_strong_positive_correlation_generates_recommendation() -> None:
    """
    Strong positive correlations should produce an insight
    and a multicollinearity recommendation.
    """

    dataframe = pd.DataFrame(
        {
            "Age": [1, 2, 3, 4, 5],
            "Income": [10, 20, 30, 40, 50],
        }
    )

    summary = generate_insight_summary(
        dataframe
    )

    assert (
        "Highly correlated numeric features detected."
        in summary.insights
    )

    assert (
        "Review correlated features to reduce multicollinearity."
        in summary.recommendations
    )

def test_strong_negative_correlation_generates_insight() -> None:
    """
    Strong negative correlations should generate an insight.
    """

    dataframe = pd.DataFrame(
        {
            "Feature_A": [1, 2, 3, 4, 5],
            "Feature_B": [50, 40, 30, 20, 10],
        }
    )

    summary = generate_insight_summary(
        dataframe
    )

    assert (
        "Strong negative correlations detected."
        in summary.insights
    )

def test_no_quality_issues_generates_default_insight() -> None:
    """
    A clean dataset with no strong correlations should
    produce the default insight.
    """

    dataframe = pd.DataFrame(
        {
            "Age": [20, 45, 31, 52, 27],
            "Salary": [420, 180, 760, 330, 590],
        }
    )

    summary = generate_insight_summary(
        dataframe
    )

    assert summary.insights == [
        "No significant data quality issues detected."
    ]

    assert summary.recommendations == []