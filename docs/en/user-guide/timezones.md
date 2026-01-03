# Timezones

Jalali timestamps support timezone localization and conversion by delegating to
pandas' timezone handling.

## JalaliTimestamp

```python
from jalali_pandas import JalaliTimestamp

ts = JalaliTimestamp(1402, 6, 15, 12, 0)

localized = ts.tz_localize("Asia/Tehran")
converted = localized.tz_convert("UTC")
```

Rules:

- `tz_localize()` requires a naive timestamp.
- `tz_convert()` requires a timezone-aware timestamp.

## Series accessor

```python
import pandas as pd

s = pd.Series(pd.date_range("2023-03-21", periods=2, freq="D"))
j = s.jalali.to_jalali()

j_local = j.jalali.tz_localize("Asia/Tehran")
j_utc = j_local.jalali.tz_convert("UTC")
```
