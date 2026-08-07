import pandas as pd

from datapilot import analyze
from datapilot.reporting.html import (
    generate_html_report,
)

df = pd.read_csv(
    "datasets/missing.csv",
)

report = analyze(df)

generate_html_report(
    report,
    "report.html",
)

print("Report generated.")