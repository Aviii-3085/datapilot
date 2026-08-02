"""
Tests for data type analysis.
"""

from datapilot.analysis.datatype import (
    generate_data_type_summary,
)


def test_generate_data_type_summary(
    sample_dataframe,
) -> None:
    """
    Test data type summary generation.
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