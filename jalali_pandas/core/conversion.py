"""Vectorized conversion utilities for Jalali-Gregorian date conversions.

This module provides optimized conversion functions using NumPy for
efficient batch processing of date conversions.
"""

from __future__ import annotations

import threading
from datetime import date
from functools import lru_cache
from typing import TYPE_CHECKING

import jdatetime
import numpy as np
import pandas as pd

from jalali_pandas.core.calendar import days_in_month

if TYPE_CHECKING:
    from numpy.typing import NDArray


_COMMON_JALALI_YEAR_START = 1300
_COMMON_JALALI_YEAR_END = 1500
_LOOKUP_MIN_SIZE = 1000

_LOOKUP_LOCK = threading.Lock()
_LOOKUP_READY = False
_JALALI_TO_GREGORIAN_LOOKUP: dict[tuple[int, int, int], tuple[int, int, int]] = {}
_GREGORIAN_TO_JALALI_LOOKUP: dict[tuple[int, int, int], tuple[int, int, int]] = {}


def _ensure_lookup_tables() -> None:
    """Build lookup tables for common Jalali/Gregorian date ranges."""
    global _LOOKUP_READY, _JALALI_TO_GREGORIAN_LOOKUP, _GREGORIAN_TO_JALALI_LOOKUP

    if _LOOKUP_READY:
        return

    with _LOOKUP_LOCK:
        if _LOOKUP_READY:
            return

        jalali_to_gregorian: dict[tuple[int, int, int], tuple[int, int, int]] = {}
        gregorian_to_jalali: dict[tuple[int, int, int], tuple[int, int, int]] = {}

        for year in range(_COMMON_JALALI_YEAR_START, _COMMON_JALALI_YEAR_END + 1):
            for month in range(1, 13):
                max_day = days_in_month(year, month)
                for day in range(1, max_day + 1):
                    jdate = jdatetime.date(year, month, day)
                    gdate = jdate.togregorian()
                    g_key = (gdate.year, gdate.month, gdate.day)
                    j_key = (year, month, day)
                    jalali_to_gregorian[j_key] = g_key
                    gregorian_to_jalali[g_key] = j_key

        _JALALI_TO_GREGORIAN_LOOKUP = jalali_to_gregorian
        _GREGORIAN_TO_JALALI_LOOKUP = gregorian_to_jalali
        _LOOKUP_READY = True


@lru_cache(maxsize=16384)
def jalali_to_gregorian_scalar(year: int, month: int, day: int) -> tuple[int, int, int]:
    """Convert a single Jalali date to Gregorian.

    Args:
        year: Jalali year.
        month: Jalali month (1-12).
        day: Jalali day.

    Returns:
        Tuple of (gregorian_year, gregorian_month, gregorian_day).
    """
    if _LOOKUP_READY:
        cached = _JALALI_TO_GREGORIAN_LOOKUP.get((year, month, day))
        if cached is not None:
            return cached

    jdate = jdatetime.date(year, month, day)
    gdate = jdate.togregorian()
    return gdate.year, gdate.month, gdate.day


@lru_cache(maxsize=16384)
def gregorian_to_jalali_scalar(year: int, month: int, day: int) -> tuple[int, int, int]:
    """Convert a single Gregorian date to Jalali.

    Args:
        year: Gregorian year.
        month: Gregorian month (1-12).
        day: Gregorian day.

    Returns:
        Tuple of (jalali_year, jalali_month, jalali_day).
    """
    if _LOOKUP_READY:
        cached = _GREGORIAN_TO_JALALI_LOOKUP.get((year, month, day))
        if cached is not None:
            return cached

    gdate = date(year, month, day)
    jdate = jdatetime.date.fromgregorian(date=gdate)
    return jdate.year, jdate.month, jdate.day


def jalali_to_gregorian_vectorized(
    year: NDArray[np.int64],
    month: NDArray[np.int64],
    day: NDArray[np.int64],
    *,
    use_lookup: bool = True,
) -> tuple[NDArray[np.int64], NDArray[np.int64], NDArray[np.int64]]:
    """Convert arrays of Jalali dates to Gregorian.

    Args:
        year: Array of Jalali years.
        month: Array of Jalali months (1-12).
        day: Array of Jalali days.

    Returns:
        Tuple of (gregorian_year, gregorian_month, gregorian_day) arrays.
    """
    n = len(year)
    if use_lookup and n >= _LOOKUP_MIN_SIZE:
        _ensure_lookup_tables()

    lookup = _JALALI_TO_GREGORIAN_LOOKUP if _LOOKUP_READY else None
    g_year: NDArray[np.int64] = np.empty(n, dtype=np.int64)
    g_month: NDArray[np.int64] = np.empty(n, dtype=np.int64)
    g_day: NDArray[np.int64] = np.empty(n, dtype=np.int64)

    for i in range(n):
        key = (int(year[i]), int(month[i]), int(day[i]))
        if lookup is not None:
            cached = lookup.get(key)
            if cached is not None:
                gy, gm, gd = cached
            else:
                gy, gm, gd = jalali_to_gregorian_scalar(*key)
        else:
            gy, gm, gd = jalali_to_gregorian_scalar(*key)
        g_year[i] = gy
        g_month[i] = gm
        g_day[i] = gd

    return g_year, g_month, g_day


