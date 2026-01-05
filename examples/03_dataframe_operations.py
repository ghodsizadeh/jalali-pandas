"""DataFrame operations examples for jalali-pandas.

This module demonstrates how to use the .jalali accessor on pandas DataFrames
for grouping and aggregating data by Jalali date components.
"""

import pandas as pd

import jalali_pandas  # noqa: F401 - registers accessors

# =============================================================================
# Setup: Create Sample DataFrame
# =============================================================================

print("=" * 60)
print("Sample DataFrame Setup")
print("=" * 60)

# Create a DataFrame with monthly data spanning 2 years
df = pd.DataFrame(
    {
        "date": pd.date_range("2019-01-01", periods=24, freq="ME"),
        "sales": [100 + i * 10 for i in range(24)],
        "category": ["A", "B"] * 12,
    }
)

# Convert to Jalali
df["jdate"] = df["date"].jalali.to_jalali()

print("Sample DataFrame:")
print(df.head(10))

# =============================================================================
# Grouping by Year
# =============================================================================

print("\n" + "=" * 60)
print("Grouping by Year")
print("=" * 60)

yearly = df.jalali.groupby("year").sum(numeric_only=True)
print("Sum by Jalali year:")
print(yearly)

# =============================================================================
# Grouping by Month
# =============================================================================

print("\n" + "=" * 60)
print("Grouping by Month")
print("=" * 60)

monthly = df.jalali.groupby("month").mean(numeric_only=True)
print("Mean by Jalali month:")
print(monthly)

# =============================================================================
# Grouping by Year-Month
# =============================================================================

print("\n" + "=" * 60)
print("Grouping by Year-Month (ym)")
print("=" * 60)

ym = df.jalali.groupby("ym").sum(numeric_only=True)
print("Sum by Jalali year-month:")
print(ym.head(10))

# =============================================================================
# Grouping by Quarter
# =============================================================================

print("\n" + "=" * 60)
print("Grouping by Quarter")
print("=" * 60)

quarterly = df.jalali.groupby("quarter").sum(numeric_only=True)
print("Sum by Jalali quarter:")
print(quarterly)

# =============================================================================
# Grouping by Year-Quarter
# =============================================================================

print("\n" + "=" * 60)
print("Grouping by Year-Quarter (yq)")
print("=" * 60)

yq = df.jalali.groupby("yq").sum(numeric_only=True)
print("Sum by Jalali year-quarter:")
print(yq)

# =============================================================================
# Multiple Grouping Keys
# =============================================================================

print("\n" + "=" * 60)
print("Multiple Grouping Keys")
print("=" * 60)

multi = df.jalali.groupby("yq").sum(numeric_only=True)
print("Sum by Jalali year and quarter:")
print(multi)

# =============================================================================
# Aggregation Functions
# =============================================================================

print("\n" + "=" * 60)
print("Various Aggregation Functions")
print("=" * 60)

print("\nMin by year:")
print(df.jalali.groupby("year").min(numeric_only=True))

print("\nMax by year:")
print(df.jalali.groupby("year").max(numeric_only=True))

print("\nCount by year:")
print(df.jalali.groupby("year").count())

print("\n" + "=" * 60)
print("Examples completed successfully!")
print("=" * 60)
