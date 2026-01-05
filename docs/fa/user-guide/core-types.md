# انواع اصلی

## JalaliTimestamp

`JalaliTimestamp` نوع اسکالر برای تاریخ‌های جلالی است.

```python
from jalali_pandas import JalaliTimestamp

ts = JalaliTimestamp(1402, 6, 15, 10, 30)
print(ts.year, ts.month, ts.day)
print(ts.to_gregorian())
```

متدها و ویژگی‌های مهم:

- `JalaliTimestamp.from_gregorian(pd.Timestamp)`
- `JalaliTimestamp.strptime(string, format)`
- `to_gregorian()`
- `normalize()`, `replace(...)`
- `tz_localize(...)`, `tz_convert(...)`

## JalaliDatetimeDtype

نوع داده افزونه‌ای pandas برای تاریخ جلالی.

```python
from jalali_pandas.core.dtypes import JalaliDatetimeDtype

dtype = JalaliDatetimeDtype()
```

## JalaliDatetimeArray

آرایه افزونه‌ای برای نگه‌داری مقادیر جلالی.

```python
from jalali_pandas.core.arrays import JalaliDatetimeArray
from jalali_pandas import JalaliTimestamp

arr = JalaliDatetimeArray._from_sequence(
    [JalaliTimestamp(1402, 1, 1), JalaliTimestamp(1402, 1, 2)]
)
```

## ابزارهای تقویم

```python
from jalali_pandas.core.calendar import is_leap_year, days_in_month, days_in_year

is_leap_year(1403)
days_in_month(1402, 12)
days_in_year(1402)
```
