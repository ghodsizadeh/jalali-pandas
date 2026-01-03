# Index & Range Generation

## JalaliDatetimeIndex

```python
import jalali_pandas as jp

idx = jp.JalaliDatetimeIndex(["1402-01-01", "1402-01-02"], name="dates")
idx.to_gregorian()
```

Useful operations:

- `get_loc("1402-01")` for partial string indexing
- `union`, `intersection`, `difference`
- `shift(..., freq=...)`
- `snap(freq="s")`

## jalali_date_range

```python
import jalali_pandas as jp

jp.jalali_date_range("1402-01-01", periods=5, freq="D")
jp.jalali_date_range("1402-01-01", "1402-01-10", freq="D")
jp.jalali_date_range("1402-01-01", periods=3, freq="JME")
```

### Parameters

- Exactly two of `start`, `end`, `periods` must be provided.
- `freq` accepts Jalali offsets (JME/JMS/JQE/JQS/JYE/JYS/JW) or common pandas
  frequencies (D/H/MIN/S/W) and their multipliers (e.g., `2D`).
- `inclusive` controls boundary inclusion: `both`, `left`, `right`, `neither`.

### Timezone support

`jalali_date_range(..., tz=...)` stores the timezone in the dtype.
