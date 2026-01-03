# jalali_pandas

پشتیبانی کامل از تقویم جلالی (شمسی) برای pandas با انواع داده، ایندکس، افست‌ها
و اکسسورهای اختصاصی.

## نکات کلیدی

- نوع `JalaliTimestamp` برای تاریخ جلالی
- `JalaliDatetimeIndex` و `jalali_date_range` برای سری‌های زمانی
- تبدیل برداری تاریخ‌ها
- افست‌های جلالی با alias های JME/JMS/JQE/JQS/JYE/JYS/JW
- اکسسورهای `.jalali` برای Series و DataFrame
- ابزارهای گروه‌بندی و بازنمونه‌گیری بر اساس مرزهای جلالی

## مثال سریع

```python
import pandas as pd
import jalali_pandas as jp

s = pd.Series(pd.date_range("2023-03-21", periods=3, freq="D"))
j = s.jalali.to_jalali()

idx = jp.jalali_date_range("1402-01-01", periods=3, freq="D")
```

## مسیر بعدی

- نصب: `fa/installation.md`
- شروع سریع: `fa/quickstart.md`
- راهنمای کاربر: `fa/user-guide/core-types.md`
- مثال‌ها: `fa/examples/index.md`
