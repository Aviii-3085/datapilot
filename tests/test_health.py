"""
Tests for dataset health assessment.
"""

from datapilot.analysis.health import (
    generate_dataset_health,
)


def test_generate_dataset_health(
    sample_dataframe,
) -> None:
    """
    Test dataset health assessment.
    """

    health = generate_dataset_health(
        sample_dataframe
    )

    assert health.score == 85
    assert health.grade == "B"
    assert health.status == "Good"
    assert health.ml_ready is False

    assert health.strengths == [
        "All columns have recognized data types."
    ]

    assert health.weaknesses == [
        "3 missing values detected.",
        "1 duplicate rows detected.",
    ]

    assert health.recommendations == [
        "Handle missing values before further analysis.",
        "Remove duplicate rows.",
    ]