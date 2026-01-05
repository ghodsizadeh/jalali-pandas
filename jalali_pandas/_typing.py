"""Type aliases and protocols for jalali-pandas."""

from __future__ import annotations

from collections.abc import Sequence
from datetime import date, datetime, tzinfo
from typing import (
    TYPE_CHECKING,
    Any,
    Literal,
    Protocol,
    TypeVar,
    Union,
    runtime_checkable,
)

import numpy as np
import numpy.typing as npt
import pandas as pd
from pandas._libs.tslibs.nattype import NaTType as PandasNaTType
from typing_extensions import TypeAlias

if TYPE_CHECKING:
    from jalali_pandas.core.arrays import JalaliDatetimeArray
    from jalali_pandas.core.indexes import JalaliDatetimeIndex
    from jalali_pandas.core.timestamp import JalaliTimestamp
    from jalali_pandas.offsets.base import JalaliOffset

# =============================================================================
# Scalar Types
# =============================================================================

# Type for NaT
NaTType: TypeAlias = PandasNaTType

# Jalali scalar or NaT
JalaliScalar = Union["JalaliTimestamp", NaTType]
JalaliScalarOrNaT = Union["JalaliTimestamp", NaTType]

# =============================================================================
# Array-like Types
# =============================================================================

# Jalali array-like inputs
JalaliArrayLike = Union[
    Sequence["JalaliTimestamp"],
    Sequence[str],
    "JalaliDatetimeArray",
    "JalaliDatetimeIndex",
    npt.NDArray[np.object_],
]

# =============================================================================
# Datetime-like Types
# =============================================================================

# Single datetime-like value
DatetimeLike = Union[
    str,
    datetime,
    date,
    pd.Timestamp,
    "JalaliTimestamp",
    np.datetime64,
]

# Array of datetime-like values
DatetimeLikeArrayLike = Union[
    Sequence[DatetimeLike],
    pd.Series,
    pd.DatetimeIndex,
    "JalaliDatetimeIndex",
    npt.NDArray[np.datetime64],
]

# =============================================================================
# Frequency Types
# =============================================================================

# Frequency specification
FrequencyLike = Union[str, pd.DateOffset, "JalaliOffset"]

# =============================================================================
# Timezone Types
# =============================================================================

# Timezone specification
TimezoneType = Union[str, tzinfo, None]

# =============================================================================
# Error Handling Types
# =============================================================================

# Error handling mode
ErrorsType = Literal["raise", "coerce", "ignore"]

# =============================================================================
# Range Types
# =============================================================================

# Inclusive mode for date ranges
InclusiveType = Literal["both", "neither", "left", "right"]

# =============================================================================
# GroupBy Types
# =============================================================================

# GroupBy key types
GroupByKeyType = Union[
    str,
    Sequence[str],
    Literal[
        "year", "month", "day", "week", "quarter", "ym", "yq", "ymd", "md", "dayofweek"
    ],
]

# =============================================================================
# Resample Types
# =============================================================================

# Resample rule type
ResampleRuleType = Union[str, "JalaliOffset"]

# =============================================================================
# Generic Type Variables
# =============================================================================

# Generic type variable
T = TypeVar("T")

# Jalali timestamp type variable
JT = TypeVar("JT", bound="JalaliTimestamp")

# =============================================================================
# Protocols
# =============================================================================


@runtime_checkable
class JalaliDatetimeLike(Protocol):
    """Protocol for objects that can be converted to JalaliTimestamp."""

    @property
    def year(self) -> int:
        """Jalali year."""
        ...

    @property
    def month(self) -> int:
        """Jalali month (1-12)."""
        ...

    @property
    def day(self) -> int:
        """Jalali day (1-31)."""
        ...

    def togregorian(self) -> datetime:
        """Convert to Gregorian datetime."""
        ...


@runtime_checkable
class JalaliOffsetLike(Protocol):
    """Protocol for Jalali calendar-aware offsets."""

    @property
    def n(self) -> int:
        """Number of periods."""
        ...

    def __add__(self, other: Any) -> Any:
        """Add offset to a timestamp."""
        ...

    def __radd__(self, other: Any) -> Any:
        """Right add offset to a timestamp."""
        ...

    def rollforward(self, dt: Any) -> Any:
        """Roll forward to next valid date."""
        ...

    def rollback(self, dt: Any) -> Any:
        """Roll back to previous valid date."""
        ...

    def is_on_offset(self, dt: Any) -> bool:
        """Check if date is on offset boundary."""
        ...


# =============================================================================
# Internal Types
# =============================================================================

# Internal storage type (int64 nanoseconds)
Int64Array = npt.NDArray[np.int64]

# Boolean array
BoolArray = npt.NDArray[np.bool_]

# String array
StrArray = npt.NDArray[np.str_]

# Object array
ObjectArray = npt.NDArray[np.object_]

# =============================================================================
# Exports
# =============================================================================

__all__ = [
    # Scalar types
    "NaTType",
    "JalaliScalar",
    "JalaliScalarOrNaT",
    # Array-like types
    "JalaliArrayLike",
    # Datetime-like types
    "DatetimeLike",
    "DatetimeLikeArrayLike",
    # Frequency types
    "FrequencyLike",
    # Timezone types
    "TimezoneType",
    # Error handling types
    "ErrorsType",
    # Range types
    "InclusiveType",
    # GroupBy types
    "GroupByKeyType",
    # Resample types
    "ResampleRuleType",
    # Type variables
    "T",
    "JT",
    # Protocols
    "JalaliDatetimeLike",
    "JalaliOffsetLike",
    # Internal types
    "Int64Array",
    "BoolArray",
    "StrArray",
    "ObjectArray",
]
