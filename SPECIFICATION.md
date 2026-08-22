# Datapilot Specification

This document defines the expected behavior of Datapilot.

It acts as the source of truth for project behavior, feature requirements,
scoring rules, and implementation decisions.

When implementation and documentation disagree, this specification should be
updated first.

---

# Project Goal

Datapilot is an intelligent Python library that helps users understand their
datasets through automated analysis, interpretation, and actionable
recommendations.

Datapilot does not aim to replace a data scientist.

Instead, it automates repetitive exploratory analysis while providing
meaningful insights and guidance.

---

# Core Principles

1. Statistics before interpretation.
2. Interpretation before recommendation.
3. AI explains results but never generates recommendations independently.
4. Every recommendation must be deterministic.
5. Every recommendation must have a documented reason.
6. Analysis should describe observed statistical properties without assuming
   semantic meaning that is not present in the dataset.

---

# Supported Input

Datapilot accepts:

- Pandas DataFrame
- CSV files
- Excel files
- Headerless comma-separated `.data` files

All supported input types are converted internally into a Pandas DataFrame.

Common textual representations of missing values are normalized during file
loading.

Recognized missing-value markers include:

- `?`
- `NA`
- `N/A`
- `null`
- `NULL`
- `None`
- `none`

For headerless `.data` files, Datapilot does not assume a dataset-specific
schema. Generic column identifiers are used because the file itself does not
provide column names.

Future versions may support:

- Parquet
- SQL databases
- Arrow Tables
- Polars DataFrames

---

# Public Entry Point

```python
from datapilot import analyze

report = analyze(data)
````

All supported input types should produce the same `Report` object.

---

# Report Object

The Report object represents the complete analysis of a dataset.

Current methods include:

```python
report.summary()
report.missing_values()
report.duplicates()
report.data_types()
report.dataset_health()
report.statistics()
report.outliers()
report.correlation()
report.insights()
```

Future methods may include:

```python
report.recommendations()
report.visualize()
report.export_html()
report.export_pdf()
report.explain()
report.ask()
```

---

# Dataset Summary

The summary should include:

* Number of rows
* Number of columns
* Memory usage
* Column names

Additional analysis is available through the Report interface:

* Missing values
* Duplicate rows
* Data types
* Statistics
* Outliers
* Correlations
* Dataset health
* Insights

---

# Health Score

The dataset health score ranges from:

```text
0 - 100
```

The score is deterministic and is calculated from three components.

## Missing Value Penalty

Missing values contribute a maximum penalty of 40 points.

```text
missing_penalty =
    (missing_percentage / 100) × 40
```

## Duplicate Row Penalty

Duplicate rows contribute a maximum penalty of 35 points.

```text
duplicate_penalty =
    (duplicate_percentage / 100) × 35
```

## Structure Penalty

Unsupported or unrecognized column data types contribute a maximum penalty
of 25 points.

```text
structure_penalty =
    (unrecognized_columns / total_columns) × 25
```

If the dataset contains no columns, the structure penalty is zero.

## Final Score

```text
health_score =
    100
    - missing_penalty
    - duplicate_penalty
    - structure_penalty
```

The final score is:

* Rounded to the nearest integer.
* Clamped to the range `0–100`.

Therefore:

```text
0 <= health_score <= 100
```

## Health Grade

| Score  | Grade | Status    |
| ------ | ----- | --------- |
| 95–100 | A+    | Excellent |
| 90–94  | A     | Healthy   |
| 80–89  | B     | Good      |
| 70–79  | C     | Fair      |
| 60–69  | D     | Poor      |
| 0–59   | F     | Critical  |

The grade and status are deterministic consequences of the health score.

---

# ML Readiness

Datapilot does not train machine learning models.

The current `ml_ready` field is a deterministic heuristic intended to
indicate whether the dataset passes basic quality thresholds.

A dataset is considered ML-ready when all of the following are true:

```text
health_score >= 85
AND
missing_percentage <= 20
AND
duplicate_percentage <= 5
```

This field does not guarantee that a dataset is suitable for a specific
machine learning task.

It does not evaluate:

* Feature engineering requirements
* Target suitability
* Class imbalance
* Data leakage
* Identifier semantics
* Model-specific assumptions
* Domain-specific requirements

These may be addressed by future analytical capabilities.

---

# Statistics Engine

The statistics engine is responsible for computing facts only.

Examples:

* Missing values
* Duplicate rows
* Correlation
* Outliers
* Descriptive statistics

It never makes recommendations.

For descriptive statistics, numeric columns identified by their Pandas data
types are analyzed.

Datapilot does not currently infer semantic roles such as:

* Identifier
* Target
* Feature
* Measurement

A numeric identifier may therefore be included in numeric statistical
analysis.

Semantic column-role detection is outside the current v0.3 scope.

---

# Data Type Analysis

Data types are determined from the Pandas DataFrame representation.

Datapilot currently identifies:

* Numeric columns
* Categorical columns
* Boolean columns
* Datetime columns

Numeric classification is based on the underlying Pandas data type.

Datapilot does not currently infer semantic meaning from column names.

For example, a column named `PassengerId` may be classified as numeric if its
underlying values are numeric.

---

# Outlier Analysis

Datapilot detects statistical outliers in numeric columns using the
Interquartile Range (IQR) method.

For each numeric column:

```text
IQR = Q3 - Q1

