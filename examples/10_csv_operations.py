"""Working with CSV files and Jalali dates examples.

This module demonstrates how to read, write, and manipulate CSV files
containing Jalali dates using jalali-pandas.
"""

import io

import numpy as np
import pandas as pd

from jalali_pandas import JalaliTimestamp, to_jalali_datetime

# =============================================================================
# Scenario 1: Reading CSV with Jalali Date Strings
# =============================================================================

print("=" * 60)
print("Scenario 1: Reading CSV with Jalali Date Strings")
print("=" * 60)

# Create a sample CSV with Jalali dates
csv_data = """date,product,quantity,price
1402-01-01,Product A,10,50000
1402-01-15,Product B,5,75000
1402-02-01,Product A,8,50000
1402-02-20,Product C,3,120000
1402-03-10,Product B,12,75000
"""

# Read CSV
df = pd.read_csv(io.StringIO(csv_data))
print("\nRaw CSV data:")
print(df)
print(f"\nData types:\n{df.dtypes}")

# Parse Jalali date strings
df["jalali_date"] = df["date"].jalali.parse_jalali("%Y-%m-%d")
print("\nAfter parsing Jalali dates:")
print(df)
print(f"\nData types:\n{df.dtypes}")

# =============================================================================
# Scenario 2: Reading CSV with Gregorian Dates and Converting
# =============================================================================

print("\n" + "=" * 60)
print("Scenario 2: Reading CSV with Gregorian Dates and Converting")
print("=" * 60)

# Create CSV with Gregorian dates
csv_data_gregorian = """date,product,quantity,price
2023-03-21,Product A,10,50000
2023-04-04,Product B,5,75000
2023-04-21,Product A,8,50000
2023-05-10,Product C,3,120000
2023-05-31,Product B,12,75000
"""

# Read CSV
df = pd.read_csv(io.StringIO(csv_data_gregorian))
df["date"] = pd.to_datetime(df["date"])
print("\nCSV with Gregorian dates:")
print(df)

# Convert to Jalali
df["jalali_date"] = df["date"].jalali.to_jalali()
df["jyear"] = df["jalali_date"].jalali.year
df["jmonth"] = df["jalali_date"].jalali.month

print("\nAfter conversion to Jalali:")
print(df[["date", "jalali_date", "jyear", "jmonth", "product", "quantity"]])

# =============================================================================
# Scenario 3: Writing CSV with Jalali Dates
# =============================================================================

print("\n" + "=" * 60)
print("Scenario 3: Writing CSV with Jalali Dates")
print("=" * 60)

# Create DataFrame with Jalali dates
df = pd.DataFrame(
    {
        "jalali_date": [
            JalaliTimestamp(1402, 1, 1),
            JalaliTimestamp(1402, 1, 15),
            JalaliTimestamp(1402, 2, 1),
            JalaliTimestamp(1402, 2, 15),
            JalaliTimestamp(1402, 3, 1),
        ],
        "product": ["A", "B", "A", "C", "B"],
        "sales": [100, 150, 120, 200, 180],
    }
)

print("\nDataFrame with Jalali dates:")
print(df)

# Format Jalali dates as strings for CSV export
df["date_str"] = df["jalali_date"].jalali.strftime("%Y-%m-%d")
print("\nWith formatted date strings:")
print(df[["date_str", "product", "sales"]])

# Prepare for CSV export
export_df = df[["date_str", "product", "sales"]]
export_df.columns = ["date", "product", "sales"]

print("\nReady for CSV export:")
print(export_df.to_csv(index=False))

# =============================================================================
# Scenario 4: Handling Different Date Formats in CSV
# =============================================================================

print("\n" + "=" * 60)
print("Scenario 4: Handling Different Date Formats in CSV")
print("=" * 60)

# CSV with mixed date formats
csv_data_mixed = """date,amount
1402-01-01,100000
1402/01/15,150000
14020120,200000
2023-03-21,250000
"""

df = pd.read_csv(io.StringIO(csv_data_mixed))
print("\nCSV with mixed date formats:")
print(df)


