# Accessors

Importing `jalali_pandas` registers the `.jalali` accessor on Series and
DataFrames.

## Series accessor (`JalaliSeriesAccessor`)

The Series accessor expects `jdatetime` values or Jalali strings. If you have
Gregorian datetimes, convert first with `series.jalali.to_jalali()`.

### Conversion

- `to_jalali()`
- `to_gregorian()`
- `parse_jalali(format="%Y-%m-%d")`

### Properties

- `year`, `month`, `day`, `hour`, `minute`, `second`, `microsecond`, `nanosecond`
- `quarter`, `weekday`, `dayofweek`, `dayofyear`
- `week`, `weekofyear`, `weeknumber`
- `daysinmonth`, `days_in_month`

### Boolean properties

- `is_leap_year`
- `is_month_start`, `is_month_end`
- `is_quarter_start`, `is_quarter_end`
- `is_year_start`, `is_year_end`

### Formatting and rounding

- `strftime(format)`
- `month_name(locale="fa"|"en")`, `day_name(locale="fa"|"en")`
- `normalize()`, `floor(freq)`, `ceil(freq)`, `round(freq)`

```python
import pandas as pd
import jalali_pandas  # registers accessor

series = pd.Series(pd.date_range("2023-03-21", periods=3))
jseries = series.jalali.to_jalali()

# English names are the default
print(jseries.jalali.month_name())

# Farsi names
print(jseries.jalali.month_name(locale="fa"))
```

### Timezone helpers

`tz_localize` and `tz_convert` return timezone-aware Gregorian datetimes:

- `tz_localize(tz, ambiguous="raise", nonexistent="raise")`
- `tz_convert(tz)`

## DataFrame accessor (`JalaliDataFrameAccessor`)

The DataFrame accessor expects at least one column with `jdatetime` values.
Create one with `.jalali.to_jalali()` and set it explicitly if you have multiple
Jalali columns.

### Key methods

- `set_date_column(column)`
- `groupby(grouper)`
- `resample(resample_type)` where `resample_type` is `month|quarter|year|week`
- `convert_columns(columns, to_jalali=True, format="%Y-%m-%d")`
- `to_period(freq="ME")`
- `filter_by_year`, `filter_by_month`, `filter_by_quarter`, `filter_by_date_range`

Supported groupby keys:

`year`, `month`, `day`, `week`, `dayofweek`, `dayofmonth`, `quarter`,
`dayofyear`, `ym`, `yq`, `ymd`, `md`

```python
import pandas as pd
import jalali_pandas

df = pd.DataFrame({"date": pd.date_range("2023-03-21", periods=10)})
df["jdate"] = df["date"].jalali.to_jalali()

monthly = df.jalali.groupby("month").size()
converted = df.jalali.convert_columns("date", to_jalali=True)
```

## Legacy accessors

- `jalali_pandas.df_handler.JalaliDataframeAccessor`
- `jalali_pandas.serie_handler.JalaliSerieAccessor`

Use the new accessors in `jalali_pandas.accessors.*` for full features.
