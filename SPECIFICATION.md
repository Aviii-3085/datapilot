# Datapilot Specification

This document defines the expected behavior of Datapilot.

It acts as the source of truth for project behavior, feature requirements, scoring rules, and implementation decisions.

When implementation and documentation disagree, this specification should be updated first.

---

# Project Goal

Datapilot is an intelligent Python library that helps users understand their datasets through automated analysis, interpretation, and actionable recommendations.

Datapilot does not aim to replace a data scientist.

Instead, it automates repetitive exploratory analysis while providing meaningful insights and guidance.

---

# Core Principles

1. Statistics before interpretation.
2. Interpretation before recommendation.
3. AI explains results but never generates recommendations independently.
4. Every recommendation must be deterministic.
5. Every recommendation must have a documented reason.

---

# Supported Input (Version 0.1)

Datapilot should accept:

- Pandas DataFrame
- CSV files
- Excel files

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
```

All supported input types should produce the same `Report` object.

---

# Report Object

The Report object represents the complete analysis of a dataset.

Future methods include:

```python
report.summary()
report.health_score()
report.insights()
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

- Number of rows
- Number of columns
- Memory usage
- Column names
- Column data types
- Missing values
- Duplicate rows

---

# Health Score

The dataset health score ranges from:

```
0 - 100
```

A score of:

| Score | Meaning |
|--------|----------|
| 90–100 | Excellent |
| 75–89 | Good |
| 60–74 | Fair |
| 40–59 | Poor |
| 0–39 | Critical |

The scoring algorithm will be fully documented.

No hidden calculations.

---

# Statistics Engine

The statistics engine is responsible for computing facts only.

Examples:

- Missing values
- Duplicate rows
- Correlation
- Outliers
- Skewness
- Cardinality
- Class imbalance
- Descriptive statistics

It never makes recommendations.

---

# Interpretation Engine

The interpretation engine converts statistical findings into meaningful observations.

Example

Statistic:

```
Correlation = 0.95
```

Interpretation:

```
Possible multicollinearity detected.
```

---

# Recommendation Engine

The recommendation engine generates deterministic recommendations.

Example

Finding:

```
Positive skew
```

Recommendation:

```
Median imputation
```

Every recommendation must include an explanation.

---

# AI Layer

The AI layer is optional.

Responsibilities:

- Explain findings.
- Simplify technical language.
- Answer user questions.

The AI layer never replaces the Statistics Engine or Recommendation Engine.

---

# Performance Goals

Datapilot should:

- Support large datasets efficiently.
- Avoid unnecessary recalculations.
- Cache expensive computations.
- Minimize memory overhead.

---

# Error Handling

Datapilot should provide clear error messages.

Examples:

- Unsupported file type
- Empty dataset
- Corrupted dataset
- Missing dependencies

Errors should explain both the problem and the suggested solution.

---

# Future Features

Potential future additions include:

- Time series analysis
- NLP dataset support
- Image dataset support
- Plugin architecture
- Custom recommendation rules
- Interactive dashboard
- Cloud deployment

---

# Non-Goals

Datapilot will not:

- Train machine learning models.
- Replace AutoML frameworks.
- Replace visualization libraries.
- Make decisions without deterministic analysis.

---

# Development Principles

Every feature should satisfy the following:

- Solves a real problem.
- Has a clear purpose.
- Is modular.
- Is testable.
- Is documented.
- Does not unnecessarily increase complexity.

---

# Decision Log

This section records significant architectural and product decisions made during the development of Datapilot.

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

- Simple to learn
- Pythonic
- Easy to remember
- Hides internal complexity

---

## DP-002 — Report Object

**Status:** Accepted

### Decision

The `analyze()` function returns a `Report` object.

### Rationale

The Report object becomes the single interface between the user and Datapilot, reducing API complexity and improving extensibility.

---

## DP-003 — AI Responsibilities

**Status:** Accepted

### Decision

The AI layer will only explain findings.

It will never independently generate recommendations.

### Rationale

Recommendations must remain deterministic, reproducible, and based on documented statistical rules.

---

## DP-004 — Internal Data Representation

**Status:** Accepted

### Decision

All supported input types will be converted internally into a Pandas DataFrame.

### Rationale

Maintaining a single internal representation simplifies development and reduces duplicate logic.

---

## DP-005 — Project Philosophy

**Status:** Accepted

### Decision

Datapilot should prioritize helping users understand their datasets rather than simply generating statistics.

### Rationale

The project aims to bridge the gap between automated EDA and practical decision-making.