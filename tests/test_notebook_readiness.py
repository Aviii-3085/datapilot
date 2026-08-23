"""
Tests for Datapilot v0.4 Notebook Readiness.
"""

import pandas as pd

from datapilot.analysis.models import DatasetSummary
from datapilot.analysis.notebook_readiness import (
    generate_notebook_readiness,
)


def test_notebook_workflow_is_ready_for_non_empty_dataset() -> None:
    dataframe = pd.DataFrame(
        {
            "Age": [20, 21, 22],
            "Salary": [100, 200, 300],
        }
    )

    summary = DatasetSummary(
        rows=len(dataframe),
        columns=len(dataframe.columns),
        memory_usage_mb=0.01,
        column_names=list(dataframe.columns),
    )

    readiness = generate_notebook_readiness(
        summary
    )

    assert readiness.score == 100.0
    assert readiness.status == "Ready"
    assert readiness.workflow == "analyze() -> Report"
    assert readiness.compatibility == (
        "Not individually assessed"
    )


def test_notebook_readiness_does_not_claim_environment_compatibility() -> None:
    summary = DatasetSummary(
        rows=3,
        columns=2,
        memory_usage_mb=0.01,
        column_names=["Age", "Salary"],
    )

    readiness = generate_notebook_readiness(
        summary
    )

    assert "Jupyter Notebook" in (
        readiness.target_environments
    )

    assert "Jupyter-specific integration" in (
        readiness.not_assessed
    )

    assert "Google Colab-specific integration" in (
        readiness.not_assessed
    )

    assert "VS Code Notebook-specific integration" in (
        readiness.not_assessed
    )


def test_empty_dataset_is_not_notebook_ready() -> None:
    summary = DatasetSummary(
        rows=0,
        columns=2,
        memory_usage_mb=0.0,
        column_names=["Age", "Salary"],
    )

    readiness = generate_notebook_readiness(
        summary
    )

    assert readiness.score == 0.0
    assert readiness.status == "Not Ready"