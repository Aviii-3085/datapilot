"""
Tests for Datapilot v0.4 statistical interpretation.
"""

import pandas as pd

from datapilot.analysis.statistical_profile import (
    generate_statistical_profile,
)


def test_symmetric_distribution_is_identified() -> None:
    dataframe = pd.DataFrame(
        {
            "Value": [-2, -1, 0, 1, 2],
        }
    )

    profile = generate_statistical_profile(
        dataframe
    )

    assert (
        profile["Value"]["skewness_interpretation"]
        == "Approximately symmetric"
    )


def test_right_skew_is_identified() -> None:
    dataframe = pd.DataFrame(
        {
            "Value": [1, 1, 1, 1, 2, 10],
        }
    )

    profile = generate_statistical_profile(
        dataframe
    )

    assert (
        profile["Value"]["skewness_interpretation"]
        == "Strong right skew"
    )


def test_left_skew_is_identified() -> None:
    dataframe = pd.DataFrame(
        {
            "Value": [-10, -2, -1, -1, -1, -1],
        }
    )

    profile = generate_statistical_profile(
        dataframe
    )

    assert (
        profile["Value"]["skewness_interpretation"]
        == "Strong left skew"
    )


def test_kurtosis_interpretation_is_provided() -> None:
    dataframe = pd.DataFrame(
        {
            "Value": [1, 2, 3, 4, 5],
        }
    )

    profile = generate_statistical_profile(
        dataframe
    )

    assert "kurtosis_interpretation" in profile["Value"]


def test_outlier_signal_is_reported_without_calling_values_errors() -> None:
    dataframe = pd.DataFrame(
        {
            "Value": [1, 2, 2, 2, 3, 100],
        }
    )

    profile = generate_statistical_profile(
        dataframe
    )

    assert "outlier_signal" in profile["Value"]
    assert "values" in profile["Value"]["outlier_signal"]


def test_non_numeric_columns_are_not_profiled() -> None:
    dataframe = pd.DataFrame(
        {
            "Name": ["A", "B", "C"],
            "Category": ["X", "Y", "Z"],
        }
    )

    profile = generate_statistical_profile(
        dataframe
    )

    assert profile == {}


def test_all_missing_numeric_column_is_not_interpreted() -> None:
    dataframe = pd.DataFrame(
        {
            "Value": [None, None, None],
        }
    )

    profile = generate_statistical_profile(
        dataframe
    )

    assert profile == {}