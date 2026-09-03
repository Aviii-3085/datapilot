"""
Deterministic consistency analysis for Datapilot v0.4.1.
"""

from collections import Counter

import pandas as pd

from .models import ConsistencySummary


def generate_consistency_summary(
    dataframe: pd.DataFrame,
) -> ConsistencySummary:
    """
    Detect objectively observable type inconsistencies.

    Missing values are excluded from type analysis because they are
    assessed separately by Dataset Completeness.

    Consistency degradation is based on the proportion of non-missing
    values whose underlying type differs from the dominant type within
    their column.
    """

    inconsistent_columns: list[str] = []
    inconsistent_value_count = 0
    total_non_missing = 0

    for column in dataframe.columns:
        series = dataframe[column].dropna()

        if series.empty:
            continue

        type_counts = Counter(
            type(value)
            for value in series
        )

        column_total = len(series)
        dominant_count = max(type_counts.values())
        column_inconsistent_count = (
            column_total - dominant_count
        )

        total_non_missing += column_total

        if column_inconsistent_count > 0:
            inconsistent_columns.append(str(column))
            inconsistent_value_count += column_inconsistent_count

    if total_non_missing == 0:
        consistency_percentage = 0.0
    else:
        consistency_percentage = (
            inconsistent_value_count
            / total_non_missing
        ) * 100.0

    return ConsistencySummary(
        inconsistent_columns=inconsistent_columns,
        inconsistent_value_count=inconsistent_value_count,
        consistency_percentage=round(
            consistency_percentage,
            2,
        ),
    )
