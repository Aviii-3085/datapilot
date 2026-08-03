"""
HTML renderer for Datapilot reports.
"""

from pathlib import Path

from datapilot.core.report import Report

from .placeholders import build_placeholders


class HTMLRenderer:
    """
    Render Datapilot reports using HTML templates.
    """

    def __init__(
        self,
        template_path: str | Path,
    ) -> None:
        """
        Initialize the renderer.
        """

        self._template_path = Path(
            template_path,
        )

    def render(
        self,
        report: Report,
        output_path: str | Path,
    ) -> None:
        """
        Render the HTML report.
        """

        template = self._template_path.read_text(
            encoding="utf-8",
        )

        replacements = build_placeholders(
            report,
        )

        html = template

        for placeholder, value in replacements.items():
            html = html.replace(
                placeholder,
                value,
            )

        Path(output_path).write_text(
            html,
            encoding="utf-8",
        )