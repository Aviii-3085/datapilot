"""
Notebook readiness assessment for Datapilot v0.4.
"""

from .models import DatasetSummary, NotebookReadiness


def generate_notebook_readiness(
    summary: DatasetSummary,
) -> NotebookReadiness:
    """
    Assess whether the current Datapilot workflow is suitable for
    interactive notebook use.

    This assesses Datapilot's public workflow only. It does not claim
    compatibility with a specific notebook application.
    """

    has_dataset = (
        summary.rows > 0
        and summary.columns > 0
    )

    score = 100.0 if has_dataset else 0.0

    status = (
        "Ready"
        if has_dataset
        else "Not Ready"
    )

    return NotebookReadiness(
        score=score,
        status=status,
        workflow="analyze() -> Report",
        target_environments=[
            "Jupyter Notebook",
            "JupyterLab",
            "Google Colab",
            "VS Code Notebooks",
        ],
        compatibility="Not individually assessed",
        assessed=[
            "Datapilot exposes a public analyze() workflow.",
            "The workflow returns a structured Report object.",
            "The workflow accepts a pandas DataFrame.",
        ],
        not_assessed=[
            "Notebook application compatibility",
            "Jupyter-specific integration",
            "Google Colab-specific integration",
            "VS Code Notebook-specific integration",
        ],
        recommendations=[
            "Use the public analyze() API inside a notebook.",
            "Validate the workflow in the target notebook environment "
            "before claiming environment-specific compatibility.",
        ],
    )