"""
Dataset loading utilities for Datapilot.

This module is responsible for loading supported dataset formats
and converting them into a pandas DataFrame.
"""

from pathlib import Path
from typing import Any

import pandas as pd
from pandas.errors import EmptyDataError, ParserError


CSV_EXTENSIONS = {".csv", ".data"}
EXCEL_EXTENSIONS = {".xlsx", ".xls"}

MISSING_VALUE_MARKERS = [
    "?",
    "NA",
    "N/A",
    "NULL",
    "null",
    "None",
    "none",
    "",
]


def load_dataset(
    data: Any,
) -> pd.DataFrame:
    """
    Load a supported dataset into a pandas DataFrame.
    """

    if isinstance(data, pd.DataFrame):
        return _load_dataframe(data)

    if isinstance(data, (str, Path)):
        return _load_file(Path(data))

    raise TypeError(
        f"Unsupported input type: {type(data).__name__}"
    )


def _load_dataframe(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Return a copy of the provided DataFrame.
    """

    if dataframe.empty:
        raise ValueError(
            "Dataset is empty. "
            "Provide a dataset containing at least one row "
            "and one column."
        )

    return dataframe.copy(deep=True)


def _load_file(
    path: Path,
) -> pd.DataFrame:
    """
    Load a dataset from a supported file.
    """

    if not path.exists():
        raise FileNotFoundError(
            f"Dataset file not found: '{path}'. "
            "Check that the file path is correct."
        )

    if not path.is_file():
        raise ValueError(
            f"Dataset path is not a file: '{path}'."
        )

    suffix = path.suffix.lower()

    if suffix in CSV_EXTENSIONS:
        return _load_csv(path)

    if suffix in EXCEL_EXTENSIONS:
        return _load_excel(path)

    raise ValueError(
        f"Unsupported file format: '{suffix}'. "
        "Supported formats are CSV, DATA, XLSX, and XLS."
    )


def _load_csv(
    path: Path,
) -> pd.DataFrame:
    """
    Load a CSV or headerless DATA file.
    """

    try:
        dataframe = pd.read_csv(
            path,
            header=(
                None
                if path.suffix.lower() == ".data"
                else "infer"
            ),
            na_values=MISSING_VALUE_MARKERS,
            keep_default_na=True,
        )

    except EmptyDataError as exc:
        raise ValueError(
            f"Dataset file '{path.name}' is empty. "
            "Provide a dataset containing data."
        ) from exc

    except ParserError as exc:
        raise ValueError(
            f"Could not parse dataset file '{path.name}'. "
            "Check that the file is a valid CSV/DATA file."
        ) from exc

    if dataframe.empty:
        raise ValueError(
            f"Dataset file '{path.name}' contains no data."
        )

    return dataframe


def _load_excel(
    path: Path,
) -> pd.DataFrame:
    """
    Load an Excel file.
    """

    dataframe = pd.read_excel(path)

    if dataframe.empty:
        raise ValueError(
            f"Dataset file '{path.name}' contains no data."
        )

    return dataframe
