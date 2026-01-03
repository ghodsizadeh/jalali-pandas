# Example: Offsets

Source: `examples/04_offsets.py`

```python
from jalali_pandas import JalaliTimestamp
from jalali_pandas.offsets import JalaliMonthEnd, JalaliWeek, FRIDAY

ts = JalaliTimestamp(1402, 6, 15)

next_month_end = ts + JalaliMonthEnd()
next_friday = ts + JalaliWeek(weekday=FRIDAY)
```

## Parse aliases

```python
from jalali_pandas.offsets import parse_jalali_frequency

parse_jalali_frequency("JME")
parse_jalali_frequency("2JQE")
```
