"""
Data models used by Datapilot analysis modules.
"""

from dataclasses import dataclass

import pandas as pd


@dataclass(slots=True)
class DatasetSummary:
    """
    Summary information about a dataset.
    """

    rows: int
    columns: int
    memory_usage_mb: float
    column_names: list[str]


@dataclass(slots=True)
class MissingValueSummary:
    """
    Summary information about missing values in a dataset.
    """

    total_missing: int
    missing_percentage: float
    columns_with_missing: dict[str, int]
    columns_without_missing: list[str]


@dataclass(slots=True)
class DuplicateSummary:
    """
    Summary information about duplicate rows in a dataset.
    """

    total_duplicates: int
    duplicate_percentage: float


@dataclass(slots=True)
class DataTypeSummary:
    """
    Summary information about dataset column types.
    """

    numeric_columns: list[str]
    categorical_columns: list[str]
    boolean_columns: list[str]
    datetime_columns: list[str]


@dataclass(slots=True)
class DatasetHealth:
    """
    Overall Dataset Health assessment.
    """

    score: float
    grade: str
    status: str
    completeness_score: float
    duplicate_score: float
    structure_score: float
    consistency_score: float
    strengths: list[str]
    weaknesses: list[str]
    recommendations: list[str]

@dataclass(slots=True)
class MLReadiness:
    """
    Observable machine-learning readiness assessment.

    A score represents preparation signals only. It does not
    guarantee that a successful ML model can be trained.
    """

    score: float | None
    assessment_coverage: float
    status: str
    completeness_score: float
    feature_quality_score: float
    data_stability_score: float
    consistency_score: float
    distribution_score: float
    target_readiness: str
    strengths: list[str]
    weaknesses: list[str]
    recommendations: list[str]

@dataclass(slots=True)
class NotebookReadiness:
    """
    Observable readiness assessment for notebook workflows.
    """

    score: float
    status: str
    workflow: str
    target_environments: list[str]
    compatibility: str
    assessed: list[str]
    not_assessed: list[str]
    recommendations: list[str]

@dataclass(slots=True)
class StatisticsSummary:
    """
    Statistical summary of numeric columns.
    """

    column_statistics: dict[str, dict[str, float]]


@dataclass(slots=True)
class OutlierSummary:
    """
    Summary of outlier detection.
    """

    total_outliers: int
    outlier_percentage: float
    columns_with_outliers: dict[str, int]
    columns_without_outliers: list[str]

@dataclass(slots=True)
class DataIntegritySummary:
    """
    Summary of observable data-integrity signals.

    Signals indicate conditions that may deserve review.
    They do not establish factual invalidity.
    """

    missing_value_columns: list[str]
    duplicate_rows: int
    outlier_columns: list[str]
    identifier_like_columns: list[str]
    constant_columns: list[str]
    empty_columns: list[str]
    structural_signals: list[str]

@dataclass(slots=True)
class CorrelationSummary:
    """
    Summary of correlation analysis.
    """

    correlation_matrix: pd.DataFrame
    strong_positive_pairs: dict[str, float]
    strong_negative_pairs: dict[str, float]


@dataclass(slots=True)
class InsightSummary:
    """
    Summary of generated dataset insights.
    """

    insights: list[str]
    recommendations: list[str]