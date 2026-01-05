# Feature Parity Checklist

## Overview

This document provides a comprehensive checklist comparing pandas Gregorian datetime functionality with what jalali-pandas needs to implement for full Jalali calendar support.

---

## Scalar Types

### pandas.Timestamp vs JalaliTimestamp

| Feature | pandas.Timestamp | JalaliTimestamp | Status |
|---------|------------------|-----------------|--------|
| **Construction** | | | |
| From components | `Timestamp(2023, 1, 1)` | `JalaliTimestamp(1402, 1, 1)` | 🔴 TODO |
| From string | `Timestamp("2023-01-01")` | `JalaliTimestamp("1402-01-01")` | 🔴 TODO |
| From datetime | `Timestamp(datetime(...))` | `JalaliTimestamp.from_gregorian(...)` | 🔴 TODO |
| now() | `Timestamp.now()` | `JalaliTimestamp.now()` | 🔴 TODO |
| today() | `Timestamp.today()` | `JalaliTimestamp.today()` | 🔴 TODO |
| **Properties** | | | |
| year | ✅ | ✅ | 🟡 Exists (via accessor) |
| month | ✅ | ✅ | 🟡 Exists (via accessor) |
| day | ✅ | ✅ | 🟡 Exists (via accessor) |
| hour | ✅ | ✅ | 🟡 Exists (via accessor) |
| minute | ✅ | ✅ | 🟡 Exists (via accessor) |
| second | ✅ | ✅ | 🟡 Exists (via accessor) |
| microsecond | ✅ | 🔴 | 🔴 TODO |
| nanosecond | ✅ | 🔴 | 🔴 TODO |
| dayofweek | ✅ | ✅ | 🟡 Exists (via accessor) |
| dayofyear | ✅ | 🔴 | 🔴 TODO |
| weekofyear | ✅ | ✅ | 🟡 Exists (via accessor) |
| quarter | ✅ | ✅ | 🟡 Exists (via accessor) |
| daysinmonth | ✅ | 🔴 | 🔴 TODO |
| is_leap_year | ✅ | 🔴 | 🔴 TODO |
| is_month_start | ✅ | 🔴 | 🔴 TODO |
| is_month_end | ✅ | 🔴 | 🔴 TODO |
| is_quarter_start | ✅ | 🔴 | 🔴 TODO |
| is_quarter_end | ✅ | 🔴 | 🔴 TODO |
| is_year_start | ✅ | 🔴 | 🔴 TODO |
| is_year_end | ✅ | 🔴 | 🔴 TODO |
| tz | ✅ | 🔴 | 🔴 TODO |
| **Methods** | | | |
| strftime() | ✅ | 🔴 | 🔴 TODO |
| isoformat() | ✅ | 🔴 | 🔴 TODO |
| date() | ✅ | 🔴 | 🔴 TODO |
| time() | ✅ | 🔴 | 🔴 TODO |
| normalize() | ✅ | 🔴 | 🔴 TODO |
| replace() | ✅ | 🔴 | 🔴 TODO |
| floor() | ✅ | 🔴 | 🔴 TODO |
| ceil() | ✅ | 🔴 | 🔴 TODO |
| round() | ✅ | 🔴 | 🔴 TODO |
| tz_localize() | ✅ | 🔴 | 🔴 TODO |
| tz_convert() | ✅ | 🔴 | 🔴 TODO |
| **Arithmetic** | | | |
| + Timedelta | ✅ | 🔴 | 🔴 TODO |
| - Timedelta | ✅ | 🔴 | 🔴 TODO |
| - Timestamp | ✅ | 🔴 | 🔴 TODO |
| + Offset | ✅ | 🔴 | 🔴 TODO |
| **Comparison** | | | |
| ==, !=, <, >, <=, >= | ✅ | 🔴 | 🔴 TODO |

---

## Array Types

### pandas.DatetimeArray vs JalaliDatetimeArray

