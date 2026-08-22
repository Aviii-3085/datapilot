"""
Tests for missing value analysis.
"""

import pandas as pd

from datapilot.analysis.missing import (
    generate_missing_value_summary,
)


def test_generate_missing_value_summary(
    sample_dataframe,
) -> None:
    """
    Test standard missing value analysis.
    """

    summary = generate_missing_value_summary(
        sample_dataframe
    )

    assert summary.total_missing == 3
    assert summary.missing_percentage == 15.0

    assert summary.columns_with_missing == {
        "Age": 1,
        "Salary": 1,
        "Department": 1,
    }

    assert summary.columns_without_missing == [
        "Is_Manager",
        "Joining_Date",
    ]


def test_dataset_with_no_missing_values() -> None:
    """
    A complete dataset should report zero missing values.
    """

    dataframe = pd.DataFrame(
        {
            "Age": [20, 21, 22],
            "Name": ["A", "B", "C"],
        }
    )

    summary = generate_missing_value_summary(
        dataframe
    )

    assert summary.total_missing == 0
    assert summary.missing_percentage == 0.0
    assert summary.columns_with_missing == {}
    assert summary.columns_without_missing == [
        "Age",
        "Name",
    ]


def test_all_values_missing_in_one_column() -> None:
    """
    A completely missing column should report every row
    as missing.
    """

    dataframe = pd.DataFrame(
        {
            "Age": [None, None, None, None],
            "Name": ["A", "B", "C", "D"],
        }
    )

    summary = generate_missing_value_summary(
        dataframe
    )

    assert summary.total_missing == 4
    assert summary.missing_percentage == 50.0

    assert summary.columns_with_missing == {
        "Age": 4,
    }

    assert summary.columns_without_missing == [
        "Name",
    ]


def test_missing_values_across_multiple_columns() -> None:
    """
    Missing values across different columns should all
    contribute to the total.
    """

    dataframe = pd.DataFrame(
        {
            "A": [1, None, 3, None],
            "B": [None, 2, 3, 4],
            "C": ["x", "y", None, "z"],
        }
    )

    summary = generate_missing_value_summary(
        dataframe
    )

    assert summary.total_missing == 4

    # 4 missing cells out of 12 total cells.
    assert summary.missing_percentage == 33.33

    assert summary.columns_with_missing == {
        "A": 2,
        "B": 1,
        "C": 1,
    }

    assert summary.columns_without_missing == []


def test_empty_dataframe() -> None:
    """
    An empty DataFrame should not cause division-by-zero
    and should report zero missing values.
    """

    dataframe = pd.DataFrame()

    summary = generate_missing_value_summary(
        dataframe
    )

    assert summary.total_missing == 0
    assert summary.missing_percentage == 0.0
    assert summary.columns_with_missing == {}
    assert summary.columns_without_missing == []