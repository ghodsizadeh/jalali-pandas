# API Design Specification

## Design Principles

1. **Pandas-Native Feel**: APIs should feel like natural extensions of pandas
2. **Type Safety**: Full type annotations with mypy/pyright compatibility
3. **Performance**: Vectorized operations wherever possible
4. **Backward Compatibility**: Existing accessor API should continue to work
5. **Explicit over Implicit**: Clear conversion boundaries between Jalali and Gregorian

---

## Core Types

### 1. JalaliTimestamp (Scalar)

The scalar representation of a single Jalali datetime point.

```python
from jalali_pandas import JalaliTimestamp

# Construction
jts = JalaliTimestamp(1402, 6, 15)  # Year, Month, Day
jts = JalaliTimestamp(1402, 6, 15, 14, 30, 0)  # With time
jts = JalaliTimestamp("1402-06-15")  # From string
jts = JalaliTimestamp("1402/06/15 14:30:00", format="%Y/%m/%d %H:%M:%S")
jts = JalaliTimestamp.now()  # Current time
jts = JalaliTimestamp.today()  # Today at midnight

# From Gregorian
jts = JalaliTimestamp.from_gregorian(pd.Timestamp("2023-09-06"))
jts = JalaliTimestamp.from_gregorian(datetime.datetime(2023, 9, 6))

# To Gregorian
ts = jts.to_gregorian()  # Returns pd.Timestamp

# Properties (read-only)
jts.year          # int: 1402
jts.month         # int: 6
jts.day           # int: 15
jts.hour          # int: 14
jts.minute        # int: 30
jts.second        # int: 0
jts.microsecond   # int: 0
jts.nanosecond    # int: 0
jts.dayofweek     # int: 0-6 (Saturday=0 in Jalali calendar)
jts.dayofyear     # int: 1-366
jts.weekofyear    # int: 1-53
jts.quarter       # int: 1-4
jts.daysinmonth   # int: 29-31
jts.is_leap_year  # bool
jts.is_month_start  # bool
jts.is_month_end    # bool
jts.is_quarter_start  # bool
jts.is_quarter_end    # bool
jts.is_year_start     # bool
jts.is_year_end       # bool

# Methods
jts.strftime("%Y/%m/%d")  # "1402/06/15"
jts.isoformat()           # "1402-06-15T14:30:00"
jts.date()                # JalaliDate (date only)
jts.time()                # datetime.time
jts.normalize()           # JalaliTimestamp with time set to 00:00:00
jts.replace(year=1403)    # New JalaliTimestamp with replaced components
jts.floor("D")            # Floor to day
jts.ceil("M")             # Ceil to month
jts.round("h")            # Round to hour

# Timezone support
jts.tz                    # timezone info or None
jts.tz_localize("Asia/Tehran")
jts.tz_convert("UTC")

# Arithmetic
jts + pd.Timedelta(days=1)
jts - pd.Timedelta(hours=5)
jts - other_jts  # Returns pd.Timedelta

# Comparison
jts == other_jts
jts < other_jts
jts >= other_jts

# Special values
JalaliTimestamp.min  # Minimum representable
JalaliTimestamp.max  # Maximum representable
pd.NaT  # Use pandas NaT for missing values
```

### 2. JalaliDatetimeDtype (ExtensionDtype)

```python
from jalali_pandas import JalaliDatetimeDtype

dtype = JalaliDatetimeDtype()
dtype = JalaliDatetimeDtype(tz="Asia/Tehran")

# Properties
dtype.name        # "jalali_datetime64[ns]" or "jalali_datetime64[ns, Asia/Tehran]"
dtype.tz          # timezone or None
dtype.type        # JalaliTimestamp
dtype.na_value    # pd.NaT

# Usage
pd.Series([...], dtype=JalaliDatetimeDtype())
pd.Series([...], dtype="jalali_datetime64[ns]")  # String alias
```

### 3. JalaliDatetimeArray (ExtensionArray)

Internal array type backing Series/Index with Jalali datetime data.

```python
from jalali_pandas import JalaliDatetimeArray

# Construction (typically internal)
arr = JalaliDatetimeArray._from_sequence([jts1, jts2, jts3])
arr = JalaliDatetimeArray._from_sequence_of_strings(["1402-01-01", "1402-01-02"])

# Properties (vectorized, return arrays)
arr.year          # np.ndarray[int]
arr.month         # np.ndarray[int]
arr.day           # np.ndarray[int]
# ... all scalar properties available as vectorized

# Methods (vectorized)
arr.strftime("%Y/%m/%d")  # np.ndarray[str]
arr.to_gregorian()        # DatetimeArray
arr.normalize()           # JalaliDatetimeArray
arr.floor("D")            # JalaliDatetimeArray
arr.ceil("M")             # JalaliDatetimeArray
arr.round("h")            # JalaliDatetimeArray
```

### 4. JalaliDatetimeIndex (Index)

