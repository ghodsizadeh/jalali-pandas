"""
Jalali Pandas - Full Jalali calendar support for pandas.

This package provides native Jalali (Persian/Shamsi) calendar support
for pandas, including custom dtypes, timestamps, and time series operations.
"""

from jalali_pandas._version import __version__
from jalali_pandas.accessors.dataframe import JalaliDataFrameAccessor
from jalali_pandas.accessors.series import JalaliSeriesAccessor
from jalali_pandas.api import (
    jalali_date_range,
    to_gregorian_datetime,
    to_jalali_datetime,
)
from jalali_pandas.core.arrays import JalaliDatetimeArray
from jalali_pandas.core.calendar import (
    days_in_month,
    days_in_year,
    is_leap_year,
)
from jalali_pandas.core.dtypes import JalaliDatetimeDtype
from jalali_pandas.core.indexes import JalaliDatetimeIndex
from jalali_pandas.core.timestamp import JalaliTimestamp
from jalali_pandas.df_handler import JalaliDataframeAccessor
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
    # Accessors (new enhanced versions)
    "JalaliDataFrameAccessor",
    "JalaliSeriesAccessor",
    # Legacy accessors (for backward compatibility)
    "JalaliDataframeAccessor",
    "JalaliSerieAccessor",
]
