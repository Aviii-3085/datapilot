"""
Report object for Datapilot.

The Report class is the primary interface returned by the
public `analyze()` function.
"""

import pandas as pd

from ..analysis.models import DatasetSummary, MissingValueSummary
from ..analysis.summary import generate_summary
from ..analysis.missing import generate_missing_value_summary


class Report:
    """
    Represents the analysis results of a dataset.
    """

    def __init__(self, dataframe: pd.DataFrame) -> None:
        """
        Initialize a Report object.

        Parameters
        ----------
        dataframe : pandas.DataFrame
            Dataset to analyze.
        """
        self._df = dataframe

    def summary(self) -> DatasetSummary:
        """
        Return a summary of the dataset.
        """
        return generate_summary(self._df)

    def missing_values(self) -> MissingValueSummary:
        """
        Return missing value statistics for the dataset.
        """
        return generate_missing_value_summary(self._df)