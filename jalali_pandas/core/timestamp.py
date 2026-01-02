"""JalaliTimestamp - Scalar Jalali datetime type."""

from __future__ import annotations

from datetime import datetime, time, timedelta
from datetime import tzinfo as dt_tzinfo
from typing import TYPE_CHECKING, Optional, Union, cast

import jdatetime
import numpy as np
import pandas as pd

from jalali_pandas.core.calendar import (
    days_in_month,
    is_leap_year,
    quarter_of_month,
    validate_jalali_date,
    week_of_year,
    weekday_of_jalali,
)

if TYPE_CHECKING:
    from typing import Literal


class JalaliTimestamp:
    """A Jalali (Persian/Shamsi) calendar timestamp.

    Similar to pandas.Timestamp but for the Jalali calendar system.

    Attributes:
        year: Jalali year.
        month: Jalali month (1-12).
        day: Jalali day (1-31).
        hour: Hour (0-23).
        minute: Minute (0-59).
        second: Second (0-59).
        microsecond: Microsecond (0-999999).
        nanosecond: Nanosecond (0-999).
        tzinfo: Timezone information.

    Examples:
        >>> ts = JalaliTimestamp(1402, 6, 15)
        >>> ts.year
        1402
        >>> ts.month
        6
        >>> ts.to_gregorian()
        Timestamp('2023-09-06 00:00:00')
    """

    __slots__ = (
        "_year",
        "_month",
        "_day",
        "_hour",
        "_minute",
        "_second",
        "_microsecond",
        "_nanosecond",
        "_tzinfo",
        "_gregorian_cache",
    )

    def __init__(
        self,
        year: int,
        month: int = 1,
        day: int = 1,
        hour: int = 0,
        minute: int = 0,
        second: int = 0,
        microsecond: int = 0,
        nanosecond: int = 0,
        tzinfo: dt_tzinfo | None = None,
    ) -> None:
        """Initialize a JalaliTimestamp.

        Args:
            year: Jalali year.
            month: Jalali month (1-12). Defaults to 1.
            day: Jalali day. Defaults to 1.
            hour: Hour (0-23). Defaults to 0.
            minute: Minute (0-59). Defaults to 0.
            second: Second (0-59). Defaults to 0.
            microsecond: Microsecond (0-999999). Defaults to 0.
            nanosecond: Nanosecond (0-999). Defaults to 0.
            tzinfo: Timezone. Defaults to None.

        Raises:
            ValueError: If any component is out of valid range.
        """
        validate_jalali_date(year, month, day)

        if not 0 <= hour <= 23:
            raise ValueError(f"Hour must be 0-23, got {hour}")
        if not 0 <= minute <= 59:
            raise ValueError(f"Minute must be 0-59, got {minute}")
        if not 0 <= second <= 59:
            raise ValueError(f"Second must be 0-59, got {second}")
        if not 0 <= microsecond <= 999999:
            raise ValueError(f"Microsecond must be 0-999999, got {microsecond}")
        if not 0 <= nanosecond <= 999:
            raise ValueError(f"Nanosecond must be 0-999, got {nanosecond}")

        self._year = year
        self._month = month
        self._day = day
        self._hour = hour
        self._minute = minute
        self._second = second
        self._microsecond = microsecond
        self._nanosecond = nanosecond
        self._tzinfo = tzinfo
        self._gregorian_cache: pd.Timestamp | None = None

    # -------------------------------------------------------------------------
    # Properties
    # -------------------------------------------------------------------------

    @property
    def year(self) -> int:
        """Jalali year."""
        return self._year

    @property
    def month(self) -> int:
        """Jalali month (1-12)."""
        return self._month

    @property
    def day(self) -> int:
        """Jalali day (1-31)."""
        return self._day

    @property
    def hour(self) -> int:
        """Hour (0-23)."""
        return self._hour

    @property
    def minute(self) -> int:
        """Minute (0-59)."""
        return self._minute

    @property
    def second(self) -> int:
        """Second (0-59)."""
        return self._second

    @property
    def microsecond(self) -> int:
        """Microsecond (0-999999)."""
        return self._microsecond

    @property
    def nanosecond(self) -> int:
        """Nanosecond (0-999)."""
        return self._nanosecond

    @property
    def tzinfo(self) -> dt_tzinfo | None:
        """Timezone information."""
        return self._tzinfo

    @property
    def tz(self) -> dt_tzinfo | None:
        """Alias for tzinfo."""
        return self._tzinfo

    # -------------------------------------------------------------------------
    # Derived Properties
    # -------------------------------------------------------------------------

    @property
    def quarter(self) -> int:
        """Quarter of the year (1-4)."""
        return quarter_of_month(self._month)

    @property
    def dayofweek(self) -> int:
        """Day of week (0=Saturday, 6=Friday)."""
        return weekday_of_jalali(self._year, self._month, self._day)

    @property
    def weekday(self) -> int:
        """Alias for dayofweek."""
        return self.dayofweek

    @property
    def dayofyear(self) -> int:
        """Day of year (1-366)."""
        from jalali_pandas.core.calendar import day_of_year

        return day_of_year(self._year, self._month, self._day)

    @property
    def week(self) -> int:
        """Week of year (1-53)."""
        return week_of_year(self._year, self._month, self._day)

    @property
    def weekofyear(self) -> int:
        """Alias for week."""
        return self.week

    @property
    def days_in_month(self) -> int:
        """Number of days in the month."""
        return days_in_month(self._year, self._month)

    @property
    def daysinmonth(self) -> int:
        """Alias for days_in_month."""
        return self.days_in_month

    @property
    def is_leap_year(self) -> bool:
        """Whether the year is a leap year."""
        return is_leap_year(self._year)

    @property
    def is_month_start(self) -> bool:
        """Whether the date is the first day of the month."""
        return self._day == 1

    @property
    def is_month_end(self) -> bool:
        """Whether the date is the last day of the month."""
        return self._day == self.days_in_month

    @property
    def is_quarter_start(self) -> bool:
        """Whether the date is the first day of a quarter."""
        return self._month in (1, 4, 7, 10) and self._day == 1

    @property
    def is_quarter_end(self) -> bool:
        """Whether the date is the last day of a quarter."""
        return self._month in (3, 6, 9, 12) and self.is_month_end

    @property
    def is_year_start(self) -> bool:
        """Whether the date is the first day of the year (Nowruz)."""
        return self._month == 1 and self._day == 1

    @property
    def is_year_end(self) -> bool:
        """Whether the date is the last day of the year."""
        return self._month == 12 and self.is_month_end

    # -------------------------------------------------------------------------
    # Conversion Methods
    # -------------------------------------------------------------------------

    def to_gregorian(self) -> pd.Timestamp:
        """Convert to pandas Timestamp (Gregorian).

        Returns:
            Equivalent pandas Timestamp in Gregorian calendar.
        """
        if self._gregorian_cache is not None:
            return self._gregorian_cache

        gregorian = jdatetime.datetime(
            self._year,
            self._month,
            self._day,
            self._hour,
            self._minute,
            self._second,
            self._microsecond,
        ).togregorian()
        ts = pd.Timestamp(
            year=gregorian.year,
            month=gregorian.month,
            day=gregorian.day,
            hour=gregorian.hour,
            minute=gregorian.minute,
            second=gregorian.second,
            microsecond=gregorian.microsecond,
            nanosecond=self._nanosecond,
            tz=self._tzinfo,
        )

        self._gregorian_cache = ts
        return ts

    def to_pydatetime(self) -> datetime:
        """Convert to Python datetime (Gregorian).

        Returns:
            Equivalent Python datetime in Gregorian calendar.
        """
        return self.to_gregorian().to_pydatetime()

    def to_datetime64(self) -> np.datetime64:
        """Convert to numpy datetime64.

        Returns:
            Equivalent numpy datetime64.
        """
        return self.to_gregorian().to_datetime64()

    @classmethod
    def from_gregorian(
        cls,
        ts: pd.Timestamp | datetime | str,
        tz: dt_tzinfo | str | None = None,
    ) -> JalaliTimestamp:
        """Create JalaliTimestamp from Gregorian datetime.

        Args:
            ts: Gregorian timestamp (pandas Timestamp, datetime, or string).
            tz: Timezone to use. Defaults to None.

        Returns:
            Equivalent JalaliTimestamp.
        """
        if (
            isinstance(ts, str)
            or isinstance(ts, datetime)
            and not isinstance(ts, pd.Timestamp)
        ):
            ts = pd.Timestamp(ts)

        if tz is not None:
            ts = ts.tz_localize(tz) if ts.tzinfo is None else ts.tz_convert(tz)

        jalali = jdatetime.datetime.fromgregorian(datetime=ts.to_pydatetime())

        return cls(
            year=jalali.year,
            month=jalali.month,
            day=jalali.day,
            hour=jalali.hour,
            minute=jalali.minute,
            second=jalali.second,
            microsecond=jalali.microsecond,
            nanosecond=ts.nanosecond,
            tzinfo=ts.tzinfo,
        )

    @classmethod
    def now(cls, tz: dt_tzinfo | str | None = None) -> JalaliTimestamp:
        """Get current JalaliTimestamp.

        Args:
            tz: Timezone. Defaults to None (local time).

        Returns:
            Current time as JalaliTimestamp.
        """
        return cls.from_gregorian(pd.Timestamp.now(tz=tz))

    @classmethod
    def today(cls) -> JalaliTimestamp:
        """Get today's date as JalaliTimestamp (midnight).

        Returns:
            Today's date as JalaliTimestamp.
        """
        now = cls.now()
        return cls(now.year, now.month, now.day)

    # -------------------------------------------------------------------------
    # String Methods
    # -------------------------------------------------------------------------

    def strftime(self, fmt: str) -> str:
        """Format timestamp as string.

        Supports standard strftime codes adapted for Jalali calendar.

        Args:
            fmt: Format string.

        Returns:
            Formatted string.
        """
        replacements = {
            "%Y": f"{self._year:04d}",
            "%y": f"{self._year % 100:02d}",
            "%m": f"{self._month:02d}",
            "%d": f"{self._day:02d}",
            "%H": f"{self._hour:02d}",
            "%M": f"{self._minute:02d}",
            "%S": f"{self._second:02d}",
            "%f": f"{self._microsecond:06d}",
            "%j": f"{self.dayofyear:03d}",
            "%W": f"{self.week:02d}",
            "%w": str(self.dayofweek),
        }

        result = fmt
        for code, value in replacements.items():
            result = result.replace(code, value)

        return result

    @classmethod
    def strptime(cls, date_string: str, fmt: str) -> JalaliTimestamp:
        """Parse string to JalaliTimestamp.

        Args:
            date_string: Date string to parse.
            fmt: Format string.

        Returns:
            Parsed JalaliTimestamp.
        """
        # Simple implementation for common formats
        import re

        # Build regex pattern from format string
        pattern = fmt
        groups: dict[str, str] = {}

        replacements = [
            ("%Y", r"(?P<year>\d{4})", "year"),
            ("%y", r"(?P<year2>\d{2})", "year2"),
            ("%m", r"(?P<month>\d{1,2})", "month"),
            ("%d", r"(?P<day>\d{1,2})", "day"),
            ("%H", r"(?P<hour>\d{1,2})", "hour"),
            ("%M", r"(?P<minute>\d{1,2})", "minute"),
            ("%S", r"(?P<second>\d{1,2})", "second"),
        ]

        for code, regex, name in replacements:
            if code in pattern:
                pattern = pattern.replace(code, regex)
                groups[name] = ""

        match = re.match(pattern, date_string)
        if not match:
            raise ValueError(f"Cannot parse '{date_string}' with format '{fmt}'")

        data = match.groupdict()

        year = int(data.get("year", 0) or data.get("year2", 0))
        if "year2" in data and data["year2"]:
            year = 1300 + year if year < 100 else year

        return cls(
            year=year,
            month=int(data.get("month", 1)),
            day=int(data.get("day", 1)),
            hour=int(data.get("hour", 0)),
            minute=int(data.get("minute", 0)),
            second=int(data.get("second", 0)),
        )

    def isoformat(self, sep: str = "T") -> str:
        """Return ISO 8601 formatted string.

        Args:
            sep: Separator between date and time. Defaults to 'T'.

        Returns:
            ISO formatted string.
        """
        date_part = f"{self._year:04d}-{self._month:02d}-{self._day:02d}"
        time_part = f"{self._hour:02d}:{self._minute:02d}:{self._second:02d}"

        if self._microsecond or self._nanosecond:
            time_part += f".{self._microsecond:06d}"

        result = f"{date_part}{sep}{time_part}"

        if self._tzinfo is not None:
            # Get timezone offset
            offset = self._tzinfo.utcoffset(None)
            if offset is not None:
                total_seconds = int(offset.total_seconds())
                hours, remainder = divmod(abs(total_seconds), 3600)
                minutes = remainder // 60
                sign = "+" if total_seconds >= 0 else "-"
                result += f"{sign}{hours:02d}:{minutes:02d}"

        return result

    # -------------------------------------------------------------------------
    # Arithmetic Operations
    # -------------------------------------------------------------------------

    def __add__(self, other: timedelta | pd.Timedelta) -> JalaliTimestamp:
        """Add timedelta to timestamp."""
        if isinstance(other, (timedelta, pd.Timedelta)):
            new_gregorian = self.to_gregorian() + other
            return JalaliTimestamp.from_gregorian(new_gregorian)
        return NotImplemented

    def __radd__(self, other: timedelta | pd.Timedelta) -> JalaliTimestamp:
        """Right add timedelta to timestamp."""
        return self.__add__(other)

    def __sub__(
        self, other: JalaliTimestamp | timedelta | pd.Timedelta
    ) -> JalaliTimestamp | pd.Timedelta:
        """Subtract timedelta or another timestamp."""
        if isinstance(other, JalaliTimestamp):
            return self.to_gregorian() - other.to_gregorian()
        if isinstance(other, (timedelta, pd.Timedelta)):
            new_gregorian = self.to_gregorian() - other
            return JalaliTimestamp.from_gregorian(new_gregorian)
        return NotImplemented

    # -------------------------------------------------------------------------
    # Comparison Operations
    # -------------------------------------------------------------------------

    def __eq__(self, other: object) -> bool:
        """Check equality."""
        if isinstance(other, JalaliTimestamp):
            return (
                self._year == other._year
                and self._month == other._month
                and self._day == other._day
                and self._hour == other._hour
                and self._minute == other._minute
                and self._second == other._second
                and self._microsecond == other._microsecond
                and self._nanosecond == other._nanosecond
            )
        return False

    def __ne__(self, other: object) -> bool:
        """Check inequality."""
        return not self.__eq__(other)

    def __lt__(self, other: JalaliTimestamp) -> bool:
        """Less than comparison."""
        if not isinstance(other, JalaliTimestamp):
            return NotImplemented
        return self.to_gregorian() < other.to_gregorian()

    def __le__(self, other: JalaliTimestamp) -> bool:
        """Less than or equal comparison."""
        if not isinstance(other, JalaliTimestamp):
            return NotImplemented
        return self.to_gregorian() <= other.to_gregorian()

    def __gt__(self, other: JalaliTimestamp) -> bool:
        """Greater than comparison."""
        if not isinstance(other, JalaliTimestamp):
            return NotImplemented
        return self.to_gregorian() > other.to_gregorian()

    def __ge__(self, other: JalaliTimestamp) -> bool:
        """Greater than or equal comparison."""
        if not isinstance(other, JalaliTimestamp):
            return NotImplemented
        return self.to_gregorian() >= other.to_gregorian()

    def __hash__(self) -> int:
        """Hash for use in sets and dicts."""
        return hash(
            (
                self._year,
                self._month,
                self._day,
                self._hour,
                self._minute,
                self._second,
                self._microsecond,
                self._nanosecond,
            )
        )

    # -------------------------------------------------------------------------
    # String Representations
    # -------------------------------------------------------------------------

    def __repr__(self) -> str:
        """Detailed string representation."""
        tz_str = f", tz='{self._tzinfo}'" if self._tzinfo else ""
        return f"JalaliTimestamp('{self.isoformat()}'{tz_str})"

    def __str__(self) -> str:
        """Human-readable string representation."""
        return self.isoformat(sep=" ")

    # -------------------------------------------------------------------------
    # Replacement Methods
    # -------------------------------------------------------------------------

    def replace(
        self,
        year: int | None = None,
        month: int | None = None,
        day: int | None = None,
        hour: int | None = None,
        minute: int | None = None,
        second: int | None = None,
        microsecond: int | None = None,
        nanosecond: int | None = None,
        tzinfo: dt_tzinfo | None | object = ...,
    ) -> JalaliTimestamp:
        """Return timestamp with replaced components.

        Args:
            year: New year (or None to keep current).
            month: New month (or None to keep current).
            day: New day (or None to keep current).
            hour: New hour (or None to keep current).
            minute: New minute (or None to keep current).
            second: New second (or None to keep current).
            microsecond: New microsecond (or None to keep current).
            nanosecond: New nanosecond (or None to keep current).
            tzinfo: New timezone (or ... to keep current).

        Returns:
            New JalaliTimestamp with replaced components.
        """
        return JalaliTimestamp(
            year=year if year is not None else self._year,
            month=month if month is not None else self._month,
            day=day if day is not None else self._day,
            hour=hour if hour is not None else self._hour,
            minute=minute if minute is not None else self._minute,
            second=second if second is not None else self._second,
            microsecond=microsecond if microsecond is not None else self._microsecond,
            nanosecond=nanosecond if nanosecond is not None else self._nanosecond,
            tzinfo=self._tzinfo if tzinfo is ... else cast(Optional[dt_tzinfo], tzinfo),
        )

    def normalize(self) -> JalaliTimestamp:
        """Return timestamp with time set to midnight.

        Returns:
            New JalaliTimestamp at midnight.
        """
        return self.replace(hour=0, minute=0, second=0, microsecond=0, nanosecond=0)

    def date(self) -> JalaliTimestamp:
        """Return date part only (time set to midnight).

        Returns:
            New JalaliTimestamp at midnight.
        """
        return self.normalize()

    def time(self) -> time:
        """Return time part as Python time object.

        Returns:
            Python time object.
        """
        return time(
            hour=self._hour,
            minute=self._minute,
            second=self._second,
            microsecond=self._microsecond,
            tzinfo=self._tzinfo,
        )

    # -------------------------------------------------------------------------
    # Timezone Methods
    # -------------------------------------------------------------------------

    def tz_localize(
        self,
        tz: dt_tzinfo | str | None,
        ambiguous: str = "raise",
        nonexistent: str = "raise",
    ) -> JalaliTimestamp:
        """Localize tz-naive timestamp to a timezone.

        Args:
            tz: Timezone to localize to. Can be a timezone object or string.
            ambiguous: How to handle ambiguous times. Defaults to 'raise'.
            nonexistent: How to handle nonexistent times. Defaults to 'raise'.

        Returns:
            New JalaliTimestamp with timezone.

        Raises:
            TypeError: If timestamp is already tz-aware.
        """
        if self._tzinfo is not None:
            raise TypeError(
                "Cannot localize tz-aware timestamp. "
                "Use tz_convert() to convert between timezones."
            )

        # Convert to Gregorian, localize, then convert back
        gregorian = self.to_gregorian()
        localized = gregorian.tz_localize(
            tz, ambiguous=ambiguous, nonexistent=nonexistent
        )

        # Create new JalaliTimestamp with the timezone
        return JalaliTimestamp(
            year=self._year,
            month=self._month,
            day=self._day,
            hour=self._hour,
            minute=self._minute,
            second=self._second,
            microsecond=self._microsecond,
            nanosecond=self._nanosecond,
            tzinfo=localized.tzinfo,
        )

    def tz_convert(self, tz: dt_tzinfo | str | None) -> JalaliTimestamp:
        """Convert tz-aware timestamp to another timezone.

        Args:
            tz: Target timezone. Can be a timezone object or string.

        Returns:
            New JalaliTimestamp in the target timezone.

        Raises:
            TypeError: If timestamp is tz-naive.
        """
        if self._tzinfo is None:
            raise TypeError(
                "Cannot convert tz-naive timestamp. "
                "Use tz_localize() first to add timezone."
            )

        # Convert to Gregorian, convert timezone, then convert back to Jalali
        gregorian = self.to_gregorian()
        converted = gregorian.tz_convert(tz)

        # Convert the new Gregorian time back to Jalali
        return JalaliTimestamp.from_gregorian(converted)


