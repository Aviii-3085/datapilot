"""
HTML report generation for Datapilot.
"""

import shutil
from pathlib import Path

from datapilot.core.report import Report

from .renderer import HTMLRenderer


def generate_html_report(
    report: Report,
    output_path: str | Path,
) -> None:
    """
    Generate a Datapilot HTML report.
    """

    output_path = Path(output_path)

    project_root = (
        Path(__file__).parent.parent
    )

    template = (
        project_root
        / "templates"
        / "report.html"
    )

    css_source = (
        project_root
        / "assets"
        / "style.css"
    )

    renderer = HTMLRenderer(
        template_path=template,
    )

    renderer.render(
        report=report,
        output_path=output_path,
    )

    shutil.copy2(
        css_source,
        output_path.parent / "style.css",
    )