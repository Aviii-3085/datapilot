import pandas as pd

from datapilot.analysis.statistics import (
    generate_statistics_summary,
)


def test_generate_statistics_summary() -> None:
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