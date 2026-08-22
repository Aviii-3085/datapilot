"""
HTML renderer for Datapilot reports.
"""

from pathlib import Path
from time import perf_counter

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

        start_time = perf_counter()

        template = self._template_path.read_text(
            encoding="utf-8",
        )

        replacements = build_placeholders(
            report,
        )

        generation_duration = (
            perf_counter() - start_time
        )

        replacements["{{GENERATION_DURATION}}"] = (
            f"{generation_duration:.3f} seconds"
        )

        html = template

        for placeholder, value in replacements.items():
            html = html.replace(
                placeholder,
                value,
            )

        output_path = Path(output_path)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_path.write_text(
            html,
            encoding="utf-8",
        )