| Feature | pandas | jalali-pandas | Status |
|---------|--------|---------------|--------|
| **Construction** | | | |
| _from_sequence() | ✅ | 🔴 | 🔴 TODO |
| _from_sequence_of_strings() | ✅ | 🔴 | 🔴 TODO |
| _from_factorized() | ✅ | 🔴 | 🔴 TODO |
| **Required Methods** | | | |
| __len__ | ✅ | 🔴 | 🔴 TODO |
| __getitem__ | ✅ | 🔴 | 🔴 TODO |
| __setitem__ | ✅ | 🔴 | 🔴 TODO |
| __iter__ | ✅ | 🔴 | 🔴 TODO |
| isna() | ✅ | 🔴 | 🔴 TODO |
| copy() | ✅ | 🔴 | 🔴 TODO |
| _concat_same_type() | ✅ | 🔴 | 🔴 TODO |
| **Vectorized Properties** | | | |
| year, month, day, etc. | ✅ | 🔴 | 🔴 TODO |
| **Vectorized Methods** | | | |
| strftime() | ✅ | 🔴 | 🔴 TODO |
| normalize() | ✅ | 🔴 | 🔴 TODO |
| floor(), ceil(), round() | ✅ | 🔴 | 🔴 TODO |

---

## Index Types

### pandas.DatetimeIndex vs JalaliDatetimeIndex

| Feature | pandas | jalali-pandas | Status |
|---------|--------|---------------|--------|
| **Construction** | | | |
| From list | ✅ | 🔴 | 🔴 TODO |
| From strings | ✅ | 🔴 | 🔴 TODO |
| With freq | ✅ | 🔴 | 🔴 TODO |
| **Indexing** | | | |
| Integer indexing | ✅ | 🔴 | 🔴 TODO |
| String indexing | ✅ | 🔴 | 🔴 TODO |
| Partial string (year) | ✅ | 🔴 | 🔴 TODO |
| Partial string (month) | ✅ | 🔴 | 🔴 TODO |
| Slice indexing | ✅ | 🔴 | 🔴 TODO |
| **Properties** | | | |
| freq | ✅ | 🔴 | 🔴 TODO |
| tz | ✅ | 🔴 | 🔴 TODO |
| All datetime properties | ✅ | 🔴 | 🔴 TODO |
| **Methods** | | | |
| shift() | ✅ | 🔴 | 🔴 TODO |
| snap() | ✅ | 🔴 | 🔴 TODO |
| to_gregorian() | N/A | 🔴 | 🔴 TODO |
| **Set Operations** | | | |
| union() | ✅ | 🔴 | 🔴 TODO |
| intersection() | ✅ | 🔴 | 🔴 TODO |
| difference() | ✅ | 🔴 | 🔴 TODO |

---

## Date Range Generation

### pandas.date_range vs jalali_date_range

| Feature | pandas | jalali-pandas | Status |
|---------|--------|---------------|--------|
| start + periods | ✅ | 🔴 | 🔴 TODO |
| start + end | ✅ | 🔴 | 🔴 TODO |
| end + periods | ✅ | 🔴 | 🔴 TODO |
| **Frequencies** | | | |
| Daily (D) | ✅ | 🔴 | 🔴 TODO |
| Hourly (h) | ✅ | 🔴 | 🔴 TODO |
| Minutely (min) | ✅ | 🔴 | 🔴 TODO |
| Secondly (s) | ✅ | 🔴 | 🔴 TODO |
| Weekly (W) | ✅ | 🔴 | 🔴 TODO |
| Month End (ME) | ✅ | JME | 🔴 TODO |
| Month Start (MS) | ✅ | JMS | 🔴 TODO |
| Quarter End (QE) | ✅ | JQE | 🔴 TODO |
| Quarter Start (QS) | ✅ | JQS | 🔴 TODO |
| Year End (YE) | ✅ | JYE | 🔴 TODO |
| Year Start (YS) | ✅ | JYS | 🔴 TODO |
| **Parameters** | | | |
| tz | ✅ | 🔴 | 🔴 TODO |
| normalize | ✅ | 🔴 | 🔴 TODO |
| name | ✅ | 🔴 | 🔴 TODO |
| inclusive | ✅ | 🔴 | 🔴 TODO |

---

## Frequency Offsets

### pandas.offsets vs jalali_pandas.offsets

