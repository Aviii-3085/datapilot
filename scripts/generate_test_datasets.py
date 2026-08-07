from pathlib import Path

import pandas as pd

DATASETS_DIR = Path(__file__).parent.parent / "datasets"
DATASETS_DIR.mkdir(exist_ok=True)


clean = pd.DataFrame(
    {
        "ID": [1, 2, 3, 4, 5],
        "Age": [22, 25, 28, 30, 32],
        "Salary": [30000, 36000, 42000, 47000, 52000],
        "Experience": [1, 3, 5, 6, 8],
        "Rating": [4.2, 4.1, 4.4, 4.3, 4.6],
    }
)

clean.to_csv(
    DATASETS_DIR / "clean.csv",
    index=False,
)

print("Generated clean.csv")

missing = pd.DataFrame(
    {
        "ID": [1, 2, 3, 4, 5],
        "Age": [22, None, 28, 31, None],
        "Salary": [30000, 35000, None, 48000, None],
        "Department": [
            "IT",
            "HR",
            "Finance",
            None,
            "IT",
        ],
    }
)

missing.to_csv(
    DATASETS_DIR / "missing.csv",
    index=False,
)

print("Generated missing.csv")


duplicates = pd.DataFrame(
    {
        "ID": [1, 2, 3, 2, 3, 3],
        "Age": [22, 25, 30, 25, 30, 30],
        "Salary": [
            30000,
            35000,
            50000,
            35000,
            50000,
            50000,
        ],
    }
)

duplicates.to_csv(
    DATASETS_DIR / "duplicates.csv",
    index=False,
)

print("Generated duplicates.csv")

outliers = pd.DataFrame(
    {
        "Age": [
            22,
            24,
            25,
            23,
            24,
            25,
            26,
            27,
            28,
            45,
        ],
        "Salary": [
            30000,
            32000,
            33000,
            31000,
            30500,
            31500,
            34000,
            35000,
            36000,
            500000,
        ],
    }
)

outliers.to_csv(
    DATASETS_DIR / "outliers.csv",
    index=False,
)

print("Generated outliers.csv")


correlation = pd.DataFrame(
    {
        "Age": [
            20,
            25,
            30,
            35,
            40,
            45,
            50,
            55,
            60,
            65,
        ],
        "Salary": [
            20000,
            25000,
            30000,
            35000,
            40000,
            45000,
            50000,
            55000,
            60000,
            65000,
        ],
        "Bonus": [
            2000,
            2500,
            3000,
            3500,
            4000,
            4500,
            5000,
            5500,
            6000,
            6500,
        ],
    }
)

correlation.to_csv(
    DATASETS_DIR / "correlation.csv",
    index=False,
)

print("Generated correlation.csv")

mixed = pd.DataFrame(
    {
        "ID": [
            1,
            2,
            3,
            4,
            5,
            5,
            7,
            8,
            9,
            10,
        ],
        "Age": [
            22,
            None,
            28,
            31,
            25,
            25,
            27,
            120,
            30,
            None,
        ],
        "Salary": [
            30000,
            35000,
            None,
            48000,
            52000,
            52000,
            54000,
            1000000,
            None,
            60000,
        ],
        "Department": [
            "IT",
            "HR",
            "Finance",
            None,
            "IT",
            "IT",
            "Sales",
            "Sales",
            None,
            "HR",
        ],
        "Experience": [
            1,
            2,
            5,
            7,
            4,
            4,
            6,
            40,
            8,
            3,
        ],
        "Performance": [
            70,
            72,
            80,
            88,
            90,
            90,
            91,
            100,
            95,
            74,
        ],
    }
)

mixed.to_csv(
    DATASETS_DIR / "mixed.csv",
    index=False,
)

print("Generated mixed.csv")