```python
from jalali_pandas import JalaliDatetimeIndex

# Construction
idx = JalaliDatetimeIndex([jts1, jts2, jts3])
idx = JalaliDatetimeIndex(["1402-01-01", "1402-01-02", "1402-01-03"])
idx = JalaliDatetimeIndex(["1402-01-01", "1402-01-02"], freq="D")

# From date_range
idx = jalali_date_range("1402-01-01", periods=10, freq="D")
idx = jalali_date_range("1402-01-01", "1402-01-10", freq="D")

# Properties (same as JalaliDatetimeArray)
idx.year, idx.month, idx.day, ...

# Indexing operations
series[JalaliTimestamp(1402, 1, 1)]
series["1402-01-01"]  # String indexing
series["1402-01"]     # Partial string indexing (whole month)
series["1402"]        # Partial string indexing (whole year)
series["1402-01-01":"1402-01-10"]  # Slicing

# Conversion
idx.to_gregorian()  # DatetimeIndex
```

---

## Top-Level Functions

### Date Range Generation

```python
from jalali_pandas import jalali_date_range, jalali_period_range

# jalali_date_range - generates JalaliDatetimeIndex
jalali_date_range(
    start: str | JalaliTimestamp | None = None,
    end: str | JalaliTimestamp | None = None,
    periods: int | None = None,
    freq: str | JalaliOffset | None = None,
    tz: str | tzinfo | None = None,
    normalize: bool = False,
    name: str | None = None,
    inclusive: str = "both",  # "both", "neither", "left", "right"
) -> JalaliDatetimeIndex

# Examples
jalali_date_range("1402-01-01", periods=10, freq="D")
jalali_date_range("1402-01-01", "1402-12-29", freq="ME")  # Month end
jalali_date_range("1402-01-01", periods=4, freq="QE")     # Quarter end
jalali_date_range("1400-01-01", "1402-12-29", freq="YE")  # Year end

# jalali_period_range - generates JalaliPeriodIndex
jalali_period_range(
    start: str | JalaliTimestamp | None = None,
    end: str | JalaliTimestamp | None = None,
    periods: int | None = None,
    freq: str | None = None,
    name: str | None = None,
) -> JalaliPeriodIndex

# Examples
jalali_period_range("1402-01", periods=12, freq="M")  # 12 months
jalali_period_range("1400", "1402", freq="Y")         # 3 years
```

### Conversion Functions

```python
from jalali_pandas import to_jalali_datetime, to_gregorian_datetime

# to_jalali_datetime - parse to JalaliDatetimeIndex or Series
to_jalali_datetime(
    arg: str | list | Series | DatetimeIndex,
    format: str | None = None,
    errors: str = "raise",  # "raise", "coerce", "ignore"
    dayfirst: bool = False,
    yearfirst: bool = True,
    utc: bool = False,
) -> JalaliDatetimeIndex | Series

# Examples
to_jalali_datetime(["1402-01-01", "1402-01-02"])
to_jalali_datetime(pd.Series(["1402/01/01", "1402/01/02"]), format="%Y/%m/%d")
to_jalali_datetime(pd.DatetimeIndex([...]))  # Convert from Gregorian

# to_gregorian_datetime - convert Jalali to Gregorian
to_gregorian_datetime(
    arg: JalaliTimestamp | JalaliDatetimeIndex | Series,
) -> pd.Timestamp | pd.DatetimeIndex | pd.Series
```

---

## Frequency Offsets

### Jalali-Specific Offsets

```python
from jalali_pandas.offsets import (
    JalaliYearEnd,      # YE-J or JYE
    JalaliYearBegin,    # YS-J or JYS
    JalaliQuarterEnd,   # QE-J or JQE
    JalaliQuarterBegin, # QS-J or JQS
    JalaliMonthEnd,     # ME-J or JME
    JalaliMonthBegin,   # MS-J or JMS
    JalaliWeek,         # W-J or JW (Saturday-based by default)
)

# Usage
offset = JalaliMonthEnd()
offset = JalaliMonthEnd(n=2)  # Every 2 months
offset = JalaliQuarterEnd(month=3)  # Q1 ends in Khordad
offset = JalaliWeek(weekday=4)  # Week ending on Wednesday

# With date_range
jalali_date_range("1402-01-01", periods=12, freq=JalaliMonthEnd())
jalali_date_range("1402-01-01", periods=12, freq="JME")  # String alias

# Offset arithmetic
jts + JalaliMonthEnd()
jts + JalaliMonthEnd(3)
jts - JalaliYearBegin()

# Offset methods
offset.rollforward(jts)  # Next valid date
offset.rollback(jts)     # Previous valid date
offset.is_on_offset(jts) # Is date on offset boundary
```

### Frequency Aliases

| Alias | Description | Jalali-Specific |
|-------|-------------|-----------------|
| `D` | Calendar day | No |
| `h` | Hour | No |
| `min` | Minute | No |
| `s` | Second | No |
| `ms` | Millisecond | No |
| `us` | Microsecond | No |
| `ns` | Nanosecond | No |
| `W` | Week (Sunday) | No |
| `JW` | Jalali Week (Saturday) | Yes |
| `JME` | Jalali Month End | Yes |
| `JMS` | Jalali Month Start | Yes |
| `JQE` | Jalali Quarter End | Yes |
| `JQS` | Jalali Quarter Start | Yes |
| `JYE` | Jalali Year End | Yes |
| `JYS` | Jalali Year Start | Yes |

