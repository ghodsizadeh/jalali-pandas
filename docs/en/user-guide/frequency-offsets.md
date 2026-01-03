# Frequency Offsets

Jalali offsets follow pandas-style DateOffset behavior but use Jalali calendar
rules.

## Offset classes

- `JalaliMonthBegin`, `JalaliMonthEnd`
- `JalaliQuarterBegin`, `JalaliQuarterEnd`
- `JalaliYearBegin`, `JalaliYearEnd`
- `JalaliWeek` (custom weekday)

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
- JW

```python
from jalali_pandas.offsets import parse_jalali_frequency, list_jalali_aliases

parse_jalali_frequency("JME")
list_jalali_aliases()
```

You can register your own alias with `register_jalali_alias`.
