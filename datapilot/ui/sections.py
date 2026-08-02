"""
Reusable rendering sections for Datapilot.
"""

from rich.align import Align
from rich.table import Table
from rich.text import Text

from datapilot.core.report import Report

from .console import console
from .dashboard import render_dashboard
from .panels import title_panel


def render_header() -> None:
    """
    Render the Datapilot header.
    """

    header = Text(justify="center")

    header.append(
        "DATAPILOT\n",
        style="title",
    )

    header.append(
        "Data Quality Assessment & EDA\n",
        style="info",
    )

    header.append(
        "v0.1.0-alpha",
        style="accent",
    )

    console.print(
        title_panel(
            Align.center(header)
        )
    )

    console.print()


def render_summary(report: Report) -> None:
    """
    Render dataset summary.
    """

    summary = report.summary()

    table = Table(
        title="Dataset Overview",
        show_header=False,
        border_style="accent",
        expand=True,
    )

    table.add_column(style="label", width=20)
    table.add_column(style="value")

    table.add_row("Rows", str(summary.rows))
    table.add_row("Columns", str(summary.columns))
    table.add_row(
        "Memory",
        f"{summary.memory_usage_mb:.2f} MB",
    )
    table.add_row(
        "Column Names",
        ", ".join(summary.column_names),
    )

    console.print(table)


def render_health(report: Report) -> None:
    """
    Render the Datapilot dashboard.
    """

    console.print()

    console.print(
        render_dashboard(report)
    )

    console.print()