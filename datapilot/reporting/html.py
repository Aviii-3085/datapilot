"""
HTML report generation for Datapilot.
"""

from pathlib import Path

from datapilot.core.report import Report


def generate_html_report(
    report: Report,
    output_path: str | Path,
) -> None:
    """
    Generate an HTML report.
    """

    summary = report.summary()
    health = report.dataset_health()
    missing = report.missing_values()
    duplicates = report.duplicates()
    insights = report.insights()

    html = f"""<!DOCTYPE html>
<html lang="en">

<head>
<meta charset="UTF-8">
<title>Datapilot Report</title>

<style>

body {{
    font-family: Arial, Helvetica, sans-serif;
    margin: 40px;
    background: #f6f8fa;
}}

.container {{
    max-width: 1000px;
    margin: auto;
}}

.card {{
    background: white;
    padding: 20px;
    margin-bottom: 20px;
    border-radius: 10px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.08);
}}

h1 {{
    color: #2563eb;
}}

table {{
    width: 100%;
    border-collapse: collapse;
}}

th,
td {{
    padding: 10px;
    border-bottom: 1px solid #ddd;
    text-align: left;
}}

ul {{
    margin: 0;
}}

</style>

</head>

<body>

<div class="container">

<h1>Datapilot Report</h1>

<div class="card">
<h2>Dataset Summary</h2>

<table>

<tr>
<td>Rows</td>
<td>{summary.rows}</td>
</tr>

<tr>
<td>Columns</td>
<td>{summary.columns}</td>
</tr>

<tr>
<td>Memory Usage</td>
<td>{summary.memory_usage_mb:.2f} MB</td>
</tr>

</table>

</div>

<div class="card">

<h2>Dataset Health</h2>

<p><strong>Score:</strong> {health.score}/100</p>

<p><strong>Grade:</strong> {health.grade}</p>

<p><strong>Status:</strong> {health.status}</p>

</div>

<div class="card">

<h2>Missing Values</h2>

<p>Total Missing: {missing.total_missing}</p>

<p>Missing Percentage: {missing.missing_percentage:.2f}%</p>

</div>

<div class="card">

<h2>Duplicate Rows</h2>

<p>Total Duplicates: {duplicates.total_duplicates}</p>

</div>

<div class="card">

<h2>Insights</h2>

<ul>

{''.join(f'<li>{item}</li>' for item in insights.insights)}

</ul>

</div>

</div>

</body>

</html>
"""

    Path(output_path).write_text(
        html,
        encoding="utf-8",
    )