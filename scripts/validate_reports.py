"""
Generate HTML reports for all validation datasets.
"""

from pathlib import Path

import pandas as pd

from datapilot import analyze
from datapilot.reporting.html import (
    generate_html_report,
)

PROJECT_ROOT = Path(__file__).parent.parent

DATASETS_DIR = PROJECT_ROOT / "datasets"

REPORTS_DIR = PROJECT_ROOT / "reports"

REPORTS_DIR.mkdir(exist_ok=True)


for dataset in sorted(
    DATASETS_DIR.glob("*.csv")
):
    dataframe = pd.read_csv(dataset)

    report = analyze(dataframe)

    output_file = (
        REPORTS_DIR
        / f"{dataset.stem}.html"
    )

    generate_html_report(
        report,
        output_file,
    )

    print(
        f"Generated {output_file.name}"
    )

print()

print(
    f"Generated {len(list(DATASETS_DIR.glob('*.csv')))} reports."
)