# Function to parse mixed formats
def parse_date_string(date_str):
    """Parse various Jalali date formats."""
    if pd.isna(date_str):
        return pd.NaT

    formats = ["%Y-%m-%d", "%Y/%m/%d", "%Y%m%d"]

    # Try Jalali formats first
    for fmt in formats:
        try:
            return JalaliTimestamp.strptime(str(date_str), fmt)
        except ValueError:
            continue

    # Try Gregorian format
    try:
        gregorian = pd.to_datetime(date_str)
        return to_jalali_datetime(gregorian)
    except ValueError:
        return pd.NaT


df["parsed_date"] = df["date"].apply(parse_date_string)
print("\nAfter parsing:")
print(df)

# =============================================================================
# Scenario 5: Large Dataset Processing
# =============================================================================

print("\n" + "=" * 60)
print("Scenario 5: Large Dataset Processing")
print("=" * 60)

# Generate a large dataset
np.random.seed(42)
n_rows = 10000

# Create random Jalali dates
dates = []
for _ in range(n_rows):
    year = np.random.choice([1401, 1402, 1403])
    month = np.random.randint(1, 13)
    from jalali_pandas import days_in_month

    day = np.random.randint(1, days_in_month(year, month) + 1)
    dates.append(JalaliTimestamp(year, month, day))

df = pd.DataFrame(
    {
        "jalali_date": dates,
        "product": np.random.choice(["A", "B", "C", "D"], n_rows),
        "quantity": np.random.randint(1, 100, n_rows),
        "price": np.random.randint(10000, 100000, n_rows),
    }
)

# Calculate total
df["total"] = df["quantity"] * df["price"]

print(f"\nGenerated dataset with {len(df)} rows")
print("Sample data:")
print(df.head())

# Group by Jalali month
df["jmonth"] = df["jalali_date"].jalali.month
monthly_summary = df.groupby("jmonth").agg(
    {
        "total": ["sum", "mean", "count"],
    }
)

print("\nMonthly summary:")
print(monthly_summary.head())

# =============================================================================
# Scenario 6: Reading CSV with Persian Numerals
# =============================================================================

print("\n" + "=" * 60)
print("Scenario 6: Reading CSV with Persian Numerals")
print("=" * 60)

# CSV with Persian numerals (example)
csv_data_persian = """date,amount
۱۴۰۲/۰۱/۰۱,۱۰۰۰۰۰
۱۴۰۲/۰۱/۱۵,۱۵۰۰۰۰
"""

print("\nNote: CSV with Persian numerals requires preprocessing")
print("Persian numerals: ۰ ۱ ۲ ۳ ۴ ۵ ۶ ۷ ۸ ۹")
print("Arabic numerals:  0 1 2 3 4 5 6 7 8 9")


# Function to convert Persian numerals to Arabic
def persian_to_arabic_numerals(text):
    """Convert Persian numerals to Arabic numerals."""
    persian_nums = "۰۱۲۳۴۵۶۷۸۹"
    arabic_nums = "0123456789"
    translation_table = str.maketrans(persian_nums, arabic_nums)
    return text.translate(translation_table)


# Example usage
persian_date = "۱۴۰۲/۰۱/۰۱"
arabic_date = persian_to_arabic_numerals(persian_date)
print(f"\nPersian: {persian_date}")
print(f"Arabic:  {arabic_date}")

# =============================================================================
# Scenario 7: Exporting with Multiple Date Formats
# =============================================================================

print("\n" + "=" * 60)
print("Scenario 7: Exporting with Multiple Date Formats")
print("=" * 60)

df = pd.DataFrame(
    {
        "jalali_date": [
            JalaliTimestamp(1402, 1, 1),
            JalaliTimestamp(1402, 6, 15),
            JalaliTimestamp(1402, 12, 29),
        ],
        "value": [100, 200, 300],
    }
)

# Multiple export formats
df["format_ymd"] = df["jalali_date"].jalali.strftime("%Y-%m-%d")
df["format_ymd_slash"] = df["jalali_date"].jalali.strftime("%Y/%m/%d")
df["format_dmy"] = df["jalali_date"].jalali.strftime("%d-%m-%Y")
df["format_full"] = df["jalali_date"].jalali.strftime("%Y-%m-%d %H:%M:%S")

print("\nMultiple date formats for export:")
print(
    df[["jalali_date", "format_ymd", "format_ymd_slash", "format_dmy", "format_full"]]
)

# =============================================================================
# Scenario 8: Handling Missing or Invalid Dates in CSV
# =============================================================================

print("\n" + "=" * 60)
print("Scenario 8: Handling Missing or Invalid Dates in CSV")
print("=" * 60)

