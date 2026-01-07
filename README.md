[![PyPI version](https://badge.fury.io/py/jalali-pandas.svg)](https://badge.fury.io/py/jalali-pandas)
[![Python Version](https://img.shields.io/pypi/pyversions/jalali-pandas.svg)](https://pypi.org/project/jalali-pandas/)
[![pandas Version](https://img.shields.io/badge/pandas-2.0%2B-blue.svg)](https://pandas.pydata.org/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/jalali-pandas.svg?color=blue)](https://pypi.org/project/jalali-pandas/)
[![codecov](https://codecov.io/gh/ghodsizadeh/jalali-pandas/branch/main/graph/badge.svg?token=LWQ85TN0NU)](https://codecov.io/gh/ghodsizadeh/jalali-pandas)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![CI](https://github.com/ghodsizadeh/jalali-pandas/actions/workflows/ci.yml/badge.svg)](https://github.com/ghodsizadeh/jalali-pandas/actions/workflows/ci.yml)
[![Documentation](https://img.shields.io/badge/docs-mkdocs-blue.svg)](https://ghodsizadeh.github.io/jalali-pandas/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ghodsizadeh/jalali-pandas/blob/main/examples/00_zero_to_hero.ipynb)
![GitHub Repo stars](https://img.shields.io/github/stars/ghodsizadeh/jalali-pandas?logoColor=blue&style=social)

# Jalali Pandas Extension

> **Full-featured Jalali (Persian/Shamsi) calendar support for pandas** — A complete pandas extension providing native Jalali datetime types, time series operations, and calendar-aware functionality.

![Jalali Pandas python package](docs/assets/github-jalali-pandas.png)

## ✨ Features

### 🎯 Core Types
- **JalaliTimestamp**: Full-featured scalar type with all date/time properties
- **JalaliDatetimeDtype**: Registered pandas extension dtype (`jalali_datetime64[ns]`)
- **JalaliDatetimeArray**: Extension array for Series storage with vectorized operations
- **JalaliDatetimeIndex**: Complete pandas Index implementation with Jalali awareness

### 📅 Date Range & Conversion
- **jalali_date_range()**: Generate date ranges with frequency support (daily, monthly, quarterly, yearly)
- **to_jalali_datetime()** / **to_gregorian_datetime()**: Bidirectional conversion for all input types
- String parsing with multiple formats: `"1402-06-15"`, `"1402/6/15"`, `"1402-06"`, `"1402"`

### 🔄 Frequency Offsets
- **JalaliMonthEnd/Begin**: Handle Jalali month boundaries (31-day months 1-6, 30-day months 7-11, Esfand 29/30)
- **JalaliQuarterEnd/Begin**: Quarter boundaries respecting Jalali calendar
- **JalaliYearEnd/Begin**: Year boundaries (1 Farvardin start, 29/30 Esfand end)
- **JalaliWeek**: Saturday-based weeks with custom weekday support
- Frequency aliases: `JME`, `JMS`, `JQE`, `JQS`, `JYE`, `JYS`, `JW`

### 📊 Time Series Operations
- **resample_jalali()**: Jalali-aware resampling with proper calendar boundaries
- **JalaliGrouper**: Calendar-based grouping by year/month/quarter/day
- **Enhanced Accessors**: Full Series and DataFrame accessor support
  - Properties: `year`, `month`, `day`, `quarter`, `week`, `weekday`, `is_leap_year`, etc.
  - Methods: `strftime()`, `normalize()`, `floor()`, `ceil()`, `round()`, `tz_localize()`, `tz_convert()`

### 🧪 Quality & Performance
- **94% test coverage** with 563+ passing tests
- **Type hints** throughout (PEP 561 compliant)
- **Python 3.9-3.13** support
- **pandas 2.0-2.2** compatibility

## 📦 Installation

### Using pip

```bash
pip install jalali-pandas
```

For development:
```bash
pip install jalali-pandas[dev]
```

### Using uv (recommended for faster installation)

```bash
uv add jalali-pandas
```

For development:
```bash
uv add --dev jalali-pandas
```

## 🚀 Quick Start

### Basic Usage

```python
import pandas as pd
import jalali_pandas
from jalali_pandas import jalali_date_range, to_jalali_datetime

# Create a Jalali date range
jdates = jalali_date_range("1402-01-01", periods=10, freq="D")
print(jdates)
# JalaliDatetimeIndex(['1402-01-01', '1402-01-02', ..., '1402-01-10'], dtype='jalali_datetime64[ns]', freq='D')

# Convert Gregorian to Jalali
gregorian_dates = pd.date_range("2023-01-01", periods=5)
jalali_dates = to_jalali_datetime(gregorian_dates)
print(jalali_dates)
# JalaliDatetimeIndex(['1401-10-11', '1401-10-12', ..., '1401-10-15'], dtype='jalali_datetime64[ns]')
```

### Series Operations

```python
import pandas as pd
import jalali_pandas

# Create a DataFrame with Gregorian dates
df = pd.DataFrame({
    "date": pd.date_range("2023-01-01", periods=10, freq="D"),
    "value": range(10)
})

# Convert to Jalali using accessor
df["jdate"] = df["date"].jalali.to_jalali()

# Access Jalali date components
df["year"] = df["jdate"].jalali.year
df["month"] = df["jdate"].jalali.month
df["day"] = df["jdate"].jalali.day
df["quarter"] = df["jdate"].jalali.quarter
df["weekday"] = df["jdate"].jalali.weekday
df["is_leap"] = df["jdate"].jalali.is_leap_year

# Format as Persian strings
df["persian_date"] = df["jdate"].jalali.strftime("%Y/%m/%d")
```

### DataFrame Operations

```python
import pandas as pd
import jalali_pandas
from jalali_pandas import jalali_date_range

# Create DataFrame with Jalali dates
df = pd.DataFrame({
    "date": jalali_date_range("1402-01-01", periods=100, freq="D"),
    "value": range(100)
})

# Group by Jalali year and month
monthly = df.jalali.groupby(["year", "month"]).sum()

# Use shortcuts for common groupings
yearly = df.jalali.groupby("year").mean()  # Group by year
quarterly = df.jalali.groupby("yq").sum()  # Group by year-quarter
daily = df.jalali.groupby("ymd").count()   # Group by year-month-day

# Resample with Jalali calendar awareness
monthly_resample = df.set_index("date").resample_jalali("JME").sum()
quarterly_resample = df.set_index("date").resample_jalali("JQE").mean()
```

### Advanced Features

```python
from jalali_pandas import JalaliTimestamp
from jalali_pandas.offsets import JalaliMonthEnd, JalaliYearEnd

# Create Jalali timestamps
jts = JalaliTimestamp(1402, 6, 15, 12, 30, 0)
print(jts.strftime("%Y/%m/%d %H:%M"))  # 1402/06/15 12:30

# Use frequency offsets
end_of_month = jts + JalaliMonthEnd()
end_of_year = jts + JalaliYearEnd()

# Timezone support
jts_tehran = jts.tz_localize("Asia/Tehran")
jts_utc = jts_tehran.tz_convert("UTC")
```

## 📚 Documentation

- **Full Documentation**: [https://ghodsizadeh.github.io/jalali-pandas/](https://ghodsizadeh.github.io/jalali-pandas/)
- **API Reference**: [https://ghodsizadeh.github.io/jalali-pandas/en/api/](https://ghodsizadeh.github.io/jalali-pandas/en/api/)
- **Examples**: [11 Python examples + 2 Jupyter notebooks](https://github.com/ghodsizadeh/jalali-pandas/tree/main/examples)
- **Persian Documentation**: [مستندات فارسی](https://ghodsizadeh.github.io/jalali-pandas/fa/)

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](https://ghodsizadeh.github.io/jalali-pandas/en/contributing/) for details.

## 📝 License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built on top of [pandas](https://pandas.pydata.org/) and [jdatetime](https://github.com/slashmili/python-jdatetime)
- Inspired by the need for proper Jalali calendar support in data analysis

---

# راهنمای فارسی

برای مطالعه راهنمای فارسی استفاده از کتابخانه به این آدرس مراجعه کنید:

- **مستندات کامل**: [https://ghodsizadeh.github.io/jalali-pandas/fa/](https://ghodsizadeh.github.io/jalali-pandas/fa/)
- **راهنمای نصب**: [نصب و راه‌اندازی](https://ghodsizadeh.github.io/jalali-pandas/fa/installation/)
- **آموزش سریع**: [شروع سریع](https://ghodsizadeh.github.io/jalali-pandas/fa/quickstart/)
- **مقاله آموزشی**: [معرفی بسته pandas-jalali | آموزش کار با تاریخ شمسی در pandas](https://learnwithmehdi.ir/posts/jalali-pandas/)

### راهنمای ویدیویی

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/PYS4Hxmzbyg/0.jpg)](https://www.youtube.com/watch?v=PYS4Hxmzbyg)
