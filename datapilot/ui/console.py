"""
Shared Rich console for Datapilot.
"""

from rich.console import Console

from .theme import DATAPILOT_THEME

console = Console(
    theme=DATAPILOT_THEME,
    highlight=False,
)