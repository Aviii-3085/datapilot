"""
Tests for dataset summary analysis.
"""

from datapilot.analysis.summary import generate_summary


def test_generate_summary(sample_dataframe) -> None:
    """
    Test dataset summary generation.
    """

    summary = generate_summary(sample_dataframe)

    assert summary.rows == 4
    assert summary.columns == 5
    assert summary.column_names == [
        "Age",
        "Salary",
        "Department",
        "Is_Manager",
        "Joining_Date",
    ]
    assert summary.memory_usage_mb >= 0