# ایندکس و بازه تاریخ

## JalaliDatetimeIndex

`JalaliDatetimeIndex` ایندکس بومی جلالی برای Series و DataFrame است.

```python
import jalali_pandas as jp

idx = jp.JalaliDatetimeIndex(["1402-01-01", "1402-01-02"], name="dates")
gregorian = idx.to_gregorian()
```

### عملیات مهم

- ایندکس بخشی با `get_loc("1402")` یا `get_loc("1402-01")`
- مجموعه‌ها: `union`, `intersection`, `difference`
- شیفت با `shift(periods=..., freq=...)`
- هم‌راستا کردن با `snap(freq="s")`

```python
idx = jp.jalali_date_range("1402-01-01", periods=40)
mask = idx.get_loc("1402-02")  # ماسک بولی برای یک ماه
subset = idx[mask]
```

```python
shifted = idx.shift(periods=1, freq="JME")
daily_shift = idx.shift(periods=1, freq="1D")
```

## jalali_date_range

```python
import jalali_pandas as jp

jp.jalali_date_range("1402-01-01", periods=5, freq="D")
jp.jalali_date_range("1402-01-01", "1402-01-10", freq="D")
jp.jalali_date_range("1402-01-01", periods=3, freq="JME")
```

### نکات

- حداقل دو مورد از `start`, `end`, `periods` باید مشخص شود.
- اگر هر سه مورد داده شود، `freq` الزامی است.
- `freq` می‌تواند افست‌های جلالی (JME/JMS/JQE/JQS/JYE/JYS/JW) یا فرکانس‌های
  رایج pandas (D/H/MIN/S/W) و ضریب آن‌ها باشد (مثلاً `2D`, `3MIN`).
- `inclusive` برای کنترل مرزها: `both`, `left`, `right`, `neither`.

### نمونه‌های فرکانس جلالی

```python
jp.jalali_date_range("1402-01-01", periods=6, freq="JME")
jp.jalali_date_range("1402-01-01", periods=4, freq="JQE")
jp.jalali_date_range("1402-01-01", periods=5, freq="JW")
```

### منطقه زمانی

در `jalali_date_range(..., tz=...)` منطقه زمانی در dtype ذخیره می‌شود.
