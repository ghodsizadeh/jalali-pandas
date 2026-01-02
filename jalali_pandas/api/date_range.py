"""Date range generation for Jalali calendar."""

from __future__ import annotations

from collections.abc import Hashable
from typing import TYPE_CHECKING, Literal

import pandas as pd

from jalali_pandas.core.arrays import JalaliDatetimeArray
from jalali_pandas.core.dtypes import JalaliDatetimeDtype
from jalali_pandas.core.indexes import JalaliDatetimeIndex
from jalali_pandas.core.timestamp import JalaliTimestamp

if TYPE_CHECKING:
    from datetime import tzinfo

    from jalali_pandas.offsets.base import JalaliOffset


def jalali_date_range(
    start: str | JalaliTimestamp | None = None,
    end: str | JalaliTimestamp | None = None,
    periods: int | None = None,
    freq: str | JalaliOffset | None = None,
    tz: tzinfo | str | None = None,
    normalize: bool = False,
    name: Hashable = None,
    inclusive: Literal["both", "neither", "left", "right"] = "both",
) -> JalaliDatetimeIndex:
    """Return a fixed frequency JalaliDatetimeIndex.

    Parameters:
        start: Left bound for generating dates.
        end: Right bound for generating dates.
        periods: Number of periods to generate.
        freq: Frequency string or JalaliOffset. Defaults to 'D' (daily).
        tz: Timezone name for the resulting index.
        normalize: Normalize start/end dates to midnight.
        name: Name of the resulting index.
        inclusive: Include boundaries; "both", "neither", "left", "right".

    Returns:
        JalaliDatetimeIndex with the requested frequency.

    Raises:
        ValueError: If invalid parameter combinations are provided.

    Examples:
        >>> jalali_date_range("1402-01-01", periods=5, freq="D")
        JalaliDatetimeIndex(['1402-01-01', '1402-01-02', '1402-01-03',
                            '1402-01-04', '1402-01-05'],
                           dtype='jalali_datetime64[ns]', freq='D')

        >>> jalali_date_range("1402-01-01", "1402-03-31", freq="JME")
        JalaliDatetimeIndex(['1402-01-31', '1402-02-31', '1402-03-31'],
                           dtype='jalali_datetime64[ns]', freq='JME')
    """
    # Validate parameter combinations
    _validate_params(start, end, periods, freq)

    # Parse start and end
    start_ts = _parse_timestamp(start) if start is not None else None
    end_ts = _parse_timestamp(end) if end is not None else None

    # Normalize if requested
    if normalize:
        if start_ts is not None:
            start_ts = start_ts.normalize()
        if end_ts is not None:
            end_ts = end_ts.normalize()

    # Default frequency
    if freq is None:
        freq = "D"

    # Parse frequency string to offset
    offset = _parse_frequency(freq)

    # Generate the date range
    dates = _generate_range(start_ts, end_ts, periods, offset, inclusive)

    # Create the index
    tz_str = str(tz) if tz is not None and not isinstance(tz, str) else tz
    dtype = JalaliDatetimeDtype(tz=tz_str)
    array = JalaliDatetimeArray._from_sequence(dates, dtype=dtype)

    freq_str = freq if isinstance(freq, str) else str(offset)
    return JalaliDatetimeIndex._simple_new(array, name=name, freq=freq_str)


def _validate_params(
    start: str | JalaliTimestamp | None,
    end: str | JalaliTimestamp | None,
    periods: int | None,
    freq: str | JalaliOffset | None,
) -> None:
    """Validate parameter combinations."""
    # Count how many of start, end, periods are specified
    specified = sum(x is not None for x in [start, end, periods])

    if specified < 2:
        raise ValueError(
            "Of the four parameters: start, end, periods, and freq, "
            "exactly three must be specified to generate a date range."
        )

    if specified == 3 and freq is None:
        raise ValueError(
            "freq must be specified when start, end, and periods are given"
        )

    if periods is not None and periods < 0:
        raise ValueError("periods must be a non-negative integer")


def _parse_timestamp(value: str | JalaliTimestamp) -> JalaliTimestamp:
    """Parse a value to JalaliTimestamp."""
    if isinstance(value, JalaliTimestamp):
        return value

    if isinstance(value, str):
        # Try common formats
        for fmt in ["%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%Y/%m/%d", "%Y/%m/%d %H:%M:%S"]:
            try:
                return JalaliTimestamp.strptime(value, fmt)
            except ValueError:
                continue

        raise ValueError(f"Cannot parse '{value}' as JalaliTimestamp")

    raise TypeError(f"Expected str or JalaliTimestamp, got {type(value)}")


