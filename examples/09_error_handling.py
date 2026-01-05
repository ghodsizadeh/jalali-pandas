"""Error handling and edge cases examples for jalali-pandas.

This module demonstrates how to handle errors, invalid dates, and edge cases
when working with Jalali dates in pandas.
"""

import pandas as pd

from jalali_pandas import JalaliTimestamp, to_jalali_datetime

# =============================================================================
# Invalid Date Handling
# =============================================================================

print("=" * 60)
print("Invalid Date Handling")
print("=" * 60)

# Try to create invalid dates
invalid_dates = [
    (1402, 7, 31),  # Mehr has 30 days
    (1402, 12, 30),  # Esfand has 29 days in common year
    (1403, 12, 31),  # Esfand has 30 days in leap year
    (1402, 13, 1),  # Invalid month
    (1402, 0, 1),  # Invalid month
]

print("\nAttempting to create invalid dates:")
for year, month, day in invalid_dates:
    try:
        ts = JalaliTimestamp(year, month, day)
        print(f"  {year}/{month:02d}/{day:02d}: {ts} (Valid)")
    except ValueError as e:
        print(f"  {year}/{month:02d}/{day:02d}: ERROR - {e}")

# =============================================================================
# Leap Year Edge Cases
# =============================================================================

print("\n" + "=" * 60)
print("Leap Year Edge Cases")
print("=" * 60)

# Esfand 30 in leap year vs common year
try:
    leap_year_ts = JalaliTimestamp(1403, 12, 30)
    print(f"1403/12/30 (leap year): {leap_year_ts} - Valid")
except ValueError as e:
    print(f"1403/12/30 (leap year): ERROR - {e}")

try:
    common_year_ts = JalaliTimestamp(1402, 12, 30)
    print(f"1402/12/30 (common year): {common_year_ts} - Valid")
except ValueError as e:
    print(f"1402/12/30 (common year): ERROR - {e}")

# =============================================================================
# String Parsing Errors
# =============================================================================

print("\n" + "=" * 60)
print("String Parsing Errors")
print("=" * 60)

invalid_strings = [
    "1402/13/01",  # Invalid month
    "1402/07/32",  # Invalid day
    "2023-09-06",  # Gregorian format (not recognized as Jalali)
    "not-a-date",  # Invalid format
    "1402-02-30",  # Invalid day for Esfand in common year
]

print("\nAttempting to parse invalid strings:")
for date_str in invalid_strings:
    try:
        ts = JalaliTimestamp.strptime(date_str, "%Y-%m-%d")
        print(f"  '{date_str}': {ts}")
    except ValueError as e:
        print(f"  '{date_str}': ERROR - {str(e)[:60]}...")

# =============================================================================
# Handling NaT (Not a Time) Values
# =============================================================================

print("\n" + "=" * 60)
print("Handling NaT (Not a Time) Values")
print("=" * 60)

# Create Series with NaT values
dates_with_nat = pd.Series(
    [
        "1402-01-01",
        None,
        "1402-01-03",
        pd.NaT,
        "1402-01-05",
    ]
)

print("\nSeries with NaT values:")
print(dates_with_nat)

# Parse with errors='coerce'
parsed_series = dates_with_nat.jalali.parse_jalali("%Y-%m-%d")
print("\nParsed with errors='coerce':")
print(parsed_series)

# Check for NaT values
print(f"\nNumber of NaT values: {parsed_series.isna().sum()}")
print(f"Number of valid values: {parsed_series.notna().sum()}")

# =============================================================================
# Conversion Errors
# =============================================================================

print("\n" + "=" * 60)
print("Conversion Errors")
print("=" * 60)

# Converting invalid data types
invalid_inputs = [
    12345,  # Integer
    3.14,  # Float
    {"year": 1402},  # Dict
    [1402, 6, 15],  # List (not string)
]

print("\nAttempting to convert invalid inputs:")
for inp in invalid_inputs:
    try:
        result = to_jalali_datetime(inp)
        print(f"  {type(inp).__name__}: {result}")
    except (TypeError, ValueError) as e:
        print(f"  {type(inp).__name__}: ERROR - {str(e)[:60]}...")

# =============================================================================
# Edge Case: Month Boundaries
# =============================================================================

print("\n" + "=" * 60)
print("Edge Case: Month Boundaries")
print("=" * 60)

# Last day of each month
print("\nLast day of each month in 1402:")
for month in range(1, 13):
    from jalali_pandas import days_in_month

    last_day = days_in_month(1402, month)
    ts = JalaliTimestamp(1402, month, last_day)
    print(f"  Month {month:2d}: {ts.strftime('%Y-%m-%d (%A)')}")

# First day of each month
print("\nFirst day of each month in 1402:")
for month in range(1, 13):
    ts = JalaliTimestamp(1402, month, 1)
    print(f"  Month {month:2d}: {ts.strftime('%Y-%m-%d (%A)')}")

# =============================================================================
# Edge Case: Year Boundaries
# =============================================================================

print("\n" + "=" * 60)
print("Edge Case: Year Boundaries")
print("=" * 60)

# Last day of year 1402
last_day_1402 = JalaliTimestamp(1402, 12, 29)
print(f"Last day of 1402: {last_day_1402}")
print(f"  Day of week: {last_day_1402.strftime('%A')}")

