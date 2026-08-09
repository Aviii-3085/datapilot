# Datapilot

> **The first step after loading your dataset.**

Datapilot is an open-source Python library for deterministic exploratory data analysis and dataset understanding.

Every data project begins with understanding the data. Datapilot helps you understand your dataset before building machine learning models, dashboards, or AI-powered applications.

---

## Installation

Install Datapilot from PyPI:

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

Datapilot analyzes your dataset and generates structured insights, health assessments, statistical summaries, and reporting information.

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

🚀 **Datapilot v0.3.0 — Stable Release**

Datapilot is now available on PyPI as **`datapilot-kit`**.

This is the first stable release of Datapilot.

---

## License

Datapilot is open source and released under the **MIT License**.