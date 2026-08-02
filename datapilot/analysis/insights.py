"""
Insight generation for Datapilot.
"""

import pandas as pd

from .correlation import generate_correlation_summary
from .duplicate import generate_duplicate_summary
from .missing import generate_missing_value_summary
from .models import InsightSummary
from .outliers import generate_outlier_summary


def generate_insight_summary(
    dataframe: pd.DataFrame,
) -> InsightSummary:
    """
    Generate actionable dataset insights.
    """

    insights: list[str] = []

    recommendations: list[str] = []

    missing = generate_missing_value_summary(
        dataframe
    )

    duplicates = generate_duplicate_summary(
        dataframe
    )

    outliers = generate_outlier_summary(
        dataframe
    )

    correlation = generate_correlation_summary(
        dataframe
    )

    if missing.total_missing > 0:

        insights.append(
            f"Dataset contains "
            f"{missing.total_missing} missing values."
        )

        recommendations.append(
            "Handle missing values before "
            "training machine learning models."
        )

    if duplicates.total_duplicates > 0:

        insights.append(
            f"Dataset contains "
            f"{duplicates.total_duplicates} duplicate rows."
        )

        recommendations.append(
            "Remove duplicate rows."
        )

    if outliers.total_outliers > 0:

        insights.append(
            f"Detected "
            f"{outliers.total_outliers} statistical outliers."
        )

        recommendations.append(
            "Review outliers before modelling."
        )

    if correlation.strong_positive_pairs:

        insights.append(
            "Highly correlated numeric features detected."
        )

        recommendations.append(
            "Review correlated features to "
            "reduce multicollinearity."
        )

    if correlation.strong_negative_pairs:

        insights.append(
            "Strong negative correlations detected."
        )

    if not insights:

        insights.append(
            "No significant data quality issues detected."
        )

    return InsightSummary(
        insights=insights,
        recommendations=recommendations,
    )