"""
Example 05: JalaliDatetimeIndex and Date Range Generation

This example demonstrates:
- Creating JalaliDatetimeIndex from various inputs
- Using jalali_date_range() to generate date ranges
- Time series indexing with Jalali dates
- Conversion functions (to_jalali_datetime, to_gregorian_datetime)
"""

import pandas as pd

import jalali_pandas as jp

print("=" * 60)
print("Example 05: JalaliDatetimeIndex and Date Range Generation")
print("=" * 60)

# -----------------------------------------------------------------------------
# 1. Creating JalaliDatetimeIndex
# -----------------------------------------------------------------------------
print("\n1. Creating JalaliDatetimeIndex")
print("-" * 40)

# From list of strings
idx = jp.JalaliDatetimeIndex(["1402-01-01", "1402-01-15", "1402-02-01"])
print(f"From strings: {idx}")

# From list of JalaliTimestamp
timestamps = [
    jp.JalaliTimestamp(1402, 6, 1),
    jp.JalaliTimestamp(1402, 6, 15),
    jp.JalaliTimestamp(1402, 6, 31),
]
idx = jp.JalaliDatetimeIndex(timestamps)
print(f"From timestamps: {idx}")

# With name
idx = jp.JalaliDatetimeIndex(["1402-01-01", "1402-01-02"], name="dates")
print(f"With name: {idx}")

# -----------------------------------------------------------------------------
# 2. Using jalali_date_range()
# -----------------------------------------------------------------------------
print("\n2. Using jalali_date_range()")
print("-" * 40)

# Daily range with start and periods
daily = jp.jalali_date_range("1402-01-01", periods=5, freq="D")
print(f"Daily (5 days): {daily}")

# Daily range with start and end
daily = jp.jalali_date_range("1402-01-01", "1402-01-10", freq="D")
print(f"Daily (start to end): {daily}")

# Hourly range
hourly = jp.jalali_date_range("1402-01-01", periods=4, freq="H")
print(f"Hourly: {hourly}")

# Monthly (Jalali month end)
monthly = jp.jalali_date_range("1402-01-01", periods=6, freq="JME")
print(f"Monthly (JME): {monthly}")

# Quarterly (Jalali quarter end)
quarterly = jp.jalali_date_range("1402-01-01", periods=4, freq="JQE")
print(f"Quarterly (JQE): {quarterly}")

# Yearly (Jalali year end)
yearly = jp.jalali_date_range("1400-01-01", periods=3, freq="JYE")
print(f"Yearly (JYE): {yearly}")

# With multiplier
every_2_days = jp.jalali_date_range("1402-01-01", periods=5, freq="2D")
print(f"Every 2 days: {every_2_days}")

# -----------------------------------------------------------------------------
# 3. JalaliDatetimeIndex Properties
# -----------------------------------------------------------------------------
print("\n3. JalaliDatetimeIndex Properties")
print("-" * 40)

idx = jp.jalali_date_range("1402-01-15", periods=4, freq="JME")
print(f"Index: {idx}")
print(f"Year: {list(idx.year)}")
print(f"Month: {list(idx.month)}")
print(f"Day: {list(idx.day)}")
print(f"Quarter: {list(idx.quarter)}")

# -----------------------------------------------------------------------------
# 4. Time Series with JalaliDatetimeIndex
# -----------------------------------------------------------------------------
print("\n4. Time Series with JalaliDatetimeIndex")
print("-" * 40)

# Create a time series with Jalali index
idx = jp.jalali_date_range("1402-01-01", periods=10, freq="D")
data = [100 + i * 5 for i in range(10)]
series = pd.Series(data, index=idx, name="sales")
print("Time series with Jalali index:")
print(series)

# -----------------------------------------------------------------------------
# 5. Indexing Operations
# -----------------------------------------------------------------------------
print("\n5. Indexing Operations")
print("-" * 40)

idx = jp.jalali_date_range("1402-01-01", periods=30, freq="D")
series = pd.Series(range(30), index=idx)

