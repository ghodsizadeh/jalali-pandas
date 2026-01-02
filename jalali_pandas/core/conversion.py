"""Vectorized conversion utilities for Jalali-Gregorian date conversions.

This module provides optimized conversion functions using NumPy for
efficient batch processing of date conversions.
"""

from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

import jdatetime
import numpy as np
import pandas as pd

if TYPE_CHECKING:
    from numpy.typing import NDArray


def jalali_to_gregorian_scalar(year: int, month: int, day: int) -> tuple[int, int, int]:
    """Convert a single Jalali date to Gregorian.

    Args:
        year: Jalali year.
        month: Jalali month (1-12).
        day: Jalali day.

    Returns:
        Tuple of (gregorian_year, gregorian_month, gregorian_day).
    """
    jdate = jdatetime.date(year, month, day)
    gdate = jdate.togregorian()
    return gdate.year, gdate.month, gdate.day


def gregorian_to_jalali_scalar(year: int, month: int, day: int) -> tuple[int, int, int]:
    """Convert a single Gregorian date to Jalali.

    Args:
        year: Gregorian year.
        month: Gregorian month (1-12).
        day: Gregorian day.

    Returns:
        Tuple of (jalali_year, jalali_month, jalali_day).
    """
    gdate = date(year, month, day)
    jdate = jdatetime.date.fromgregorian(date=gdate)
    return jdate.year, jdate.month, jdate.day


def jalali_to_gregorian_vectorized(
    year: NDArray[np.int64],
    month: NDArray[np.int64],
    day: NDArray[np.int64],
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
    g_year = np.empty(n, dtype=np.int64)
    g_month = np.empty(n, dtype=np.int64)
    g_day = np.empty(n, dtype=np.int64)

    for i in range(n):
        gy, gm, gd = jalali_to_gregorian_scalar(
            int(year[i]), int(month[i]), int(day[i])
        )
        g_year[i] = gy
        g_month[i] = gm
        g_day[i] = gd

    return g_year, g_month, g_day


def gregorian_to_jalali_vectorized(
    year: NDArray[np.int64],
    month: NDArray[np.int64],
    day: NDArray[np.int64],
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
    j_year = np.empty(n, dtype=np.int64)
    j_month = np.empty(n, dtype=np.int64)
    j_day = np.empty(n, dtype=np.int64)

    for i in range(n):
        jy, jm, jd = gregorian_to_jalali_scalar(
            int(year[i]), int(month[i]), int(day[i])
        )
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

    return gregorian_to_jalali_vectorized(year, month, day)


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
    g_year, g_month, g_day = jalali_to_gregorian_vectorized(year, month, day)

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
