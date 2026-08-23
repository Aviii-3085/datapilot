"""
Statistical interpretation for Datapilot v0.4.
"""

import math

import pandas as pd

from .models import StatisticsSummary


def _interpret_skewness(value: float) -> str:
    """Interpret skewness as a distribution-shape signal."""

    if not math.isfinite(value):
        return "Not assessed"

    absolute_value = abs(value)

    if absolute_value < 0.5:
        return "Approximately symmetric"

    if absolute_value < 1.0:
        return "Moderately skewed"

    if value > 0:
        return "Strong right skew"

    return "Strong left skew"


def _interpret_kurtosis(value: float) -> str:
    """
    Interpret excess kurtosis as a distribution-shape signal.

    This does not classify the data as erroneous.
    """

    if not math.isfinite(value):
        return "Not assessed"

    if value < -1.0:
        return "Lower-tailed / flatter distribution"

    if value <= 1.0:
        return "Near-normal tail weight"

    return "Higher-tailed / heavier distribution"


def _interpret_outlier_signal(
    series: pd.Series,
) -> str:
    """Describe an IQR-based extreme-value signal."""

    clean = series.dropna()

    if clean.empty:
        return "Not assessed"

    q1 = clean.quantile(0.25)
    q3 = clean.quantile(0.75)
    iqr = q3 - q1

    if iqr == 0:
        return "No IQR-based outlier assessment"

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    outliers = (
        (clean < lower_bound)
        | (clean > upper_bound)
    ).sum()

    percentage = (
        outliers / len(clean)
    ) * 100

    if percentage == 0:
        return "No IQR-based outlier signal"

    return (
        f"{outliers} values ({percentage:.2f}%) "
        "outside the IQR fences"
    )


def generate_statistical_profile(
    dataframe: pd.DataFrame,
) -> dict[str, dict[str, str | float]]:
    """
    Generate contextual statistical interpretations.

    The returned interpretations describe statistical patterns only.
    They do not establish data errors, business validity, causality,
    or model suitability.
    """

    statistics = StatisticsSummary(
        column_statistics={}
    )

    numeric_dataframe = dataframe.select_dtypes(
        include="number",
    )

    profile: dict[
        str,
        dict[str, str | float],
    ] = {}

    for column in numeric_dataframe.columns:
        series = numeric_dataframe[column]

        if series.dropna().empty:
            continue

        skewness = float(series.skew())
        kurtosis = float(series.kurt())

        profile[str(column)] = {
            "skewness": skewness,
            "skewness_interpretation": _interpret_skewness(
                skewness
            ),
            "kurtosis": kurtosis,
            "kurtosis_interpretation": _interpret_kurtosis(
                kurtosis
            ),
            "outlier_signal": _interpret_outlier_signal(
                series
            ),
        }

    return profile