"""
Dataset health assessment for Datapilot.
"""

import pandas as pd

from .datatype import generate_data_type_summary
from .duplicate import generate_duplicate_summary
from .missing import generate_missing_value_summary
from .models import DatasetHealth


def generate_dataset_health(
    dataframe: pd.DataFrame,
) -> DatasetHealth:
    """
    Generate an overall health assessment for a dataset.
    """

    missing = generate_missing_value_summary(dataframe)
    duplicates = generate_duplicate_summary(dataframe)
    data_types = generate_data_type_summary(dataframe)

    score = 100.0

    # -----------------------------
    # Missing Value Penalty (40 pts)
    # -----------------------------
    score -= (missing.missing_percentage / 100) * 40

    # -----------------------------
    # Duplicate Penalty (35 pts)
    # -----------------------------
    score -= (duplicates.duplicate_percentage / 100) * 35

    # -----------------------------
    # Structure Penalty (25 pts)
    # -----------------------------
    total_columns = len(dataframe.columns)

    recognized_columns = (
        len(data_types.numeric_columns)
        + len(data_types.categorical_columns)
        + len(data_types.boolean_columns)
        + len(data_types.datetime_columns)
    )

    unrecognized_columns = max(
        total_columns - recognized_columns,
        0,
    )

    if total_columns > 0:
        score -= (
            unrecognized_columns / total_columns
        ) * 25

    score = max(0, min(100, round(score)))

    # -----------------------------
    # Grade
    # -----------------------------
    if score >= 95:
        grade = "A+"
        status = "Excellent"

    elif score >= 90:
        grade = "A"
        status = "Healthy"

    elif score >= 80:
        grade = "B"
        status = "Good"

    elif score >= 70:
        grade = "C"
        status = "Fair"

    elif score >= 60:
        grade = "D"
        status = "Poor"

    else:
        grade = "F"
        status = "Critical"

    # -----------------------------
    # ML Readiness
    # -----------------------------
    ml_ready = (
        score >= 85
        and missing.missing_percentage <= 20
        and duplicates.duplicate_percentage <= 5
    )

    # -----------------------------
    # Strengths
    # -----------------------------
    strengths = []

    if missing.total_missing == 0:
        strengths.append("No missing values detected.")

    if duplicates.total_duplicates == 0:
        strengths.append("No duplicate rows detected.")

    if unrecognized_columns == 0:
        strengths.append("All columns have recognized data types.")

    # -----------------------------
    # Weaknesses
    # -----------------------------
    weaknesses = []

    if missing.total_missing > 0:
        weaknesses.append(
            f"{missing.total_missing} missing values detected."
        )

    if duplicates.total_duplicates > 0:
        weaknesses.append(
            f"{duplicates.total_duplicates} duplicate rows detected."
        )

    if unrecognized_columns > 0:
        weaknesses.append(
            f"{unrecognized_columns} columns have unsupported data types."
        )

    # -----------------------------
    # Recommendations
    # -----------------------------
    recommendations = []

    if missing.missing_percentage > 0:
        recommendations.append(
            "Handle missing values before further analysis."
        )

    if duplicates.total_duplicates > 0:
        recommendations.append(
            "Remove duplicate rows."
        )

    if unrecognized_columns > 0:
        recommendations.append(
            "Review unsupported column data types."
        )

    if not recommendations:
        recommendations.append(
            "Dataset is ready for analysis."
        )

    return DatasetHealth(
        score=score,
        grade=grade,
        status=status,
        ml_ready=ml_ready,
        strengths=strengths,
        weaknesses=weaknesses,
        recommendations=recommendations,
    )