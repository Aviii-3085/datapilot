"""
Public API for Datapilot.
"""

from typing import Any

from ..core.loader import load_dataset
from ..core.report import Report


def analyze(data: Any) -> Report:
    """
    Analyze a dataset and return a Report object.
    """
    dataframe = load_dataset(data)
    return Report(dataframe)