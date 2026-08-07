# Datapilot

> **The first step after loading your dataset.**

Datapilot is an open-source Python library for deterministic exploratory data analysis. It helps you understand your dataset by generating dataset health assessments, statistical summaries, actionable insights, and professional HTML reports.

Every data project begins with understanding the data. Datapilot helps you analyze your data before building machine learning models, dashboards, or AI-powered applications.

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

print(report.summary())
```

---

## Features

- 📊 Dataset Summary
- 💚 Dataset Health Score
- ❓ Missing Value Analysis
- 🔁 Duplicate Detection
- 🏷️ Data Type Analysis
- 📈 Statistical Summaries
- 📉 Outlier Detection
- 🔗 Correlation Analysis
- 💡 Actionable Insights
- 🌐 Professional HTML Reports

---

## Documentation

Project documentation is available in the `docs/` directory.

- Vision
- User Journey
- API Philosophy
- API Review
- Roadmap

---

## Installation Package

Install from PyPI:

```bash
pip install datapilot-kit
```

Import into your project:

```python
from datapilot import analyze
```

---

## Project Status

🧪 **Datapilot v0.3.0rc1** — Public Release Candidate

Datapilot is now available on PyPI as **`datapilot-kit`**. The current release candidate has been published for community testing and feedback before the stable **v0.3.0** release.

---

## License

This project is licensed under the MIT License.
