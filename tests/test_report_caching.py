"""
Tests for Report-level analysis caching.
"""

import pandas as pd

from datapilot import analyze


def test_report_caches_statistics() -> None:
    """
    Repeated statistics() calls should reuse the same result.
    """

    dataframe = pd.DataFrame(
        {
            "Age": [20, 21, 22, 23],
            "Salary": [100, 200, 300, 400],
        }
    )

    report = analyze(dataframe)

    first = report.statistics()
    second = report.statistics()

    assert first is second


def test_report_caches_dataset_health() -> None:
    """
    Repeated dataset_health() calls should reuse the same result.
    """

    dataframe = pd.DataFrame(
        {
            "Age": [20, 21, 22, 23],
            "Salary": [100, 200, 300, 400],
        }
    )

    report = analyze(dataframe)

    first = report.dataset_health()
    second = report.dataset_health()

    assert first is second


def test_report_caches_insights() -> None:
    """
    Repeated insights() calls should reuse the same result.
    """

    dataframe = pd.DataFrame(
        {
            "Age": [20, 21, 22, 23],
            "Salary": [100, 200, 300, 400],
        }
    )

    report = analyze(dataframe)

    first = report.insights()
    second = report.insights()

    assert first is second