"""
Reusable cards for Datapilot.
"""

from rich.align import Align
from rich.console import Group
from rich.panel import Panel
from rich.progress_bar import ProgressBar
from rich.text import Text


def metric_card(
    title: str,
    value: str,
    subtitle: str = "",
    border_style: str = "accent",
) -> Panel:
    """
    Create a reusable metric card.
    """

    body = Text(justify="center")

    body.append(f"{title}\n\n", style="heading")
    body.append(f"{value}\n", style="score")

    if subtitle:
        body.append(subtitle, style="info")

    return Panel(
        Align.center(body),
        border_style=border_style,
        expand=True,
    )


def hero_card(
    title: str,
    value: str,
    subtitle: str,
    score: int,
    border_style: str = "green",
) -> Panel:
    """
    Create the Datapilot hero card.
    """

    body = Text(justify="center")

    body.append(f"{title}\n\n", style="heading")
    body.append(f"{value}\n", style="score")
    body.append(f"{subtitle}\n\n", style="accent")

    progress = ProgressBar(
        total=100,
        completed=score,
        width=40,
    )

    return Panel(
        Align.center(
            Group(
                body,
                progress,
            )
        ),
        border_style=border_style,
        expand=True,
        padding=(1, 2),
    )