| Offset | pandas | jalali-pandas | Status |
|--------|--------|---------------|--------|
| **Standard (Calendar-Agnostic)** | | | |
| Day | ✅ | Use pandas | ✅ Use pandas |
| Hour | ✅ | Use pandas | ✅ Use pandas |
| Minute | ✅ | Use pandas | ✅ Use pandas |
| Second | ✅ | Use pandas | ✅ Use pandas |
| Milli | ✅ | Use pandas | ✅ Use pandas |
| Micro | ✅ | Use pandas | ✅ Use pandas |
| Nano | ✅ | Use pandas | ✅ Use pandas |
| **Jalali-Specific** | | | |
| MonthEnd | ✅ | JalaliMonthEnd | 🔴 TODO |
| MonthBegin | ✅ | JalaliMonthBegin | 🔴 TODO |
| QuarterEnd | ✅ | JalaliQuarterEnd | 🔴 TODO |
| QuarterBegin | ✅ | JalaliQuarterBegin | 🔴 TODO |
| YearEnd | ✅ | JalaliYearEnd | 🔴 TODO |
| YearBegin | ✅ | JalaliYearBegin | 🔴 TODO |
| Week | ✅ | JalaliWeek | 🔴 TODO |
| **Offset Methods** | | | |
| rollforward() | ✅ | 🔴 | 🔴 TODO |
| rollback() | ✅ | 🔴 | 🔴 TODO |
| is_on_offset() | ✅ | 🔴 | 🔴 TODO |
| **Offset Arithmetic** | | | |
| + Timestamp | ✅ | 🔴 | 🔴 TODO |
| * n (multiplier) | ✅ | 🔴 | 🔴 TODO |

---

## Time Series Operations

### Resampling

| Feature | pandas | jalali-pandas | Status |
|---------|--------|---------------|--------|
| **Basic Resampling** | | | |
| resample(freq) | ✅ | 🔴 | 🔴 TODO |
| With Jalali freq (JME, etc.) | N/A | 🔴 | 🔴 TODO |
| **Aggregations** | | | |
| mean() | ✅ | 🔴 | 🔴 TODO |
| sum() | ✅ | 🔴 | 🔴 TODO |
| min() | ✅ | 🔴 | 🔴 TODO |
| max() | ✅ | 🔴 | 🔴 TODO |
| first() | ✅ | 🔴 | 🔴 TODO |
| last() | ✅ | 🔴 | 🔴 TODO |
| ohlc() | ✅ | 🔴 | 🔴 TODO |
| count() | ✅ | 🔴 | 🔴 TODO |
| nunique() | ✅ | 🔴 | 🔴 TODO |
| std() | ✅ | 🔴 | 🔴 TODO |
| var() | ✅ | 🔴 | 🔴 TODO |
| sem() | ✅ | 🔴 | 🔴 TODO |
| median() | ✅ | 🔴 | 🔴 TODO |
| quantile() | ✅ | 🔴 | 🔴 TODO |
| agg() | ✅ | 🔴 | 🔴 TODO |
| apply() | ✅ | 🔴 | 🔴 TODO |
| transform() | ✅ | 🔴 | 🔴 TODO |
| **Fill Methods** | | | |
| ffill() | ✅ | 🔴 | 🔴 TODO |
| bfill() | ✅ | 🔴 | 🔴 TODO |
| nearest() | ✅ | 🔴 | 🔴 TODO |
| asfreq() | ✅ | 🔴 | 🔴 TODO |
| interpolate() | ✅ | 🔴 | 🔴 TODO |
| **Parameters** | | | |
| closed | ✅ | 🔴 | 🔴 TODO |
| label | ✅ | 🔴 | 🔴 TODO |
| origin | ✅ | 🔴 | 🔴 TODO |
| offset | ✅ | 🔴 | 🔴 TODO |

### GroupBy

| Feature | pandas | jalali-pandas | Status |
|---------|--------|---------------|--------|
| groupby(Grouper) | ✅ | JalaliGrouper | 🔴 TODO |
| groupby year | ✅ | ✅ | 🟢 Exists |
| groupby month | ✅ | ✅ | 🟢 Exists |
| groupby day | ✅ | ✅ | 🟢 Exists |
| groupby quarter | ✅ | ✅ | 🟢 Exists |
| groupby week | ✅ | 🔴 | 🔴 TODO |
| Shortcuts (ym, ymd, etc.) | N/A | ✅ | 🟢 Exists |

### Rolling/Expanding

| Feature | pandas | jalali-pandas | Status |
|---------|--------|---------------|--------|
| rolling(window) | ✅ | 🔴 | 🔴 TODO |
| rolling(offset) | ✅ | 🔴 | 🔴 TODO |
| expanding() | ✅ | 🔴 | 🔴 TODO |

### Shifting

| Feature | pandas | jalali-pandas | Status |
|---------|--------|---------------|--------|
| shift(periods) | ✅ | 🔴 | 🔴 TODO |
| shift(freq) | ✅ | 🔴 | 🔴 TODO |
| shift(freq=JalaliOffset) | N/A | 🔴 | 🔴 TODO |

---

## Accessor API

### Series.dt vs Series.jalali

