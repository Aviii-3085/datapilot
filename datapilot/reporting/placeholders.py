"""
Placeholder generation for Datapilot HTML reports.
"""

from datetime import datetime

from datapilot.core.report import Report

from .fragments import (
    build_column_name_chips,
    build_correlation_table,
    build_health_headline,
    build_health_summary,
    build_html_list,
    build_insight_recommendations,
    build_insights,
    build_missing_table,
    build_outlier_cards,
    build_statistics_table,
)

DATAPILOT_VERSION = "0.3.0"


def _severity_class(
    percentage: float,
) -> str:
    """
    Return a visual severity class based on a percentage.

    The class is intended for report presentation only.
    """

    if percentage == 0:
        return "kpi-card--good"

    if percentage <= 5:
        return "kpi-card--warn"

    return "kpi-card--bad"


def build_placeholders(
    report: Report,
) -> dict[str, str]:
    """
    Build placeholder dictionary for the HTML template.
    """

    summary = report.summary()
    health = report.dataset_health()
    missing = report.missing_values()
    duplicates = report.duplicates()

    health_class = (
        "kpi-card--good"
        if health.score >= 90
        else "kpi-card--warn"
        if health.score >= 75
        else "kpi-card--bad"
    )

    missing_class = _severity_class(
        missing.missing_percentage,
    )

    duplicate_class = _severity_class(
        duplicates.duplicate_percentage,
    )

    unique_rows = max(
        summary.rows - duplicates.total_duplicates,
        0,
    )

    missing_columns_affected = len(
        missing.columns_with_missing,
    )

    return {
        "{{DATASET_NAME}}": "Dataset",
        "{{REPORT_GENERATED_AT}}": datetime.now().strftime(
            "%d %b %Y %H:%M",
        ),
        "{{DATAPILOT_VERSION}}": DATAPILOT_VERSION,
        "{{REPORT_SUMMARY}}": (
            "Automated Data Quality Assessment Report"
        ),

        "{{ROWS}}": str(summary.rows),
        "{{COLUMNS}}": str(summary.columns),
        "{{MEMORY_USAGE}}": (
            f"{summary.memory_usage_mb:.2f} MB"
        ),
        "{{FILE_FORMAT}}": "CSV",

        "{{COLUMN_NAME_CHIPS}}": (
            build_column_name_chips(report)
        ),

        "{{HEALTH_SCORE}}": str(health.score),
        "{{GRADE}}": health.grade,
        "{{HEALTH_STATUS}}": health.status,

        "{{HEALTH_HEADLINE}}": (
            build_health_headline(report)
        ),
        "{{HEALTH_SUMMARY}}": (
            build_health_summary(report)
        ),

        "{{STRENGTHS_LIST}}": (
            build_html_list(
                health.strengths,
            )
        ),
        "{{WEAKNESSES_LIST}}": (
            build_html_list(
                health.weaknesses,
            )
        ),
        "{{RECOMMENDATIONS_LIST}}": (
            build_html_list(
                health.recommendations,
            )
        ),

        "{{HEALTH_SCORE_SEVERITY_CLASS}}": health_class,
        "{{HEALTH_SCORE_SEVERITY_CLASS_GAUGE}}": health_class,

        "{{MISSING_VALUES_COUNT}}": str(
            missing.total_missing,
        ),
        "{{MISSING_VALUES_PERCENT}}": (
            f"{missing.missing_percentage:.1f}"
        ),
        "{{MISSING_VALUES_SEVERITY_CLASS}}": (
            missing_class
        ),
        "{{MISSING_COLUMNS_AFFECTED}}": str(
            missing_columns_affected,
        ),

        "{{MISSING_TABLE}}": (
            build_missing_table(report)
        ),

        "{{STATISTICS_TABLE}}": (
            build_statistics_table(report)
        ),

        "{{OUTLIER_CARDS}}": (
            build_outlier_cards(report)
        ),

        "{{CORRELATION_TABLE}}": (
            build_correlation_table(report)
        ),

        "{{INSIGHTS}}": (
            build_insights(report)
        ),

        "{{RECOMMENDATIONS}}": (
            build_insight_recommendations(report)
        ),

        "{{DUPLICATE_ROWS_COUNT}}": str(
            duplicates.total_duplicates,
        ),
        "{{DUPLICATE_ROWS_PERCENT}}": (
            f"{duplicates.duplicate_percentage:.1f}"
        ),
        "{{DUPLICATE_ROWS_SEVERITY_CLASS}}": (
            duplicate_class
        ),
        "{{UNIQUE_ROWS_COUNT}}": str(
            unique_rows,
        ),
    }