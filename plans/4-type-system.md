# Type System Specification

## Goals

1. **Full Type Coverage**: Every public API must have complete type annotations
2. **IDE Support**: Enable autocomplete, hover docs, and error detection in IDEs
3. **Static Analysis**: Pass mypy and pyright in strict mode
4. **Runtime Validation**: Use types for runtime validation where appropriate

---

## Type Checking Configuration

### pyproject.toml additions

```toml
[tool.mypy]
python_version = "3.9"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
warn_unreachable = true
show_error_codes = true
plugins = ["numpy.typing.mypy_plugin"]

[[tool.mypy.overrides]]
module = ["jdatetime.*"]
ignore_missing_imports = true

[tool.pyright]
pythonVersion = "3.9"
typeCheckingMode = "strict"
reportMissingImports = true
reportMissingTypeStubs = false
reportUnusedImport = true
reportUnusedClass = true
reportUnusedFunction = true
reportUnusedVariable = true
reportDuplicateImport = true
```

### py.typed marker

Create `jalali_pandas/py.typed` (empty file) to indicate PEP 561 compliance.

---

## Core Type Definitions

### Type Aliases (`jalali_pandas/_typing.py`)

```python
from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Hashable,
    Literal,
    Sequence,
    TypeVar,
    Union,
    overload,
)
from datetime import datetime, date, time, tzinfo
import numpy as np
import numpy.typing as npt
import pandas as pd

if TYPE_CHECKING:
    from jalali_pandas import (
        JalaliTimestamp,
        JalaliDatetimeArray,
        JalaliDatetimeIndex,
        JalaliDatetimeDtype,
    )
    from jalali_pandas.offsets import JalaliOffset

# Scalar types
JalaliScalar = Union["JalaliTimestamp", pd.NaT.__class__]
JalaliScalarOrNaT = Union["JalaliTimestamp", type[pd.NaT]]

# Array-like types
JalaliArrayLike = Union[
    Sequence["JalaliTimestamp"],
    Sequence[str],
    "JalaliDatetimeArray",
    "JalaliDatetimeIndex",
    npt.NDArray[np.object_],
]

# Datetime-like inputs
DatetimeLike = Union[
    str,
    datetime,
    date,
    pd.Timestamp,
    "JalaliTimestamp",
    np.datetime64,
]

DatetimeLikeArrayLike = Union[
    Sequence[DatetimeLike],
    pd.Series,
    pd.DatetimeIndex,
    "JalaliDatetimeIndex",
    npt.NDArray[np.datetime64],
]

# Frequency types
FrequencyLike = Union[str, pd.DateOffset, "JalaliOffset"]

# Timezone types
TimezoneType = Union[str, tzinfo, None]

# Error handling
ErrorsType = Literal["raise", "coerce", "ignore"]

# Inclusive type for ranges
InclusiveType = Literal["both", "neither", "left", "right"]

# Groupby types
GroupByKeyType = Union[
    str,
    Sequence[str],
    Literal["year", "month", "day", "week", "quarter", "ym", "yq", "ymd", "md"],
]

# Resample types
ResampleRuleType = Union[str, "JalaliOffset"]

# Generic type vars
T = TypeVar("T")
JT = TypeVar("JT", bound="JalaliTimestamp")
```

---

## Protocol Definitions

### JalaliDatetimeLike Protocol

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class JalaliDatetimeLike(Protocol):
    """Protocol for objects that can be converted to JalaliTimestamp."""

    @property
    def year(self) -> int: ...

    @property
    def month(self) -> int: ...

    @property
    def day(self) -> int: ...

    def togregorian(self) -> datetime: ...
```

### JalaliOffsetLike Protocol

```python
@runtime_checkable
class JalaliOffsetLike(Protocol):
    """Protocol for Jalali calendar-aware offsets."""

    def __add__(self, other: JalaliTimestamp) -> JalaliTimestamp: ...

    def __radd__(self, other: JalaliTimestamp) -> JalaliTimestamp: ...

    def rollforward(self, dt: JalaliTimestamp) -> JalaliTimestamp: ...

    def rollback(self, dt: JalaliTimestamp) -> JalaliTimestamp: ...

    def is_on_offset(self, dt: JalaliTimestamp) -> bool: ...
