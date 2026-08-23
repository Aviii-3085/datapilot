"""
Machine-learning readiness assessment for Datapilot v0.4.
"""

import pandas as pd

from .datatype import generate_data_type_summary
from .missing import generate_missing_value_summary
from .models import MLReadiness


def generate_ml_readiness(
    dataframe: pd.DataFrame,
) -> MLReadiness:
    """
    Generate observable ML preparation signals.

    Target suitability is not assessed unless a target is explicitly
    supplied. The resulting score therefore represents preparation
    quality, not guaranteed model suitability.
    """

    missing = generate_missing_value_summary(dataframe)
    data_types = generate_data_type_summary(dataframe)

    # ---------------------------------------------------------------
    # Completeness
    # ---------------------------------------------------------------

    completeness_score = max(
        0.0,
        min(
            100.0,
            100.0 - missing.missing_percentage,
        ),
    )

    # ---------------------------------------------------------------
    # Feature Quality
    # ---------------------------------------------------------------

    total_columns = len(dataframe.columns)

    if total_columns == 0:
        feature_quality_score = 0.0
    else:
        usable_columns = 0

        for column in dataframe.columns:
            series = dataframe[column]

            if series.isna().all():
                continue

            if series.nunique(dropna=True) <= 1:
                continue

            usable_columns += 1

        feature_quality_score = (
            usable_columns / total_columns
        ) * 100.0

    # ---------------------------------------------------------------
    # Data Stability
    # ---------------------------------------------------------------

    if len(dataframe) == 0:
        data_stability_score = 0.0
    else:
        duplicate_rows = int(
            dataframe.duplicated().sum()
        )

        duplicate_rate = (
            duplicate_rows / len(dataframe)
        ) * 100.0

        data_stability_score = max(
            0.0,
            min(
                100.0,
                100.0 - duplicate_rate,
            ),
        )

    # ---------------------------------------------------------------
    # Consistency
    # ---------------------------------------------------------------
    #
    # No formally specified consistency metric exists yet for ML
    # readiness. Keep this neutral rather than inventing a metric.
    #

    consistency_score = 100.0

    # ---------------------------------------------------------------
    # Distribution
    # ---------------------------------------------------------------

    numeric_columns = data_types.numeric_columns

    if not numeric_columns:
        distribution_score = 100.0
    else:
        valid_columns = 0

        for column in numeric_columns:
            series = dataframe[column].dropna()

            if len(series) < 2:
                continue

            if series.nunique() <= 1:
                continue

            valid_columns += 1

        distribution_score = (
            valid_columns / len(numeric_columns)
        ) * 100.0

    # ---------------------------------------------------------------
    # Target Readiness
    # ---------------------------------------------------------------

    target_readiness = "NOT ASSESSED"

    # ---------------------------------------------------------------
    # Overall preparation score
    # ---------------------------------------------------------------

    score = (
        completeness_score * 0.25
        + feature_quality_score * 0.20
        + data_stability_score * 0.20
        + consistency_score * 0.15
        + distribution_score * 0.20
    )

    score = round(
        max(0.0, min(100.0, score)),
        2,
    )

    # ---------------------------------------------------------------
    # Status
    # ---------------------------------------------------------------

    if score >= 90:
        status = "Strong Preparation Signals"
    elif score >= 75:
        status = "Good Preparation Signals"
    elif score >= 60:
        status = "Moderate Preparation Signals"
    elif score >= 40:
        status = "Weak Preparation Signals"
    else:
        status = "Poor Preparation Signals"

    # ---------------------------------------------------------------
    # Strengths
    # ---------------------------------------------------------------

    strengths: list[str] = []

    if completeness_score == 100.0:
        strengths.append(
            "No missing values detected."
        )

    if feature_quality_score == 100.0:
        strengths.append(
            "All columns contain usable variation."
        )

    if data_stability_score == 100.0:
        strengths.append(
            "No duplicate rows detected."
        )

    if numeric_columns:
        strengths.append(
            f"{len(numeric_columns)} numeric feature columns detected."
        )

    # ---------------------------------------------------------------
    # Weaknesses
    # ---------------------------------------------------------------

    weaknesses: list[str] = []

    if completeness_score < 100.0:
        weaknesses.append(
            f"{missing.total_missing} missing values detected."
        )

    if feature_quality_score < 100.0:
        weaknesses.append(
            "Some columns may have limited feature usefulness "
            "because they are empty or constant."
        )

    if data_stability_score < 100.0:
        weaknesses.append(
            "Duplicate rows detected."
        )

    if not numeric_columns:
        weaknesses.append(
            "No numeric columns detected."
        )

    # ---------------------------------------------------------------
    # Recommendations
    # ---------------------------------------------------------------

    recommendations: list[str] = []

    if completeness_score < 100.0:
        recommendations.append(
            "Review and handle missing values before modelling."
        )

    if feature_quality_score < 100.0:
        recommendations.append(
            "Review empty and constant columns before feature engineering."
        )

    if data_stability_score < 100.0:
        recommendations.append(
            "Review duplicate rows before modelling."
        )

    if target_readiness == "NOT ASSESSED":
        recommendations.append(
            "Provide a target variable when task-specific ML "
            "readiness assessment is required."
        )

    if not recommendations:
        recommendations.append(
            "Preparation signals are strong, but model suitability "
            "has not been established."
        )

    return MLReadiness(
        score=score,
        status=status,
        completeness_score=round(
            completeness_score,
            2,
        ),
        feature_quality_score=round(
            feature_quality_score,
            2,
        ),
        data_stability_score=round(
            data_stability_score,
            2,
        ),
        consistency_score=round(
            consistency_score,
            2,
        ),
        distribution_score=round(
            distribution_score,
            2,
        ),
        target_readiness=target_readiness,
        strengths=strengths,
        weaknesses=weaknesses,
        recommendations=recommendations,
    )