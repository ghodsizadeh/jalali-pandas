# NaT Handling

`JalaliNaT` is the Jalali equivalent of pandas `NaT`. Use `isna_jalali` to
check values.

```python
import pandas as pd
from jalali_pandas.core.timestamp import JalaliNaT, isna_jalali

isna_jalali(JalaliNaT)
isna_jalali(pd.NaT)
```

Behavior notes:

- Comparisons against `JalaliNaT` behave like pandas `NaT` (mostly False).
- `JalaliNaT.to_gregorian()` returns `pd.NaT`.