def _parse_frequency(freq: str | JalaliOffset) -> JalaliOffset | pd.DateOffset:
    """Parse frequency string to offset object."""
    if not isinstance(freq, str):
        return freq

    # Check for Jalali-specific frequencies
    from jalali_pandas.offsets.aliases import parse_jalali_frequency

    freq_upper = freq.upper()

    # Try Jalali frequency first
    try:
        return parse_jalali_frequency(freq_upper)
    except ValueError:
        pass

    # Standard pandas frequencies
    freq_map = {
        "D": pd.DateOffset(days=1),
        "H": pd.DateOffset(hours=1),
        "MIN": pd.DateOffset(minutes=1),
        "S": pd.DateOffset(seconds=1),
        "MS": pd.DateOffset(microseconds=1),
        "W": pd.DateOffset(weeks=1),
    }

    if freq_upper in freq_map:
        return freq_map[freq_upper]

    # Try parsing with multiplier (e.g., "2D", "3H")
    import re

    match = re.match(r"^(\d+)([A-Z]+)$", freq_upper)
    if match:
        n = int(match.group(1))
        unit = match.group(2)
        if unit in freq_map:
            base = freq_map[unit]
            return pd.DateOffset(
                days=base.kwds.get("days", 0) * n,
                hours=base.kwds.get("hours", 0) * n,
                minutes=base.kwds.get("minutes", 0) * n,
                seconds=base.kwds.get("seconds", 0) * n,
                weeks=base.kwds.get("weeks", 0) * n,
            )

    raise ValueError(f"Unknown frequency: '{freq}'")


def _generate_range(
    start: JalaliTimestamp | None,
    end: JalaliTimestamp | None,
    periods: int | None,
    offset: JalaliOffset | pd.DateOffset,
    inclusive: Literal["both", "neither", "left", "right"],
) -> list[JalaliTimestamp]:
    """Generate the date range."""
    from jalali_pandas.offsets.base import JalaliOffset

    dates: list[JalaliTimestamp] = []

    if start is not None and periods is not None:
        # Generate from start with periods
        # For Jalali offsets, roll forward to first valid date
        if isinstance(offset, JalaliOffset):
            current = offset.rollforward(start)
        else:
            current = start

        for _ in range(periods):
            dates.append(current)
            if isinstance(offset, JalaliOffset):
                current = offset + current
            else:
                # pd.DateOffset
                gregorian = current.to_gregorian() + offset
                current = JalaliTimestamp.from_gregorian(gregorian)

    elif end is not None and periods is not None:
        # Generate backwards from end with periods
        # For Jalali offsets, roll back to last valid date
        current = offset.rollback(end) if isinstance(offset, JalaliOffset) else end

        for _ in range(periods):
            dates.insert(0, current)
            if isinstance(offset, JalaliOffset):
                # Go back one period - use negative offset
                neg_offset = type(offset)(n=-offset.n)
                prev = neg_offset + current
                current = offset.rollback(prev)
            else:
                gregorian = current.to_gregorian() - offset
                current = JalaliTimestamp.from_gregorian(gregorian)

    elif start is not None and end is not None:
        # Generate from start to end
        # For Jalali offsets, roll forward to first valid date
        if isinstance(offset, JalaliOffset):
            current = offset.rollforward(start)
        else:
            current = start

        while current <= end:
            dates.append(current)
            if isinstance(offset, JalaliOffset):
                next_date = offset + current
            else:
                gregorian = current.to_gregorian() + offset
                next_date = JalaliTimestamp.from_gregorian(gregorian)

            # Prevent infinite loop
            if next_date <= current:
                break
            current = next_date

    # Apply inclusive parameter
    if dates:
        if inclusive == "neither":
            dates = dates[1:-1] if len(dates) > 2 else []
        elif inclusive == "left":
            dates = dates[:-1] if len(dates) > 1 else dates
        elif inclusive == "right":
            dates = dates[1:] if len(dates) > 1 else dates
        # "both" keeps all dates

    return dates


__all__ = ["jalali_date_range"]
