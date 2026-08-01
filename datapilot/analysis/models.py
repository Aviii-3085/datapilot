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