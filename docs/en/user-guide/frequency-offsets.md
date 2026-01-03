# Frequency Offsets

Jalali offsets follow pandas-style DateOffset behavior but use Jalali calendar
rules (month lengths, leap years, Jalali quarters, and week boundaries).

## Offset classes

- `JalaliMonthBegin`, `JalaliMonthEnd`
- `JalaliQuarterBegin`, `JalaliQuarterEnd`
- `JalaliYearBegin`, `JalaliYearEnd`
- `JalaliWeek` (weekly offset, optional weekday anchor)

```python
from jalali_pandas import JalaliTimestamp
from jalali_pandas.offsets import JalaliMonthEnd, JalaliWeek, FRIDAY

ts = JalaliTimestamp(1402, 6, 15)
print(ts + JalaliMonthEnd())
print(ts + JalaliWeek(weekday=FRIDAY))
```

## Frequency aliases

Aliases are registered in `jalali_pandas.offsets.aliases`:

- JME / JMS
- JQE / JQS
- JYE / JYS
- JW (weekly, default weekday is Saturday)

```python
from jalali_pandas.offsets import parse_jalali_frequency, list_jalali_aliases

parse_jalali_frequency("JME")
parse_jalali_frequency("JW")  # Saturday by default
list_jalali_aliases()
```

To target a specific weekday, use `JalaliWeek(weekday=...)` directly. You can
register your own alias with `register_jalali_alias`.
