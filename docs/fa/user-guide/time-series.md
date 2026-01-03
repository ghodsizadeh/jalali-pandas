# عملیات سری زمانی

## JalaliGrouper

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

```python
df["jdate"] = df["date"].jalali.to_jalali()
df.jalali.resample("month")
```