lower_bound = Q1 - (1.5 × IQR)

upper_bound = Q3 + (1.5 × IQR)
```

A value is considered a statistical outlier when:

```text
value < lower_bound
OR
value > upper_bound
```

Missing values are excluded from the outlier calculation.

The outlier engine reports:

* Total outliers
* Overall outlier percentage
* Outlier count by column
* Columns without detected outliers

An outlier is a statistical observation and is not automatically considered
an erroneous value.

---

# Correlation Analysis

Datapilot performs Pearson correlation analysis on numeric columns.

A correlation is considered strong when:

```text
correlation >= 0.70
```

or:

```text
correlation <= -0.70
```

The correlation engine reports:

* Correlation matrix
* Strong positive correlation pairs
* Strong negative correlation pairs

Correlation does not imply causation.

Datapilot does not currently infer semantic relationships between features.

---

# Interpretation Engine

The interpretation engine converts statistical findings into meaningful
observations.

Example:

Statistic:

```text
Correlation = 0.95
```

Interpretation:

```text
Highly correlated numeric features detected.
```

Another example:

Statistic:

```text
Outliers > 0
```

Interpretation:

```text
Statistical outliers detected.
```

Interpretations are deterministic and based on documented statistical rules.

---

# Recommendation Engine

The recommendation engine generates deterministic recommendations.

Every recommendation must have a documented trigger and reason.

## Missing Values

### Trigger

```text
total_missing > 0
```

### Recommendation

```text
Handle missing values before training machine learning models.
```

### Reason

Missing values may interfere with downstream analysis and many machine
learning algorithms.

---

## Duplicate Rows

### Trigger

```text
total_duplicates > 0
```

### Recommendation

```text
Remove duplicate rows.
```

### Reason

Duplicate observations can distort statistical analysis and downstream
modelling.

---

## Statistical Outliers

### Trigger

```text
total_outliers > 0
```

### Recommendation

```text
Review outliers before modelling.
```

### Reason

Statistical outliers may represent valid observations or unusual conditions
and should therefore be reviewed before modelling rather than automatically
removed.

---

## Strong Positive Correlation

### Trigger

At least one Pearson correlation satisfies:

```text
correlation >= 0.70
```

### Recommendation

```text
Review correlated features to reduce multicollinearity.
```

### Reason

Highly correlated features may provide redundant information and can
contribute to multicollinearity in models that are sensitive to correlated
predictors.

---

## Strong Negative Correlation

### Trigger

At least one Pearson correlation satisfies:

```text
correlation <= -0.70
```

### Current Behavior

Datapilot generates an insight:

```text
Strong negative correlations detected.
```

No separate recommendation is currently generated for this condition.

This behavior is intentional because strong negative correlation is a
statistical relationship and does not by itself imply a required
data-cleaning action.

---

# Insight Generation

The insight engine combines findings from:

* Missing value analysis
* Duplicate detection
* Outlier detection
* Correlation analysis

Insights are deterministic.

If multiple conditions are detected, multiple insights and recommendations
may be returned.

If no significant conditions are detected, Datapilot reports:

```text
No significant data quality issues detected.
```

---

# AI Layer

The AI layer is optional.

Responsibilities:

* Explain findings.
* Simplify technical language.
* Answer user questions.

The AI layer never replaces the Statistics Engine or Recommendation Engine.

The AI layer never independently determines recommendations.

---

# HTML Reporting

Datapilot provides HTML report generation containing:

* Dataset overview
* Dataset health
* Missing-value analysis
* Duplicate analysis
* Statistical summaries
* Outlier analysis
* Correlation analysis
* Insights
* Recommendations

HTML reports are generated from Datapilot analysis results and must not
perform independent statistical calculations.

---

# Performance Goals

Datapilot should:

* Support large datasets efficiently.
* Avoid unnecessary recalculations.
* Cache expensive computations where appropriate.
* Minimize memory overhead.

---

# Error Handling

Datapilot should provide clear error messages.

Examples:

* Unsupported file type
* Empty dataset
* Corrupted dataset
* Missing dependencies

Errors should explain both the problem and the suggested solution where
possible.

---

# Future Features

Potential future additions include:

* Time series analysis
* NLP dataset support
* Image dataset support
* Plugin architecture
* Custom recommendation rules
* Interactive dashboard
* Cloud deployment
* Semantic column-role detection
* Identifier detection
* Target-column detection
* Feature suitability analysis

---

# Non-Goals

Datapilot will not:

* Train machine learning models.
* Replace AutoML frameworks.
* Replace visualization libraries.
* Make decisions without deterministic analysis.
* Claim that statistical outliers are automatically erroneous.
* Claim that `ml_ready=True` guarantees suitability for a particular machine
  learning model.

---

# Development Principles

Every feature should satisfy the following:

* Solves a real problem.
* Has a clear purpose.
* Is modular.
* Is testable.
* Is documented.
* Does not unnecessarily increase complexity.

---

# Decision Log

This section records significant architectural and product decisions made
during the development of Datapilot.

Each decision receives a unique identifier and a brief explanation.

---

## DP-001 — Public API

**Status:** Accepted

### Decision

Datapilot will expose a single public entry point.

```python
from datapilot import analyze

