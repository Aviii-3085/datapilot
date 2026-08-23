"""
Tests for Datapilot v0.4 ML Readiness assessment.
"""

import pandas as pd

from datapilot.analysis.ml_readiness import (
    generate_ml_readiness,
)


def test_clean_dataset_has_strong_ml_preparation_signals() -> None:
    dataframe = pd.DataFrame(
        {
            "Age": [20, 21, 22, 23, 24],
            "Salary": [100, 200, 300, 400, 500],
        }
    )

    readiness = generate_ml_readiness(
        dataframe
    )

    assert readiness.score == 100.0
    assert readiness.status == (
        "Strong Preparation Signals"
    )

    assert readiness.completeness_score == 100.0
    assert readiness.feature_quality_score == 100.0
    assert readiness.data_stability_score == 100.0
    assert readiness.consistency_score == 100.0
    assert readiness.distribution_score == 100.0

    assert readiness.target_readiness == "NOT ASSESSED"


def test_missing_values_reduce_ml_completeness() -> None:
    dataframe = pd.DataFrame(
        {
            "Age": [20, None, 22, 23],
            "Salary": [100, 200, None, 400],
        }
    )

    readiness = generate_ml_readiness(
        dataframe
    )

    assert readiness.completeness_score < 100.0
    assert readiness.target_readiness == "NOT ASSESSED"

    assert any(
        "missing values" in weakness.lower()
        for weakness in readiness.weaknesses
    )


def test_duplicate_rows_reduce_data_stability() -> None:
    dataframe = pd.DataFrame(
        {
            "Age": [20, 20, 21, 22],
            "Salary": [100, 100, 200, 300],
        }
    )

    readiness = generate_ml_readiness(
        dataframe
    )

    assert readiness.data_stability_score < 100.0

    assert any(
        "duplicate" in weakness.lower()
        for weakness in readiness.weaknesses
    )


def test_constant_column_reduces_feature_quality() -> None:
    dataframe = pd.DataFrame(
        {
            "Age": [20, 21, 22, 23, 24],
            "Constant": [1, 1, 1, 1, 1],
        }
    )

    readiness = generate_ml_readiness(
        dataframe
    )

    assert readiness.feature_quality_score < 100.0


def test_no_numeric_columns_affects_distribution_signal() -> None:
    dataframe = pd.DataFrame(
        {
            "Name": ["A", "B", "C"],
            "Country": ["IN", "US", "UK"],
        }
    )

    readiness = generate_ml_readiness(
        dataframe
    )

    assert readiness.distribution_score == 100.0
    assert any(
        "numeric columns" in weakness.lower()
        for weakness in readiness.weaknesses
    )


def test_target_is_not_assessed_without_explicit_target() -> None:
    dataframe = pd.DataFrame(
        {
            "Age": [20, 21, 22],
            "Salary": [100, 200, 300],
        }
    )

    readiness = generate_ml_readiness(
        dataframe
    )

    assert readiness.target_readiness == "NOT ASSESSED"


def test_ml_score_uses_documented_weights() -> None:
    dataframe = pd.DataFrame(
        {
            "Age": [20, None, 22, 23],
            "Salary": [100, 200, None, 400],
        }
    )

    readiness = generate_ml_readiness(
        dataframe
    )

    expected = round(
        readiness.completeness_score * 0.25
        + readiness.feature_quality_score * 0.20
        + readiness.data_stability_score * 0.20
        + readiness.consistency_score * 0.15
        + readiness.distribution_score * 0.20,
        2,
    )

    assert readiness.score == expected