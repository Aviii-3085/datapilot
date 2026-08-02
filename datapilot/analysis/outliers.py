"""
Outlier detection for Datapilot.
"""

import pandas as pd

from .models import OutlierSummary


def generate_outlier_summary(
    dataframe: pd.DataFrame,
) -> OutlierSummary:
    """
    Detect outliers using the IQR method.
    """

    numeric_dataframe = dataframe.select_dtypes(
        include="number",
    )

    total_outliers = 0

    columns_with_outliers: dict[str, int] = {}

    columns_without_outliers: list[str] = []

    for column in numeric_dataframe.columns:

        series = numeric_dataframe[column].dropna()

        if series.empty:
            columns_without_outliers.append(
                str(column)
            )
            continue

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)

        iqr = q3 - q1

        lower_bound = q1 - (1.5 * iqr)
        upper_bound = q3 + (1.5 * iqr)

        outlier_count = int(
            (
                (series < lower_bound)
                | (series > upper_bound)
            ).sum()
        )

        if outlier_count > 0:

            columns_with_outliers[
                str(column)
            ] = outlier_count

            total_outliers += outlier_count

        else:

            columns_without_outliers.append(
                str(column)
            )

    total_numeric_values = int(
        numeric_dataframe.count().sum()
    )

    outlier_percentage = (
        round(
            (total_outliers / total_numeric_values)
            * 100,
            2,
        )
        if total_numeric_values > 0
        else 0.0
    )

    return OutlierSummary(
        total_outliers=total_outliers,
        outlier_percentage=outlier_percentage,
        columns_with_outliers=columns_with_outliers,
        columns_without_outliers=columns_without_outliers,
    )