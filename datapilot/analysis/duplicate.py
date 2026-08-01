"""
Duplicate row analysis for Datapilot.
"""

import pandas as pd

from .models import DuplicateSummary


def generate_duplicate_summary(
    dataframe: pd.DataFrame,
) -> DuplicateSummary:
    """
    Generate duplicate row statistics for a dataset.

    Parameters
    ----------
    dataframe : pandas.DataFrame
        Dataset to analyze.

    Returns
    -------
    DuplicateSummary
        Summary of duplicate rows in the dataset.
    """

    total_duplicates = int(dataframe.duplicated().sum())

    total_rows = len(dataframe)

    duplicate_percentage = (
        round((total_duplicates / total_rows) * 100, 2)
        if total_rows > 0
        else 0.0
    )

    return DuplicateSummary(
        total_duplicates=total_duplicates,
        duplicate_percentage=duplicate_percentage,
    )