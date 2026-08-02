"""
Rich renderer for Datapilot reports.
"""

from datapilot.core.report import Report

from .sections import (
    render_header,
    render_health,
    render_summary,
)


def render_report(report: Report) -> None:
    """
    Render a complete Datapilot report.
    """

    render_header()
    render_health(report)
    render_summary(report)