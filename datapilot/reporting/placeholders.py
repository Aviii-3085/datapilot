"""
Placeholder generation for Datapilot HTML reports.
"""

from datetime import datetime

from datapilot.core.report import Report

DATAPILOT_VERSION = "0.2.0"


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

        "{{HEALTH_SCORE}}": str(health.score),
        "{{GRADE}}": health.grade,
        "{{HEALTH_STATUS}}": health.status,

        "{{HEALTH_SCORE_SEVERITY_CLASS}}": health_class,
        "{{HEALTH_SCORE_SEVERITY_CLASS_GAUGE}}": health_class,

        "{{MISSING_VALUES_COUNT}}": str(
            missing.total_missing,
        ),
        "{{MISSING_VALUES_PERCENT}}": (
            f"{missing.missing_percentage:.1f}"
        ),

        "{{DUPLICATE_ROWS_COUNT}}": str(
            duplicates.total_duplicates,
        ),
        "{{DUPLICATE_ROWS_PERCENT}}": (
            f"{duplicates.duplicate_percentage:.1f}"
        ),
    }