csv_data_invalid = """date,amount
1402-01-01,100000
,150000
invalid-date,200000
1402-13-01,250000
1402-01-32,300000
"""

df = pd.read_csv(io.StringIO(csv_data_invalid))
print("\nCSV with missing and invalid dates:")
print(df)


# Parse with error handling
def safe_parse_jalali(date_str):
    """Safely parse Jalali date, return NaT on error."""
    if pd.isna(date_str) or date_str == "":
        return pd.NaT

    try:
        return JalaliTimestamp.strptime(str(date_str), "%Y-%m-%d")
    except ValueError:
        return pd.NaT


df["parsed_date"] = df["date"].apply(safe_parse_jalali)
df["is_valid"] = df["parsed_date"].notna()

print("\nAfter parsing with error handling:")
print(df)

print(f"\nValid dates: {df['is_valid'].sum()}")
print(f"Invalid dates: {df['is_valid'].eq(False).sum()}")

# =============================================================================
# Scenario 9: Batch Processing Multiple CSV Files
# =============================================================================

print("\n" + "=" * 60)
print("Scenario 9: Batch Processing Multiple CSV Files")
print("=" * 60)

# Simulate multiple CSV files
csv_files = {
    "sales_jan.csv": """date,amount
1402-01-01,100000
1402-01-15,150000
""",
    "sales_feb.csv": """date,amount
1402-02-01,120000
1402-02-20,180000
""",
    "sales_mar.csv": """date,amount
1402-03-10,200000
1402-03-25,220000
""",
}

all_data = []

for filename, content in csv_files.items():
    df = pd.read_csv(io.StringIO(content))
    df["source_file"] = filename
    df["jalali_date"] = df["date"].jalali.parse_jalali("%Y-%m-%d")
    all_data.append(df)

# Combine all data
combined_df = pd.concat(all_data, ignore_index=True)
print("\nCombined data from multiple files:")
print(combined_df)

# Calculate totals by file
file_totals = combined_df.groupby("source_file")["amount"].sum()
print("\nTotals by file:")
print(file_totals)

# =============================================================================
# Scenario 10: Creating a Date Dimension Table
# =============================================================================

print("\n" + "=" * 60)
print("Scenario 10: Creating a Date Dimension Table")
print("=" * 60)

# Generate all dates for a Jalali year
dates = []
for month in range(1, 13):
    from jalali_pandas import days_in_month

    for day in range(1, days_in_month(1402, month) + 1):
        dates.append(JalaliTimestamp(1402, month, day))

date_dim = pd.DataFrame({"date": dates})

# Add date attributes using jalali accessor
date_dim["year"] = date_dim["date"].jalali.year
date_dim["month"] = date_dim["date"].jalali.month
date_dim["day"] = date_dim["date"].jalali.day
date_dim["quarter"] = date_dim["date"].jalali.quarter
date_dim["weekday"] = date_dim["date"].jalali.weekday
date_dim["dayofyear"] = date_dim["date"].jalali.dayofyear
date_dim["is_weekend"] = date_dim["weekday"] == 0  # Friday
date_dim["is_month_start"] = date_dim["day"] == 1
date_dim["is_month_end"] = date_dim["date"].apply(
    lambda x: x.day == days_in_month(x.year, x.month)
)
date_dim["is_quarter_start"] = date_dim["month"].isin([1, 4, 7, 10]) & (
    date_dim["day"] == 1
)
date_dim["is_quarter_end"] = date_dim.apply(
    lambda row: row["day"] == days_in_month(row["year"], row["month"])
    and row["month"] in [3, 6, 9, 12],
    axis=1,
)
date_dim["is_year_start"] = (date_dim["month"] == 1) & (date_dim["day"] == 1)
date_dim["is_year_end"] = date_dim.apply(
    lambda row: row["month"] == 12 and row["day"] == days_in_month(row["year"], 12),
    axis=1,
)

print("\nDate dimension table (first 10 rows):")
print(date_dim.head(10))

print(f"\nTotal rows: {len(date_dim)}")
print(f"Date range: {date_dim['date'].min()} to {date_dim['date'].max()}")
print(f"Weekend days: {date_dim['is_weekend'].sum()}")

print("\n" + "=" * 60)
print("Examples completed successfully!")
print("=" * 60)