report = analyze(data)
```

### Rationale

* Simple to learn
* Pythonic
* Easy to remember
* Hides internal complexity

---

## DP-002 — Report Object

**Status:** Accepted

### Decision

The `analyze()` function returns a `Report` object.

### Rationale

The Report object becomes the single interface between the user and
Datapilot, reducing API complexity and improving extensibility.

---

## DP-003 — AI Responsibilities

**Status:** Accepted

### Decision

The AI layer will only explain findings.

It will never independently generate recommendations.

### Rationale

Recommendations must remain deterministic, reproducible, and based on
documented statistical rules.

---

## DP-004 — Internal Data Representation

**Status:** Accepted

### Decision

All supported input types will be converted internally into a Pandas
DataFrame.

### Rationale

Maintaining a single internal representation simplifies development and
reduces duplicate logic.

---

## DP-005 — Project Philosophy

**Status:** Accepted

### Decision

Datapilot should prioritize helping users understand their datasets rather
than simply generating statistics.

### Rationale

The project aims to bridge the gap between automated EDA and practical
decision-making.

---

## DP-006 — Missing Value Normalization

**Status:** Accepted

### Decision

Common textual missing-value markers are normalized into Pandas missing
values during file loading.

### Rationale

Real-world datasets frequently represent missing data using textual markers
such as `?`, `NA`, or `N/A`.

Normalizing these values at the loading boundary ensures that downstream
analysis modules operate on a consistent representation.

---

## DP-007 — Headerless `.data` Files

**Status:** Accepted

### Decision

Headerless comma-separated `.data` files are supported.

Datapilot does not assume a dataset-specific schema for `.data` files.
Generic column identifiers are used when column names are not provided by
the source file.

### Rationale

File extensions do not provide enough information to infer a dataset's
semantic schema.

Keeping the loader generic avoids hard-coding support for a particular
dataset.

---

## DP-008 — Deterministic Recommendations

**Status:** Accepted

### Decision

Recommendations are generated only from documented statistical rules.

### Rationale

Recommendations must be reproducible, testable, and understandable.

They must not depend on AI-generated reasoning or nondeterministic behavior.

---

## DP-009 — Semantic Column Roles

**Status:** Deferred

### Decision

Datapilot v0.3 does not infer semantic roles such as identifiers, targets,
or model features from numeric or categorical columns.

### Rationale

Data type and semantic meaning are different concepts.

Automatically excluding a numeric column such as an identifier from
statistical analysis requires additional semantic rules and should not be
introduced without a clearly defined contract.

This capability may be introduced in a future release.
