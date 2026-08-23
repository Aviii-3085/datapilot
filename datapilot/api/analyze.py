"""
Public API for Datapilot.
"""

from pathlib import Path
from typing import Any

import pandas as pd

from ..core.loader import load_dataset
from ..core.report import Report


def analyze(data: Any) -> Report:
    """
    Analyze a dataset and return a Report object.
    """

    if isinstance(data, pd.DataFrame):
        dataframe = load_dataset(data)
        return Report(
            dataframe,
            file_format="DataFrame",
        )

    if isinstance(data, (str, Path)):
        path = Path(data)
        suffix = path.suffix.lower()

        format_map = {
            ".csv": "CSV",
            ".data": "DATA",
            ".xlsx": "Excel",
            ".xls": "Excel",
        }

        file_format = format_map.get(
            suffix,
            "Unknown",
        )

        dataframe = load_dataset(path)

        return Report(
            dataframe,
            file_format=file_format,
        )

    dataframe = load_dataset(data)
    return Report(dataframe)