# Get location by string
loc = idx.get_loc("1402-01-15")
print(f"Location of '1402-01-15': {loc}")

# Partial string indexing - by year-month
mask = idx.get_loc("1402-01")
print(f"Dates in 1402-01: {mask.sum()} dates")  # type: ignore[union-attr]

# Check if date is in index
ts = jp.JalaliTimestamp(1402, 1, 5)
print(f"1402-01-05 in index: {ts in idx}")

# -----------------------------------------------------------------------------
# 6. Conversion Functions
# -----------------------------------------------------------------------------
print("\n6. Conversion Functions")
print("-" * 40)

# to_jalali_datetime - from string
jalali = jp.to_jalali_datetime("1402-06-15")
print(f"String to Jalali: {jalali}")

# to_jalali_datetime - from pandas Timestamp (Gregorian)
gregorian_ts = pd.Timestamp("2023-09-06")
jalali = jp.to_jalali_datetime(gregorian_ts)
print(f"Gregorian {gregorian_ts} -> Jalali {jalali}")

# to_jalali_datetime - from list
jalali_idx = jp.to_jalali_datetime(["1402-01-01", "1402-06-15", "1402-12-29"])
print(f"List to JalaliDatetimeIndex: {jalali_idx}")

# to_jalali_datetime - from DatetimeIndex
dti = pd.DatetimeIndex(["2023-03-21", "2023-09-06"])
jalali_idx = jp.to_jalali_datetime(dti)
print(f"DatetimeIndex to Jalali: {jalali_idx}")

# to_gregorian_datetime - from JalaliTimestamp
jalali = jp.JalaliTimestamp(1402, 6, 15)
gregorian = jp.to_gregorian_datetime(jalali)
print(f"Jalali {jalali} -> Gregorian {gregorian}")

# to_gregorian_datetime - from JalaliDatetimeIndex
jalali_idx = jp.JalaliDatetimeIndex(["1402-01-01", "1402-06-15"])
gregorian_idx = jp.to_gregorian_datetime(jalali_idx)
print(f"JalaliDatetimeIndex to DatetimeIndex: {gregorian_idx}")

# -----------------------------------------------------------------------------
# 7. Set Operations
# -----------------------------------------------------------------------------
print("\n7. Set Operations")
print("-" * 40)

idx1 = jp.JalaliDatetimeIndex(["1402-01-01", "1402-01-02", "1402-01-03"])
idx2 = jp.JalaliDatetimeIndex(["1402-01-02", "1402-01-03", "1402-01-04"])

union = idx1.union(idx2)
print(f"Union: {union}")

intersection = idx1.intersection(idx2)
print(f"Intersection: {intersection}")

difference = idx1.difference(idx2)
print(f"Difference: {difference}")

# -----------------------------------------------------------------------------
# 8. Shift Operations
# -----------------------------------------------------------------------------
print("\n8. Shift Operations")
print("-" * 40)

idx = jp.jalali_date_range("1402-01-01", periods=3, freq="D")
print(f"Original: {idx}")

shifted = idx.shift(1, freq=pd.Timedelta(days=1))
print(f"Shifted by 1 day: {shifted}")

# Shift with Jalali offset
shifted = idx.shift(1, freq=jp.JalaliMonthEnd())
print(f"Shifted by 1 month end: {shifted}")

# -----------------------------------------------------------------------------
# 9. Round-trip Conversion
# -----------------------------------------------------------------------------
print("\n9. Round-trip Conversion")
print("-" * 40)

# Gregorian -> Jalali -> Gregorian
original = pd.Timestamp("2023-09-06 14:30:00")
jalali = jp.to_jalali_datetime(original)
back = jp.to_gregorian_datetime(jalali)
print(f"Original: {original}")
print(f"To Jalali: {jalali}")
print(f"Back to Gregorian: {back}")
print(f"Round-trip successful: {original == back}")

print("\n" + "=" * 60)
print("Example complete!")
print("=" * 60)
