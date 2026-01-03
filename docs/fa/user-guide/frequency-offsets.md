# افست‌های فرکانسی

افست‌های جلالی مشابه DateOffset های pandas هستند اما قواعد تقویم جلالی را رعایت
می‌کنند.

## کلاس‌ها

- `JalaliMonthBegin`, `JalaliMonthEnd`
- `JalaliQuarterBegin`, `JalaliQuarterEnd`
- `JalaliYearBegin`, `JalaliYearEnd`
- `JalaliWeek` (با هفته دلخواه)

```python
from jalali_pandas import JalaliTimestamp
from jalali_pandas.offsets import JalaliMonthEnd, JalaliWeek, FRIDAY

ts = JalaliTimestamp(1402, 6, 15)
print(ts + JalaliMonthEnd())
print(ts + JalaliWeek(weekday=FRIDAY))
```

## alias ها

- JME / JMS
- JQE / JQS
- JYE / JYS
- JW

```python
from jalali_pandas.offsets import parse_jalali_frequency, list_jalali_aliases

parse_jalali_frequency("JME")
list_jalali_aliases()
```

با `register_jalali_alias` می‌توانید alias جدید ثبت کنید.
