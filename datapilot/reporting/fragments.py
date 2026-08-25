"""
HTML fragment builders for Datapilot reports.
"""

from datapilot.core.report import Report


def build_column_name_chips(
    report: Report,
) -> str:
    """
    Build HTML chips for dataset column names.
    """

    summary = report.summary()

    chips: list[str] = []

    for column in summary.column_names:
        chips.append(
            (
                '<span class="column-chip">'
                f"{column}"
                "</span>"
            )
        )

    return "\n".join(chips)


def build_health_headline(
    report: Report,
) -> str:
    """
    Build health headline.
    """

    health = report.dataset_health()

    return (
        f"Overall dataset quality is "
        f"{health.status.lower()}."
    )


def build_health_summary(
    report: Report,
) -> str:
    """
    Build health summary.
    """

    health = report.dataset_health()

    return (
        f"The dataset received a score of "
        f"{health.score}/100 with grade "
        f"{health.grade}."
    )


def build_html_list(
    items: list[str],
) -> str:
    """
    Convert a list of strings into HTML list items.
    """

    if not items:
        return "<li>None</li>"

    return "\n".join(
        f"<li>{item}</li>"
        for item in items
    )


def build_missing_table(
    report: Report,
) -> str:
    """
    Build missing values table.
    """

    missing = report.missing_values()

    rows: list[str] = []

    if not missing.columns_with_missing:
        return (
            "<p>No missing values were detected.</p>"
        )

    rows.append(
        """
<table class="report-table">
    <thead>
        <tr>
            <th>Column</th>
            <th>Missing Values</th>
        </tr>
    </thead>
    <tbody>
"""
    )

    for column, count in (
        missing.columns_with_missing.items()
    ):
        rows.append(
            f"""
<tr>
    <td>{column}</td>
    <td>{count}</td>
</tr>
"""
        )

    rows.append(
        """
    </tbody>
</table>
"""
    )

    return "\n".join(rows)

def build_statistics_table(
    report: Report,
) -> str:
    """
    Build statistics table.
    """

    statistics = report.statistics()

    rows: list[str] = []

    if not statistics.column_statistics:
        return (
            "<p>No numeric columns were detected.</p>"
        )

    rows.append(
        """
<table class="report-table">
    <thead>
        <tr>
            <th>Column</th>
            <th>Mean</th>
            <th>Median</th>
            <th>Std</th>
            <th>Min</th>
            <th>Max</th>
        </tr>
    </thead>
    <tbody>
"""
    )

    for (
        column,
        values,
    ) in statistics.column_statistics.items():
        rows.append(
            f"""
<tr>
    <td>{column}</td>
    <td>{values["mean"]:.2f}</td>
    <td>{values["median"]:.2f}</td>
    <td>{values["std"]:.2f}</td>
    <td>{values["min"]:.2f}</td>
    <td>{values["max"]:.2f}</td>
</tr>
"""
        )

    rows.append(
        """
    </tbody>
</table>
"""
    )

    return "\n".join(rows)

def build_outlier_cards(
    report: Report,
) -> str:
    """
    Build HTML cards for outlier analysis.
    """

    outliers = report.outliers()

    if not outliers.columns_with_outliers:
        return (
            "<p>No outliers were detected.</p>"
        )

    cards: list[str] = []

    for column, count in (
        outliers.columns_with_outliers.items()
    ):
        cards.append(
            f"""
<div class="outlier-card">
    <h4>{column}</h4>
    <p>{count} outliers detected</p>
</div>
"""
        )

    return "\n".join(cards)

def build_correlation_table(
    report: Report,
) -> str:
    """
    Build correlation table.
    """

    correlation = report.correlation()

    rows: list[str] = []

    if (
        not correlation.strong_positive_pairs
        and not correlation.strong_negative_pairs
    ):
        return (
            "<p>No strong correlations were detected.</p>"
        )

    rows.append(
        """
<table class="report-table">
    <thead>
        <tr>
            <th>Relationship</th>
            <th>Type</th>
            <th>Correlation</th>
        </tr>
    </thead>
    <tbody>
"""
    )

    for pair, value in (
        correlation.strong_positive_pairs.items()
    ):
        rows.append(
            f"""
<tr>
    <td>{pair}</td>
    <td>Positive</td>
    <td>{value:.2f}</td>
</tr>
"""
        )

    for pair, value in (
        correlation.strong_negative_pairs.items()
    ):
        rows.append(
            f"""
<tr>
    <td>{pair}</td>
    <td>Negative</td>
    <td>{value:.2f}</td>
</tr>
"""
        )

    rows.append(
        """
    </tbody>
</table>
"""
    )

    return "\n".join(rows)

def build_insights(
    report: Report,
) -> str:
    """
    Build insights HTML.
    """

    insight_summary = report.insights()

    rows: list[str] = []

    rows.append("<ul>")

    for insight in insight_summary.insights:
        rows.append(
            f"<li>{insight}</li>"
        )

    rows.append("</ul>")

    return "\n".join(rows)

