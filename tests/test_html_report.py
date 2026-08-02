from pathlib import Path

import pandas as pd

from datapilot import analyze
from datapilot.reporting.html import (
    generate_html_report,
)


def test_generate_html_report(
    tmp_path: Path,
) -> None:
    dataframe = pd.DataFrame(
        {
            "Age": [20, 21, 22],
            "Salary": [100, 200, 300],
        }
    )

    report = analyze(dataframe)

    output_file = (
        tmp_path / "report.html"
    )

    generate_html_report(
        report,
        output_file,
    )

    assert output_file.exists()

    html = output_file.read_text(
        encoding="utf-8",
    )

    assert "Datapilot Report" in html