"""Enhanced Series accessor for Jalali datetime operations."""

from __future__ import annotations

from datetime import time
from datetime import tzinfo as dt_tzinfo
from typing import Any, Literal, cast

import jdatetime
import numpy as np
import pandas as pd

from jalali_pandas.core.calendar import (
    MONTH_NAMES_EN,
    MONTH_NAMES_FA,
    WEEKDAY_NAMES_EN,
    WEEKDAY_NAMES_FA,
    day_of_year,
    days_in_month,
    is_leap_year,
    quarter_of_month,
    week_of_year,
    weekday_of_jalali,
)


@pd.api.extensions.register_series_accessor("jalali")
class JalaliSeriesAccessor:
    """Enhanced accessor for Jalali datetime operations on pandas Series.

    Provides properties and methods for working with Jalali (Persian/Shamsi)
    dates in pandas Series.

    Attributes:
        year: Jalali year component.
        month: Jalali month component (1-12).
        day: Jalali day component.
        hour: Hour component (0-23).
        minute: Minute component (0-59).
        second: Second component (0-59).
        microsecond: Microsecond component.
        nanosecond: Nanosecond component.
        quarter: Quarter of the year (1-4).
        weekday: Day of week (0=Saturday, 6=Friday).
        dayofweek: Alias for weekday.
        dayofyear: Day of year (1-366).
        daysinmonth: Number of days in the month.
        week: Week of year.
        weekofyear: Alias for week.
        is_leap_year: Whether the year is a leap year.
        is_month_start: Whether the date is the first day of the month.
        is_month_end: Whether the date is the last day of the month.
        is_quarter_start: Whether the date is the first day of a quarter.
        is_quarter_end: Whether the date is the last day of a quarter.
        is_year_start: Whether the date is the first day of the year.
        is_year_end: Whether the date is the last day of the year.
        date: Date part (time set to midnight).
        time: Time part as Python time objects.

    Examples:
        >>> import pandas as pd
        >>> import jalali_pandas
        >>> s = pd.Series(pd.date_range("2023-03-21", periods=5))
        >>> s.jalali.to_jalali()
        >>> s.jalali.year
        >>> s.jalali.month_name()
    """

    def __init__(self, pandas_obj: pd.Series) -> None:
        """Initialize the accessor.

        Args:
            pandas_obj: A pandas Series containing datetime data.
        """
        self._obj: pd.Series = pandas_obj

    def _validate(self) -> None:
        """Validate pandas series contains jdatetime objects.

        Raises:
            TypeError: If series doesn't contain jdatetime or string dates.
        """
        if len(self._obj) == 0:
            return
        first_valid = (
            self._obj.dropna().iloc[0] if len(self._obj.dropna()) > 0 else None
        )
        if first_valid is not None and not isinstance(
            first_valid, (str, jdatetime.date, jdatetime.datetime)
        ):
            raise TypeError("pandas series must be jdatetime or string of jdate")

    def _get_jdate_attr(self, attr: str) -> pd.Series:
        """Get an attribute from jdatetime objects in the series.

        Args:
            attr: Attribute name to get.

        Returns:
            Series with the attribute values.
        """
        self._validate()

        def get_attr(x: Any) -> Any:
            if pd.isna(x):
                return np.nan
            val = getattr(x, attr, None)
            if callable(val):
                return val()
            return val

        return cast(pd.Series, self._obj.apply(get_attr))

    # -------------------------------------------------------------------------
    # Conversion Methods
    # -------------------------------------------------------------------------

    def to_jalali(self) -> pd.Series:
        """Convert Gregorian datetime to Jalali datetime.

        Returns:
            Series of jdatetime objects.
        """
        return cast(
            pd.Series,
            self._obj.apply(
                lambda x: jdatetime.datetime.fromgregorian(date=x)
                if not pd.isna(x)
                else pd.NaT
            ),
        )

    def to_gregorian(self) -> pd.Series:
        """Convert Jalali datetime to Gregorian datetime.

        Returns:
            Series of Python datetime objects.
        """
        self._validate()
        return cast(
            pd.Series,
            self._obj.apply(lambda x: x.togregorian() if not pd.isna(x) else pd.NaT),
        )

    def parse_jalali(self, format: str = "%Y-%m-%d") -> pd.Series:
        """Parse string dates to jdatetime objects.

        Args:
            format: strftime format string. Defaults to "%Y-%m-%d".

        Returns:
            Series of jdatetime objects.
        """
        return cast(
            pd.Series,
            self._obj.apply(
                lambda x: jdatetime.datetime.strptime(x, format)
                if not pd.isna(x)
                else pd.NaT
            ),
        )

    # -------------------------------------------------------------------------
    # Basic Properties
    # -------------------------------------------------------------------------

    @property
    def year(self) -> pd.Series:
        """Get Jalali year."""
        return self._get_jdate_attr("year")

    @property
    def month(self) -> pd.Series:
        """Get Jalali month (1-12)."""
        return self._get_jdate_attr("month")

    @property
    def day(self) -> pd.Series:
        """Get Jalali day."""
        return self._get_jdate_attr("day")

    @property
    def hour(self) -> pd.Series:
        """Get hour component (0-23)."""
        return self._get_jdate_attr("hour")

    @property
    def minute(self) -> pd.Series:
        """Get minute component (0-59)."""
        return self._get_jdate_attr("minute")

    @property
    def second(self) -> pd.Series:
        """Get second component (0-59)."""
        return self._get_jdate_attr("second")

    @property
    def microsecond(self) -> pd.Series:
        """Get microsecond component."""
        return self._get_jdate_attr("microsecond")

    @property
    def nanosecond(self) -> pd.Series:
        """Get nanosecond component (always 0 for jdatetime)."""
        self._validate()
        return cast(
            pd.Series,
            self._obj.apply(lambda x: 0 if not pd.isna(x) else np.nan),
        )

    @property
    def weekday(self) -> pd.Series:
        """Get Jalali weekday (0=Saturday, 6=Friday)."""
        return self._get_jdate_attr("weekday")

    @property
    def dayofweek(self) -> pd.Series:
        """Alias for weekday."""
        return self.weekday

    @property
    def weeknumber(self) -> pd.Series:
        """Get week number of the year."""
        return self._get_jdate_attr("weeknumber")

    @property
    def week(self) -> pd.Series:
        """Get week number of the year."""
        self._validate()

        def get_week(x: Any) -> Any:
            if pd.isna(x):
                return np.nan
            return week_of_year(x.year, x.month, x.day)

        return cast(pd.Series, self._obj.apply(get_week))

    @property
    def weekofyear(self) -> pd.Series:
        """Alias for week."""
        return self.week

    @property
    def quarter(self) -> pd.Series:
        """Get Jalali quarter (1-4)."""
        self._validate()

        def get_quarter(x: Any) -> Any:
            if pd.isna(x):
                return np.nan
            return quarter_of_month(x.month)

        return cast(pd.Series, self._obj.apply(get_quarter))

    @property
    def dayofyear(self) -> pd.Series:
        """Get day of year (1-366)."""
        self._validate()

        def get_dayofyear(x: Any) -> Any:
            if pd.isna(x):
                return np.nan
            return day_of_year(x.year, x.month, x.day)

        return cast(pd.Series, self._obj.apply(get_dayofyear))

    @property
    def daysinmonth(self) -> pd.Series:
        """Get number of days in the month."""
        self._validate()

        def get_daysinmonth(x: Any) -> Any:
            if pd.isna(x):
                return np.nan
            return days_in_month(x.year, x.month)

        return cast(pd.Series, self._obj.apply(get_daysinmonth))

    @property
    def days_in_month(self) -> pd.Series:
        """Alias for daysinmonth."""
        return self.daysinmonth

    # -------------------------------------------------------------------------
    # Boolean Properties
    # -------------------------------------------------------------------------

    @property
    def is_leap_year(self) -> pd.Series:
        """Check if the year is a leap year."""
        self._validate()

        def check_leap(x: Any) -> Any:
            if pd.isna(x):
                return False
            return is_leap_year(x.year)

        return cast(pd.Series, self._obj.apply(check_leap))

    @property
    def is_month_start(self) -> pd.Series:
        """Check if the date is the first day of the month."""
        self._validate()

        def check_month_start(x: Any) -> Any:
            if pd.isna(x):
                return False
            return x.day == 1

        return cast(pd.Series, self._obj.apply(check_month_start))

    @property
    def is_month_end(self) -> pd.Series:
        """Check if the date is the last day of the month."""
        self._validate()

        def check_month_end(x: Any) -> Any:
            if pd.isna(x):
                return False
            return x.day == days_in_month(x.year, x.month)

        return cast(pd.Series, self._obj.apply(check_month_end))

    @property
    def is_quarter_start(self) -> pd.Series:
        """Check if the date is the first day of a quarter."""
        self._validate()

        def check_quarter_start(x: Any) -> Any:
            if pd.isna(x):
                return False
            return x.month in (1, 4, 7, 10) and x.day == 1

        return cast(pd.Series, self._obj.apply(check_quarter_start))

    @property
    def is_quarter_end(self) -> pd.Series:
        """Check if the date is the last day of a quarter."""
        self._validate()

        def check_quarter_end(x: Any) -> Any:
            if pd.isna(x):
                return False
            if x.month not in (3, 6, 9, 12):
                return False
            return x.day == days_in_month(x.year, x.month)

        return cast(pd.Series, self._obj.apply(check_quarter_end))

    @property
    def is_year_start(self) -> pd.Series:
        """Check if the date is the first day of the year (Nowruz)."""
        self._validate()

        def check_year_start(x: Any) -> Any:
            if pd.isna(x):
                return False
            return x.month == 1 and x.day == 1

        return cast(pd.Series, self._obj.apply(check_year_start))

    @property
    def is_year_end(self) -> pd.Series:
        """Check if the date is the last day of the year."""
        self._validate()

        def check_year_end(x: Any) -> Any:
            if pd.isna(x):
                return False
            return x.month == 12 and x.day == days_in_month(x.year, 12)

        return cast(pd.Series, self._obj.apply(check_year_end))

    # -------------------------------------------------------------------------
    # Date/Time Properties
    # -------------------------------------------------------------------------

    @property
    def date(self) -> pd.Series:
        """Get date part (time set to midnight)."""
        self._validate()

        def get_date(x: Any) -> Any:
            if pd.isna(x):
                return pd.NaT
            if isinstance(x, jdatetime.datetime):
                return jdatetime.datetime(x.year, x.month, x.day)
            return x

        return cast(pd.Series, self._obj.apply(get_date))

    @property
    def time(self) -> pd.Series:
        """Get time part as Python time objects."""
        self._validate()

        def get_time(x: Any) -> Any:
            if pd.isna(x):
                return None
            if isinstance(x, jdatetime.datetime):
                return time(
                    hour=x.hour,
                    minute=x.minute,
                    second=x.second,
                    microsecond=x.microsecond,
                )
            return time(0, 0, 0)

        return cast(pd.Series, self._obj.apply(get_time))

    # -------------------------------------------------------------------------
    # String Methods
    # -------------------------------------------------------------------------

    def strftime(self, date_format: str) -> pd.Series:
        """Format dates as strings.

        Args:
            date_format: strftime format string.

        Returns:
            Series of formatted strings.
        """
        self._validate()

        def format_date(x: Any) -> Any:
            if pd.isna(x):
                return None
            return x.strftime(date_format)

        return cast(pd.Series, self._obj.apply(format_date))

    def month_name(self, locale: Literal["fa", "en"] = "en") -> pd.Series:
        """Get month names.

        Args:
            locale: Language for month names. 'fa' for Persian, 'en' for English.
                Defaults to 'en'.

        Returns:
            Series of month names.
        """
        self._validate()
        names = MONTH_NAMES_FA if locale == "fa" else MONTH_NAMES_EN

        def get_month_name(x: Any) -> Any:
            if pd.isna(x):
                return None
            return names[x.month - 1]

        return cast(pd.Series, self._obj.apply(get_month_name))

    def day_name(self, locale: Literal["fa", "en"] = "en") -> pd.Series:
        """Get day names.

        Args:
            locale: Language for day names. 'fa' for Persian, 'en' for English.
                Defaults to 'en'.

        Returns:
            Series of day names.
        """
        self._validate()
        names = WEEKDAY_NAMES_FA if locale == "fa" else WEEKDAY_NAMES_EN

        def get_day_name(x: Any) -> Any:
            if pd.isna(x):
                return None
            wd = weekday_of_jalali(x.year, x.month, x.day)
            return names[wd]

        return cast(pd.Series, self._obj.apply(get_day_name))

    # -------------------------------------------------------------------------
    # Normalization Methods
    # -------------------------------------------------------------------------

    def normalize(self) -> pd.Series:
        """Normalize dates to midnight.

        Returns:
            Series with time components set to zero.
        """
        self._validate()

        def normalize_date(x: Any) -> Any:
            if pd.isna(x):
                return pd.NaT
            if isinstance(x, jdatetime.datetime):
                return jdatetime.datetime(x.year, x.month, x.day)
            return x

        return cast(pd.Series, self._obj.apply(normalize_date))

    def floor(self, freq: str) -> pd.Series:
        """Floor dates to specified frequency.

        Args:
            freq: Frequency string. Supported: 'D' (day), 'h' (hour),
                'min' (minute), 's' (second).

        Returns:
            Series with floored dates.
        """
        self._validate()

        def floor_date(x: Any) -> Any:
            if pd.isna(x):
                return pd.NaT
            if not isinstance(x, jdatetime.datetime):
                return x

            if freq in ("D", "d"):
                return jdatetime.datetime(x.year, x.month, x.day)
            elif freq in ("h", "H"):
                return jdatetime.datetime(x.year, x.month, x.day, x.hour)
            elif freq in ("min", "T"):
                return jdatetime.datetime(x.year, x.month, x.day, x.hour, x.minute)
            elif freq in ("s", "S"):
                return jdatetime.datetime(
                    x.year, x.month, x.day, x.hour, x.minute, x.second
                )
            else:
                raise ValueError(f"Unsupported frequency: {freq}")

        return cast(pd.Series, self._obj.apply(floor_date))

    def ceil(self, freq: str) -> pd.Series:
        """Ceil dates to specified frequency.

        Args:
            freq: Frequency string. Supported: 'D' (day), 'h' (hour),
                'min' (minute), 's' (second).

        Returns:
            Series with ceiled dates.
        """
        self._validate()

        def ceil_date(x: Any) -> Any:
            if pd.isna(x):
                return pd.NaT
            if not isinstance(x, jdatetime.datetime):
                return x

            if freq in ("D", "d"):
                if x.hour > 0 or x.minute > 0 or x.second > 0 or x.microsecond > 0:
                    # Add one day
                    greg = x.togregorian()
                    greg = greg + pd.Timedelta(days=1)
                    new_j = jdatetime.datetime.fromgregorian(datetime=greg)
                    return jdatetime.datetime(new_j.year, new_j.month, new_j.day)
                return jdatetime.datetime(x.year, x.month, x.day)
            elif freq in ("h", "H"):
                if x.minute > 0 or x.second > 0 or x.microsecond > 0:
                    greg = x.togregorian()
                    greg = greg + pd.Timedelta(hours=1)
                    new_j = jdatetime.datetime.fromgregorian(datetime=greg)
                    return jdatetime.datetime(
                        new_j.year, new_j.month, new_j.day, new_j.hour
                    )
                return jdatetime.datetime(x.year, x.month, x.day, x.hour)
            elif freq in ("min", "T"):
                if x.second > 0 or x.microsecond > 0:
                    greg = x.togregorian()
                    greg = greg + pd.Timedelta(minutes=1)
                    new_j = jdatetime.datetime.fromgregorian(datetime=greg)
                    return jdatetime.datetime(
                        new_j.year, new_j.month, new_j.day, new_j.hour, new_j.minute
                    )
                return jdatetime.datetime(x.year, x.month, x.day, x.hour, x.minute)
            elif freq in ("s", "S"):
                if x.microsecond > 0:
                    greg = x.togregorian()
                    greg = greg + pd.Timedelta(seconds=1)
                    new_j = jdatetime.datetime.fromgregorian(datetime=greg)
                    return jdatetime.datetime(
                        new_j.year,
                        new_j.month,
                        new_j.day,
                        new_j.hour,
                        new_j.minute,
                        new_j.second,
                    )
                return jdatetime.datetime(
                    x.year, x.month, x.day, x.hour, x.minute, x.second
                )
            else:
                raise ValueError(f"Unsupported frequency: {freq}")

        return cast(pd.Series, self._obj.apply(ceil_date))

    def round(self, freq: str) -> pd.Series:
        """Round dates to specified frequency.

        Args:
            freq: Frequency string. Supported: 'D' (day), 'h' (hour),
                'min' (minute), 's' (second).

        Returns:
            Series with rounded dates.
        """
        self._validate()

        def round_date(x: Any) -> Any:
            if pd.isna(x):
                return pd.NaT
            if not isinstance(x, jdatetime.datetime):
                return x

            if freq in ("D", "d"):
                # Round to nearest day (12:00 is the midpoint)
                if x.hour >= 12:
                    greg = x.togregorian()
                    greg = greg + pd.Timedelta(days=1)
                    new_j = jdatetime.datetime.fromgregorian(datetime=greg)
                    return jdatetime.datetime(new_j.year, new_j.month, new_j.day)
                return jdatetime.datetime(x.year, x.month, x.day)
            elif freq in ("h", "H"):
                if x.minute >= 30:
                    greg = x.togregorian()
                    greg = greg + pd.Timedelta(hours=1)
                    new_j = jdatetime.datetime.fromgregorian(datetime=greg)
                    return jdatetime.datetime(
                        new_j.year, new_j.month, new_j.day, new_j.hour
                    )
                return jdatetime.datetime(x.year, x.month, x.day, x.hour)
            elif freq in ("min", "T"):
                if x.second >= 30:
                    greg = x.togregorian()
                    greg = greg + pd.Timedelta(minutes=1)
                    new_j = jdatetime.datetime.fromgregorian(datetime=greg)
                    return jdatetime.datetime(
                        new_j.year, new_j.month, new_j.day, new_j.hour, new_j.minute
                    )
                return jdatetime.datetime(x.year, x.month, x.day, x.hour, x.minute)
            elif freq in ("s", "S"):
                if x.microsecond >= 500000:
                    greg = x.togregorian()
                    greg = greg + pd.Timedelta(seconds=1)
                    new_j = jdatetime.datetime.fromgregorian(datetime=greg)
                    return jdatetime.datetime(
                        new_j.year,
                        new_j.month,
                        new_j.day,
                        new_j.hour,
                        new_j.minute,
                        new_j.second,
                    )
                return jdatetime.datetime(
                    x.year, x.month, x.day, x.hour, x.minute, x.second
                )
            else:
                raise ValueError(f"Unsupported frequency: {freq}")

        return cast(pd.Series, self._obj.apply(round_date))

    # -------------------------------------------------------------------------
    # Timezone Methods
    # -------------------------------------------------------------------------

    def tz_localize(
        self,
        tz: dt_tzinfo | str | None,
        ambiguous: str = "raise",
        nonexistent: str = "raise",
    ) -> pd.Series:
        """Localize tz-naive dates to a timezone.

        This converts the jdatetime objects to Gregorian, localizes them,
        and returns the localized Gregorian datetimes.

        Args:
            tz: Timezone to localize to.
            ambiguous: How to handle ambiguous times. Defaults to 'raise'.
            nonexistent: How to handle nonexistent times. Defaults to 'raise'.

        Returns:
            Series of timezone-aware Gregorian datetimes.
        """
        self._validate()
        gregorian = self.to_gregorian()
        dt_index = pd.DatetimeIndex(pd.to_datetime(gregorian))
        localized = dt_index.tz_localize(
            tz, ambiguous=ambiguous, nonexistent=nonexistent
        )
        return cast(
            pd.Series,
            pd.Series(localized, index=self._obj.index, name=self._obj.name),
        )

    def tz_convert(self, tz: dt_tzinfo | str | None) -> pd.Series:
        """Convert tz-aware dates to another timezone.

        This converts the jdatetime objects to Gregorian, converts timezone,
        and returns the converted Gregorian datetimes.

        Args:
            tz: Target timezone.

        Returns:
            Series of timezone-converted Gregorian datetimes.
        """
        self._validate()
        gregorian = self.to_gregorian()
        dt_index = pd.DatetimeIndex(pd.to_datetime(gregorian))
        converted = dt_index.tz_convert(tz)
        return cast(
            pd.Series,
            pd.Series(converted, index=self._obj.index, name=self._obj.name),
        )


__all__ = ["JalaliSeriesAccessor"]
