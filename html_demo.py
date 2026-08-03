import pandas as pd

from datapilot import analyze
from datapilot.reporting.html import (
    generate_html_report,
)

dataframe = pd.DataFrame(
    {
        "Age": [20, 21, 22, 23],
        "Salary": [100, 200, 300, 400],
        "Department": [
            "IT",
            "HR",
            "IT",
            "Finance",
        ],
    }
)

report = analyze(dataframe)

generate_html_report(
    report,
    "report.html",
)

print("HTML report generated successfully!")