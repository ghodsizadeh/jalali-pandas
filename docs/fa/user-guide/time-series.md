# عملیات سری زمانی

## مرور کلی

دو مسیر اصلی وجود دارد:

1. **تاریخ‌های میلادی/ایندکس میلادی** → از `JalaliGrouper`،
   `jalali_groupby` یا `resample_jalali` استفاده کنید.
2. **ستون‌های `jdatetime`** → از اکسسور دیتافریم
   (`df.jalali.groupby(...)` و `df.jalali.resample(...)`) استفاده کنید.

`JalaliGrouper` و `resample_jalali` تاریخ‌های میلادی را انتظار دارند. اگر
مقادیر `jdatetime` دارید، آن‌ها را به میلادی تبدیل کنید یا از اکسسور دیتافریم
استفاده کنید.

## JalaliGrouper

`JalaliGrouper` گروه‌بندی را بر اساس مرزهای جلالی انجام می‌دهد و برچسب‌ها
به صورت `pd.Timestamp` (میلادی) هستند.

```python
import pandas as pd
from jalali_pandas.api import JalaliGrouper

df = pd.DataFrame({
    "date": pd.date_range("2023-03-21", periods=10, freq="D"),
    "value": range(10),
})

grouper = JalaliGrouper(key="date", freq="JME")
result = df.groupby(grouper.get_grouper(df)).sum()
```

## jalali_groupby

```python
from jalali_pandas.api import jalali_groupby

result = jalali_groupby(df, key="date", freq="JME").sum()
```

## JalaliResampler و resample_jalali

`JalaliResampler` نیاز به `pd.DatetimeIndex` دارد.

```python
from jalali_pandas.api import resample_jalali

series = df.set_index("date")["value"]
resampled = resample_jalali(series, freq="JME").sum()
```

## resample در اکسسور دیتافریم

`JalaliDataFrameAccessor.resample()` از گروه‌بندی ماه/فصل/سال/هفته پشتیبانی
می‌کند (برای دیتافریم با ستون `jdatetime`).

```python
df["jdate"] = df["date"].jalali.to_jalali()
monthly = df.jalali.resample("month")
```
