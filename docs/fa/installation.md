# نصب

## پیش‌نیازها

- پایتون 3.9+
- pandas >= 2.0
- numpy >= 1.23
- jdatetime >= 4.0

## نصب با pip

```bash
pip install -U jalali-pandas
```

## نصب با uv

```bash
uv pip install jalali-pandas
```

## افزونه‌های اختیاری (برای مشارکت)

```bash
uv sync --extra dev
uv sync --extra docs
```

## تأیید نصب

```python
import jalali_pandas as jp
import pandas as pd

print(f"نسخه jalali-pandas: {jp.__version__}")
ts = jp.JalaliTimestamp(1402, 6, 15)
gregorian = pd.Timestamp("2023-09-06")
jalali = jp.JalaliTimestamp.from_gregorian(gregorian)
print(f"تایم‌استمپ ایجاد شده: {ts}")
print(f"تبدیل شده: {gregorian} -> {jalali}")
```

خروجی مورد انتظار:

```
نسخه jalali-pandas: 1.0.0a1
تایم‌استمپ ایجاد شده: 1402-06-15 00:00:00
تبدیل شده: 2023-09-06 00:00:00 -> 1402-06-15 00:00:00
```
