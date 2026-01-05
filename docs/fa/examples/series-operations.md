# مثال: عملیات سری

منبع: `examples/02_series_operations.py`

```python
import pandas as pd
import jalali_pandas

s = pd.Series(pd.date_range("2023-03-21", periods=3, freq="D"))
j = s.jalali.to_jalali()

j.jalali.year
j.jalali.month
j.jalali.day
```

```python
df = pd.DataFrame({"date_str": ["1402/01/01", "1402/01/15"]})
df["jdate"] = df["date_str"].jalali.parse_jalali("%Y/%m/%d")
```
