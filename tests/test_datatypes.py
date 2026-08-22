"""
Tests for data type analysis.
"""

import pandas as pd

from datapilot.analysis.datatype import (
    generate_data_type_summary,
)


def test_generate_data_type_summary(
    sample_dataframe,
) -> None:
    """
    Test standard data type classification.
    """

    summary = generate_data_type_summary(
        sample_dataframe
    )

    assert summary.numeric_columns == [
        "Age",
        "Salary",
    ]

    assert summary.categorical_columns == [
        "Department",
    ]

    assert summary.boolean_columns == [
        "Is_Manager",
    ]

    assert summary.datetime_columns == [
        "Joining_Date",
    ]


def test_string_dtype_is_categorical() -> None:
    """
    Pandas string dtype should be classified as categorical.
    """

    dataframe = pd.DataFrame(
        {
            "Name": pd.Series(
                ["Alice", "Bob", "Charlie"],
                dtype="string",
            ),
        }
    )

    summary = generate_data_type_summary(
        dataframe
    )

    assert summary.numeric_columns == []
    assert summary.categorical_columns == ["Name"]
    assert summary.boolean_columns == []
    assert summary.datetime_columns == []


def test_category_dtype_is_categorical() -> None:
    """
    Pandas category dtype should be classified as categorical.
    """

    dataframe = pd.DataFrame(
        {
            "Department": pd.Series(
                ["IT", "HR", "Sales"],
                dtype="category",
            ),
        }
    )

    summary = generate_data_type_summary(
        dataframe
    )

    assert summary.numeric_columns == []
    assert summary.categorical_columns == [
        "Department"
    ]
    assert summary.boolean_columns == []
    assert summary.datetime_columns == []


def test_boolean_columns_are_classified_separately() -> None:
    """
    Boolean columns should not be classified as numeric.
    """

    dataframe = pd.DataFrame(
        {
            "Is_Manager": [
                True,
                False,
                True,
                False,
            ],
        }
    )

    summary = generate_data_type_summary(
        dataframe
    )

    assert summary.numeric_columns == []
    assert summary.categorical_columns == []
    assert summary.boolean_columns == [
        "Is_Manager"
    ]
    assert summary.datetime_columns == []


def test_datetime_columns_are_classified_separately() -> None:
    """
    Datetime columns should be classified as datetime.
    """

    dataframe = pd.DataFrame(
        {
            "Joining_Date": pd.to_datetime(
                [
                    "2023-01-01",
                    "2023-02-01",
                    "2023-03-01",
                ]
            ),
        }
    )

    summary = generate_data_type_summary(
        dataframe
    )

    assert summary.numeric_columns == []
    assert summary.categorical_columns == []
    assert summary.boolean_columns == []
    assert summary.datetime_columns == [
        "Joining_Date"
    ]


def test_multiple_data_types_are_mutually_exclusive() -> None:
    """
    Each column should belong to exactly one recognized
    data type category.
    """

    dataframe = pd.DataFrame(
        {
            "Age": [20, 21, 22],
            "Name": ["A", "B", "C"],
            "Active": [True, False, True],
            "Date": pd.to_datetime(
                [
                    "2023-01-01",
                    "2023-02-01",
                    "2023-03-01",
                ]
            ),
        }
    )

    summary = generate_data_type_summary(
        dataframe
    )

    all_classified_columns = (
        summary.numeric_columns
        + summary.categorical_columns
        + summary.boolean_columns
        + summary.datetime_columns
    )

    assert sorted(all_classified_columns) == [
        "Active",
        "Age",
        "Date",
        "Name",
    ]

    assert len(all_classified_columns) == len(
        set(all_classified_columns)
    )


def test_empty_dataframe() -> None:
    """
    An empty DataFrame with no columns should produce
    empty type classifications.
    """

    dataframe = pd.DataFrame()

    summary = generate_data_type_summary(
        dataframe
    )

    assert summary.numeric_columns == []
    assert summary.categorical_columns == []
    assert summary.boolean_columns == []
    assert summary.datetime_columns == []