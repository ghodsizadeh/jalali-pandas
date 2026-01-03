# افست‌های فرکانسی

افست‌های جلالی شبیه DateOffset‌های pandas هستند اما قواعد تقویم جلالی را رعایت
می‌کنند (طول ماه‌ها، سال کبیسه، فصل‌ها و مرز هفته).

## کلاس‌ها

- `JalaliMonthBegin`, `JalaliMonthEnd`
- `JalaliQuarterBegin`, `JalaliQuarterEnd`
- `JalaliYearBegin`, `JalaliYearEnd`
- `JalaliWeek` (افست هفتگی با امکان تعیین روز هفته)

```python
from jalali_pandas import JalaliTimestamp
from jalali_pandas.offsets import JalaliMonthEnd, JalaliWeek, FRIDAY

ts = JalaliTimestamp(1402, 6, 15)
print(ts + JalaliMonthEnd())
print(ts + JalaliWeek(weekday=FRIDAY))
```

## نام‌های مستعار فرکانس

- JME / JMS
- JQE / JQS
- JYE / JYS
- JW (هفتگی، پیش‌فرض شنبه)

```python
from jalali_pandas.offsets import parse_jalali_frequency, list_jalali_aliases

parse_jalali_frequency("JME")
parse_jalali_frequency("JW")  # پیش‌فرض شنبه
list_jalali_aliases()
```

برای تعیین روز هفته خاص از `JalaliWeek(weekday=...)` استفاده کنید. با
`register_jalali_alias` می‌توانید نام مستعار جدید ثبت کنید.
