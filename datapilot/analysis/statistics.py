"""
Statistical analysis for Datapilot.
"""

from typing import SupportsFloat, cast

import pandas as pd

from .models import StatisticsSummary


def generate_statistics_summary(
    dataframe: pd.DataFrame,
) -> StatisticsSummary:
    """
    Generate descriptive statistics for all numeric columns.
    """

    numeric_dataframe = dataframe.select_dtypes(
        include="number",
    )

    statistics: dict[str, dict[str, float]] = {}

    for column in numeric_dataframe.columns:
        series = numeric_dataframe[column]

        description = series.describe()

        statistics[str(column)] = {
            "count": float(cast(SupportsFloat, description["count"])),
            "mean": float(cast(SupportsFloat, description["mean"])),
            "median": float(cast(SupportsFloat, series.median())),
            "std": float(cast(SupportsFloat, description["std"])),
            "variance": float(cast(SupportsFloat, series.var())),
            "min": float(cast(SupportsFloat, description["min"])),
            "q1": float(cast(SupportsFloat, description["25%"])),
            "q3": float(cast(SupportsFloat, description["75%"])),
            "max": float(cast(SupportsFloat, description["max"])),
            "skewness": float(cast(SupportsFloat, series.skew())),
            "kurtosis": float(cast(SupportsFloat, series.kurt())),
        }

    return StatisticsSummary(
        column_statistics=statistics,
    )