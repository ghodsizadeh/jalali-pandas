# اکسسورها

با `import jalali_pandas` اکسسور `.jalali` روی Series و DataFrame ثبت می‌شود.

## اکسسور Series (`JalaliSeriesAccessor`)

اکسسور Series انتظار مقادیر `jdatetime` یا رشته‌های جلالی را دارد. اگر
تاریخ‌های میلادی دارید ابتدا با `series.jalali.to_jalali()` تبدیل کنید.

### تبدیل

- `to_jalali()`
- `to_gregorian()`
- `parse_jalali(format="%Y-%m-%d")`

### ویژگی‌ها

- `year`, `month`, `day`, `hour`, `minute`, `second`, `microsecond`, `nanosecond`
- `quarter`, `weekday`, `dayofweek`, `dayofyear`
- `week`, `weekofyear`, `weeknumber`
- `daysinmonth`, `days_in_month`

### ویژگی‌های بولی

- `is_leap_year`
- `is_month_start`, `is_month_end`
- `is_quarter_start`, `is_quarter_end`
- `is_year_start`, `is_year_end`

### قالب‌بندی و رند کردن

- `strftime(format)`
- `month_name(locale="fa"|"en")`, `day_name(locale="fa"|"en")`
- `normalize()`, `floor(freq)`, `ceil(freq)`, `round(freq)`

```python
import pandas as pd
import jalali_pandas  # registers accessor

series = pd.Series(pd.date_range("2023-03-21", periods=3))
jseries = series.jalali.to_jalali()

# پیش‌فرض انگلیسی است
print(jseries.jalali.month_name())

# نام فارسی
print(jseries.jalali.month_name(locale="fa"))
```

### منطقه زمانی

`tz_localize` و `tz_convert` خروجی را به صورت تاریخ‌های میلادیِ آگاه از
منطقه زمانی برمی‌گردانند:

- `tz_localize(tz, ambiguous="raise", nonexistent="raise")`
- `tz_convert(tz)`

## اکسسور DataFrame (`JalaliDataFrameAccessor`)

اکسسور دیتافریم نیاز به حداقل یک ستون از نوع `jdatetime` دارد. آن را با
`.jalali.to_jalali()` بسازید و اگر چند ستون دارید از `set_date_column` استفاده
کنید.

### متدهای اصلی

- `set_date_column(column)`
- `groupby(grouper)`
- `resample(resample_type)` با مقادیر `month|quarter|year|week`
- `convert_columns(columns, to_jalali=True, format="%Y-%m-%d")`
- `to_period(freq="ME")`
- `filter_by_year`, `filter_by_month`, `filter_by_quarter`, `filter_by_date_range`

کلیدهای groupby:

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

## اکسسورهای قدیمی

- `jalali_pandas.df_handler.JalaliDataframeAccessor`
- `jalali_pandas.serie_handler.JalaliSerieAccessor`

برای امکانات کامل از اکسسورهای جدید استفاده کنید.