```

---

## Class Type Signatures

### JalaliTimestamp

```python
from __future__ import annotations
from typing import overload, Literal

class JalaliTimestamp:
    """Jalali calendar timestamp scalar."""

    # Class attributes
    min: ClassVar[JalaliTimestamp]
    max: ClassVar[JalaliTimestamp]
    resolution: ClassVar[pd.Timedelta]

    # Construction overloads
    @overload
    def __new__(
        cls,
        year: int,
        month: int = 1,
        day: int = 1,
        hour: int = 0,
        minute: int = 0,
        second: int = 0,
        microsecond: int = 0,
        nanosecond: int = 0,
        tzinfo: TimezoneType = None,
    ) -> JalaliTimestamp: ...

    @overload
    def __new__(
        cls,
        ts_input: str | datetime | pd.Timestamp | np.datetime64,
        *,
        format: str | None = None,
        tz: TimezoneType = None,
    ) -> JalaliTimestamp: ...

    # Class methods
    @classmethod
    def now(cls, tz: TimezoneType = None) -> JalaliTimestamp: ...

    @classmethod
    def today(cls, tz: TimezoneType = None) -> JalaliTimestamp: ...

    @classmethod
    def from_gregorian(
        cls,
        dt: datetime | pd.Timestamp | np.datetime64,
        tz: TimezoneType = None,
    ) -> JalaliTimestamp: ...

    # Properties
    @property
    def year(self) -> int: ...

    @property
    def month(self) -> int: ...

    @property
    def day(self) -> int: ...

    @property
    def hour(self) -> int: ...

    @property
    def minute(self) -> int: ...

    @property
    def second(self) -> int: ...

    @property
    def microsecond(self) -> int: ...

    @property
    def nanosecond(self) -> int: ...

    @property
    def dayofweek(self) -> int: ...

    @property
    def dayofyear(self) -> int: ...

    @property
    def weekofyear(self) -> int: ...

    @property
    def quarter(self) -> int: ...

    @property
    def daysinmonth(self) -> int: ...

    @property
    def is_leap_year(self) -> bool: ...

    @property
    def is_month_start(self) -> bool: ...

    @property
    def is_month_end(self) -> bool: ...

    @property
    def is_quarter_start(self) -> bool: ...

    @property
    def is_quarter_end(self) -> bool: ...

    @property
    def is_year_start(self) -> bool: ...

    @property
    def is_year_end(self) -> bool: ...

    @property
    def tz(self) -> tzinfo | None: ...

    # Methods
    def to_gregorian(self) -> pd.Timestamp: ...

    def strftime(self, format: str) -> str: ...

    def isoformat(self, sep: str = "T", timespec: str = "auto") -> str: ...

    def date(self) -> JalaliDate: ...

    def time(self) -> time: ...

    def normalize(self) -> JalaliTimestamp: ...

    def replace(
        self,
        year: int | None = None,
        month: int | None = None,
        day: int | None = None,
        hour: int | None = None,
        minute: int | None = None,
        second: int | None = None,
        microsecond: int | None = None,
        nanosecond: int | None = None,
        tzinfo: TimezoneType | object = ...,  # Use sentinel for "unchanged"
    ) -> JalaliTimestamp: ...

    def floor(self, freq: FrequencyLike) -> JalaliTimestamp: ...

    def ceil(self, freq: FrequencyLike) -> JalaliTimestamp: ...

    def round(self, freq: FrequencyLike) -> JalaliTimestamp: ...

    def tz_localize(
        self,
        tz: TimezoneType,
        ambiguous: str = "raise",
        nonexistent: str = "raise",
    ) -> JalaliTimestamp: ...

    def tz_convert(self, tz: TimezoneType) -> JalaliTimestamp: ...

    # Arithmetic
    def __add__(self, other: pd.Timedelta | JalaliOffset) -> JalaliTimestamp: ...

    def __radd__(self, other: pd.Timedelta | JalaliOffset) -> JalaliTimestamp: ...

    def __sub__(
        self, other: pd.Timedelta | JalaliOffset | JalaliTimestamp
    ) -> JalaliTimestamp | pd.Timedelta: ...

    # Comparison
    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...
    def __lt__(self, other: JalaliTimestamp) -> bool: ...
    def __le__(self, other: JalaliTimestamp) -> bool: ...
    def __gt__(self, other: JalaliTimestamp) -> bool: ...
    def __ge__(self, other: JalaliTimestamp) -> bool: ...

    # Hashing
    def __hash__(self) -> int: ...
