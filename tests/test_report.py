"""
Tests for the Datapilot Report API.
"""

import pandas as pd

from datapilot import analyze
from datapilot.core.report import Report


def test_analyze_returns_report() -> None:
    """
    analyze() should return a Report object.
    """

    dataframe = pd.DataFrame(
        {
            "Age": [20, 21, 22],
            "Salary": [100, 200, 300],
        }
    )

    report = analyze(dataframe)

    assert isinstance(report, Report)


def test_report_methods_return_expected_models() -> None:
    """
    Report methods should return their expected analysis models.
    """

    dataframe = pd.DataFrame(
        {
            "Age": [20, 21, 22, 23],
            "Salary": [100, 200, 300, 400],
            "Department": [
                "IT",
                "HR",
                "IT",
                "Sales",
            ],
        }
    )

    report = analyze(dataframe)

    assert report.summary().rows == 4
    assert report.summary().columns == 3

    assert report.missing_values().total_missing == 0

    assert report.duplicates().total_duplicates == 0

    assert report.data_types().numeric_columns == [
        "Age",
        "Salary",
    ]

    assert report.dataset_health().score == 100

    assert "Age" in (
        report.statistics().column_statistics
    )

    assert report.outliers().total_outliers == 0

    assert report.correlation().correlation_matrix.shape == (
        2,
        2,
    )

    assert len(report.insights().insights) > 0


def test_report_uses_original_dataset() -> None:
    """
    Report analysis should reflect the supplied dataset.
    """

    dataframe = pd.DataFrame(
        {
            "Age": [20, None, 22],
            "Salary": [100, 200, None],
        }
    )

    report = analyze(dataframe)

    assert report.summary().rows == 3
    assert report.missing_values().total_missing == 2