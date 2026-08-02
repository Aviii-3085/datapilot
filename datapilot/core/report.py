"""
Report object for Datapilot.

The Report class is the primary interface returned by the
public `analyze()` function.
"""

import pandas as pd

from ..analysis.datatype import generate_data_type_summary
from ..analysis.duplicate import generate_duplicate_summary
from ..analysis.health import generate_dataset_health
from ..analysis.missing import generate_missing_value_summary
from ..analysis.models import (
    DatasetHealth,
    DatasetSummary,
    DataTypeSummary,
    DuplicateSummary,
    MissingValueSummary,
    StatisticsSummary,
)
from ..analysis.statistics import generate_statistics_summary
from ..analysis.summary import generate_summary


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

    def duplicates(self) -> DuplicateSummary:
        """
        Return duplicate row statistics for the dataset.
        """
        return generate_duplicate_summary(self._df)

    def data_types(self) -> DataTypeSummary:
        """
        Return data type statistics for the dataset.
        """
        return generate_data_type_summary(self._df)

    def dataset_health(self) -> DatasetHealth:
        """
        Return the overall health assessment of the dataset.
        """
        return generate_dataset_health(self._df)
    def statistics(self) -> StatisticsSummary:
       """
       Return statistical summary.
       """

       return generate_statistics_summary(self._df)