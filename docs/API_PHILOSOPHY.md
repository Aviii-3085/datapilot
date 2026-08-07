# Datapilot API Philosophy

## Goal

The Datapilot API should feel intuitive, predictable, and Pythonic.

A user should be able to accomplish common tasks without constantly referring to documentation.

Method names should read naturally and reflect the user's intent rather than the internal implementation.

## API Design Principles

### 1. Simplicity

Common tasks should require as little code as possible.

### 2. Readability

Code should read almost like English.

### 3. Predictability

Similar operations should follow consistent naming conventions.

### 4. Explicitness

Methods should clearly communicate what they do without unexpected side effects.

### 5. Progressive Power

Beginners should be able to achieve useful results quickly, while advanced users should have access to more detailed functionality when needed.


## Current Public API Review

| Feature | Current API | Natural? | Notes |
|----------|-------------|----------|-------|
| Analyze dataset | analyze(df) | ✅ | Simple and memorable |
| Summary | report.summary() | ✅ | Clear |
| Missing Values | report.missing_values() | ✅ | Clear |
| Duplicates | report.duplicates() | ✅ | Good |
| Statistics | report.statistics() | ✅ | Familiar |
| Correlation | report.correlation() | ✅ | Familiar |
| Outliers | report.outliers() | ✅ | Familiar |
| Insights | report.insights() | ✅ | Strong feature |
| Dataset Health | report.dataset_health() | 🤔 | Consider shorter alias like report.health() in future |


## Future API Ideas

These ideas are intentionally deferred until future releases.

```python
report.show()
```

Display the report in the most appropriate format for the current environment.

```python
report.save("report.html")
```

Save a report without requiring additional helper functions.

```python
report.export("pdf")
```

Export reports in different formats through a unified interface.

```python
report.dashboard()
```

Launch an interactive dashboard.

```python
report.ask("Why is my health score low?")
```

Future AI-assisted explanation built on top of Datapilot's structured analysis.