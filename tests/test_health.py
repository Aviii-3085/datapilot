"""
Tests for Datapilot v0.4 Dataset Health assessment.
"""

import pandas as pd

from datapilot.analysis.health import (
    generate_dataset_health,
)


def test_generate_dataset_health(
    sample_dataframe,
) -> None:
    """
    Test the v0.4 Dataset Health structure and scoring.
    """

    health = generate_dataset_health(
        sample_dataframe
    )

    assert 0 <= health.score <= 100

    assert health.completeness_score < 100
    assert health.duplicate_score < 100
    assert health.structure_score == 100
    assert health.consistency_score == 100

    assert health.grade in {
        "A",
        "B",
        "C",
        "D",
        "F",
    }

    assert health.status in {
        "Excellent",
        "Good",
        "Moderate",
        "Needs Attention",
        "Poor",
    }

    assert health.strengths == [
        "No mixed underlying value types detected.",
        "All columns have recognized data types.",
        "No completely empty columns detected.",
    ]
    assert health.weaknesses == [
        "3 missing values detected.",
        "1 duplicate rows detected.",
    ]

    assert health.recommendations == [
        "Review missing values before further analysis.",
        "Review duplicate rows before modelling or aggregation.",
    ]


def test_clean_dataset_has_perfect_health() -> None:
    """
    A clean, structurally valid dataset should receive a perfect
    Dataset Health score.
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

    assert health.score == 100.0
    assert health.grade == "A"
    assert health.status == "Excellent"

    assert health.completeness_score == 100.0
    assert health.duplicate_score == 100.0
    assert health.structure_score == 100.0
    assert health.consistency_score == 100.0


def test_missing_values_reduce_completeness_score() -> None:
    """
    Missing values should reduce the Completeness score.
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

    assert health.completeness_score < 100
    assert health.duplicate_score == 100.0
    assert health.structure_score == 100.0
    assert health.consistency_score == 100.0

    assert health.weaknesses == [
        "2 missing values detected.",
    ]


def test_duplicate_rows_reduce_duplicate_score() -> None:
    """
    Duplicate rows should reduce the Duplicate score.
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

    assert health.completeness_score == 100.0
    assert health.duplicate_score < 100
    assert health.structure_score == 100.0
    assert health.consistency_score == 100.0

    assert health.weaknesses == [
        "1 duplicate rows detected.",
    ]


def test_completely_missing_dataset_has_zero_completeness() -> None:
    """
    A dataset containing only missing values should receive a zero
    Completeness score.
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

    assert health.completeness_score == 0.0
    assert health.duplicate_score == 6.31
    assert health.structure_score == 50.0
    assert health.consistency_score == 100.0

    assert 0 <= health.score <= 100


def test_constant_column_reduces_structure_score() -> None:
    """
    Constant columns should produce a structural penalty.
    """

    dataframe = pd.DataFrame(
        {
            "Age": [20, 21, 22, 23, 24],
            "Constant": [1, 1, 1, 1, 1],
        }
    )

    health = generate_dataset_health(
        dataframe
    )

    assert health.completeness_score == 100.0
    assert health.duplicate_score == 100.0
    assert health.structure_score < 100.0
    assert health.consistency_score == 100.0


def test_completely_empty_column_reduces_structure_score() -> None:
    """
    Completely empty columns should produce a structural penalty.
    """

    dataframe = pd.DataFrame(
        {
            "Age": [20, 21, 22, 23, 24],
            "Empty": [None, None, None, None, None],
        }
    )

    health = generate_dataset_health(
        dataframe
    )

    assert health.completeness_score == 43.53
    assert health.structure_score < 100.0
    assert health.consistency_score == 100.0

    assert any(
        "completely empty columns" in weakness
        for weakness in health.weaknesses
    )


def test_health_score_uses_documented_dimension_weights() -> None:
    """
    Verify the documented 30/20/25/25 weighting.
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

    expected = round(
        health.completeness_score * 0.30
        + health.duplicate_score * 0.20
        + health.structure_score * 0.25
        + health.consistency_score * 0.25,
        2,
    )

    assert health.score == expected

def test_completeness_score_follows_nonlinear_degradation_curve() -> None:
    """
    Completeness should use the v0.4.1 nonlinear degradation curve.
    """

    dataframe = pd.DataFrame(
        {
            "Value": [None] * 10 + list(range(90)),
        }
    )

    health = generate_dataset_health(
        dataframe
    )

    assert health.completeness_score == 88.12

def test_duplicate_score_follows_nonlinear_degradation_curve() -> None:
    """
    Duplicate scoring should use the v0.4.1 nonlinear degradation curve.
    """

    dataframe = pd.DataFrame(
        {
            "Value": list(range(90)) + [0] * 10,
        }
    )

    health = generate_dataset_health(
        dataframe
    )

    assert health.duplicate_score == 88.12
