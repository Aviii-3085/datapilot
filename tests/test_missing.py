"""
Tests for missing value analysis.
"""

from datapilot.analysis.missing import (
    generate_missing_value_summary,
)


def test_generate_missing_value_summary(
    sample_dataframe,
) -> None:
    """
    Test missing value summary generation.
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