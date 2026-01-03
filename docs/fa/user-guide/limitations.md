# محدودیت‌ها

محدودیت‌های فعلی بر اساس پیاده‌سازی:

- `JalaliDataFrameAccessor` نیاز به حداقل یک ستون `jdatetime` دارد.
- `JalaliResampler` فقط با `pd.DatetimeIndex` کار می‌کند.
- `jalali_date_range` باید دقیقاً دو مورد از `start`, `end`, `periods` را داشته
  باشد.
- `to_jalali_datetime` فقط چند فرمت مشخص را بدون `format` پشتیبانی می‌کند.
- `JalaliDatetimeArray` از آرایه object استفاده می‌کند و ممکن است کندتر باشد.

در صورت مشاهده مشکل، یک issue با مثال حداقلی ثبت کنید.
