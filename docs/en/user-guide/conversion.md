# Conversion

## Public conversion helpers

- `to_jalali_datetime(...)`
- `to_gregorian_datetime(...)`

```python
import pandas as pd
import jalali_pandas as jp

jp.to_jalali_datetime("1402-06-15")

jp.to_jalali_datetime(pd.Timestamp("2023-09-06"))

jp.to_jalali_datetime(["1402-01-01", "1402-01-02"])

jidx = jp.JalaliDatetimeIndex(["1402-01-01", "1402-01-02"])
jp.to_gregorian_datetime(jidx)
```

## Error handling

`to_jalali_datetime(..., errors=...)` supports:

- `"raise"` (default)
- `"coerce"` → invalid values become `pd.NaT`
- `"ignore"` → return the original input (only for Series)

## Supported string formats (when `format=None`)

The parser tries these formats in order:

- `%Y-%m-%d %H:%M:%S`
- `%Y-%m-%d`
- `%Y/%m/%d %H:%M:%S`
- `%Y/%m/%d`
- `%Y%m%d`

## Vectorized conversion helpers

These are internal helpers used by arrays and indexes:

- `gregorian_to_jalali_vectorized`
- `jalali_to_gregorian_vectorized`
- `datetime64_to_jalali`
- `jalali_to_datetime64`

Use the public API unless you need lower-level access.
