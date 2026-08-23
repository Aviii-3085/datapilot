"""
Data integrity signal analysis for Datapilot v0.4.
"""

import pandas as pd

from .duplicate import generate_duplicate_summary
from .missing import generate_missing_value_summary
from .models import DataIntegritySummary
from .outliers import generate_outlier_summary


def _find_identifier_like_columns(
    dataframe: pd.DataFrame,
) -> list[str]:
    """
    Identify columns that appear identifier-like.

    This is a structural signal only. It does not determine whether
    a column is actually an identifier in the domain context.
    """

    identifier_columns: list[str] = []

    if len(dataframe) == 0:
        return identifier_columns

    for column in dataframe.columns:
        series = dataframe[column]

        non_missing = series.dropna()

        if non_missing.empty:
            continue

        unique_count = non_missing.nunique()

        if unique_count == len(non_missing):
            identifier_columns.append(
                str(column)
            )

    return identifier_columns


def _find_constant_columns(
    dataframe: pd.DataFrame,
) -> list[str]:
    """
    Identify columns containing only one unique non-missing value.
    """

    constant_columns: list[str] = []

    for column in dataframe.columns:
        series = dataframe[column].dropna()

        if series.empty:
            continue

        if series.nunique() <= 1:
            constant_columns.append(
                str(column)
            )

    return constant_columns


def _find_empty_columns(
    dataframe: pd.DataFrame,
) -> list[str]:
    """
    Identify columns containing only missing values.
    """

    empty_columns: list[str] = []

    for column in dataframe.columns:
        if dataframe[column].isna().all():
            empty_columns.append(
                str(column)
            )

    return empty_columns


def generate_data_integrity_summary(
    dataframe: pd.DataFrame,
) -> DataIntegritySummary:
    """
    Generate observable data-integrity signals.

    These signals indicate conditions that may deserve review.
    They do not establish factual invalidity or domain correctness.
    """

    missing = generate_missing_value_summary(
        dataframe
    )

    duplicates = generate_duplicate_summary(
        dataframe
    )

    outliers = generate_outlier_summary(
        dataframe
    )

    identifier_like_columns = (
        _find_identifier_like_columns(
            dataframe
        )
    )

    constant_columns = _find_constant_columns(
        dataframe
    )

    empty_columns = _find_empty_columns(
        dataframe
    )

    structural_signals: list[str] = []

    if empty_columns:
        structural_signals.append(
            f"{len(empty_columns)} completely empty "
            "column(s) detected."
        )

    if constant_columns:
        structural_signals.append(
            f"{len(constant_columns)} constant "
            "column(s) detected."
        )

    if identifier_like_columns:
        structural_signals.append(
            f"{len(identifier_like_columns)} "
            "identifier-like column(s) detected."
        )

    if duplicates.total_duplicates > 0:
        structural_signals.append(
            f"{duplicates.total_duplicates} duplicate "
            "row(s) detected."
        )

    if outliers.total_outliers > 0:
        structural_signals.append(
            f"{outliers.total_outliers} outlier "
            "value(s) detected across numeric columns."
        )

    if missing.total_missing > 0:
        structural_signals.append(
            f"{missing.total_missing} missing "
            "value(s) detected."
        )

    return DataIntegritySummary(
        missing_value_columns=list(
            missing.columns_with_missing.keys()
        ),
        duplicate_rows=duplicates.total_duplicates,
        outlier_columns=list(
            outliers.columns_with_outliers.keys()
        ),
        identifier_like_columns=identifier_like_columns,
        constant_columns=constant_columns,
        empty_columns=empty_columns,
        structural_signals=structural_signals,
    )