def build_insight_recommendations(
    report: Report,
) -> str:
    """
    Build recommendation HTML.
    """

    insight_summary = report.insights()

    rows: list[str] = []

    rows.append("<ul>")

    for recommendation in (
        insight_summary.recommendations
    ):
        rows.append(
            f"<li>{recommendation}</li>"
        )

    rows.append("</ul>")

    return "\n".join(rows)


def build_ml_readiness(
    report: Report,
) -> str:
    """
    Build ML readiness HTML.
    """

    readiness = report.ml_readiness()

    score = (
        f"{readiness.score:.2f}"
        if readiness.score is not None
        else "N/A"
    )

    score_width = (
        max(min(readiness.score, 100.0), 0.0)
        if readiness.score is not None
        else 0.0
    )

    dimensions = [
        (
            "Completeness",
            readiness.completeness_score,
        ),
        (
            "Feature Quality",
            readiness.feature_quality_score,
        ),
        (
            "Data Stability",
            readiness.data_stability_score,
        ),
        (
            "Consistency",
            readiness.consistency_score,
        ),
        (
            "Distribution",
            readiness.distribution_score,
        ),
    ]

    dimension_rows: list[str] = []

    for label, value in dimensions:
        dimension_rows.append(
            f"""
<div class="progress-row">
    <span class="progress-label">{label}</span>
    <div class="progress-track">
        <div
            class="progress-fill"
            style="width: {value:.2f}%;"
        ></div>
    </div>
    <span class="progress-value numeral">
        {value:.2f}/100
    </span>
</div>
"""
        )

    target_status = (
        readiness.target_readiness
    )

    assessment_coverage = (
        f"{readiness.assessment_coverage:.2f}%"
    )

    return f"""
<div class="card card-pad">

    <div class="health-hero">

        <div class="kpi-card">
            <div class="kpi-label">ML Readiness</div>
            <div class="kpi-value">
                {score}<span class="kpi-unit">/100</span>
            </div>
            <div class="kpi-sub">
                {readiness.status}
            </div>
        </div>

        <div class="health-hero-body">

            <div class="health-hero-top">
                <div class="health-hero-title">
                    Preparation signals for machine learning
                </div>

                <span class="badge badge--grade">
                    {readiness.status}
                </span>
            </div>

            <p class="section-subtitle mt-0">
                This score represents observable preparation
                signals. It does not guarantee that a successful
                ML model can be trained.
            </p>

            <div class="progress-row">
                <span class="progress-label">
                    Overall score
                </span>

                <div class="progress-track">
                    <div
                        class="progress-fill"
                        style="width: {score_width:.2f}%;"
                    ></div>
                </div>

                <span class="progress-value numeral">
                    {score}/100
                </span>
            </div>

        </div>

    </div>

    <div style="margin-top: var(--sp-6);">
        <h4>Readiness dimensions</h4>

        {"".join(dimension_rows)}
    </div>

    <div class="pill-grid" style="margin-top: var(--sp-6);">

        <div class="pill-card">
            <div class="kpi-label">Assessment Coverage</div>
            <div class="kpi-value">
                {assessment_coverage}
            </div>
        </div>

        <div class="pill-card">
            <div class="kpi-label">Target Readiness</div>
            <div class="kpi-value">
                {target_status}
            </div>
        </div>

    </div>

    <div class="trait-columns" style="margin-top: var(--sp-6);">

        <div>
            <h4>Strengths</h4>

            <div class="trait-list trait-list--strength">
                {build_html_list(readiness.strengths)}
            </div>
        </div>

        <div>
            <h4>Weaknesses</h4>

            <div class="trait-list trait-list--weakness">
                {build_html_list(readiness.weaknesses)}
            </div>
        </div>

    </div>

    <div style="margin-top: var(--sp-6);">

        <h4>Recommendations</h4>

        <div class="trait-list">
            {build_html_list(readiness.recommendations)}
        </div>

    </div>

</div>
"""

def build_statistical_profile(
    report: Report,
) -> str:
    """
    Build contextual statistical profile HTML.
    """

    profile = report.statistical_profile()

    if not profile:
        return (
            "<p>No numeric columns were available "
            "for statistical interpretation.</p>"
        )

    rows: list[str] = []

    for column, values in profile.items():
        rows.append(
            f"""
<tr>
    <td>{column}</td>
    <td>{values["skewness"]:.2f}</td>
    <td>{values["skewness_interpretation"]}</td>
    <td>{values["kurtosis"]:.2f}</td>
    <td>{values["kurtosis_interpretation"]}</td>
    <td>{values["outlier_signal"]}</td>
</tr>
"""
        )

    return f"""
<table class="report-table">
    <thead>
        <tr>
            <th>Column</th>
            <th>Skewness</th>
            <th>Skewness Interpretation</th>
            <th>Kurtosis</th>
            <th>Kurtosis Interpretation</th>
            <th>Outlier Signal</th>
        </tr>
    </thead>
    <tbody>
        {"".join(rows)}
    </tbody>
</table>
"""