| Feature | pandas .dt | jalali-pandas .jalali | Status |
|---------|------------|----------------------|--------|
| **Conversion** | | | |
| to_jalali() | N/A | ✅ | 🟢 Exists |
| to_gregorian() | N/A | ✅ | 🟢 Exists |
| parse_jalali() | N/A | ✅ | 🟢 Exists |
| **Properties** | | | |
| year | ✅ | ✅ | 🟢 Exists |
| month | ✅ | ✅ | 🟢 Exists |
| day | ✅ | ✅ | 🟢 Exists |
| hour | ✅ | ✅ | 🟢 Exists |
| minute | ✅ | ✅ | 🟢 Exists |
| second | ✅ | ✅ | 🟢 Exists |
| microsecond | ✅ | 🔴 | 🔴 TODO |
| nanosecond | ✅ | 🔴 | 🔴 TODO |
| dayofweek / weekday | ✅ | ✅ | 🟢 Exists |
| dayofyear | ✅ | 🔴 | 🔴 TODO |
| weekofyear | ✅ | ✅ | 🟢 Exists |
| quarter | ✅ | ✅ | 🟢 Exists |
| daysinmonth | ✅ | 🔴 | 🔴 TODO |
| is_leap_year | ✅ | 🔴 | 🔴 TODO |
| is_month_start | ✅ | 🔴 | 🔴 TODO |
| is_month_end | ✅ | 🔴 | 🔴 TODO |
| is_quarter_start | ✅ | 🔴 | 🔴 TODO |
| is_quarter_end | ✅ | 🔴 | 🔴 TODO |
| is_year_start | ✅ | 🔴 | 🔴 TODO |
| is_year_end | ✅ | 🔴 | 🔴 TODO |
| date | ✅ | 🔴 | 🔴 TODO |
| time | ✅ | 🔴 | 🔴 TODO |
| tz | ✅ | 🔴 | 🔴 TODO |
| **Methods** | | | |
| strftime() | ✅ | 🔴 | 🔴 TODO |
| normalize() | ✅ | 🔴 | 🔴 TODO |
| floor() | ✅ | 🔴 | 🔴 TODO |
| ceil() | ✅ | 🔴 | 🔴 TODO |
| round() | ✅ | 🔴 | 🔴 TODO |
| tz_localize() | ✅ | 🔴 | 🔴 TODO |
| tz_convert() | ✅ | 🔴 | 🔴 TODO |
| month_name() | ✅ | 🔴 | 🔴 TODO |
| day_name() | ✅ | 🔴 | 🔴 TODO |

### DataFrame.jalali

| Feature | jalali-pandas | Status |
|---------|---------------|--------|
| groupby() | ✅ | 🟢 Exists |
| resample() | 🔴 NotImplemented | 🔴 TODO |
| set_date_column() | 🔴 | 🔴 TODO |
| convert_columns() | 🔴 | 🔴 TODO |

---

## I/O Integration

| Feature | pandas | jalali-pandas | Status |
|---------|--------|---------------|--------|
| CSV read with parsing | ✅ | 🔴 | 🔴 TODO |
| CSV write with formatting | ✅ | 🔴 | 🔴 TODO |
| Parquet roundtrip | ✅ | 🔴 | 🔴 TODO |
| JSON roundtrip | ✅ | 🔴 | 🔴 TODO |
| Excel roundtrip | ✅ | 🔴 | 🔴 TODO |

---

## Summary Statistics

| Category | Total Features | Implemented | TODO |
|----------|----------------|-------------|------|
| JalaliTimestamp | ~40 | 0 | 40 |
| JalaliDatetimeArray | ~15 | 0 | 15 |
| JalaliDatetimeIndex | ~20 | 0 | 20 |
| Date Range | ~15 | 0 | 15 |
| Offsets | ~10 | 0 | 10 |
| Resampling | ~25 | 0 | 25 |
| GroupBy | ~10 | 5 | 5 |
| Rolling/Shifting | ~5 | 0 | 5 |
| Series Accessor | ~30 | 12 | 18 |
| DataFrame Accessor | ~5 | 1 | 4 |
| I/O | ~5 | 0 | 5 |
| **TOTAL** | **~180** | **~18** | **~162** |

---

## Legend

- 🟢 **Exists**: Feature is implemented and working
- 🟡 **Partial**: Feature exists but needs enhancement
- 🔴 **TODO**: Feature needs to be implemented
- ✅ **Available in pandas**: Reference implementation exists
- N/A: Not applicable