```

### JalaliDatetimeDtype

```python
from pandas.api.extensions import ExtensionDtype

class JalaliDatetimeDtype(ExtensionDtype):
    """Pandas ExtensionDtype for Jalali datetime."""

    # Required ExtensionDtype attributes
    name: str
    type: type[JalaliTimestamp]
    na_value: pd.NaT.__class__

    def __init__(self, tz: TimezoneType = None) -> None: ...

    @property
    def tz(self) -> tzinfo | None: ...

    @classmethod
    def construct_array_type(cls) -> type[JalaliDatetimeArray]: ...

    @classmethod
    def construct_from_string(cls, string: str) -> JalaliDatetimeDtype: ...

    def __eq__(self, other: object) -> bool: ...

    def __hash__(self) -> int: ...
```

### JalaliDatetimeArray

```python
from pandas.api.extensions import ExtensionArray

class JalaliDatetimeArray(ExtensionArray):
    """Pandas ExtensionArray for Jalali datetime data."""

    # Required ExtensionArray attributes
    dtype: JalaliDatetimeDtype

    def __init__(
        self,
        values: npt.NDArray[np.int64],  # Internal storage as int64 nanoseconds
        dtype: JalaliDatetimeDtype | None = None,
        copy: bool = False,
    ) -> None: ...

    # Construction methods
    @classmethod
    def _from_sequence(
        cls,
        scalars: Sequence[JalaliScalar | str | None],
        *,
        dtype: JalaliDatetimeDtype | None = None,
        copy: bool = False,
    ) -> JalaliDatetimeArray: ...

    @classmethod
    def _from_sequence_of_strings(
        cls,
        strings: Sequence[str],
        *,
        dtype: JalaliDatetimeDtype | None = None,
        copy: bool = False,
    ) -> JalaliDatetimeArray: ...

    @classmethod
    def _from_factorized(
        cls,
        values: npt.NDArray[np.int64],
        original: JalaliDatetimeArray,
    ) -> JalaliDatetimeArray: ...

    # Properties (vectorized)
    @property
    def year(self) -> npt.NDArray[np.int64]: ...

    @property
    def month(self) -> npt.NDArray[np.int64]: ...

    @property
    def day(self) -> npt.NDArray[np.int64]: ...

    @property
    def hour(self) -> npt.NDArray[np.int64]: ...

    @property
    def minute(self) -> npt.NDArray[np.int64]: ...

    @property
    def second(self) -> npt.NDArray[np.int64]: ...

    @property
    def microsecond(self) -> npt.NDArray[np.int64]: ...

    @property
    def nanosecond(self) -> npt.NDArray[np.int64]: ...

    @property
    def dayofweek(self) -> npt.NDArray[np.int64]: ...

    @property
    def dayofyear(self) -> npt.NDArray[np.int64]: ...

    @property
    def weekofyear(self) -> npt.NDArray[np.int64]: ...

    @property
    def quarter(self) -> npt.NDArray[np.int64]: ...

    @property
    def daysinmonth(self) -> npt.NDArray[np.int64]: ...

    @property
    def is_leap_year(self) -> npt.NDArray[np.bool_]: ...

    @property
    def is_month_start(self) -> npt.NDArray[np.bool_]: ...

    @property
    def is_month_end(self) -> npt.NDArray[np.bool_]: ...

    @property
    def is_quarter_start(self) -> npt.NDArray[np.bool_]: ...

    @property
    def is_quarter_end(self) -> npt.NDArray[np.bool_]: ...

    @property
    def is_year_start(self) -> npt.NDArray[np.bool_]: ...

    @property
    def is_year_end(self) -> npt.NDArray[np.bool_]: ...

    # Methods (vectorized)
    def to_gregorian(self) -> pd.arrays.DatetimeArray: ...

    def strftime(self, format: str) -> npt.NDArray[np.str_]: ...

    def normalize(self) -> JalaliDatetimeArray: ...

    def floor(self, freq: FrequencyLike) -> JalaliDatetimeArray: ...

    def ceil(self, freq: FrequencyLike) -> JalaliDatetimeArray: ...

    def round(self, freq: FrequencyLike) -> JalaliDatetimeArray: ...

    def tz_localize(
        self,
        tz: TimezoneType,
        ambiguous: str = "raise",
        nonexistent: str = "raise",
    ) -> JalaliDatetimeArray: ...

    def tz_convert(self, tz: TimezoneType) -> JalaliDatetimeArray: ...

    # Required ExtensionArray methods
    def __len__(self) -> int: ...

    @overload
    def __getitem__(self, key: int) -> JalaliTimestamp: ...

    @overload
    def __getitem__(
        self, key: slice | npt.NDArray[np.bool_] | npt.NDArray[np.int_]
    ) -> JalaliDatetimeArray: ...

    def __setitem__(
        self,
        key: int | slice | npt.NDArray[np.bool_] | npt.NDArray[np.int_],
        value: JalaliScalar | JalaliArrayLike,
    ) -> None: ...

    def __iter__(self) -> Iterator[JalaliTimestamp]: ...

    def isna(self) -> npt.NDArray[np.bool_]: ...

    def copy(self) -> JalaliDatetimeArray: ...

    def _concat_same_type(
        cls, to_concat: Sequence[JalaliDatetimeArray]
    ) -> JalaliDatetimeArray: ...
