# اکسسورها

اکسسورها تحت `.jalali` برای Series و DataFrame ثبت شده‌اند.

## اکسسور Series (`JalaliSeriesAccessor`)

تبدیل:

- `to_jalali()`
- `to_gregorian()`
- `parse_jalali(format)`

ویژگی‌ها:

- `year`, `month`, `day`, `hour`, `minute`, `second`
- `weekday`, `dayofweek`, `dayofyear`, `week`, `weekofyear`
- `quarter`, `daysinmonth`
- `is_leap_year`, `is_month_start`, `is_month_end`, `is_year_start`, `is_year_end`

قالب‌بندی و رند کردن:

- `strftime(format)`
- `month_name(locale="fa"|"en")`, `day_name(locale="fa"|"en")`
- `normalize()`, `floor(freq)`, `ceil(freq)`, `round(freq)`

منطقه زمانی:

- `tz_localize(tz)`
- `tz_convert(tz)`

## اکسسور DataFrame (`JalaliDataFrameAccessor`)

متدهای اصلی:

- `set_date_column(column)`
- `groupby(grouper)`
- `resample(resample_type)`
- `convert_columns(columns, errors="raise")`
- `to_period(freq="M")`
- `filter_by_year`, `filter_by_month`, `filter_by_quarter`, `filter_by_date_range`

اکسسور دیتافریم نیاز به ستون jdatetime دارد.

## اکسسورهای قدیمی

- `jalali_pandas.df_handler.JalaliDataframeAccessor`
- `jalali_pandas.serie_handler.JalaliSerieAccessor`

برای امکانات کامل از اکسسورهای جدید استفاده کنید.
