"""Jalali quarter offsets."""

from __future__ import annotations

from typing import TYPE_CHECKING

from jalali_pandas.core.calendar import days_in_month
from jalali_pandas.offsets.base import JalaliOffset

if TYPE_CHECKING:
    from jalali_pandas.core.timestamp import JalaliTimestamp

# Quarter start months: Farvardin(1), Tir(4), Mehr(7), Dey(10)
QUARTER_START_MONTHS = (1, 4, 7, 10)
# Quarter end months: Khordad(3), Shahrivar(6), Azar(9), Esfand(12)
QUARTER_END_MONTHS = (3, 6, 9, 12)


class JalaliQuarterBegin(JalaliOffset):
    """Offset to the beginning of a Jalali quarter."""

    _prefix = "JQS"

    def __add__(self, other: JalaliTimestamp) -> JalaliTimestamp:
        """Add quarters to timestamp, landing on quarter start."""
        from jalali_pandas.core.timestamp import JalaliTimestamp

        if not isinstance(other, JalaliTimestamp):
            return NotImplemented

        # Calculate current quarter (0-indexed)
        current_quarter = (other.month - 1) // 3

        # Calculate target quarter
        total_quarters = other.year * 4 + current_quarter + self._n
        new_year = total_quarters // 4
        new_quarter = total_quarters % 4
        new_month = new_quarter * 3 + 1

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
        """Subtract quarters from timestamp."""
        return self.__neg__().__add__(other)

    def rollforward(self, dt: JalaliTimestamp) -> JalaliTimestamp:
        """Roll forward to next quarter start if not already on one."""
        if self.is_on_offset(dt):
            return dt
        return self.__add__(dt)

    def rollback(self, dt: JalaliTimestamp) -> JalaliTimestamp:
        """Roll back to current quarter start."""
        from jalali_pandas.core.timestamp import JalaliTimestamp

        if self.is_on_offset(dt):
            return dt

        quarter_start_month = ((dt.month - 1) // 3) * 3 + 1
        return JalaliTimestamp(
            year=dt.year,
            month=quarter_start_month,
            day=1,
            hour=dt.hour if not self._normalize else 0,
            minute=dt.minute if not self._normalize else 0,
            second=dt.second if not self._normalize else 0,
            tzinfo=dt.tzinfo,
        )

    def is_on_offset(self, dt: JalaliTimestamp) -> bool:
        """Check if date is on quarter start."""
        return dt.month in QUARTER_START_MONTHS and dt.day == 1


class JalaliQuarterEnd(JalaliOffset):
    """Offset to the end of a Jalali quarter."""

    _prefix = "JQE"

    def __add__(self, other: JalaliTimestamp) -> JalaliTimestamp:
        """Add quarters to timestamp, landing on quarter end."""
        from jalali_pandas.core.timestamp import JalaliTimestamp

        if not isinstance(other, JalaliTimestamp):
            return NotImplemented

        # Calculate current quarter (0-indexed)
        current_quarter = (other.month - 1) // 3

        # Calculate target quarter
        total_quarters = other.year * 4 + current_quarter + self._n
        new_year = total_quarters // 4
        new_quarter = total_quarters % 4
        new_month = (new_quarter + 1) * 3  # End month of quarter
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
        """Subtract quarters from timestamp."""
        return self.__neg__().__add__(other)

    def rollforward(self, dt: JalaliTimestamp) -> JalaliTimestamp:
        """Roll forward to next quarter end if not already on one."""
        if self.is_on_offset(dt):
            return dt
        return self._get_quarter_end(dt)

    def rollback(self, dt: JalaliTimestamp) -> JalaliTimestamp:
        """Roll back to previous quarter end."""
        from jalali_pandas.core.timestamp import JalaliTimestamp

        if self.is_on_offset(dt):
            return dt

        # Go to previous quarter's end
        current_quarter = (dt.month - 1) // 3
        if current_quarter == 0:
            new_year = dt.year - 1
            new_month = 12
        else:
            new_year = dt.year
            new_month = current_quarter * 3

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
        """Check if date is on quarter end."""
        if dt.month not in QUARTER_END_MONTHS:
            return False
        return dt.day == days_in_month(dt.year, dt.month)

    def _get_quarter_end(self, dt: JalaliTimestamp) -> JalaliTimestamp:
        """Get the end of the current quarter."""
        from jalali_pandas.core.timestamp import JalaliTimestamp

        quarter_end_month = ((dt.month - 1) // 3 + 1) * 3
        return JalaliTimestamp(
            year=dt.year,
            month=quarter_end_month,
            day=days_in_month(dt.year, quarter_end_month),
            hour=dt.hour if not self._normalize else 0,
            minute=dt.minute if not self._normalize else 0,
            second=dt.second if not self._normalize else 0,
            tzinfo=dt.tzinfo,
        )


__all__ = ["JalaliQuarterBegin", "JalaliQuarterEnd"]
