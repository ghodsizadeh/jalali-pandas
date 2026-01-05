# Index & Range Generation

## JalaliDatetimeIndex

`JalaliDatetimeIndex` is the Jalali-native index type for Series and DataFrames.

```python
import jalali_pandas as jp

idx = jp.JalaliDatetimeIndex(["1402-01-01", "1402-01-02"], name="dates")
gregorian = idx.to_gregorian()
```

### Useful operations

- Partial string indexing with `get_loc("1402")` or `get_loc("1402-01")`
- Set ops: `union`, `intersection`, `difference`
- Shifts with `shift(periods=..., freq=...)`
- Snap to frequency with `snap(freq="s")`

```python
idx = jp.jalali_date_range("1402-01-01", periods=40)
mask = idx.get_loc("1402-02")  # boolean mask for a Jalali month
subset = idx[mask]
```

```python
shifted = idx.shift(periods=1, freq="JME")
daily_shift = idx.shift(periods=1, freq="1D")
```

## jalali_date_range

```python
import jalali_pandas as jp

jp.jalali_date_range("1402-01-01", periods=5, freq="D")
jp.jalali_date_range("1402-01-01", "1402-01-10", freq="D")
jp.jalali_date_range("1402-01-01", periods=3, freq="JME")
```

### Parameters

- Provide at least two of `start`, `end`, `periods`.
- If all three are provided, `freq` is required.
- `freq` accepts Jalali aliases (JME/JMS/JQE/JQS/JYE/JYS/JW) or common pandas
  frequencies (D/H/MIN/S/W) and their multipliers (e.g., `2D`, `3MIN`).
- `inclusive` controls boundary inclusion: `both`, `left`, `right`, `neither`.

### Jalali frequency examples

```python
jp.jalali_date_range("1402-01-01", periods=6, freq="JME")
jp.jalali_date_range("1402-01-01", periods=4, freq="JQE")
jp.jalali_date_range("1402-01-01", periods=5, freq="JW")
```

### Timezone support

`jalali_date_range(..., tz=...)` stores the timezone in the dtype.
