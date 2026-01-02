"""Jalali year offsets."""

from __future__ import annotations

from typing import TYPE_CHECKING

from jalali_pandas.core.calendar import days_in_month, is_leap_year
from jalali_pandas.offsets.base import JalaliOffset

if TYPE_CHECKING:
    from jalali_pandas.core.timestamp import JalaliTimestamp


class JalaliYearBegin(JalaliOffset):
    """Offset to the beginning of a Jalali year (Nowruz)."""

    _prefix = "JYS"

    def __add__(self, other: JalaliTimestamp) -> JalaliTimestamp:
        """Add years to timestamp, landing on year start (Nowruz)."""
        from jalali_pandas.core.timestamp import JalaliTimestamp

        if not isinstance(other, JalaliTimestamp):
            return NotImplemented

        new_year = other.year + self._n

        return JalaliTimestamp(
            year=new_year,
            month=1,
            day=1,
            hour=other.hour if not self._normalize else 0,
            minute=other.minute if not self._normalize else 0,
            second=other.second if not self._normalize else 0,
            microsecond=other.microsecond if not self._normalize else 0,
            nanosecond=other.nanosecond if not self._normalize else 0,
            tzinfo=other.tzinfo,
        )

    def __sub__(self, other: JalaliTimestamp) -> JalaliTimestamp:
        """Subtract years from timestamp."""
        return self.__neg__().__add__(other)

    def rollforward(self, dt: JalaliTimestamp) -> JalaliTimestamp:
        """Roll forward to next year start if not already on one."""
        if self.is_on_offset(dt):
            return dt
        return self.__add__(dt)

    def rollback(self, dt: JalaliTimestamp) -> JalaliTimestamp:
        """Roll back to current year start."""
        from jalali_pandas.core.timestamp import JalaliTimestamp

        if self.is_on_offset(dt):
            return dt

        return JalaliTimestamp(
            year=dt.year,
            month=1,
            day=1,
            hour=dt.hour if not self._normalize else 0,
            minute=dt.minute if not self._normalize else 0,
            second=dt.second if not self._normalize else 0,
            tzinfo=dt.tzinfo,
        )

    def is_on_offset(self, dt: JalaliTimestamp) -> bool:
        """Check if date is on year start (Nowruz - 1 Farvardin)."""
        return dt.month == 1 and dt.day == 1


class JalaliYearEnd(JalaliOffset):
    """Offset to the end of a Jalali year."""

    _prefix = "JYE"

    def __add__(self, other: JalaliTimestamp) -> JalaliTimestamp:
        """Add years to timestamp, landing on year end."""
        from jalali_pandas.core.timestamp import JalaliTimestamp

        if not isinstance(other, JalaliTimestamp):
            return NotImplemented

        new_year = other.year + self._n
        # Last day of Esfand (29 or 30 depending on leap year)
        new_day = 30 if is_leap_year(new_year) else 29

        return JalaliTimestamp(
            year=new_year,
            month=12,
            day=new_day,
            hour=other.hour if not self._normalize else 0,
            minute=other.minute if not self._normalize else 0,
            second=other.second if not self._normalize else 0,
            microsecond=other.microsecond if not self._normalize else 0,
            nanosecond=other.nanosecond if not self._normalize else 0,
            tzinfo=other.tzinfo,
        )

    def __sub__(self, other: JalaliTimestamp) -> JalaliTimestamp:
        """Subtract years from timestamp."""
        return self.__neg__().__add__(other)

    def rollforward(self, dt: JalaliTimestamp) -> JalaliTimestamp:
        """Roll forward to next year end if not already on one."""
        if self.is_on_offset(dt):
            return dt
        return self._get_year_end(dt)

    def rollback(self, dt: JalaliTimestamp) -> JalaliTimestamp:
        """Roll back to previous year end."""
        from jalali_pandas.core.timestamp import JalaliTimestamp

        if self.is_on_offset(dt):
            return dt

        # Go to previous year's end
        new_year = dt.year - 1
        new_day = 30 if is_leap_year(new_year) else 29

        return JalaliTimestamp(
            year=new_year,
            month=12,
            day=new_day,
            hour=dt.hour if not self._normalize else 0,
            minute=dt.minute if not self._normalize else 0,
            second=dt.second if not self._normalize else 0,
            tzinfo=dt.tzinfo,
        )

    def is_on_offset(self, dt: JalaliTimestamp) -> bool:
        """Check if date is on year end (last day of Esfand)."""
        if dt.month != 12:
            return False
        return dt.day == days_in_month(dt.year, 12)

    def _get_year_end(self, dt: JalaliTimestamp) -> JalaliTimestamp:
        """Get the end of the current year."""
        from jalali_pandas.core.timestamp import JalaliTimestamp

        return JalaliTimestamp(
            year=dt.year,
            month=12,
            day=days_in_month(dt.year, 12),
            hour=dt.hour if not self._normalize else 0,
            minute=dt.minute if not self._normalize else 0,
            second=dt.second if not self._normalize else 0,
            tzinfo=dt.tzinfo,
        )


__all__ = ["JalaliYearBegin", "JalaliYearEnd"]
