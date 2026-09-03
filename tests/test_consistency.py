import pandas as pd

from datapilot.analysis.consistency import generate_consistency_summary


def test_consistent_columns_are_not_flagged():
    dataframe = pd.DataFrame(
        {
            "age": [20, 21, 22, 23],
            "name": ["A", "B", "C", "D"],
        }
    )

    result = generate_consistency_summary(dataframe)

    assert result.inconsistent_columns == []
    assert result.inconsistent_value_count == 0
    assert result.consistency_percentage == 0.0


def test_mixed_types_are_detected():
    dataframe = pd.DataFrame(
        {
            "age": [20, 21, "22", 23],
        }
    )

    result = generate_consistency_summary(dataframe)

    assert result.inconsistent_columns == ["age"]
    assert result.inconsistent_value_count == 1
    assert result.consistency_percentage == 25.0


def test_missing_values_are_excluded():
    dataframe = pd.DataFrame(
        {
            "age": [20, 21, None, 23],
        }
    )

    result = generate_consistency_summary(dataframe)

    assert result.inconsistent_columns == []
    assert result.inconsistent_value_count == 0
    assert result.consistency_percentage == 0.0


def test_empty_dataframe():
    dataframe = pd.DataFrame()

    result = generate_consistency_summary(dataframe)

    assert result.inconsistent_columns == []
    assert result.inconsistent_value_count == 0
    assert result.consistency_percentage == 0.0
