import pandas as pd

from datapilot import analyze


df = pd.DataFrame(
    {
        "Age": [21, 22, 23],
        "Salary": [40000, 45000, 50000],
    }
)

report = analyze(df)

summary = report.summary()

print(summary)