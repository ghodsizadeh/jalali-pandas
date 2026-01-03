# Installation

## Requirements

- Python 3.9+
- pandas >= 2.0
- numpy >= 1.23
- jdatetime >= 4.0

## Install with pip

```bash
pip install -U jalali-pandas
```

## Install with uv

```bash
uv pip install jalali-pandas
```

## Optional extras (for contributors)

```bash
uv sync --extra dev
uv sync --extra docs
```

These install developer tools and documentation tooling defined in
`pyproject.toml`.

## Verify installation

```python
import jalali_pandas as jp
import pandas as pd

print(f"jalali-pandas version: {jp.__version__}")
ts = jp.JalaliTimestamp(1402, 6, 15)
gregorian = pd.Timestamp("2023-09-06")
jalali = jp.JalaliTimestamp.from_gregorian(gregorian)
print(f"Created timestamp: {ts}")
print(f"Converted: {gregorian} -> {jalali}")
```

Expected output:

```
jalali-pandas version: 1.0.0a1
Created timestamp: 1402-06-15 00:00:00
Converted: 2023-09-06 00:00:00 -> 1402-06-15 00:00:00
```
