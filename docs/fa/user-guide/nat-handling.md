# NaT

`JalaliNaT` معادل جلالی برای `NaT` در pandas است. برای بررسی از `isna_jalali`
استفاده کنید.

```python
import pandas as pd
from jalali_pandas.core.timestamp import JalaliNaT, isna_jalali

isna_jalali(JalaliNaT)
isna_jalali(pd.NaT)
```

نکات:

- مقایسه با `JalaliNaT` مشابه رفتار `NaT` است.
- `JalaliNaT.to_gregorian()` مقدار `pd.NaT` برمی‌گرداند.
