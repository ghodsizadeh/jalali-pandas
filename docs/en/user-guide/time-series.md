# Time Series Operations

## JalaliGrouper

Use `JalaliGrouper` to create group labels based on Jalali boundaries.

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

## JalaliResampler and resample_jalali

`JalaliResampler` groups by Jalali period boundaries but requires a
`pd.DatetimeIndex` as index.

```python
from jalali_pandas.api import resample_jalali

series = df.set_index("date")["value"]
resampled = resample_jalali(series, freq="JME").sum()
```

## DataFrame accessor resample

`JalaliDataFrameAccessor.resample()` supports month/quarter/year grouping for
DataFrames that contain a jdatetime column.

```python
df["jdate"] = df["date"].jalali.to_jalali()
df.jalali.resample("month")
```
