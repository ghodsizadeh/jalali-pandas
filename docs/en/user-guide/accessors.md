# Accessors

The accessors are registered under `.jalali` on Series and DataFrame.

## Series accessor (`JalaliSeriesAccessor`)

Conversion:

- `to_jalali()`
- `to_gregorian()`
- `parse_jalali(format)`

Properties:

- `year`, `month`, `day`, `hour`, `minute`, `second`
- `weekday`, `dayofweek`, `dayofyear`, `week`, `weekofyear`
- `quarter`, `daysinmonth`
- `is_leap_year`, `is_month_start`, `is_month_end`, `is_year_start`, `is_year_end`

Formatting and rounding:

- `strftime(format)`
- `month_name(locale="fa"|"en")`, `day_name(locale="fa"|"en")`
- `normalize()`, `floor(freq)`, `ceil(freq)`, `round(freq)`

Timezone helpers:

- `tz_localize(tz)`
- `tz_convert(tz)`

## DataFrame accessor (`JalaliDataFrameAccessor`)

Key methods:

- `set_date_column(column)`
- `groupby(grouper)`
- `resample(resample_type)`
- `convert_columns(columns, errors="raise")`
- `to_period(freq="M")`
- `filter_by_year`, `filter_by_month`, `filter_by_quarter`, `filter_by_date_range`

The DataFrame accessor expects at least one column with `jdatetime` values.

## Legacy accessors

The package also exports legacy accessors for compatibility:

- `jalali_pandas.df_handler.JalaliDataframeAccessor`
- `jalali_pandas.serie_handler.JalaliSerieAccessor`

Use the new accessors in `jalali_pandas.accessors.*` for full features.
