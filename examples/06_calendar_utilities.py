"""Calendar utilities examples for jalali-pandas.

This module demonstrates the calendar utility functions for checking
leap years and getting the number of days in months and years.
"""

import pandas as pd

import jalali_pandas as jp
from jalali_pandas import days_in_month, days_in_year, is_leap_year

# =============================================================================
# Leap Year Detection
# =============================================================================

print("=" * 60)
print("Leap Year Detection")
print("=" * 60)

# Check individual years
years_to_check = [1400, 1401, 1402, 1403, 1404, 1405]
for year in years_to_check:
    is_leap = is_leap_year(year)
    print(f"Year {year}: {'Leap year' if is_leap else 'Common year'}")

# Vectorized check with pandas
df_years = pd.DataFrame({"year": range(1395, 1410)})
df_years["is_leap"] = df_years["year"].apply(is_leap_year)
print("\nLeap years in range 1395-1409:")
print(df_years[df_years["is_leap"]])

# =============================================================================
# Days in Month
# =============================================================================

print("\n" + "=" * 60)
print("Days in Month")
print("=" * 60)

# Days in each month for a specific year
year = 1402
print(f"\nDays in each month for year {year}:")
for month in range(1, 13):
    days = days_in_month(year, month)
    print(f"  Month {month:2d}: {days} days")

# Compare leap vs common year (Esfand is month 12)
print("\nDays in Esfand (month 12):")
print(f"  1402 (common): {days_in_month(1402, 12)} days")
print(f"  1403 (leap):   {days_in_month(1403, 12)} days")

# Vectorized with DataFrame
df_months = pd.DataFrame({"year": [1402, 1403], "month": [12, 12]})
df_months["days"] = df_months.apply(
    lambda row: days_in_month(row["year"], row["month"]), axis=1
)
print("\nDays in Esfand for different years:")
print(df_months)

# =============================================================================
# Days in Year
# =============================================================================

print("\n" + "=" * 60)
print("Days in Year")
print("=" * 60)

# Check multiple years
years = [1400, 1401, 1402, 1403, 1404]
for year in years:
    days = days_in_year(year)
    is_leap = is_leap_year(year)
    print(f"Year {year}: {days} days ({'leap' if is_leap else 'common'})")

# Vectorized check
df_year_days = pd.DataFrame({"year": range(1400, 1410)})
df_year_days["days"] = df_year_days["year"].apply(days_in_year)
df_year_days["is_leap"] = df_year_days["year"].apply(is_leap_year)
print("\nDays in year for 1400-1409:")
print(df_year_days)

# =============================================================================
# Practical Use Cases
# =============================================================================

print("\n" + "=" * 60)
print("Practical Use Cases")
print("=" * 60)

# Use case 1: Calculate last day of month
print("\nUse case 1: Find last day of month")
ts = jp.JalaliTimestamp(1402, 6, 15)
last_day = days_in_month(ts.year, ts.month)
print(f"  Date: {ts}")
print(f"  Last day of month: {last_day}")
print(
    f"  Last day of month as timestamp: {jp.JalaliTimestamp(ts.year, ts.month, last_day)}"
)

# Use case 2: Validate date
print("\nUse case 2: Validate if date exists")


def is_valid_jalali_date(year, month, day):
    """Check if a Jalali date is valid."""
    try:
        return day <= days_in_month(year, month)
    except ValueError:
        return False


test_dates = [
    (1402, 6, 31),  # Valid (Shahrivar has 31 days)
    (1402, 7, 31),  # Invalid (Mehr has 30 days)
    (1403, 12, 30),  # Valid (leap year)
    (1402, 12, 30),  # Invalid (common year)
]

for year, month, day in test_dates:
    valid = is_valid_jalali_date(year, month, day)
    print(f"  {year}/{month:02d}/{day:02d}: {'Valid' if valid else 'Invalid'}")

# Use case 3: Calculate day of year from date components
print("\nUse case 3: Calculate day of year")


def calculate_day_of_year(year, month, day):
    """Calculate day of year from date components."""
    day_of_year = sum(days_in_month(year, m) for m in range(1, month)) + day
    return day_of_year


test_date = (1402, 6, 15)
doy = calculate_day_of_year(*test_date)
print(f"  Date: {test_date[0]}/{test_date[1]:02d}/{test_date[2]:02d}")
print(f"  Day of year: {doy}")

# Verify with JalaliTimestamp
ts_verify = jp.JalaliTimestamp(*test_date)
print(f"  Verified with JalaliTimestamp: {ts_verify.dayofyear}")

# Use case 4: Generate date range for a specific month
print("\nUse case 4: Generate all dates in a month")
year, month = 1402, 6
days = days_in_month(year, month)
dates = [jp.JalaliTimestamp(year, month, day) for day in range(1, days + 1)]
print(f"  All dates in {year}/{month:02d}:")
print(f"  First: {dates[0]}")
print(f"  Last:  {dates[-1]}")
print(f"  Total: {len(dates)} days")

# Use case 5: Calculate percentage of year passed
print("\nUse case 5: Calculate percentage of year passed")


def year_percentage(year, month, day):
    """Calculate what percentage of the year has passed."""
    day_of_year = calculate_day_of_year(year, month, day)
    total_days = days_in_year(year)
    return (day_of_year / total_days) * 100


date = (1402, 6, 15)
percentage = year_percentage(*date)
print(f"  Date: {date[0]}/{date[1]:02d}/{date[2]:02d}")
print(f"  Percentage of year passed: {percentage:.2f}%")

# =============================================================================
# Edge Cases and Special Dates
# =============================================================================

print("\n" + "=" * 60)
print("Edge Cases and Special Dates")
print("=" * 60)

# Nowruz (first day of year)
nowruz = jp.JalaliTimestamp(1402, 1, 1)
print(f"\nNowruz 1402: {nowruz}")
print(f"  Day of year: {nowruz.dayofyear}")
print(f"  Days in year: {days_in_year(1402)}")

# Last day of leap year
last_day_1403 = jp.JalaliTimestamp(1403, 12, 30)
print(f"\nLast day of 1403 (leap year): {last_day_1403}")
print(f"  Day of year: {last_day_1403.dayofyear}")
print(f"  Days in year: {days_in_year(1403)}")

# Last day of common year
last_day_1402 = jp.JalaliTimestamp(1402, 12, 29)
print(f"\nLast day of 1402 (common year): {last_day_1402}")
print(f"  Day of year: {last_day_1402.dayofyear}")
print(f"  Days in year: {days_in_year(1402)}")

print("\n" + "=" * 60)
print("Examples completed successfully!")
print("=" * 60)
