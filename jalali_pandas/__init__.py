"""
Jalali Pandas - Full Jalali calendar support for pandas.

This package provides native Jalali (Persian/Shamsi) calendar support
for pandas, including custom dtypes, timestamps, and time series operations.
"""

from jalali_pandas._version import __version__

# API functions
from jalali_pandas.api import (
    jalali_date_range,
    to_gregorian_datetime,
    to_jalali_datetime,
)
from jalali_pandas.core.arrays import JalaliDatetimeArray

# Calendar utilities
from jalali_pandas.core.calendar import (
    days_in_month,
    days_in_year,
    is_leap_year,
)
from jalali_pandas.core.dtypes import JalaliDatetimeDtype

# Index
from jalali_pandas.core.indexes import JalaliDatetimeIndex

# Core types
from jalali_pandas.core.timestamp import JalaliTimestamp

# Accessors
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
    "JalaliDatetimeIndex",
    # API functions
    "jalali_date_range",
    "to_jalali_datetime",
    "to_gregorian_datetime",
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
