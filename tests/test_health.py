"""
Tests for dataset health assessment.
"""

import pandas as pd

from datapilot.analysis.health import (
    generate_dataset_health,
)


def test_generate_dataset_health(
    sample_dataframe,
) -> None:
    """
    Test dataset health assessment.
    """

    health = generate_dataset_health(
        sample_dataframe
    )

    assert health.score == 85
    assert health.grade == "B"
    assert health.status == "Good"
    assert health.ml_ready is False

    assert health.strengths == [
        "All columns have recognized data types."
    ]

    assert health.weaknesses == [
        "3 missing values detected.",
        "1 duplicate rows detected.",
    ]

    assert health.recommendations == [
        "Handle missing values before further analysis.",
        "Remove duplicate rows.",
    ]


def test_healthy_dataset_is_ml_ready() -> None:
    """
    A clean dataset should receive an excellent health score
    and be considered ML-ready.
    """

    dataframe = pd.DataFrame(
        {
            "Age": [20, 21, 22, 23, 24],
            "Salary": [100, 200, 300, 400, 500],
        }
    )

    health = generate_dataset_health(
        dataframe
    )

    assert health.score == 100
    assert health.grade == "A+"
    assert health.status == "Excellent"
    assert health.ml_ready is True


def test_missing_values_reduce_health_score() -> None:
    """
    Missing values should reduce the health score
    and prevent ML readiness.
    """

    dataframe = pd.DataFrame(
        {
            "Age": [20, None, 22, 23],
            "Salary": [100, 200, None, 400],
        }
    )

    health = generate_dataset_health(
        dataframe
    )

    assert health.score < 100
    assert health.ml_ready is False
    assert health.weaknesses == [
        "2 missing values detected.",
    ]


def test_duplicate_rows_reduce_health_score() -> None:
    """
    Duplicate rows should reduce the health score
    and prevent ML readiness.
    """

    dataframe = pd.DataFrame(
        {
            "Age": [20, 20, 21, 22],
            "Salary": [100, 100, 200, 300],
        }
    )

    health = generate_dataset_health(
        dataframe
    )

    assert health.score < 100
    assert health.ml_ready is False
    assert health.weaknesses == [
        "1 duplicate rows detected.",
    ]


def test_missing_and_duplicates_can_make_dataset_not_ml_ready() -> None:
    """
    Severe data-quality problems should prevent ML readiness.
    """

    dataframe = pd.DataFrame(
        {
            "Age": [None] * 10,
            "Salary": [None] * 10,
        }
    )

    health = generate_dataset_health(
        dataframe
    )

    assert health.score < 85
    assert health.ml_ready is False
    assert health.score >= 0
    assert health.score <= 100

def test_high_column_missingness_prevents_ml_readiness() -> None:
    """
    A severely incomplete column should prevent ML readiness.
    """

    dataframe = pd.DataFrame(
        {
            "Age": [20, 21, 22, 23, 24],
            "Cabin": [None, None, None, None, "A1"],
        }
    )

    health = generate_dataset_health(
        dataframe
    )

    assert health.ml_ready is False

def test_titanic_like_missingness_prevents_ml_readiness() -> None:
    """
    A dataset with one highly incomplete column and another
    substantially incomplete column should not be ML-ready.
    """

    dataframe = pd.DataFrame(
        {
            "Age": [20, None, 22, 23, None],
            "Cabin": [None, None, None, None, "A1"],
        }
    )

    health = generate_dataset_health(
        dataframe
    )

    assert health.ml_ready is False