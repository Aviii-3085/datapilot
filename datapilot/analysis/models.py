"""
Data models used by Datapilot analysis modules.
"""

from dataclasses import dataclass


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
    Overall health assessment of a dataset.
    """

    score: int
    grade: str
    status: str
    ml_ready: bool
    strengths: list[str]
    weaknesses: list[str]
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