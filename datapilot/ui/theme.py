"""
Datapilot Rich theme.
"""

from rich.theme import Theme

DATAPILOT_THEME = Theme(
    {
        "title": "bold cyan",
        "heading": "bold bright_blue",
        "success": "bold green",
        "warning": "bold yellow",
        "error": "bold red",
        "info": "cyan",
        "score": "bold magenta",
        "label": "bold white",
        "value": "bright_white",
        "accent": "bright_cyan",
    }
)