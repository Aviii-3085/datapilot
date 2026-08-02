"""
Reusable Rich tables for Datapilot.
"""

from rich.table import Table


def create_table(title: str | None = None) -> Table:
    """
    Create a standard Datapilot table.
    """

    table = Table(
        title=title,
        show_header=True,
        header_style="heading",
        border_style="accent",
        expand=True,
    )

    return table