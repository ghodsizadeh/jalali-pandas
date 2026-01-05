"""Pandas accessors for Jalali datetime operations."""

from jalali_pandas.accessors.dataframe import JalaliDataFrameAccessor
from jalali_pandas.accessors.series import JalaliSeriesAccessor

__all__ = [
    "JalaliSeriesAccessor",
    "JalaliDataFrameAccessor",
]
