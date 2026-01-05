# Example: Basic Usage

Source: `examples/01_basic_usage.py`

## Create timestamps and convert

```python
from jalali_pandas import JalaliTimestamp
import pandas as pd

ts = JalaliTimestamp(1402, 6, 15)

gregorian = pd.Timestamp("2023-09-06")
ts_from_greg = JalaliTimestamp.from_gregorian(gregorian)
```

## Common operations

```python
ts.normalize()
ts.replace(year=1403, month=1)
ts.strftime("%Y-%m-%d")
```
