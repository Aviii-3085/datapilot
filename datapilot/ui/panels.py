from rich.console import RenderableType
from rich.panel import Panel


def title_panel(
    content: RenderableType,
) -> Panel:
    """
    Create the standard Datapilot title panel.
    """

    return Panel(
        content,
        expand=True,
        border_style="accent",
    )