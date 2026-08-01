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