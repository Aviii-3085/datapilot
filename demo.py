import pandas as pd

from datapilot import analyze


def main() -> None:
    df = pd.DataFrame(
        {
            "Age": [21, None, 23, 21],
            "Salary": [40000, None, 50000, 40000],
            "Department": ["IT", "HR", None, "IT"],
            "Is_Manager": [True, False, False, True],
            "Joining_Date": pd.to_datetime(
                [
                    "2023-01-01",
                    "2023-02-15",
                    "2023-03-10",
                    "2023-01-01",
                ]
            ),
        }
    )

    report = analyze(df)

    summary = report.summary()
    missing = report.missing_values()
    duplicates = report.duplicates()
    data_types = report.data_types()
    health = report.dataset_health()

    print("\n=== Datapilot Summary ===")
    print(f"Rows                 : {summary.rows}")
    print(f"Columns              : {summary.columns}")
    print(f"Memory (MB)          : {summary.memory_usage_mb}")
    print(f"Column Names         : {summary.column_names}")

    print("\n=== Missing Value Analysis ===")
    print(f"Total Missing Values : {missing.total_missing}")
    print(f"Missing Percentage   : {missing.missing_percentage}%")
    print(f"Columns With Missing : {missing.columns_with_missing}")
    print(f"Columns Without Missing : {missing.columns_without_missing}")

    print("\n=== Duplicate Analysis ===")
    print(f"Total Duplicates     : {duplicates.total_duplicates}")
    print(f"Duplicate Percentage : {duplicates.duplicate_percentage}%")

    print("\n=== Data Type Analysis ===")
    print(f"Numeric Columns      : {data_types.numeric_columns}")
    print(f"Categorical Columns  : {data_types.categorical_columns}")
    print(f"Boolean Columns      : {data_types.boolean_columns}")
    print(f"Datetime Columns     : {data_types.datetime_columns}")

    print("\n=== Dataset Health Assessment ===")
    print(f"Score                : {health.score}/100")
    print(f"Grade                : {health.grade}")
    print(f"Status               : {health.status}")
    print(f"ML Ready             : {health.ml_ready}")

    print("\nStrengths")
    for item in health.strengths:
        print(f"  ✓ {item}")

    print("\nWeaknesses")
    for item in health.weaknesses:
        print(f"  • {item}")

    print("\nRecommendations")
    for item in health.recommendations:
        print(f"  → {item}")


if __name__ == "__main__":
    main()