"""
Dataset summary analysis for Datapilot.
"""

import pandas as pd

from .models import DatasetSummary


def generate_summary(dataframe: pd.DataFrame) -> DatasetSummary:
    """
    Generate a summary of the dataset.

    Parameters
    ----------
    dataframe : pandas.DataFrame
        Dataset to summarize.

    Returns
    -------
    DatasetSummary
        Summary information about the dataset.
    """

    memory_usage = float(
        dataframe.memory_usage(deep=True).sum()
        / 1024
        / 1024
    )

    return DatasetSummary(
        rows=dataframe.shape[0],
        columns=dataframe.shape[1],
        memory_usage_mb=round(memory_usage, 2),
        column_names=list(dataframe.columns),
    )