def gregorian_to_jalali_vectorized(
    year: NDArray[np.int64],
    month: NDArray[np.int64],
    day: NDArray[np.int64],
    *,
    use_lookup: bool = True,
) -> tuple[NDArray[np.int64], NDArray[np.int64], NDArray[np.int64]]:
    """Convert arrays of Gregorian dates to Jalali.

    Args:
        year: Array of Gregorian years.
        month: Array of Gregorian months (1-12).
        day: Array of Gregorian days.

    Returns:
        Tuple of (jalali_year, jalali_month, jalali_day) arrays.
    """
    n = len(year)
    if use_lookup and n >= _LOOKUP_MIN_SIZE:
        _ensure_lookup_tables()

    lookup = _GREGORIAN_TO_JALALI_LOOKUP if _LOOKUP_READY else None
    j_year: NDArray[np.int64] = np.empty(n, dtype=np.int64)
    j_month: NDArray[np.int64] = np.empty(n, dtype=np.int64)
    j_day: NDArray[np.int64] = np.empty(n, dtype=np.int64)

    for i in range(n):
        key = (int(year[i]), int(month[i]), int(day[i]))
        if lookup is not None:
            cached = lookup.get(key)
            if cached is not None:
                jy, jm, jd = cached
            else:
                jy, jm, jd = gregorian_to_jalali_scalar(*key)
        else:
            jy, jm, jd = gregorian_to_jalali_scalar(*key)
        j_year[i] = jy
        j_month[i] = jm
        j_day[i] = jd

    return j_year, j_month, j_day


def datetime64_to_jalali(
    dt: NDArray[np.datetime64],
) -> tuple[NDArray[np.int64], NDArray[np.int64], NDArray[np.int64]]:
    """Convert numpy datetime64 array to Jalali date components.

    Args:
        dt: Array of numpy datetime64 values.

    Returns:
        Tuple of (jalali_year, jalali_month, jalali_day) arrays.
    """
    # Convert to pandas DatetimeIndex for easy component extraction
    dti = pd.DatetimeIndex(dt)
    year = dti.year.to_numpy().astype(np.int64)
    month = dti.month.to_numpy().astype(np.int64)
    day = dti.day.to_numpy().astype(np.int64)

    return gregorian_to_jalali_vectorized(year, month, day, use_lookup=True)


def jalali_to_datetime64(
    year: NDArray[np.int64],
    month: NDArray[np.int64],
    day: NDArray[np.int64],
    hour: NDArray[np.int64] | None = None,
    minute: NDArray[np.int64] | None = None,
    second: NDArray[np.int64] | None = None,
    microsecond: NDArray[np.int64] | None = None,
    nanosecond: NDArray[np.int64] | None = None,
) -> NDArray[np.datetime64]:
    """Convert Jalali date components to numpy datetime64 array.

    Args:
        year: Array of Jalali years.
        month: Array of Jalali months (1-12).
        day: Array of Jalali days.
        hour: Optional array of hours.
        minute: Optional array of minutes.
        second: Optional array of seconds.
        microsecond: Optional array of microseconds.
        nanosecond: Optional array of nanoseconds.

    Returns:
        Array of numpy datetime64 values.
    """
    g_year, g_month, g_day = jalali_to_gregorian_vectorized(
        year, month, day, use_lookup=True
    )

    # Build datetime strings
    n = len(year)
    if hour is None:
        hour = np.zeros(n, dtype=np.int64)
    if minute is None:
        minute = np.zeros(n, dtype=np.int64)
    if second is None:
        second = np.zeros(n, dtype=np.int64)
    if microsecond is None:
        microsecond = np.zeros(n, dtype=np.int64)
    if nanosecond is None:
        nanosecond = np.zeros(n, dtype=np.int64)

    # Create datetime64 array
    # Convert to nanoseconds since epoch
    dates = pd.to_datetime(
        {
            "year": g_year,
            "month": g_month,
            "day": g_day,
            "hour": hour,
            "minute": minute,
            "second": second,
        }
    )

    # Add microseconds and nanoseconds
    result = (
        dates
        + pd.to_timedelta(microsecond, unit="us")
        + pd.to_timedelta(nanosecond, unit="ns")
    )

    return result.to_numpy()


__all__ = [
    "jalali_to_gregorian_scalar",
    "gregorian_to_jalali_scalar",
    "jalali_to_gregorian_vectorized",
    "gregorian_to_jalali_vectorized",
    "datetime64_to_jalali",
    "jalali_to_datetime64",
]
