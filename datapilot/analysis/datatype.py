"""
Data type analysis for Datapilot.
"""

import pandas as pd

from .models import DataTypeSummary


def generate_data_type_summary(
    dataframe: pd.DataFrame,
) -> DataTypeSummary:
    """
    Generate data type statistics for a dataset.

    Parameters
    ----------
    dataframe : pandas.DataFrame
        Dataset to analyze.

    Returns
    -------
    DataTypeSummary
        Summary of dataset column types.
    """

    numeric_columns = dataframe.select_dtypes(
        include=["number"]
    ).columns.tolist()

    categorical_columns = dataframe.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    boolean_columns = dataframe.select_dtypes(
        include=["bool"]
    ).columns.tolist()

    datetime_columns = dataframe.select_dtypes(
        include=["datetime", "datetimetz"]
    ).columns.tolist()

    return DataTypeSummary(
        numeric_columns=numeric_columns,
        categorical_columns=categorical_columns,
        boolean_columns=boolean_columns,
        datetime_columns=datetime_columns,
    )