"""Jalali month offsets."""

from __future__ import annotations

from typing import TYPE_CHECKING

from jalali_pandas.core.calendar import days_in_month
from jalali_pandas.offsets.base import JalaliOffset

if TYPE_CHECKING:
    from jalali_pandas.core.timestamp import JalaliTimestamp


class JalaliMonthBegin(JalaliOffset):
    """Offset to the beginning of a Jalali month."""

    _prefix = "JMS"

    def __add__(self, other: JalaliTimestamp) -> JalaliTimestamp:
        """Add months to timestamp, landing on month start."""
        from jalali_pandas.core.timestamp import JalaliTimestamp

        if not isinstance(other, JalaliTimestamp):
            return NotImplemented

        # Calculate target month
        total_months = other.year * 12 + other.month - 1 + self._n
        new_year = total_months // 12
        new_month = total_months % 12 + 1

        return JalaliTimestamp(
            year=new_year,
            month=new_month,
            day=1,
            hour=other.hour if not self._normalize else 0,
            minute=other.minute if not self._normalize else 0,
            second=other.second if not self._normalize else 0,
            microsecond=other.microsecond if not self._normalize else 0,
            nanosecond=other.nanosecond if not self._normalize else 0,
            tzinfo=other.tzinfo,
        )

    def __sub__(self, other: JalaliTimestamp) -> JalaliTimestamp:
        """Subtract months from timestamp."""
        return self.__neg__().__add__(other)

    def rollforward(self, dt: JalaliTimestamp) -> JalaliTimestamp:
        """Roll forward to next month start if not already on one."""
        if self.is_on_offset(dt):
            return dt
        return self.__add__(dt)

    def rollback(self, dt: JalaliTimestamp) -> JalaliTimestamp:
        """Roll back to previous month start."""
        from jalali_pandas.core.timestamp import JalaliTimestamp

        if self.is_on_offset(dt):
            return dt
        return JalaliTimestamp(
            year=dt.year,
            month=dt.month,
            day=1,
            hour=dt.hour if not self._normalize else 0,
            minute=dt.minute if not self._normalize else 0,
            second=dt.second if not self._normalize else 0,
            tzinfo=dt.tzinfo,
        )

    def is_on_offset(self, dt: JalaliTimestamp) -> bool:
        """Check if date is on month start."""
        return dt.day == 1


class JalaliMonthEnd(JalaliOffset):
    """Offset to the end of a Jalali month."""

    _prefix = "JME"

    def __add__(self, other: JalaliTimestamp) -> JalaliTimestamp:
        """Add months to timestamp, landing on month end."""
        from jalali_pandas.core.timestamp import JalaliTimestamp

        if not isinstance(other, JalaliTimestamp):
            return NotImplemented

        # Calculate target month
        total_months = other.year * 12 + other.month - 1 + self._n
        new_year = total_months // 12
        new_month = total_months % 12 + 1
        new_day = days_in_month(new_year, new_month)

        return JalaliTimestamp(
            year=new_year,
            month=new_month,
            day=new_day,
            hour=other.hour if not self._normalize else 0,
            minute=other.minute if not self._normalize else 0,
            second=other.second if not self._normalize else 0,
            microsecond=other.microsecond if not self._normalize else 0,
            nanosecond=other.nanosecond if not self._normalize else 0,
            tzinfo=other.tzinfo,
        )

    def __sub__(self, other: JalaliTimestamp) -> JalaliTimestamp:
        """Subtract months from timestamp."""
        return self.__neg__().__add__(other)

    def rollforward(self, dt: JalaliTimestamp) -> JalaliTimestamp:
        """Roll forward to next month end if not already on one."""
        if self.is_on_offset(dt):
            return dt
        return self._get_month_end(dt)

    def rollback(self, dt: JalaliTimestamp) -> JalaliTimestamp:
        """Roll back to previous month end."""
        from jalali_pandas.core.timestamp import JalaliTimestamp

        if self.is_on_offset(dt):
            return dt

        # Go to previous month's end
        if dt.month == 1:
            new_year = dt.year - 1
            new_month = 12
        else:
            new_year = dt.year
            new_month = dt.month - 1

        new_day = days_in_month(new_year, new_month)
        return JalaliTimestamp(
            year=new_year,
            month=new_month,
            day=new_day,
            hour=dt.hour if not self._normalize else 0,
            minute=dt.minute if not self._normalize else 0,
            second=dt.second if not self._normalize else 0,
            tzinfo=dt.tzinfo,
        )

    def is_on_offset(self, dt: JalaliTimestamp) -> bool:
        """Check if date is on month end."""
        return dt.day == days_in_month(dt.year, dt.month)

    def _get_month_end(self, dt: JalaliTimestamp) -> JalaliTimestamp:
        """Get the end of the current month."""
        from jalali_pandas.core.timestamp import JalaliTimestamp

        return JalaliTimestamp(
            year=dt.year,
            month=dt.month,
            day=days_in_month(dt.year, dt.month),
            hour=dt.hour if not self._normalize else 0,
            minute=dt.minute if not self._normalize else 0,
            second=dt.second if not self._normalize else 0,
            tzinfo=dt.tzinfo,
        )


__all__ = ["JalaliMonthBegin", "JalaliMonthEnd"]
