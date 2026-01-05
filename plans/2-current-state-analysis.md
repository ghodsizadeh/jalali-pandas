# Current State Analysis

## Overview

`jalali-pandas` is currently a lightweight pandas extension that provides basic Jalali (Persian/Shamsi) calendar support through pandas accessor APIs. It uses `jdatetime` as the underlying Jalali datetime library.

## Current Architecture

### Package Structure
```
jalali_pandas/
├── __init__.py           # Exports JalaliDataframeAccessor, JalaliSerieAccessor
├── serie_handler.py      # Series accessor implementation
└── df_handler.py         # DataFrame accessor implementation
```

### Dependencies
- **jdatetime>=3.8.2**: Core Jalali datetime library
- **pandas**: Required but not version-pinned in pyproject.toml

### Current API Surface

#### Series Accessor (`series.jalali.*`)

| Method/Property | Type | Description | Status |
|-----------------|------|-------------|--------|
| `to_jalali()` | Method | Convert Gregorian datetime to Jalali | ✅ Implemented |
| `to_gregorian()` | Method | Convert Jalali datetime to Gregorian | ✅ Implemented |
| `parse_jalali(format)` | Method | Parse string to Jalali datetime | ✅ Implemented |
| `year` | Property | Extract Jalali year | ✅ Implemented |
| `month` | Property | Extract Jalali month | ✅ Implemented |
| `day` | Property | Extract Jalali day | ✅ Implemented |
| `hour` | Property | Extract hour | ✅ Implemented |
| `minute` | Property | Extract minute | ✅ Implemented |
| `second` | Property | Extract second | ✅ Implemented |
| `weekday` | Property | Extract Jalali weekday | ✅ Implemented |
| `weeknumber` | Property | Extract Jalali week number | ✅ Implemented |
| `quarter` | Property | Extract Jalali quarter | ✅ Implemented |

#### DataFrame Accessor (`df.jalali.*`)

| Method | Description | Status |
|--------|-------------|--------|
| `groupby(grouper)` | Group by Jalali date components | ✅ Implemented |
| `resample(type)` | Resample by Jalali frequency | ❌ NotImplementedError |

**Groupby shortcuts**: `year`, `month`, `day`, `week`, `dayofweek`, `dayofmonth`, `ym`, `yq`, `ymd`, `md`

## Current Limitations

### 1. **No Native Dtype**
- Jalali dates are stored as Python `jdatetime.datetime` objects in object dtype columns
- No vectorized operations - all operations use `.apply()` which is slow
- No integration with pandas' internal datetime machinery

### 2. **No Type Hints**
- No type annotations on any public API
- No `py.typed` marker
- No mypy/pyright compatibility

### 3. **Missing Time Series Features**

| Feature | Pandas Equivalent | Status |
|---------|-------------------|--------|
| Date range generation | `pd.date_range()` | ❌ Missing |
| Jalali DatetimeIndex | `pd.DatetimeIndex` | ❌ Missing |
| Resampling | `df.resample()` | ❌ NotImplemented |
| Frequency offsets | `pd.offsets.*` | ❌ Missing |
| Period support | `pd.Period`, `pd.PeriodIndex` | ❌ Missing |
| Timedelta support | `pd.Timedelta` | ❌ Missing |
| Timezone support | `tz_localize`, `tz_convert` | ❌ Missing |
| Rolling windows | `df.rolling()` with Jalali offsets | ❌ Missing |
| Shifting | `df.shift()` with Jalali freq | ❌ Missing |
| asfreq | `df.asfreq()` | ❌ Missing |

### 4. **Missing Datetime Properties**

| Property | Description | Status |
|----------|-------------|--------|
| `dayofyear` | Day of Jalali year (1-366) | ❌ Missing |
| `daysinmonth` | Days in current Jalali month | ❌ Missing |
| `is_leap_year` | Whether year is Jalali leap year | ❌ Missing |
| `is_month_start` | Is first day of Jalali month | ❌ Missing |
| `is_month_end` | Is last day of Jalali month | ❌ Missing |
| `is_quarter_start` | Is first day of Jalali quarter | ❌ Missing |
| `is_quarter_end` | Is last day of Jalali quarter | ❌ Missing |
| `is_year_start` | Is first day of Jalali year | ❌ Missing |
| `is_year_end` | Is last day of Jalali year | ❌ Missing |
| `week` | ISO week number equivalent | ❌ Missing |
| `microsecond` | Microsecond component | ❌ Missing |
| `nanosecond` | Nanosecond component | ❌ Missing |

### 5. **Missing Datetime Methods**

| Method | Description | Status |
|--------|-------------|--------|
| `strftime(format)` | Format to string | ❌ Missing |
| `normalize()` | Set time to midnight | ❌ Missing |
| `floor(freq)` | Floor to frequency | ❌ Missing |
| `ceil(freq)` | Ceil to frequency | ❌ Missing |
| `round(freq)` | Round to frequency | ❌ Missing |
| `tz_localize()` | Localize timezone | ❌ Missing |
| `tz_convert()` | Convert timezone | ❌ Missing |
| `date` | Extract date part | ❌ Missing |
| `time` | Extract time part | ❌ Missing |

### 6. **Code Quality Issues**
- Uses `print()` statements for debugging (in `__validate`)
- Inconsistent validation (some methods validate, some don't)
- No NA/NaT handling
- No error handling for edge cases

## Test Coverage

Current tests cover:
- Basic conversion (Gregorian ↔ Jalali)
- String parsing
- Property extraction (year, month, day, etc.)
- DataFrame groupby operations
- Error cases (wrong column types, invalid groupby keys)

Missing test coverage:
- Edge cases (leap years, month boundaries)
- NaT/NA handling
- Large dataset performance
- Timezone scenarios
- Round-trip conversions

## What We Need to Build

To achieve full Jalali time series support in pandas, we need:

1. **Core Infrastructure**
   - `JalaliTimestamp` scalar type
   - `JalaliDatetimeArray` (pandas ExtensionArray)
   - `JalaliDatetimeDtype` (pandas ExtensionDtype)
   - `JalaliDatetimeIndex` (pandas Index subclass)

2. **Date/Time Generation**
   - `jalali_date_range()` function
   - `jalali_period_range()` function
   - `to_jalali_datetime()` parsing function

3. **Frequency Offsets**
   - `JalaliYearEnd`, `JalaliYearBegin`
   - `JalaliQuarterEnd`, `JalaliQuarterBegin`
   - `JalaliMonthEnd`, `JalaliMonthBegin`
   - `JalaliWeek`
   - Standard offsets (Day, Hour, Minute, Second, etc.)

4. **Time Series Operations**
   - Resampling with Jalali boundaries
   - Rolling/expanding with Jalali offsets
   - Shifting with Jalali frequencies
   - asfreq with Jalali frequencies

5. **Type System**
   - Full type annotations
   - py.typed marker
   - Stub files if needed

6. **Documentation**
   - API reference (FastAPI-style with Zensical)
   - User guide with examples
   - Migration guide from current API