```

### JalaliDatetimeIndex

```python
class JalaliDatetimeIndex(pd.Index):
    """Pandas Index for Jalali datetime data."""

    # Construction
    def __new__(
        cls,
        data: JalaliArrayLike | None = None,
        freq: FrequencyLike | None = None,
        tz: TimezoneType = None,
        dtype: JalaliDatetimeDtype | None = None,
        copy: bool = False,
        name: Hashable = None,
    ) -> JalaliDatetimeIndex: ...

    # Properties (same as JalaliDatetimeArray)
    @property
    def year(self) -> pd.Index: ...
    # ... all other properties

    # Methods
    def to_gregorian(self) -> pd.DatetimeIndex: ...

    # ... all other methods from JalaliDatetimeArray

    # Index-specific methods
    def snap(self, freq: FrequencyLike = "s") -> JalaliDatetimeIndex: ...

    def shift(
        self,
        periods: int = 1,
        freq: FrequencyLike | None = None,
    ) -> JalaliDatetimeIndex: ...
```

---

## Function Signatures

### jalali_date_range

```python
def jalali_date_range(
    start: str | JalaliTimestamp | None = None,
    end: str | JalaliTimestamp | None = None,
    periods: int | None = None,
    freq: FrequencyLike | None = None,
    tz: TimezoneType = None,
    normalize: bool = False,
    name: Hashable = None,
    inclusive: InclusiveType = "both",
) -> JalaliDatetimeIndex: ...
```

### to_jalali_datetime

```python
@overload
def to_jalali_datetime(
    arg: str | JalaliTimestamp | datetime | pd.Timestamp,
    format: str | None = None,
    errors: ErrorsType = "raise",
) -> JalaliTimestamp: ...

@overload
def to_jalali_datetime(
    arg: Sequence[str] | pd.DatetimeIndex,
    format: str | None = None,
    errors: ErrorsType = "raise",
) -> JalaliDatetimeIndex: ...

