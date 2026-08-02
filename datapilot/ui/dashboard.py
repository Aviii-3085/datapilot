"""
Dashboard layout for Datapilot.
"""

from rich.columns import Columns
from rich.console import Group

from datapilot.core.report import Report

from .cards import hero_card, metric_card


def _health_color(score: int) -> str:
    """
    Return a border color based on dataset health.
    """

    if score >= 90:
        return "green"

    if score >= 75:
        return "yellow"

    return "red"


def render_dashboard(report: Report) -> Group:
    """
    Render the Datapilot dashboard.
    """

    health = report.dataset_health()
    missing = report.missing_values()
    duplicates = report.duplicates()

    hero = hero_card(
        title="DATASET HEALTH",
        value=f"{health.score}/100",
        subtitle=f"Grade {health.grade} • {health.status}",
        score=health.score,
        border_style=_health_color(health.score),
    )

    cards = [
        metric_card(
            title="Missing",
            value=f"{missing.missing_percentage:.1f}%",
            subtitle=f"{missing.total_missing} values",
            border_style=(
                "green"
                if missing.missing_percentage == 0
                else "yellow"
                if missing.missing_percentage <= 10
                else "red"
            ),
        ),
        metric_card(
            title="Duplicates",
            value=f"{duplicates.duplicate_percentage:.1f}%",
            subtitle=f"{duplicates.total_duplicates} rows",
            border_style=(
                "green"
                if duplicates.total_duplicates == 0
                else "yellow"
                if duplicates.duplicate_percentage <= 5
                else "red"
            ),
        ),
        metric_card(
            title="ML Ready",
            value="YES" if health.ml_ready else "NO",
            subtitle="Training Status",
            border_style=(
                "green"
                if health.ml_ready
                else "red"
            ),
        ),
    ]

    metrics = Columns(
        cards,
        equal=True,
        expand=True,
    )

    return Group(
        hero,
        metrics,
    )