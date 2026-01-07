"""Jalali calendar rules and utilities."""

from __future__ import annotations

import numpy as np
import numpy.typing as npt

# Jalali epoch: 1 Farvardin 1 = March 22, 622 CE (Julian)
# In terms of days from Unix epoch (1970-01-01)
JALALI_EPOCH: int = -12219379200  # nanoseconds would be this * 1e9

# Month lengths for non-leap years
MONTH_LENGTHS: tuple[int, ...] = (31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 29)

# Month lengths for leap years (Esfand has 30 days)
MONTH_LENGTHS_LEAP: tuple[int, ...] = (31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 30)

# Cumulative days at start of each month (non-leap)
MONTH_STARTS: tuple[int, ...] = (0, 31, 62, 93, 124, 155, 186, 216, 246, 276, 306, 336)

# Month names in Persian
MONTH_NAMES_FA: tuple[str, ...] = (
    "فروردین",
    "اردیبهشت",
    "خرداد",
    "تیر",
    "مرداد",
    "شهریور",
    "مهر",
    "آبان",
    "آذر",
    "دی",
    "بهمن",
    "اسفند",
)

# Month names in English
MONTH_NAMES_EN: tuple[str, ...] = (
    "Farvardin",
    "Ordibehesht",
    "Khordad",
    "Tir",
    "Mordad",
    "Shahrivar",
    "Mehr",
    "Aban",
    "Azar",
    "Dey",
    "Bahman",
    "Esfand",
)

# Weekday names in Persian (Saturday=0 in Jalali calendar)
WEEKDAY_NAMES_FA: tuple[str, ...] = (
    "شنبه",
    "یکشنبه",
    "دوشنبه",
    "سه‌شنبه",
    "چهارشنبه",
    "پنجشنبه",
    "جمعه",
)

# Weekday names in English
WEEKDAY_NAMES_EN: tuple[str, ...] = (
    "Shanbeh",
    "Yekshanbeh",
    "Doshanbeh",
    "Seshanbeh",
    "Chaharshanbeh",
    "Panjshanbeh",
    "Jomeh",
)

# Leap year remainders in the 33-year cycle (jdatetime-compatible)
LEAP_YEAR_REMAINDERS: tuple[int, ...] = (1, 5, 9, 13, 17, 22, 26, 30)


def is_leap_year(year: int) -> bool:
    """Check if a Jalali year is a leap year.

    Uses the 33-year cycle algorithm used by jdatetime.

    Args:
        year: Jalali year.

    Returns:
        True if the year is a leap year, False otherwise.
    """
    return year % 33 in LEAP_YEAR_REMAINDERS


def is_leap_year_vectorized(years: npt.NDArray[np.int64]) -> npt.NDArray[np.bool_]:
    """Vectorized check for leap years.

    Args:
        years: Array of Jalali years.

    Returns:
        Boolean array indicating leap years.
    """
    remainders = years % 33
    return np.isin(remainders, LEAP_YEAR_REMAINDERS)


def days_in_year(year: int) -> int:
    """Get the number of days in a Jalali year.

    Args:
        year: Jalali year.

    Returns:
        365 for normal years, 366 for leap years.
    """
    return 366 if is_leap_year(year) else 365


def days_in_month(year: int, month: int) -> int:
    """Get the number of days in a Jalali month.

    Args:
        year: Jalali year.
        month: Jalali month (1-12).

    Returns:
        Number of days in the month.

    Raises:
        ValueError: If month is not in range 1-12.
    """
    if not 1 <= month <= 12:
        raise ValueError(f"Month must be 1-12, got {month}")

    if month == 12:
        return 30 if is_leap_year(year) else 29
    return MONTH_LENGTHS[month - 1]


def days_in_month_vectorized(
    years: npt.NDArray[np.int64], months: npt.NDArray[np.int64]
) -> npt.NDArray[np.int64]:
    """Vectorized calculation of days in month.

    Args:
        years: Array of Jalali years.
        months: Array of Jalali months (1-12).

    Returns:
        Array of days in each month.
    """
    # Base month lengths (non-leap)
    month_lengths = np.array(MONTH_LENGTHS, dtype=np.int64)
    result = month_lengths[months - 1]

    # Adjust Esfand for leap years
    is_esfand = months == 12
    is_leap = is_leap_year_vectorized(years)
    result = np.where(is_esfand & is_leap, 30, result)

    return result


def quarter_of_month(month: int) -> int:
    """Get the quarter for a given month.

    Args:
        month: Jalali month (1-12).

    Returns:
        Quarter number (1-4).
    """
    return (month - 1) // 3 + 1


def week_of_year(year: int, month: int, day: int) -> int:
    """Get the week number of the year.

    Week 1 is the first week containing at least 4 days.
    Weeks start on Saturday (Jalali calendar convention).

    Args:
        year: Jalali year.
        month: Jalali month (1-12).
        day: Jalali day.

    Returns:
        Week number (1-53).
    """
    # Calculate day of year
    doy = day_of_year(year, month, day)

    # Calculate weekday of first day of year (0=Saturday)
    first_day_weekday = weekday_of_jalali(year, 1, 1)

    # ISO-like week calculation adapted for Saturday start
    # Week 1 is the week containing the first Thursday (day 5 in 0-indexed Sat start)
    week = (doy + first_day_weekday - 1) // 7 + 1

    return week


