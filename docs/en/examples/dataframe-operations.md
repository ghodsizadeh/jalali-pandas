# Example: DataFrame Operations

Source: `examples/03_dataframe_operations.py`

```python
import pandas as pd
import jalali_pandas

df = pd.DataFrame({
    "date": pd.date_range("2019-01-01", periods=6, freq="ME"),
    "sales": [100, 120, 90, 140, 160, 110],
})

df["jdate"] = df["date"].jalali.to_jalali()

yearly = df.jalali.groupby("year").sum(numeric_only=True)
```
