# API Design

This document defines the public interface of Datapilot.

The goal is to keep the library simple for users while allowing the internal implementation to evolve over time without breaking existing code.

---

# Design Principles

- The public API should be simple.
- The internal implementation should remain modular.
- Backward compatibility should be prioritized whenever possible.
- AI should explain results, not generate them.

---

# Entry Point

Datapilot exposes a single primary entry point.

```python
from datapilot import analyze

report = analyze(data)
```

`data` may be one of the following:

- Pandas DataFrame
- CSV file
- Excel file

Future versions may support:

- Parquet
- SQL connections
- Arrow Tables
- Polars DataFrames

---

# Report Object

The `analyze()` function returns a `Report` object.

```python
report = analyze(data)
```

The `Report` object acts as the primary interface between the user and Datapilot.

---

# Planned Methods

## summary()

Returns a high-level overview of the dataset.

Example

```python
report.summary()
```

---

## health_score()

Returns the overall dataset quality score.

Example

```python
report.health_score()
```

---

## insights()

Returns important findings discovered during analysis.

Example

```python
report.insights()
```

---

## recommendations()

Returns actionable preprocessing and machine learning recommendations.

Example

```python
report.recommendations()
```

---

## visualize()

Displays visual summaries of the dataset.

Example

```python
report.visualize()
```

---

## export_html()

Exports an interactive HTML report.

Example

```python
report.export_html("report.html")
```

---

## export_pdf()

Exports a PDF report.

Example

```python
report.export_pdf("report.pdf")
```

---

## explain()

Provides natural language explanations for findings.

Example

```python
report.explain()
```

This feature may optionally use an LLM.

---

## ask()

Allows users to ask questions about their dataset.

Example

```python
report.ask("Why is my health score low?")
```

This feature is planned for a future release.

---

# Planned Properties

The following properties may be directly accessible.

```python
report.rows

report.columns

report.health

report.statistics

report.insights

report.recommendations
```

These names may evolve during development.

---

# Internal Pipeline

```
Input
   │
   ▼
Loader
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
Report Object
```

The public API should never expose internal implementation details.

---

# Design Goals

The API should be:

- Simple
- Predictable
- Consistent
- Beginner-friendly
- Extensible

---

# Versioning

Breaking changes to the public API should only occur during major version releases.

Minor releases should remain backward compatible whenever possible.