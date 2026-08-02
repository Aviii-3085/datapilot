"""
Tests for duplicate row analysis.
"""

from datapilot.analysis.duplicate import (
    generate_duplicate_summary,
)


def test_generate_duplicate_summary(
    sample_dataframe,
) -> None:
    """
    Test duplicate row summary generation.
    """

    summary = generate_duplicate_summary(
        sample_dataframe
    )

    assert summary.total_duplicates == 1
    assert summary.duplicate_percentage == 25.0