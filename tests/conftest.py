"""
Shared test fixtures for Datapilot.
"""

import pandas as pd
import pytest


@pytest.fixture
def sample_dataframe() -> pd.DataFrame:
    """
    Return a sample DataFrame for testing.
    """

    return pd.DataFrame(
        {
            "Age": [21, None, 23, 21],
            "Salary": [40000, None, 50000, 40000],
            "Department": ["IT", "HR", None, "IT"],
            "Is_Manager": [True, False, False, True],
            "Joining_Date": pd.to_datetime(
                [
                    "2023-01-01",
                    "2023-02-15",
                    "2023-03-10",
                    "2023-01-01",
                ]
            ),
        }
    )