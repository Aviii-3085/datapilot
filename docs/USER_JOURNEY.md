# Datapilot User Journey

## Goal

Understand every step a first-time user takes from installation to receiving their first meaningful insight.

The objective is to minimize friction and maximize clarity throughout the workflow.

## First-Time User Workflow

1. Discover Datapilot
2. Install Datapilot
3. Import the library
4. Load a dataset
5. Analyze the dataset
6. Understand the results
7. Export or share the report


## Friction Audit

| Step | Current Experience | Friction | Future Improvement |
|------|--------------------|----------|--------------------|
| Discover | GitHub / PyPI | Unknown library | Better documentation |
| Install | pip install datapilot | Low | Keep simple |
| Import | from datapilot import analyze | Low | Keep simple |
| Load Dataset | pd.read_csv() | None | Already familiar |
| Analyze | analyze(df) | Very Low | Maintain simplicity |
| View Results | HTML report generation | Medium | Improve accessibility |
| Export | HTML | Low | Add PDF, Notebook, etc. |