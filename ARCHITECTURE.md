# Architecture

## Overview

Datapilot is an open-source Python library that combines automated exploratory data analysis with intelligent interpretation and actionable machine learning recommendations.

The project is designed as a modular pipeline where each component has a single responsibility. This makes the codebase easier to understand, test, maintain, and extend.

The AI layer is optional and is only responsible for explaining insights in natural language. All analysis and recommendations are generated deterministically by Datapilot itself.

---

## Design Philosophy

Datapilot is built around four principles:

1. Analyze
2. Interpret
3. Recommend
4. Explain

The objective is not only to show statistics but to help users understand what those statistics mean and what actions should be taken next.

---

## High-Level Pipeline

```
                Input
                  │
                  ▼
         Data Loading Layer
                  │
                  ▼
        Statistics Engine
                  │
                  ▼
      Interpretation Engine
                  │
                  ▼
     Recommendation Engine
                  │
                  ▼
        Report Generation
                  │
                  ▼
     Optional AI Explanation
```

---

## Project Structure

```
datapilot/
│
├── core/
│   Core data models and shared functionality.
│
├── analysis/
│   Statistical analysis and dataset profiling.
│
├── interpretation/
│   Converts statistical findings into meaningful insights.
│
├── recommendations/
│   Generates preprocessing and machine learning recommendations.
│
├── reports/
│   HTML, PDF and future report generation.
│
├── visualization/
│   Charts and graphical summaries.
│
├── cli/
│   Command-line interface.
│
├── llm/
│   AI explanation layer.
│
└── utils/
    Shared helper functions.
```

---

## Responsibilities

### Data Loading

Responsible for loading datasets from different sources.

Supported sources (planned):

- CSV
- Excel
- Parquet
- SQL
- Pandas DataFrame

Regardless of the input source, every dataset is internally converted into a Pandas DataFrame.

---

### Statistics Engine

Responsible for computing factual information about the dataset.

Examples:

- Dataset shape
- Column types
- Missing values
- Duplicate rows
- Correlations
- Outliers
- Class imbalance
- Skewness
- Cardinality
- Descriptive statistics

This module never makes recommendations.

---

### Interpretation Engine

Responsible for understanding statistical findings.

Example:

Input

```
Missing values: 42%
Column: Salary
```

Output

```
The missing percentage is high and may significantly impact model performance.
```

This layer converts numbers into insights.

---

### Recommendation Engine

Responsible for deciding what users should do next.

Examples:

- Mean or median imputation
- Drop highly correlated features
- Handle class imbalance
- Feature scaling
- Encoding strategy
- Suggested machine learning algorithms

Recommendations are deterministic and based on predefined rules.

---

### AI Explanation Layer

The AI layer is optional.

Its only responsibility is to explain Datapilot's findings in natural language.

The AI does not perform analysis and does not generate recommendations independently.

Example

Recommendation:

```
Use median imputation.
```

AI explanation:

> Median imputation is recommended because the column is positively skewed and contains relatively few missing values.

---

## Design Goals

Datapilot should always be:

- Modular
- Extensible
- Testable
- Reliable
- Beginner-friendly
- Production-ready

---

## Engineering Principles

- One responsibility per module.
- Deterministic recommendations.
- AI explains but never decides.
- Every feature must be testable.
- Public APIs should remain simple.
- Internal implementation can evolve without changing the user interface.

---

## Public API

The intended user experience is intentionally simple.

```python
from datapilot import analyze

report = analyze("employees.csv")

report.summary()
report.health_score()
report.insights()
report.recommendations()
report.export_html("report.html")
```

Future versions may also support:

```python
analyze(dataframe)
analyze("employees.xlsx")
analyze(sql_connection)
```

---

## Long-Term Vision

Datapilot aims to become an intelligent data analysis toolkit that helps users:

- Understand their data
- Identify data quality issues
- Receive actionable recommendations
- Build better machine learning pipelines
- Learn from their datasets rather than simply visualize them

Rather than replacing data scientists, Datapilot is designed to assist them by automating repetitive analysis while providing meaningful explanations.