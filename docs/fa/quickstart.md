# شروع سریع

این بخش در چند دقیقه شما را با بخش‌های اصلی آشنا می‌کند.

## 1) ایمپورت و ثبت اکسسورها

```python
import pandas as pd
import jalali_pandas as jp
```

## 2) ساخت JalaliTimestamp

```python
from jalali_pandas import JalaliTimestamp

ts = JalaliTimestamp(1402, 6, 15)
```

## 3) تبدیل میلادی → جلالی

```python
gregorian = pd.Timestamp("2023-09-06")
jalali = jp.to_jalali_datetime(gregorian)
```

## 4) ساخت بازه تاریخ جلالی

```python
idx = jp.jalali_date_range("1402-01-01", periods=5, freq="D")
```

## 5) استفاده از اکسسورها

```python
s = pd.Series(pd.date_range("2023-03-21", periods=3, freq="D"))
jalali_series = s.jalali.to_jalali()
months = jalali_series.jalali.month
```

## 6) گروه‌بندی بر اساس سال جلالی

```python
df = pd.DataFrame({"date": s, "value": [1, 2, 3]})
df["jdate"] = df["date"].jalali.to_jalali()
result = df.jalali.groupby("year").sum(numeric_only=True)
```
