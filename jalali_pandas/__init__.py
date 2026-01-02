"""
Jalali Pandas - Full Jalali calendar support for pandas.

This package provides native Jalali (Persian/Shamsi) calendar support
for pandas, including custom dtypes, timestamps, and time series operations.
"""

from jalali_pandas._version import __version__
from jalali_pandas.core.arrays import JalaliDatetimeArray

# Calendar utilities
from jalali_pandas.core.calendar import (
    days_in_month,
    days_in_year,
    is_leap_year,
)
from jalali_pandas.core.dtypes import JalaliDatetimeDtype

# Core types
from jalali_pandas.core.timestamp import JalaliTimestamp

# Legacy accessors (backward compatibility)
from jalali_pandas.df_handler import JalaliDataframeAccessor

# Frequency offsets
from jalali_pandas.offsets import (
    JalaliMonthBegin,
    JalaliMonthEnd,
    JalaliOffset,
    JalaliQuarterBegin,
    JalaliQuarterEnd,
    JalaliYearBegin,
    JalaliYearEnd,
)
from jalali_pandas.serie_handler import JalaliSerieAccessor

__all__ = [
    # Version
    "__version__",
    # Core types
    "JalaliTimestamp",
    "JalaliDatetimeDtype",
    "JalaliDatetimeArray",
    # Calendar utilities
    "is_leap_year",
    "days_in_month",
    "days_in_year",
    # Frequency offsets
    "JalaliOffset",
    "JalaliMonthBegin",
    "JalaliMonthEnd",
    "JalaliQuarterBegin",
    "JalaliQuarterEnd",
    "JalaliYearBegin",
    "JalaliYearEnd",
    # Accessors
    "JalaliDataframeAccessor",
    "JalaliSerieAccessor",
]