class _JalaliNaTType:
    """Singleton class representing Not-a-Time for Jalali timestamps.

    This is analogous to pandas.NaT for Jalali datetimes.
    """

    _instance: _JalaliNaTType | None = None

    def __new__(cls) -> _JalaliNaTType:
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __repr__(self) -> str:
        return "JalaliNaT"

    def __str__(self) -> str:
        return "JalaliNaT"

    def __bool__(self) -> Literal[False]:
        return False

    def __hash__(self) -> int:
        return hash("JalaliNaT")

    # Comparison operations - NaT comparisons always return False (except !=)
    def __eq__(self, other: object) -> bool:
        return isinstance(other, _JalaliNaTType) or other is pd.NaT

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __lt__(self, other: object) -> bool:
        return False

    def __le__(self, other: object) -> bool:
        return isinstance(other, _JalaliNaTType)

    def __gt__(self, other: object) -> bool:
        return False

    def __ge__(self, other: object) -> bool:
        return isinstance(other, _JalaliNaTType)

    # Arithmetic operations return NaT
    def __add__(self, other: object) -> _JalaliNaTType:
        return self

    def __radd__(self, other: object) -> _JalaliNaTType:
        return self

    def __sub__(self, other: object) -> _JalaliNaTType:
        return self

    def __rsub__(self, other: object) -> _JalaliNaTType:
        return self

    # Properties return NaN or NaT equivalents
    @property
    def year(self) -> float:
        return float("nan")

    @property
    def month(self) -> float:
        return float("nan")

    @property
    def day(self) -> float:
        return float("nan")

    @property
    def hour(self) -> float:
        return float("nan")

    @property
    def minute(self) -> float:
        return float("nan")

    @property
    def second(self) -> float:
        return float("nan")

    @property
    def microsecond(self) -> float:
        return float("nan")

    @property
    def nanosecond(self) -> float:
        return float("nan")

    @property
    def tzinfo(self) -> None:
        return None

    @property
    def tz(self) -> None:
        return None

    @property
    def quarter(self) -> float:
        return float("nan")

    @property
    def dayofweek(self) -> float:
        return float("nan")

    @property
    def weekday(self) -> float:
        return float("nan")

    @property
    def dayofyear(self) -> float:
        return float("nan")

    @property
    def week(self) -> float:
        return float("nan")

    @property
    def weekofyear(self) -> float:
        return float("nan")

    @property
    def days_in_month(self) -> float:
        return float("nan")

    @property
    def daysinmonth(self) -> float:
        return float("nan")

    @property
    def is_leap_year(self) -> bool:
        return False

    @property
    def is_month_start(self) -> bool:
        return False

    @property
    def is_month_end(self) -> bool:
        return False

    @property
    def is_quarter_start(self) -> bool:
        return False

    @property
    def is_quarter_end(self) -> bool:
        return False

    @property
    def is_year_start(self) -> bool:
        return False

    @property
    def is_year_end(self) -> bool:
        return False

    def to_gregorian(self) -> pd.NaTType:  # type: ignore[name-defined]
        return pd.NaT

    def to_pydatetime(self) -> None:
        return None

    def to_datetime64(self) -> np.datetime64:
        return np.datetime64("NaT")

    def strftime(self, _fmt: str) -> str:
        return "NaT"

    def isoformat(self, _sep: str = "T") -> str:
        return "NaT"

    def normalize(self) -> _JalaliNaTType:
        return self

    def date(self) -> _JalaliNaTType:
        return self

    def time(self) -> None:
        return None

    def replace(self, **_kwargs: object) -> _JalaliNaTType:
        return self

    def tz_localize(self, _tz: object) -> _JalaliNaTType:
        return self

    def tz_convert(self, _tz: object) -> _JalaliNaTType:
        return self


# Singleton instance
JalaliNaT: _JalaliNaTType = _JalaliNaTType()

# Type alias for JalaliTimestamp or NaT
JalaliTimestampOrNaT = Union["JalaliTimestamp", _JalaliNaTType]


def isna_jalali(value: object) -> bool:
    """Check if a value is JalaliNaT or pandas NaT.

    Args:
        value: Value to check.

    Returns:
        True if value is NaT.
    """
    return isinstance(value, _JalaliNaTType) or value is pd.NaT or pd.isna(value)


__all__ = ["JalaliTimestamp", "JalaliNaT", "isna_jalali", "JalaliTimestampOrNaT"]