def day_of_year(year: int, month: int, day: int) -> int:
    """Get the day of year (1-366).

    Args:
        year: Jalali year.
        month: Jalali month (1-12).
        day: Jalali day.

    Returns:
        Day of year (1-366).
    """
    max_day = days_in_month(year, month)
    if not 1 <= day <= max_day:
        raise ValueError(f"Day must be 1-{max_day} for month {month}, got {day}")
    return MONTH_STARTS[month - 1] + day


def weekday_of_jalali(year: int, month: int, day: int) -> int:
    """Get the weekday of a Jalali date.

    Args:
        year: Jalali year.
        month: Jalali month (1-12).
        day: Jalali day.

    Returns:
        Weekday (0=Saturday, 6=Friday).
    """
    # Convert to Julian Day Number and calculate weekday
    jdn = jalali_to_jdn(year, month, day)
    # Adjust for Jalali weekday convention (0=Saturday, 6=Friday)
    return (jdn + 2) % 7


def jalali_to_jdn(year: int, month: int, day: int) -> int:
    """Convert Jalali date to Julian Day Number.

    Args:
        year: Jalali year.
        month: Jalali month (1-12).
        day: Jalali day.

    Returns:
        Julian Day Number.
    """
    # Algorithm based on the 2820-year cycle
    a = year - 474 if year > 0 else year - 473
    b = a % 2820

    jdn = (
        day
        + (month - 1) * 30
        + min(6, month - 1)
        + ((b * 682 - 110) // 2816)
        + (b - 1) * 365
        + (a // 2820) * 1029983
        + 2121445
    )
    return jdn


def jdn_to_jalali(jdn: int) -> tuple[int, int, int]:
    """Convert Julian Day Number to Jalali date.

    Args:
        jdn: Julian Day Number.

    Returns:
        Tuple of (year, month, day).
    """
    # Use the inverse of jalali_to_jdn algorithm
    # Based on the 2820-year cycle
    jdn_offset = jdn - 2121445  # Epoch matching jalali_to_jdn

    cycle_2820 = jdn_offset // 1029983
    day_in_cycle = jdn_offset % 1029983

    if day_in_cycle < 0:
        cycle_2820 -= 1
        day_in_cycle += 1029983

    # Find year within cycle using binary search approach
    # For year b within cycle, start of year (day=1, month=1) has offset:
    # 1 + ((b*682-110)//2816) + (b-1)*365
    def days_to_year_start(b: int) -> int:
        return 1 + ((b * 682 - 110) // 2816) + (b - 1) * 365

    # Binary search for the year
    lo, hi = 0, 2820
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if days_to_year_start(mid) <= day_in_cycle:
            lo = mid
        else:
            hi = mid - 1

    year_in_cycle = lo
    remaining_days = day_in_cycle - days_to_year_start(year_in_cycle)

    year = cycle_2820 * 2820 + year_in_cycle + 474

    # Find month and day from remaining_days (0-indexed day within year)
    if remaining_days < 186:  # First 6 months (31 days each)
        month = remaining_days // 31 + 1
        day = remaining_days % 31 + 1
    else:
        remaining_days -= 186
        if remaining_days < 150:  # Months 7-11 (30 days each)
            month = remaining_days // 30 + 7
            day = remaining_days % 30 + 1
        else:
            remaining_days -= 150
            month = 12
            day = remaining_days + 1

    return (year, month, day)


def validate_jalali_date(year: int, month: int, day: int) -> bool:
    """Validate a Jalali date.

    Args:
        year: Jalali year.
        month: Jalali month (1-12).
        day: Jalali day.

    Returns:
        True if the date is valid.

    Raises:
        ValueError: If the date is invalid.
    """
    if not 1 <= month <= 12:
        raise ValueError(f"Month must be 1-12, got {month}")

    max_day = days_in_month(year, month)
    if not 1 <= day <= max_day:
        raise ValueError(f"Day must be 1-{max_day} for month {month}, got {day}")

    return True


__all__ = [
    "JALALI_EPOCH",
    "MONTH_LENGTHS",
    "MONTH_LENGTHS_LEAP",
    "MONTH_STARTS",
    "MONTH_NAMES_FA",
    "MONTH_NAMES_EN",
    "WEEKDAY_NAMES_FA",
    "WEEKDAY_NAMES_EN",
    "is_leap_year",
    "is_leap_year_vectorized",
    "days_in_year",
    "days_in_month",
    "days_in_month_vectorized",
    "quarter_of_month",
    "week_of_year",
    "day_of_year",
    "weekday_of_jalali",
    "jalali_to_jdn",
    "jdn_to_jalali",
    "validate_jalali_date",
]
