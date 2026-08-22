from pathlib import Path

import pandas as pd

from datapilot import analyze
from datapilot.reporting.html import generate_html_report


def test_generate_html_report(
    tmp_path: Path,
) -> None:
    dataframe = pd.DataFrame(
        {
            "Age": [20, 21, None, 22],
            "Salary": [100, 200, 300, 300],
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

    print("\n--- HTML REPORT DEBUG ---")
    print("Version present:", "0.3.0" in html)
    print(
        "Duration placeholder present:",
        "{{GENERATION_DURATION}}" in html,
    )

    duration_lines = [
        line.strip()
        for line in html.splitlines()
        if "completed in" in line
    ]

    print("Duration lines:", duration_lines)
    print("--- END HTML REPORT DEBUG ---\n")

    assert "Datapilot Report" in html
    assert "Data Quality Report" in html

    assert "4" in html
    assert "2" in html

    assert "1" in html
    assert "12.5%" in html

    assert "0.3.0" in html

    assert "{{GENERATION_DURATION}}" not in html
    assert "{{DUPLICATE_GROUPS_COUNT}}" not in html
    assert "{{DISTRIBUTION_ANALYSIS_CONTENT}}" not in html
    assert "Missing Values" in html
    assert "Duplicate Rows" in html
    assert "Statistics" in html
    assert "Outlier Analysis" in html
    assert "Correlation Analysis" in html
    assert "Insights" in html
    assert "Recommendations" in html
