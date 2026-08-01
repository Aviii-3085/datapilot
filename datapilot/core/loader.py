"""
Dataset loading utilities for Datapilot.

This module is responsible for loading supported dataset formats
and converting them into a pandas DataFrame.
"""

from pathlib import Path
from typing import Any

import pandas as pd

CSV_EXTENSIONS = {".csv"}
EXCEL_EXTENSIONS = {".xlsx", ".xls"}


def load_dataset(data: Any) -> pd.DataFrame:
    """
    Load a supported dataset into a pandas DataFrame.

    Parameters
    ----------
    data : Any
        A pandas DataFrame or a supported file path.

    Returns
    -------
    pandas.DataFrame
        The loaded dataset.

    Raises
    ------
    TypeError
        If the input type is unsupported.
    ValueError
        If the file extension is unsupported.
    """

    if isinstance(data, pd.DataFrame):
        return _load_dataframe(data)

    if isinstance(data, (str, Path)):
        return _load_file(Path(data))

    raise TypeError(
        f"Unsupported input type: {type(data).__name__}"
    )


def _load_dataframe(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Return a copy of the provided DataFrame.
    """

    return dataframe.copy()


def _load_file(path: Path) -> pd.DataFrame:
    """
    Load a dataset from a supported file.
    """

    suffix = path.suffix.lower()

    if suffix in CSV_EXTENSIONS:
        return _load_csv(path)

    if suffix in EXCEL_EXTENSIONS:
        return _load_excel(path)

    raise ValueError(
        f"Unsupported file format: '{suffix}'"
    )


def _load_csv(path: Path) -> pd.DataFrame:
    """
    Load a CSV file.
    """

    return pd.read_csv(path)


def _load_excel(path: Path) -> pd.DataFrame:
    """
    Load an Excel file.
    """

    return pd.read_excel(path)