# First day of year 1403
first_day_1403 = JalaliTimestamp(1403, 1, 1)
print(f"First day of 1403: {first_day_1403}")
print(f"  Day of week: {first_day_1403.strftime('%A')}")

# Difference
diff = first_day_1403 - last_day_1402
print(f"Days between: {diff.days}")

# =============================================================================
# Edge Case: Time Component Validation
# =============================================================================

print("\n" + "=" * 60)
print("Edge Case: Time Component Validation")
print("=" * 60)

invalid_times = [
    (1402, 6, 15, 24, 0, 0),  # Invalid hour
    (1402, 6, 15, 23, 60, 0),  # Invalid minute
    (1402, 6, 15, 23, 59, 60),  # Invalid second
    (1402, 6, 15, -1, 0, 0),  # Negative hour
]

print("\nAttempting to create timestamps with invalid times:")
for year, month, day, hour, minute, second in invalid_times:
    try:
        ts = JalaliTimestamp(year, month, day, hour, minute, second)
        print(
            f"  {year}/{month:02d}/{day:02d} {hour:02d}:{minute:02d}:{second:02d}: {ts}"
        )
    except ValueError as e:
        print(
            f"  {year}/{month:02d}/{day:02d} {hour:02d}:{minute:02d}:{second:02d}: ERROR - {e}"
        )

# =============================================================================
# Edge Case: Date Arithmetic at Boundaries
# =============================================================================

print("\n" + "=" * 60)
print("Edge Case: Date Arithmetic at Boundaries")
print("=" * 60)

from datetime import timedelta

# Last day of month + 1 day
ts = JalaliTimestamp(1402, 6, 31)  # Last day of Shahrivar
next_day = ts + timedelta(days=1)
print(f"Last day of Shahrivar: {ts}")
print(f"+ 1 day: {next_day}")

# Last day of year + 1 day
ts = JalaliTimestamp(1402, 12, 29)  # Last day of 1402
next_day = ts + timedelta(days=1)
print(f"\nLast day of 1402: {ts}")
print(f"+ 1 day: {next_day}")

# First day of year - 1 day
ts = JalaliTimestamp(1403, 1, 1)  # First day of 1403
prev_day = ts - timedelta(days=1)
print(f"\nFirst day of 1403: {ts}")
print(f"- 1 day: {prev_day}")

# =============================================================================
# Handling Mixed Date Formats in DataFrame
# =============================================================================

print("\n" + "=" * 60)
print("Handling Mixed Date Formats in DataFrame")
print("=" * 60)

df = pd.DataFrame(
    {
        "date_str": [
            "1402-01-01",
            "1402/01/02",
            "14020103",  # Compact format
            None,
            "invalid-date",
            "1402-01-06",
        ]
    }
)

print("\nDataFrame with mixed date formats:")
print(df)


# Try to parse with different formats
def parse_mixed_dates(date_str):
    """Try multiple date formats."""
    if pd.isna(date_str):
        return pd.NaT

    formats = ["%Y-%m-%d", "%Y/%m/%d", "%Y%m%d"]
    for fmt in formats:
        try:
            return JalaliTimestamp.strptime(date_str, fmt)
        except ValueError:
            continue

    return pd.NaT


df["parsed_date"] = df["date_str"].apply(parse_mixed_dates)
print("\nParsed dates:")
print(df)

# =============================================================================
# Best Practices for Error Handling
# =============================================================================

print("\n" + "=" * 60)
print("Best Practices for Error Handling")
print("=" * 60)

print("\n1. Always validate dates before creating JalaliTimestamp:")


def safe_create_jalali_timestamp(year, month, day):
    """Safely create JalaliTimestamp with validation."""
    from jalali_pandas import days_in_month

    # Validate month
    if not 1 <= month <= 12:
        raise ValueError(f"Month must be 1-12, got {month}")

    # Validate day
    max_days = days_in_month(year, month)
    if not 1 <= day <= max_days:
        raise ValueError(
            f"Day must be 1-{max_days} for month {month} in year {year}, got {day}"
        )

    return JalaliTimestamp(year, month, day)


try:
    ts = safe_create_jalali_timestamp(1402, 6, 31)
    print(f"  Valid date: {ts}")
except ValueError as e:
    print(f"  Validation error: {e}")

print("\n2. Use errors='coerce' when parsing potentially invalid data:")
dates = pd.Series(["1402-01-01", "invalid", None, "1402-01-04"])
parsed = dates.jalali.parse_jalali("%Y-%m-%d")
print(f"  Original: {dates.tolist()}")
print(f"  Parsed: {parsed.tolist()}")

print("\n3. Always check for NaT values before operations:")
series = pd.Series([JalaliTimestamp(1402, 1, 1), pd.NaT, JalaliTimestamp(1402, 1, 3)])
valid_only = series.dropna()
print(f"  Original count: {len(series)}")
print(f"  Valid count: {len(valid_only)}")

print("\n4. Use try-except for date arithmetic at boundaries:")
try:
    ts = JalaliTimestamp(1402, 12, 29)
    next_day = ts + timedelta(days=365)
    print(f"  {ts} + 365 days = {next_day}")
except OverflowError as e:
    print(f"  Arithmetic error: {e}")

print("\n" + "=" * 60)
print("Examples completed successfully!")
print("=" * 60)
