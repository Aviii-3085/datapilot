# Datapilot

> **The first step after loading your dataset.**

Datapilot is an open-source Python library that automates exploratory data analysis by generating deterministic dataset insights, health assessments, statistical summaries, and professional HTML reports.

Every data project begins with understanding the data. Datapilot helps you understand your dataset before building machine learning models, dashboards, or AI-powered applications.

---

## Installation

```bash
pip install datapilot-kit
```

---

## Quick Start

```python
import pandas as pd

from datapilot import analyze

df = pd.read_csv("dataset.csv")

report = analyze(df)
```

---

## Features

- Dataset Summary
- Dataset Health Score
- Missing Value Analysis
- Duplicate Detection
- Data Type Analysis
- Statistical Summaries
- Outlier Detection
- Correlation Analysis
- Actionable Insights
- Professional HTML Reports

---

## Documentation

Project documentation is available in the `docs/` directory.

- Vision
- User Journey
- API Philosophy
- API Review
- Roadmap

---

## Status

🚧 Datapilot v0.3 — Public Preview (In Development)

The project is currently being prepared for its first public release.