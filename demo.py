import pandas as pd

from datapilot import analyze


def main() -> None:
    df = pd.DataFrame(
        {
            "Age": [21, None, 23],
            "Salary": [40000, None, 50000],
            "Department": ["IT", "HR", None],
        }
    )

    report = analyze(df)

    summary = report.summary()
    missing = report.missing_values()

    print("\n=== Datapilot Summary ===")
    print(f"Rows          : {summary.rows}")
    print(f"Columns       : {summary.columns}")
    print(f"Memory (MB)   : {summary.memory_usage_mb}")
    print(f"Column Names  : {summary.column_names}")

    print("\n=== Missing Value Analysis ===")
    print(f"Total Missing Values      : {missing.total_missing}")
    print(f"Missing Percentage        : {missing.missing_percentage}%")
    print(f"Columns With Missing      : {missing.columns_with_missing}")
    print(f"Columns Without Missing   : {missing.columns_without_missing}")


if __name__ == "__main__":
    main()