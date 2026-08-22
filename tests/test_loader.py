"""
Tests for Datapilot dataset loading.
"""

from pathlib import Path

import pandas as pd
import pytest

from datapilot.core.loader import load_dataset


def test_load_dataframe_returns_copy() -> None:
    """
    Loading a DataFrame should return an independent copy.
    """
    dataframe = pd.DataFrame(
        {
            "Age": [20, 21],
            "Name": ["A", "B"],
        }
    )

    loaded = load_dataset(dataframe)

    assert loaded.equals(dataframe)
    assert loaded is not dataframe


def test_load_csv_with_missing_markers(
    tmp_path: Path,
) -> None:
    """
    Common textual missing-value markers should become NaN.
    """
    csv_file = tmp_path / "dataset.csv"

    csv_file.write_text(
        "Age,Name,Department\n"
        "20,Alice,IT\n"
        "?,Bob,HR\n"
        "22,Charlie,?\n",
        encoding="utf-8",
    )

    dataframe = load_dataset(csv_file)

    assert dataframe.shape == (3, 3)
    assert pd.isna(dataframe.loc[1, "Age"])
    assert pd.isna(dataframe.loc[2, "Department"])


def test_load_headerless_data_file(
    tmp_path: Path,
) -> None:
    """
    Headerless .data files should not treat the first data row as a header.
    """
    data_file = tmp_path / "dataset.data"

    data_file.write_text(
        "39, State-gov, 77516, Bachelors\n"
        "50, Self-emp-not-inc, 83311, Bachelors\n",
        encoding="utf-8",
    )

    dataframe = load_dataset(data_file)

    assert dataframe.shape == (2, 4)
    assert dataframe.iloc[0, 0] == 39
    assert dataframe.iloc[1, 0] == 50


def test_load_excel_file(
    tmp_path: Path,
) -> None:
    """
    Excel files should be loaded into a DataFrame.
    """
    excel_file = tmp_path / "dataset.xlsx"

    original = pd.DataFrame(
        {
            "Age": [20, 21],
            "Salary": [100, 200],
        }
    )

    original.to_excel(
        excel_file,
        index=False,
    )

    loaded = load_dataset(excel_file)

    assert loaded.equals(original)


def test_unsupported_file_format(
    tmp_path: Path,
) -> None:
    """
    Unsupported file formats should raise a clear error.
    """
    file_path = tmp_path / "dataset.txt"

    file_path.write_text(
        "example",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="Unsupported file format",
    ):
        load_dataset(file_path)

def test_empty_csv_raises_clear_error(
    tmp_path: Path,
) -> None:
    """
    Empty CSV files should raise a clear Datapilot error.
    """
    csv_file = tmp_path / "empty.csv"

    csv_file.write_text(
        "",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="is empty",
    ):
        load_dataset(csv_file)


def test_empty_dataframe_raises_clear_error() -> None:
    """
    Empty DataFrames should raise a clear Datapilot error.
    """
    dataframe = pd.DataFrame()

    with pytest.raises(
        ValueError,
        match="Dataset is empty",
    ):
        load_dataset(dataframe)


def test_missing_file_raises_clear_error(
    tmp_path: Path,
) -> None:
    """
    Missing dataset files should raise a clear error.
    """
    file_path = tmp_path / "missing.csv"

    with pytest.raises(
        FileNotFoundError,
        match="Dataset file not found",
    ):
        load_dataset(file_path)


def test_malformed_csv_raises_clear_error(
    tmp_path: Path,
) -> None:
    """
    Malformed CSV files should raise a clear Datapilot error.
    """
    csv_file = tmp_path / "malformed.csv"

    csv_file.write_text(
        "Age,Name\n"
        "20,Alice\n"
        "21,Bob,Unexpected\n",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="Could not parse dataset file",
    ):
        load_dataset(csv_file)


def test_load_lowercase_none_as_missing(tmp_path: Path) -> None:
    csv_file = tmp_path / 'lowercase_none.csv'
    csv_file.write_text('Age,Name\n20,Alice\nnone,Bob\n', encoding='utf-8')
    dataframe = load_dataset(csv_file)
    assert pd.isna(dataframe.loc[1, 'Age'])