---

## Series Accessor API (Enhanced)

The existing `.jalali` accessor will be enhanced:

```python
import jalali_pandas  # Registers accessor

series = pd.Series([...])  # Jalali datetime series

# Existing API (backward compatible)
series.jalali.to_jalali()
series.jalali.to_gregorian()
series.jalali.parse_jalali(format)
series.jalali.year
series.jalali.month
series.jalali.day
series.jalali.hour
series.jalali.minute
series.jalali.second
series.jalali.weekday
series.jalali.weeknumber
series.jalali.quarter

# New properties
series.jalali.dayofyear
series.jalali.daysinmonth
series.jalali.is_leap_year
series.jalali.is_month_start
series.jalali.is_month_end
series.jalali.is_quarter_start
series.jalali.is_quarter_end
series.jalali.is_year_start
series.jalali.is_year_end
series.jalali.date  # Date part only
series.jalali.time  # Time part only
series.jalali.tz    # Timezone

# New methods
series.jalali.strftime(format)
series.jalali.normalize()
series.jalali.floor(freq)
series.jalali.ceil(freq)
series.jalali.round(freq)
series.jalali.tz_localize(tz)
series.jalali.tz_convert(tz)
series.jalali.month_name(locale="fa")  # "فروردین", "اردیبهشت", ...
series.jalali.day_name(locale="fa")    # "شنبه", "یکشنبه", ...
```

---

## DataFrame Accessor API (Enhanced)

```python
import jalali_pandas

df = pd.DataFrame(...)

# Existing API (backward compatible)
df.jalali.groupby("year")
df.jalali.groupby("ym")
df.jalali.groupby(["year", "month", "day"])

# New: Resampling (fully implemented)
df.jalali.resample("JME").mean()      # Monthly (Jalali month end)
df.jalali.resample("JQE").sum()       # Quarterly
df.jalali.resample("JYE").agg(...)    # Yearly
df.jalali.resample("D").ffill()       # Daily with forward fill

# New: Set Jalali column for operations
df.jalali.set_date_column("my_jalali_col")

# New: Convert entire DataFrame datetime columns
df.jalali.convert_columns(["col1", "col2"], to="jalali")
df.jalali.convert_columns(["col1", "col2"], to="gregorian")
```

---

## Resampling API

```python
# Using JalaliDatetimeIndex
series = pd.Series(data, index=jalali_date_range(...))
series.resample("JME").mean()  # Works natively

# Using DataFrame with Jalali column
df.resample("JME", on="jalali_date_col").mean()

# Using accessor
df.jalali.resample("JME").mean()

# Resampler methods (all standard pandas methods)
resampler = series.resample("JME")
resampler.mean()
resampler.sum()
resampler.min()
resampler.max()
resampler.first()
resampler.last()
resampler.ohlc()
resampler.count()
resampler.nunique()
resampler.std()
resampler.var()
resampler.sem()
resampler.median()
resampler.quantile(q)
resampler.agg(func)
resampler.apply(func)
resampler.transform(func)
resampler.ffill()
resampler.bfill()
resampler.nearest()
resampler.asfreq()
resampler.interpolate()
```

---

## Grouper API

```python
from jalali_pandas import JalaliGrouper

# Group by Jalali time components
df.groupby(JalaliGrouper(key="date_col", freq="JME")).mean()
df.groupby(JalaliGrouper(key="date_col", freq="JQE")).sum()

# Multiple groupers
df.groupby([
    JalaliGrouper(key="date_col", freq="JYE"),
    "category"
]).mean()
```

---

## Rolling/Expanding with Jalali Offsets

```python
# Rolling with Jalali offset window
series.rolling(window=JalaliMonthEnd(3)).mean()  # 3 Jalali months
series.rolling(window="3JME").mean()             # String alias

# Expanding
series.expanding().mean()
```

---

## Shifting

```python
# Shift by Jalali frequency
series.shift(freq="JME")      # Shift by 1 Jalali month
series.shift(freq="JME", periods=3)  # Shift by 3 Jalali months
series.shift(freq=JalaliMonthEnd(2))  # Using offset object
```

---

## IO Integration

```python
# Reading with Jalali parsing
pd.read_csv(
    "file.csv",
    parse_dates=["date_col"],
    date_parser=lambda x: to_jalali_datetime(x, format="%Y/%m/%d")
)

# Writing with Jalali formatting
df.to_csv("file.csv", date_format="%Y/%m/%d")  # Uses strftime
```

---

## Error Handling

All functions should support consistent error handling:

```python
# errors parameter
to_jalali_datetime(data, errors="raise")   # Raise on invalid (default)
to_jalali_datetime(data, errors="coerce")  # Return NaT on invalid
to_jalali_datetime(data, errors="ignore")  # Return input on invalid
```

---

## Null Handling

- Use `pd.NaT` for missing Jalali datetime values
- All operations should propagate NaT correctly
- Comparison with NaT returns False (like NaN)
- NaT == NaT returns False (like NaN)
