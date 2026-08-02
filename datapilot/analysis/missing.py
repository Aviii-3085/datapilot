"""
Missing value analysis for Datapilot.
"""

import pandas as pd

from .models import MissingValueSummary


def generate_missing_value_summary(
    dataframe: pd.DataFrame,
) -> MissingValueSummary:
    """
    Generate missing value statistics for a dataset.

    Parameters
    ----------
    dataframe : pandas.DataFrame
        Dataset to analyze.

    Returns
    -------
    MissingValueSummary
        Summary of missing values in the dataset.
    """

    total_missing = int(dataframe.isna().sum().sum())

    total_cells = dataframe.shape[0] * dataframe.shape[1]

    missing_percentage = (
        round((total_missing / total_cells) * 100, 2)
        if total_cells > 0
        else 0.0
    )

    missing_per_column = dataframe.isna().sum()

    columns_with_missing = {
        str(column): int(count)
        for column, count in missing_per_column.items()
        if count > 0
    }

    columns_without_missing = [
        str(column)
        for column, count in missing_per_column.items()
        if count == 0
    ]

    return MissingValueSummary(
        total_missing=total_missing,
        missing_percentage=missing_percentage,
        columns_with_missing=columns_with_missing,
        columns_without_missing=columns_without_missing,
    )