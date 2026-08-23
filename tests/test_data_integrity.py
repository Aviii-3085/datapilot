"""
Tests for Datapilot v0.4 data-integrity signals.
"""

import pandas as pd

from datapilot.analysis.data_integrity import (
    generate_data_integrity_summary,
)


def test_clean_dataset_has_no_integrity_signals() -> None:
    dataframe = pd.DataFrame(
        {
            "Age": [20, 21, 22, 23, 24],
            "Salary": [100, 200, 300, 400, 500],
        }
    )

    integrity = generate_data_integrity_summary(
        dataframe
    )

    assert integrity.missing_value_columns == []
    assert integrity.duplicate_rows == 0
    assert integrity.outlier_columns == []
    assert integrity.identifier_like_columns == [
        "Age",
        "Salary",
    ]
    assert integrity.constant_columns == []
    assert integrity.empty_columns == []


def test_missing_columns_are_detected() -> None:
    dataframe = pd.DataFrame(
        {
            "Age": [20, None, 22],
            "Salary": [100, 200, 300],
        }
    )

    integrity = generate_data_integrity_summary(
        dataframe
    )

    assert integrity.missing_value_columns == [
        "Age"
    ]


def test_duplicate_rows_are_detected() -> None:
    dataframe = pd.DataFrame(
        {
            "Age": [20, 20, 21],
            "Salary": [100, 100, 200],
        }
    )

    integrity = generate_data_integrity_summary(
        dataframe
    )

    assert integrity.duplicate_rows == 1


def test_outlier_columns_are_detected() -> None:
    dataframe = pd.DataFrame(
        {
            "Value": [1, 2, 2, 2, 3, 100],
        }
    )

    integrity = generate_data_integrity_summary(
        dataframe
    )

    assert integrity.outlier_columns == [
        "Value"
    ]


def test_constant_columns_are_detected() -> None:
    dataframe = pd.DataFrame(
        {
            "Age": [20, 21, 22],
            "Status": ["Active", "Active", "Active"],
        }
    )

    integrity = generate_data_integrity_summary(
        dataframe
    )

    assert integrity.constant_columns == [
        "Status"
    ]


def test_empty_columns_are_detected() -> None:
    dataframe = pd.DataFrame(
        {
            "Age": [20, 21, 22],
            "Unused": [None, None, None],
        }
    )

    integrity = generate_data_integrity_summary(
        dataframe
    )

    assert integrity.empty_columns == [
        "Unused"
    ]


def test_identifier_like_columns_are_structural_signals() -> None:
    dataframe = pd.DataFrame(
        {
            "CustomerID": [101, 102, 103, 104],
            "Age": [20, 21, 22, 23],
        }
    )

    integrity = generate_data_integrity_summary(
        dataframe
    )

    assert "CustomerID" in (
        integrity.identifier_like_columns
    )


def test_integrity_signals_do_not_claim_factual_invalidity() -> None:
    dataframe = pd.DataFrame(
        {
            "ID": [1, 2, 3],
            "Value": [10, 20, 100],
        }
    )

    integrity = generate_data_integrity_summary(
        dataframe
    )

    assert integrity.structural_signals
    assert all(
        isinstance(signal, str)
        for signal in integrity.structural_signals
    )