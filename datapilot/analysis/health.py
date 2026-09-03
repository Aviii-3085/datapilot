"""
Dataset health assessment for Datapilot v0.4.
"""

import pandas as pd

from .datatype import generate_data_type_summary
from .consistency import generate_consistency_summary
from .duplicate import generate_duplicate_summary
from .missing import generate_missing_value_summary
from .models import DatasetHealth
from .scoring import degradation_score


def _grade_and_status(score: float) -> tuple[str, str]:
    """Return the qualitative grade and status for a health score."""
    if score >= 90:
        return "A", "Excellent"

    if score >= 75:
        return "B", "Good"

    if score >= 60:
        return "C", "Moderate"

    if score >= 40:
        return "D", "Needs Attention"

    return "F", "Poor"


def generate_dataset_health(
    dataframe: pd.DataFrame,
) -> DatasetHealth:
    """
    Generate the v0.4 Dataset Health assessment.

    Dataset Health consists of:

    - Completeness: 30%
    - Duplicates: 20%
    - Structure: 25%
    - Consistency: 25%

    Only objectively measurable signals are used.
    """

    missing = generate_missing_value_summary(dataframe)
    duplicates = generate_duplicate_summary(dataframe)
    data_types = generate_data_type_summary(dataframe)
    consistency = generate_consistency_summary(dataframe)

    # ------------------------------------------------------------------
    # Completeness
    # ------------------------------------------------------------------

    completeness_score = degradation_score(
       missing.missing_percentage,
    )

    # ------------------------------------------------------------------
    # Duplicates
    # ------------------------------------------------------------------

    duplicate_score = degradation_score(
        duplicates.duplicate_percentage,
   )

    # ------------------------------------------------------------------
    # Structure
    # ------------------------------------------------------------------

    total_columns = len(dataframe.columns)

    recognized_columns = (
        len(data_types.numeric_columns)
        + len(data_types.categorical_columns)
        + len(data_types.boolean_columns)
        + len(data_types.datetime_columns)
    )

    recognized_columns = min(
        recognized_columns,
        total_columns,
    )

    if total_columns == 0:
        type_recognition_score = 0.0
        empty_column_score = 0.0
        constant_column_score = 0.0
    else:
        type_recognition_score = (
            recognized_columns / total_columns
        ) * 100.0

        empty_columns = int(
            dataframe.isna().all(axis=0).sum()
        )

        empty_column_rate = (
            empty_columns / total_columns
        ) * 100.0

        empty_column_score = (
            100.0 - empty_column_rate
        )

        constant_columns = 0

        for column in dataframe.columns:
            if dataframe[column].nunique(
                dropna=False
            ) <= 1:
                constant_columns += 1

        constant_column_rate = (
            constant_columns / total_columns
        ) * 100.0

        constant_column_score = (
            100.0 - constant_column_rate
        )

    structure_score = (
        type_recognition_score * 0.50
        + empty_column_score * 0.25
        + constant_column_score * 0.25
    )

    structure_score = max(
        0.0,
        min(100.0, structure_score),
    )

    # ------------------------------------------------------------------
    # Consistency
    # ------------------------------------------------------------------

    consistency_score = degradation_score(
        consistency.consistency_percentage,
    )

    # ------------------------------------------------------------------
    # Overall score
    # ------------------------------------------------------------------

    score = (
        completeness_score * 0.30
        + duplicate_score * 0.20
        + structure_score * 0.25
        + consistency_score * 0.25
    )

    score = max(
        0.0,
        min(100.0, score),
    )

    score = round(score, 2)

    grade, status = _grade_and_status(score)

    # ------------------------------------------------------------------
    # Strengths
    # ------------------------------------------------------------------

    strengths: list[str] = []

    if missing.total_missing == 0:
        strengths.append(
            "No missing values detected."
        )

    if duplicates.total_duplicates == 0:
        strengths.append(
            "No duplicate rows detected."
        )

    if not consistency.inconsistent_columns:
        strengths.append(
            "No mixed underlying value types detected."
        )

    if recognized_columns == total_columns:
        strengths.append(
            "All columns have recognized data types."
        )

    if total_columns > 0:
        empty_columns = int(
            dataframe.isna().all(axis=0).sum()
        )

        if empty_columns == 0:
            strengths.append(
                "No completely empty columns detected."
            )

    # ------------------------------------------------------------------
    # Weaknesses
    # ------------------------------------------------------------------

    weaknesses: list[str] = []

    if missing.total_missing > 0:
        weaknesses.append(
            f"{missing.total_missing} missing values detected."
        )

    if duplicates.total_duplicates > 0:
        weaknesses.append(
            f"{duplicates.total_duplicates} duplicate rows detected."
        )

    unrecognized_columns = max(
        total_columns - recognized_columns,
        0,
    )

    if consistency.inconsistent_columns:
        weaknesses.append(
            f"{len(consistency.inconsistent_columns)} columns contain mixed underlying value types."
        )

    if unrecognized_columns > 0:
        weaknesses.append(
            f"{unrecognized_columns} columns have unsupported "
            "data types."
        )

    if total_columns > 0:
        empty_columns = int(
            dataframe.isna().all(axis=0).sum()
        )

        if empty_columns > 0:
            weaknesses.append(
                f"{empty_columns} completely empty columns detected."
            )

    # ------------------------------------------------------------------
    # Recommendations
    # ------------------------------------------------------------------

    recommendations: list[str] = []

    if missing.missing_percentage > 0:
        recommendations.append(
            "Review missing values before further analysis."
        )

    if duplicates.total_duplicates > 0:
        recommendations.append(
            "Review duplicate rows before modelling or aggregation."
        )

    if unrecognized_columns > 0:
        recommendations.append(
            "Review unsupported column data types."
        )

    if consistency.inconsistent_columns:
        recommendations.append(
            "Review columns containing mixed underlying value types."
        )

    if not recommendations:
        recommendations.append(
            "No major structural data-quality issues detected."
        )

    return DatasetHealth(
        score=score,
        grade=grade,
        status=status,
        completeness_score=round(
            completeness_score,
            2,
        ),
        duplicate_score=round(
            duplicate_score,
            2,
        ),
        structure_score=round(
            structure_score,
            2,
        ),
        consistency_score=round(
            consistency_score,
            2,
        ),
        strengths=strengths,
        weaknesses=weaknesses,
        recommendations=recommendations,
    )
