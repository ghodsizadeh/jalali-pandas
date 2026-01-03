# تبدیل‌ها

## توابع عمومی

- `to_jalali_datetime(...)`
- `to_gregorian_datetime(...)`

```python
import pandas as pd
import jalali_pandas as jp

jp.to_jalali_datetime("1402-06-15")

jp.to_jalali_datetime(pd.Timestamp("2023-09-06"))

jp.to_jalali_datetime(["1402-01-01", "1402-01-02"])

jidx = jp.JalaliDatetimeIndex(["1402-01-01", "1402-01-02"])
jp.to_gregorian_datetime(jidx)
```

## مدیریت خطا

`to_jalali_datetime(..., errors=...)` از این حالت‌ها پشتیبانی می‌کند:

- `"raise"` (پیش‌فرض)
- `"coerce"` → مقدار نامعتبر به `pd.NaT` تبدیل می‌شود
- `"ignore"` → فقط برای Series، ورودی بدون تغییر برگردانده می‌شود

## فرمت‌های پیش‌فرض رشته‌ای

در صورت `format=None` این فرمت‌ها به ترتیب تست می‌شوند:

- `%Y-%m-%d %H:%M:%S`
- `%Y-%m-%d`
- `%Y/%m/%d %H:%M:%S`
- `%Y/%m/%d`
- `%Y%m%d`

## توابع برداری داخلی

- `gregorian_to_jalali_vectorized`
- `jalali_to_gregorian_vectorized`
- `datetime64_to_jalali`
- `jalali_to_datetime64`
