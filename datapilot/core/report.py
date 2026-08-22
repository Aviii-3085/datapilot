"""
Report object for Datapilot.

The Report class is the primary interface returned by the
public `analyze()` function.
"""

import pandas as pd

from ..analysis.correlation import (
    generate_correlation_summary,
)
from ..analysis.datatype import generate_data_type_summary
from ..analysis.duplicate import generate_duplicate_summary
from ..analysis.health import generate_dataset_health
from ..analysis.insights import (
    generate_insight_summary,
)
from ..analysis.missing import generate_missing_value_summary
from ..analysis.models import (
    CorrelationSummary,
    DatasetHealth,
    DatasetSummary,
    DataTypeSummary,
    DuplicateSummary,
    InsightSummary,
    MissingValueSummary,
    OutlierSummary,
    StatisticsSummary,
)
from ..analysis.outliers import generate_outlier_summary
from ..analysis.statistics import generate_statistics_summary
from ..analysis.summary import generate_summary


class Report:
    """
    Represents the analysis results of a dataset.
    """

    def __init__(
        self,
        dataframe: pd.DataFrame,
    ) -> None:
        """
        Initialize a Report object.

        Parameters
        ----------
        dataframe : pandas.DataFrame
            Dataset to analyze.
        """

        self._df = dataframe

        self._summary: DatasetSummary | None = None
        self._missing_values: MissingValueSummary | None = None
        self._duplicates: DuplicateSummary | None = None
        self._data_types: DataTypeSummary | None = None
        self._dataset_health: DatasetHealth | None = None
        self._statistics: StatisticsSummary | None = None
        self._outliers: OutlierSummary | None = None
        self._correlation: CorrelationSummary | None = None
        self._insights: InsightSummary | None = None

    def summary(self) -> DatasetSummary:
        """
        Return a summary of the dataset.
        """

        if self._summary is None:
            self._summary = generate_summary(
                self._df
            )

        return self._summary

    def missing_values(
        self,
    ) -> MissingValueSummary:
        """
        Return missing value statistics for the dataset.
        """

        if self._missing_values is None:
            self._missing_values = (
                generate_missing_value_summary(
                    self._df
                )
            )

        return self._missing_values

    def duplicates(
        self,
    ) -> DuplicateSummary:
        """
        Return duplicate row statistics for the dataset.
        """

        if self._duplicates is None:
            self._duplicates = (
                generate_duplicate_summary(
                    self._df
                )
            )

        return self._duplicates

    def data_types(
        self,
    ) -> DataTypeSummary:
        """
        Return data type statistics for the dataset.
        """

        if self._data_types is None:
            self._data_types = (
                generate_data_type_summary(
                    self._df
                )
            )

        return self._data_types

    def dataset_health(
        self,
    ) -> DatasetHealth:
        """
        Return the overall health assessment of the dataset.
        """

        if self._dataset_health is None:
            self._dataset_health = (
                generate_dataset_health(
                    self._df
                )
            )

        return self._dataset_health

    def statistics(
        self,
    ) -> StatisticsSummary:
        """
        Return statistical summary.
        """

        if self._statistics is None:
            self._statistics = (
                generate_statistics_summary(
                    self._df
                )
            )

        return self._statistics

    def outliers(
        self,
    ) -> OutlierSummary:
        """
        Return outlier statistics.
        """

        if self._outliers is None:
            self._outliers = (
                generate_outlier_summary(
                    self._df
                )
            )

        return self._outliers

    def correlation(
        self,
    ) -> CorrelationSummary:
        """
        Return correlation analysis.
        """

        if self._correlation is None:
            self._correlation = (
                generate_correlation_summary(
                    self._df
                )
            )

        return self._correlation

    def insights(
        self,
    ) -> InsightSummary:
        """
        Return generated dataset insights.
        """

        if self._insights is None:
            self._insights = (
                generate_insight_summary(
                    self._df
                )
            )

        return self._insights