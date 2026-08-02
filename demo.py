"""
Datapilot demonstration script.
"""

import pandas as pd

from datapilot import analyze
from datapilot.ui.renderer import render_report


def main() -> None:
    """
    Run a Datapilot demonstration.
    """

    dataframe = pd.DataFrame(
        {
            "Age": [21, None, 24, 21],
            "Salary": [50000, 60000, None, 50000],
            "Department": [
                "IT",
                None,
                "HR",
                "IT",
            ],
            "Is_Manager": [
                True,
                False,
                False,
                True,
            ],
            "Joining_Date": pd.to_datetime(
                [
                    "2024-01-01",
                    "2024-02-15",
                    "2024-03-20",
                    "2024-01-01",
                ]
            ),
        }
    )

    report = analyze(dataframe)

    render_report(report)
if __name__ == "__main__":
    main()