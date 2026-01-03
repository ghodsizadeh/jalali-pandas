# مثال: ایندکس و بازه تاریخ

منبع: `examples/05_index_and_date_range.py`

```python
import pandas as pd
import jalali_pandas as jp

idx = jp.JalaliDatetimeIndex(["1402-01-01", "1402-01-15"])

rng = jp.jalali_date_range("1402-01-01", periods=3, freq="JME")
```

```python
jalali = jp.to_jalali_datetime(pd.Timestamp("2023-09-06"))
back = jp.to_gregorian_datetime(jalali)
```
