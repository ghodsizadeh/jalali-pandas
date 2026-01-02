"""Jalali calendar offsets examples.

This module demonstrates how to use Jalali calendar-aware offsets
for date arithmetic that respects Jalali calendar boundaries.
"""

from jalali_pandas import JalaliTimestamp
from jalali_pandas.offsets import (
    FRIDAY,
    JalaliMonthBegin,
    JalaliMonthEnd,
    JalaliQuarterBegin,
    JalaliQuarterEnd,
    JalaliWeek,
    JalaliYearBegin,
    JalaliYearEnd,
    parse_jalali_frequency,
)

# =============================================================================
# Month Offsets
# =============================================================================

print("=" * 60)
print("Month Offsets")
print("=" * 60)

ts = JalaliTimestamp(1402, 6, 15)
print(f"Starting date: {ts}")

# Month End
month_end = JalaliMonthEnd()
result = ts + month_end
print(f"+ JalaliMonthEnd(): {result}")

# Month Begin
month_begin = JalaliMonthBegin()
result = ts + month_begin
print(f"+ JalaliMonthBegin(): {result}")

# Multiple months
result = ts + JalaliMonthEnd(n=3)
print(f"+ JalaliMonthEnd(n=3): {result}")

# =============================================================================
# Quarter Offsets
# =============================================================================

print("\n" + "=" * 60)
print("Quarter Offsets")
print("=" * 60)

ts = JalaliTimestamp(1402, 2, 15)
print(f"Starting date: {ts}")

# Quarter End
quarter_end = JalaliQuarterEnd()
result = ts + quarter_end
print(f"+ JalaliQuarterEnd(): {result}")

# Quarter Begin
quarter_begin = JalaliQuarterBegin()
result = ts + quarter_begin
print(f"+ JalaliQuarterBegin(): {result}")

# Multiple quarters
result = ts + JalaliQuarterEnd(n=2)
print(f"+ JalaliQuarterEnd(n=2): {result}")

# =============================================================================
# Year Offsets
# =============================================================================

print("\n" + "=" * 60)
print("Year Offsets")
print("=" * 60)

ts = JalaliTimestamp(1402, 6, 15)
print(f"Starting date: {ts}")

# Year End (last day of Esfand)
year_end = JalaliYearEnd()
result = ts + year_end
print(f"+ JalaliYearEnd(): {result}")

# Year Begin (Nowruz - 1 Farvardin)
year_begin = JalaliYearBegin()
result = ts + year_begin
print(f"+ JalaliYearBegin(): {result}")

# Multiple years
result = ts + JalaliYearEnd(n=2)
print(f"+ JalaliYearEnd(n=2): {result}")

# =============================================================================
# Rollforward and Rollback
# =============================================================================

print("\n" + "=" * 60)
print("Rollforward and Rollback")
print("=" * 60)

ts = JalaliTimestamp(1402, 6, 15)
print(f"Starting date: {ts}")

# Rollforward to next month end
month_end = JalaliMonthEnd()
rolled = month_end.rollforward(ts)
print(f"Rollforward to month end: {rolled}")

# Rollback to previous month end
rolled_back = month_end.rollback(ts)
print(f"Rollback to month end: {rolled_back}")

# Check if on offset
print(f"Is {ts} on month end? {month_end.is_on_offset(ts)}")
print(f"Is {rolled} on month end? {month_end.is_on_offset(rolled)}")

# =============================================================================
# Leap Year Handling
# =============================================================================

print("\n" + "=" * 60)
print("Leap Year Handling")
print("=" * 60)

# 1403 is a leap year, 1402 is not
ts_non_leap = JalaliTimestamp(1402, 11, 15)
ts_leap = JalaliTimestamp(1403, 11, 15)

year_end = JalaliYearEnd()

result_non_leap = ts_non_leap + year_end
result_leap = ts_leap + year_end

print(f"Non-leap year (1402) year end: {result_non_leap}")
print(f"Leap year (1403) year end: {result_leap}")

# =============================================================================
# Offset Arithmetic
# =============================================================================

print("\n" + "=" * 60)
print("Offset Arithmetic")
print("=" * 60)

offset = JalaliMonthEnd()
print(f"Original offset: {offset}")

# Multiply
doubled = offset * 2
print(f"Multiplied by 2: {doubled}")

# Negate
negated = -offset
print(f"Negated: {negated}")

# Apply negated offset (go backwards)
ts = JalaliTimestamp(1402, 6, 15)
result = ts + negated
print(f"{ts} + negated offset = {result}")

# =============================================================================
# Week Offsets
# =============================================================================

print("\n" + "=" * 60)
print("Week Offsets")
print("=" * 60)

ts = JalaliTimestamp(1402, 6, 15)
print(f"Starting date: {ts} (weekday={ts.dayofweek})")

# Week offset (default: Saturday)
week = JalaliWeek()
result = ts + week
print(f"+ JalaliWeek(): {result} (weekday={result.dayofweek})")

# Week offset with custom weekday (Friday)
week_fri = JalaliWeek(weekday=FRIDAY)
result = ts + week_fri
print(f"+ JalaliWeek(weekday=FRIDAY): {result} (weekday={result.dayofweek})")

# Multiple weeks
result = ts + JalaliWeek(n=2)
print(f"+ JalaliWeek(n=2): {result}")

# =============================================================================
# Frequency Aliases
# =============================================================================

print("\n" + "=" * 60)
print("Frequency Aliases")
print("=" * 60)

# Parse frequency strings
parsed_offset = parse_jalali_frequency("JME")
print(f"parse_jalali_frequency('JME'): {parsed_offset}")

parsed_offset = parse_jalali_frequency("2JQE")
print(f"parse_jalali_frequency('2JQE'): {parsed_offset}")

parsed_offset = parse_jalali_frequency("-1JYS")
print(f"parse_jalali_frequency('-1JYS'): {parsed_offset}")

parsed_offset = parse_jalali_frequency("JW")
print(f"parse_jalali_frequency('JW'): {parsed_offset}")

print("\n" + "=" * 60)
print("Examples completed successfully!")
print("=" * 60)