@overload
def to_jalali_datetime(
    arg: pd.Series,
    format: str | None = None,
    errors: ErrorsType = "raise",
) -> pd.Series: ...
```

---

## Accessor Type Signatures

### JalaliSeriesAccessor

```python
@pd.api.extensions.register_series_accessor("jalali")
class JalaliSeriesAccessor:
    """Accessor for Jalali datetime operations on Series."""

    def __init__(self, pandas_obj: pd.Series) -> None: ...

    # Conversion methods
    def to_jalali(self) -> pd.Series: ...
    def to_gregorian(self) -> pd.Series: ...
    def parse_jalali(self, format: str = "%Y-%m-%d") -> pd.Series: ...

    # Properties
    @property
    def year(self) -> pd.Series: ...

    @property
    def month(self) -> pd.Series: ...

    @property
    def day(self) -> pd.Series: ...

    @property
    def hour(self) -> pd.Series: ...

    @property
    def minute(self) -> pd.Series: ...

    @property
    def second(self) -> pd.Series: ...

    @property
    def microsecond(self) -> pd.Series: ...

    @property
    def nanosecond(self) -> pd.Series: ...

    @property
    def dayofweek(self) -> pd.Series: ...

    @property
    def weekday(self) -> pd.Series: ...  # Alias for dayofweek

    @property
    def dayofyear(self) -> pd.Series: ...

    @property
    def weekofyear(self) -> pd.Series: ...

    @property
    def weeknumber(self) -> pd.Series: ...  # Alias for weekofyear

    @property
    def quarter(self) -> pd.Series: ...

    @property
    def daysinmonth(self) -> pd.Series: ...

    @property
    def is_leap_year(self) -> pd.Series: ...

    @property
    def is_month_start(self) -> pd.Series: ...

    @property
    def is_month_end(self) -> pd.Series: ...

    @property
    def is_quarter_start(self) -> pd.Series: ...

    @property
    def is_quarter_end(self) -> pd.Series: ...

    @property
    def is_year_start(self) -> pd.Series: ...

    @property
    def is_year_end(self) -> pd.Series: ...

    @property
    def date(self) -> pd.Series: ...

    @property
    def time(self) -> pd.Series: ...

    @property
    def tz(self) -> tzinfo | None: ...

    # Methods
    def strftime(self, format: str) -> pd.Series: ...

    def normalize(self) -> pd.Series: ...

    def floor(self, freq: FrequencyLike) -> pd.Series: ...

    def ceil(self, freq: FrequencyLike) -> pd.Series: ...

    def round(self, freq: FrequencyLike) -> pd.Series: ...

    def tz_localize(
        self,
        tz: TimezoneType,
        ambiguous: str = "raise",
        nonexistent: str = "raise",
    ) -> pd.Series: ...

    def tz_convert(self, tz: TimezoneType) -> pd.Series: ...

    def month_name(self, locale: str = "fa") -> pd.Series: ...

    def day_name(self, locale: str = "fa") -> pd.Series: ...
```

### JalaliDataFrameAccessor

```python
@pd.api.extensions.register_dataframe_accessor("jalali")
class JalaliDataFrameAccessor:
    """Accessor for Jalali datetime operations on DataFrames."""

    def __init__(self, pandas_obj: pd.DataFrame) -> None: ...

    def set_date_column(self, column: str) -> JalaliDataFrameAccessor: ...

    def groupby(
        self,
        grouper: GroupByKeyType,
    ) -> pd.core.groupby.DataFrameGroupBy: ...

    def resample(
        self,
        rule: ResampleRuleType,
        closed: Literal["left", "right"] | None = None,
        label: Literal["left", "right"] | None = None,
        origin: str | JalaliTimestamp = "start_day",
        offset: pd.Timedelta | None = None,
    ) -> pd.core.resample.Resampler: ...

    def convert_columns(
        self,
        columns: str | list[str],
        to: Literal["jalali", "gregorian"],
        format: str | None = None,
    ) -> pd.DataFrame: ...
```

---

## Stub Files (Optional)

If needed for complex cases, create `.pyi` stub files in `jalali_pandas/` for each module to provide additional type information that can't be expressed in runtime code.

---

## Testing Type Annotations

### Using mypy

```bash
mypy jalali_pandas --strict
```

### Using pyright

```bash
pyright jalali_pandas
```

### CI Integration

Add to GitHub Actions workflow:

```yaml
- name: Type check with mypy
  run: mypy jalali_pandas --strict

- name: Type check with pyright
  run: pyright jalali_pandas
```
