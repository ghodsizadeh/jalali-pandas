"""Basic usage examples for jalali-pandas.

This module demonstrates the fundamental features of jalali-pandas,
including JalaliTimestamp creation, conversion, and basic operations.
"""

from datetime import timedelta

import pandas as pd

import jalali_pandas  # noqa: F401 - registers accessors
from jalali_pandas import JalaliTimestamp

# =============================================================================
# JalaliTimestamp Creation
# =============================================================================

print("=" * 60)
print("JalaliTimestamp Creation")
print("=" * 60)

# Create from components
ts = JalaliTimestamp(1402, 6, 15)
print(f"From components: {ts}")

# Create with time
ts_with_time = JalaliTimestamp(1402, 6, 15, 14, 30, 45)
print(f"With time: {ts_with_time}")

# Create from Gregorian
gregorian = pd.Timestamp("2023-09-06")
ts_from_greg = JalaliTimestamp.from_gregorian(gregorian)
print(f"From Gregorian {gregorian}: {ts_from_greg}")

# Current time
ts_now = JalaliTimestamp.now()
print(f"Current time: {ts_now}")

# Today at midnight
ts_today = JalaliTimestamp.today()
print(f"Today: {ts_today}")

# =============================================================================
# JalaliTimestamp Properties
# =============================================================================

print("\n" + "=" * 60)
print("JalaliTimestamp Properties")
print("=" * 60)

ts = JalaliTimestamp(1402, 6, 15, 10, 30, 45)

print(f"Year: {ts.year}")
print(f"Month: {ts.month}")
print(f"Day: {ts.day}")
print(f"Hour: {ts.hour}")
print(f"Minute: {ts.minute}")
print(f"Second: {ts.second}")
print(f"Quarter: {ts.quarter}")
print(f"Day of week (0=Saturday): {ts.dayofweek}")
print(f"Day of year: {ts.dayofyear}")
print(f"Week of year: {ts.week}")
print(f"Days in month: {ts.days_in_month}")
print(f"Is leap year: {ts.is_leap_year}")
print(f"Is month start: {ts.is_month_start}")
print(f"Is month end: {ts.is_month_end}")

# =============================================================================
# Conversion
# =============================================================================

print("\n" + "=" * 60)
print("Conversion")
print("=" * 60)

ts = JalaliTimestamp(1402, 1, 1)
gregorian = ts.to_gregorian()
print(f"Jalali {ts} -> Gregorian {gregorian}")

# Round-trip conversion
restored = JalaliTimestamp.from_gregorian(gregorian)
print(f"Round-trip: {ts} -> {gregorian} -> {restored}")
print(f"Equal: {ts == restored}")

# =============================================================================
# Formatting
# =============================================================================

print("\n" + "=" * 60)
print("Formatting")
print("=" * 60)

ts = JalaliTimestamp(1402, 6, 15, 14, 30, 45)

print(f"strftime('%Y-%m-%d'): {ts.strftime('%Y-%m-%d')}")
print(f"strftime('%Y/%m/%d %H:%M'): {ts.strftime('%Y/%m/%d %H:%M')}")
print(f"isoformat(): {ts.isoformat()}")
print(f"str(): {str(ts)}")

# =============================================================================
# Arithmetic
# =============================================================================

print("\n" + "=" * 60)
print("Arithmetic")
print("=" * 60)

ts = JalaliTimestamp(1402, 1, 1)

# Add days
ts_plus_10 = ts + timedelta(days=10)
print(f"{ts} + 10 days = {ts_plus_10}")

# Subtract days
ts_minus_5 = ts - timedelta(days=5)
print(f"{ts} - 5 days = {ts_minus_5}")

# Difference between timestamps
ts1 = JalaliTimestamp(1402, 1, 15)
ts2 = JalaliTimestamp(1402, 1, 10)
diff = ts1 - ts2
print(f"{ts1} - {ts2} = {diff}")

# =============================================================================
# Comparison
# =============================================================================

print("\n" + "=" * 60)
print("Comparison")
print("=" * 60)

ts1 = JalaliTimestamp(1402, 6, 15)
ts2 = JalaliTimestamp(1402, 6, 16)
ts3 = JalaliTimestamp(1402, 6, 15)

print(f"{ts1} == {ts3}: {ts1 == ts3}")
print(f"{ts1} < {ts2}: {ts1 < ts2}")
print(f"{ts2} > {ts1}: {ts2 > ts1}")

# =============================================================================
# Replace and Normalize
# =============================================================================

print("\n" + "=" * 60)
print("Replace and Normalize")
print("=" * 60)

ts = JalaliTimestamp(1402, 6, 15, 14, 30, 45)

# Replace components
new_ts = ts.replace(year=1403, month=1)
print(f"Original: {ts}")
print(f"After replace(year=1403, month=1): {new_ts}")

# Normalize (set time to midnight)
normalized = ts.normalize()
print(f"Normalized: {normalized}")

print("\n" + "=" * 60)
print("Examples completed successfully!")
print("=" * 60)
