# ایندکس و بازه تاریخ

## JalaliDatetimeIndex

```python
import jalali_pandas as jp

idx = jp.JalaliDatetimeIndex(["1402-01-01", "1402-01-02"], name="dates")
idx.to_gregorian()
```

عملیات مهم:

- `get_loc("1402-01")` برای ایندکس بخشی
- `union`, `intersection`, `difference`
- `shift(..., freq=...)`
- `snap(freq="s")`

## jalali_date_range

```python
import jalali_pandas as jp

jp.jalali_date_range("1402-01-01", periods=5, freq="D")
jp.jalali_date_range("1402-01-01", "1402-01-10", freq="D")
jp.jalali_date_range("1402-01-01", periods=3, freq="JME")
```

### نکات

- دقیقاً دو مورد از `start`, `end`, `periods` باید مشخص شود.
- `freq` می‌تواند افست‌های جلالی (JME/JMS/JQE/JQS/JYE/JYS/JW) یا فرکانس‌های
  رایج pandas باشد.
- `inclusive` برای کنترل مرزها استفاده می‌شود: `both`, `left`, `right`, `neither`.

### منطقه زمانی

در `jalali_date_range(..., tz=...)` منطقه زمانی در dtype ذخیره می‌شود.
