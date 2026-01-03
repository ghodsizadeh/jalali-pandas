# jalali_pandas

Jalali (Persian/Shamsi) calendar support for pandas, with native types,
indexes, offsets, and accessors.

## Highlights

- JalaliTimestamp scalar with conversion to/from Gregorian
- JalaliDatetimeIndex and jalali_date_range for time series work
- Vectorized conversion utilities
- Jalali-aware frequency offsets (JME/JMS/JQE/JQS/JYE/JYS/JW)
- Series/DataFrame accessors under `.jalali`
- Grouping and resampling helpers for Jalali boundaries

## Quick example

```python
import pandas as pd
import jalali_pandas as jp

# Convert Gregorian to Jalali
s = pd.Series(pd.date_range("2023-03-21", periods=3, freq="D"))
j = s.jalali.to_jalali()

# Build a Jalali index
idx = jp.jalali_date_range("1402-01-01", periods=3, freq="D")
```

## Next steps

- Installation: `en/installation.md`
- Quickstart: `en/quickstart.md`
- User guide: `en/user-guide/core-types.md`
- Examples: `en/examples/index.md`
