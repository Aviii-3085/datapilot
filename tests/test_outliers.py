import pandas as pd

from datapilot.analysis.outliers import (
    generate_outlier_summary,
)


def test_generate_outlier_summary() -> None:

    dataframe = pd.DataFrame(
        {
            "Age": [
                20,
                21,
                22,
                23,
                24,
                150,
            ],
            "Salary": [
                10,
                20,
                30,
                40,
                50,
                60,
            ],
        }
    )

    summary = generate_outlier_summary(
        dataframe
    )

    assert summary.total_outliers == 1

    assert (
        summary.columns_with_outliers["Age"]
        == 1
    )

    assert "Salary" in (
        summary.columns_without_outliers
    )