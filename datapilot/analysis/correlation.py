"""
Correlation analysis for Datapilot.
"""

from typing import SupportsFloat, cast

import pandas as pd

from .models import CorrelationSummary


def generate_correlation_summary(
    dataframe: pd.DataFrame,
) -> CorrelationSummary:
    """
    Generate Pearson correlation analysis for numeric columns.
    """

    numeric_dataframe = dataframe.select_dtypes(
        include="number",
    )

    correlation_matrix = numeric_dataframe.corr()

    strong_positive_pairs: dict[str, float] = {}
    strong_negative_pairs: dict[str, float] = {}

    columns = list(correlation_matrix.columns)

    for i, left in enumerate(columns):
        for right in columns[i + 1:]:

            correlation = cast(
                SupportsFloat,
                correlation_matrix.loc[left, right],
            )

            value = float(correlation)

            pair = f"{left} ↔ {right}"

            if value >= 0.70:
                strong_positive_pairs[pair] = round(
                    value,
                    3,
                )

            elif value <= -0.70:
                strong_negative_pairs[pair] = round(
                    value,
                    3,
                )

    return CorrelationSummary(
        correlation_matrix=correlation_matrix,
        strong_positive_pairs=strong_positive_pairs,
        strong_negative_pairs=strong_negative_pairs,
    )