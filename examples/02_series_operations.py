"""Series operations examples for jalali-pandas.

This module demonstrates how to use the .jalali accessor on pandas Series
for converting and extracting Jalali date components.
"""

import pandas as pd

import jalali_pandas  # noqa: F401 - registers accessors

# =============================================================================
# Converting Gregorian to Jalali
# =============================================================================

print("=" * 60)
print("Converting Gregorian to Jalali")
print("=" * 60)

# Create a DataFrame with Gregorian dates
df = pd.DataFrame(
    {
        "date": pd.date_range("2023-03-21", periods=10, freq="D"),
        "value": range(10),
    }
)

print("Original DataFrame:")
print(df.head())

# Convert to Jalali
df["jdate"] = df["date"].jalali.to_jalali()
print("\nWith Jalali dates:")
print(df.head())

# =============================================================================
# Converting Jalali to Gregorian
# =============================================================================

print("\n" + "=" * 60)
print("Converting Jalali to Gregorian")
print("=" * 60)

# Convert back to Gregorian
df["gdate"] = df["jdate"].jalali.to_gregorian()
print("Converted back to Gregorian:")
print(df[["jdate", "gdate"]].head())

# =============================================================================
# Extracting Date Components
# =============================================================================

print("\n" + "=" * 60)
print("Extracting Date Components")
print("=" * 60)

# Extract various components
print(f"Years: {df['jdate'].jalali.year.tolist()}")
print(f"Months: {df['jdate'].jalali.month.tolist()}")
print(f"Days: {df['jdate'].jalali.day.tolist()}")
print(f"Weekdays: {df['jdate'].jalali.weekday.tolist()}")
print(f"Quarters: {df['jdate'].jalali.quarter.tolist()}")
print(f"Week numbers: {df['jdate'].jalali.weeknumber.tolist()}")

# =============================================================================
# Parsing Jalali Strings
# =============================================================================

print("\n" + "=" * 60)
print("Parsing Jalali Strings")
print("=" * 60)

# Create DataFrame with Jalali date strings
df_strings = pd.DataFrame(
    {
        "date_str": ["1402/01/01", "1402/01/15", "1402/02/01", "1402/06/15"],
        "value": [100, 200, 300, 400],
    }
)

print("DataFrame with string dates:")
print(df_strings)

# Parse strings to jdatetime
df_strings["jdate"] = df_strings["date_str"].jalali.parse_jalali("%Y/%m/%d")
print("\nParsed to jdatetime:")
print(df_strings)

# =============================================================================
# Time Components
# =============================================================================

print("\n" + "=" * 60)
print("Time Components")
print("=" * 60)

# Create dates with time
df_time = pd.DataFrame(
    {
        "date": pd.date_range("2023-03-21 10:30:00", periods=5, freq="h"),
    }
)
df_time["jdate"] = df_time["date"].jalali.to_jalali()

print("DataFrame with time:")
print(df_time)

print(f"\nHours: {df_time['jdate'].jalali.hour.tolist()}")
print(f"Minutes: {df_time['jdate'].jalali.minute.tolist()}")
print(f"Seconds: {df_time['jdate'].jalali.second.tolist()}")

print("\n" + "=" * 60)
print("Examples completed successfully!")
print("=" * 60)
