"""Jalali calendar frequency offsets."""

from jalali_pandas.offsets.aliases import (
    get_jalali_alias,
    get_jalali_offset,
    list_jalali_aliases,
    parse_jalali_frequency,
    register_jalali_alias,
)
from jalali_pandas.offsets.base import JalaliOffset
from jalali_pandas.offsets.month import JalaliMonthBegin, JalaliMonthEnd
from jalali_pandas.offsets.quarter import JalaliQuarterBegin, JalaliQuarterEnd
from jalali_pandas.offsets.week import (
    FRIDAY,
    MONDAY,
    SATURDAY,
    SUNDAY,
    THURSDAY,
    TUESDAY,
    WEDNESDAY,
    JalaliWeek,
)
from jalali_pandas.offsets.year import JalaliYearBegin, JalaliYearEnd

# Register week alias
register_jalali_alias("JW", JalaliWeek)

__all__ = [
    "JalaliOffset",
    "JalaliMonthBegin",
    "JalaliMonthEnd",
    "JalaliQuarterBegin",
    "JalaliQuarterEnd",
    "JalaliYearBegin",
    "JalaliYearEnd",
    "JalaliWeek",
    # Weekday constants
    "SATURDAY",
    "SUNDAY",
    "MONDAY",
    "TUESDAY",
    "WEDNESDAY",
    "THURSDAY",
    "FRIDAY",
    # Alias functions
    "register_jalali_alias",
    "get_jalali_offset",
    "get_jalali_alias",
    "parse_jalali_frequency",
    "list_jalali_aliases",
]
