"""Conversion functions for Jalali datetime."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

import pandas as pd

from jalali_pandas.core.arrays import JalaliDatetimeArray
from jalali_pandas.core.dtypes import JalaliDatetimeDtype
from jalali_pandas.core.indexes import JalaliDatetimeIndex
from jalali_pandas.core.timestamp import JalaliTimestamp

if TYPE_CHECKING:
    from collections.abc import Sequence
    from datetime import datetime

# Type aliases
ErrorsType = Literal["raise", "coerce", "ignore"]


def to_jalali_datetime(
    arg: str
    | JalaliTimestamp
    | datetime
    | pd.Timestamp
    | Sequence[str]
    | pd.DatetimeIndex
    | pd.Series,
    format: str | None = None,
    errors: ErrorsType = "raise",
) -> JalaliTimestamp | JalaliDatetimeIndex | pd.Series:
    """Convert argument to Jalali datetime.

    This function converts various datetime-like inputs to Jalali datetime
    objects. It can handle strings, pandas Timestamps, DatetimeIndex, and Series.

    Parameters:
        arg: The object to convert. Can be:
            - str: A date string to parse
            - JalaliTimestamp: Returned as-is
            - datetime/pd.Timestamp: Converted from Gregorian
            - Sequence[str]: List of date strings
            - pd.DatetimeIndex: Converted from Gregorian
            - pd.Series: Each element converted
        format: strftime format string for parsing strings.
            If None, tries common formats.
        errors: How to handle errors:
            - "raise": Raise an exception on invalid input
            - "coerce": Set invalid values to NaT
            - "ignore": Return the input unchanged on error

    Returns:
        - JalaliTimestamp for scalar inputs
        - JalaliDatetimeIndex for array-like inputs
        - pd.Series for Series inputs

    Raises:
        ValueError: If parsing fails and errors="raise".
        TypeError: If input type is not supported.

    Examples:
        >>> to_jalali_datetime("1402-06-15")
        JalaliTimestamp('1402-06-15T00:00:00')

        >>> to_jalali_datetime(pd.Timestamp("2023-09-06"))
        JalaliTimestamp('1402-06-15T00:00:00')

        >>> to_jalali_datetime(["1402-01-01", "1402-01-02"])
        JalaliDatetimeIndex(['1402-01-01', '1402-01-02'],
                           dtype='jalali_datetime64[ns]', freq=None)
    """
    # Handle scalar string
    if isinstance(arg, str):
        return _parse_string_scalar(arg, format, errors)

    # Handle JalaliTimestamp (return as-is)
    if isinstance(arg, JalaliTimestamp):
        return arg

    # Handle pandas Timestamp
    if isinstance(arg, pd.Timestamp):
        return JalaliTimestamp.from_gregorian(arg)

    # Handle datetime
    from datetime import datetime

    if isinstance(arg, datetime) and not isinstance(arg, pd.Timestamp):
        return JalaliTimestamp.from_gregorian(pd.Timestamp(arg))

    # Handle Series
    if isinstance(arg, pd.Series):
        return _convert_series(arg, format, errors)

    # Handle DatetimeIndex
    if isinstance(arg, pd.DatetimeIndex):
        return _convert_datetime_index(arg, errors)

    # Handle sequence (list, tuple, etc.)
    try:
        # Try to iterate
        items = list(arg)  # type: ignore[arg-type]
        return _convert_sequence(items, format, errors)
    except TypeError:
        pass

    raise TypeError(f"Cannot convert {type(arg)} to Jalali datetime")


def _parse_string_scalar(
    value: str,
    format: str | None,
    errors: ErrorsType,
) -> JalaliTimestamp:
    """Parse a single string to JalaliTimestamp."""
    try:
        if format is not None:
            return JalaliTimestamp.strptime(value, format)

        # Try common formats (more specific first)
        for fmt in [
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d",
            "%Y/%m/%d %H:%M:%S",
            "%Y/%m/%d",
            "%Y%m%d",
        ]:
            try:
                return JalaliTimestamp.strptime(value, fmt)
            except ValueError:
                continue

        raise ValueError(f"Cannot parse '{value}' as Jalali datetime")

    except ValueError as e:
        if errors == "raise":
            raise
        if errors == "coerce":
            return pd.NaT  # type: ignore[return-value]
        # errors == "ignore"
        raise TypeError(
            f"Cannot return original value for scalar with errors='ignore': {e}"
        ) from e


def _convert_series(
    series: pd.Series,
    format: str | None,
    errors: ErrorsType,
) -> pd.Series:
    """Convert a pandas Series to Jalali datetime Series."""
    results: list[Any] = []

    for val in series:
        try:
            if pd.isna(val):
                results.append(pd.NaT)
            elif isinstance(val, JalaliTimestamp):
                results.append(val)
            elif isinstance(val, str):
                results.append(_parse_string_scalar(val, format, "raise"))
            elif isinstance(val, pd.Timestamp):
                results.append(JalaliTimestamp.from_gregorian(val))
            else:
                # Try to convert via pandas Timestamp
                ts = pd.Timestamp(val)
                results.append(JalaliTimestamp.from_gregorian(ts))
        except (ValueError, TypeError):
            if errors == "raise":
                raise
            if errors == "coerce":
                results.append(pd.NaT)
            else:
                # errors == "ignore" - return original series
                return series

    dtype = JalaliDatetimeDtype()
    array = JalaliDatetimeArray._from_sequence(results, dtype=dtype)
    return pd.Series(array, index=series.index, name=series.name)


def _convert_datetime_index(
    index: pd.DatetimeIndex,
    errors: ErrorsType,
) -> JalaliDatetimeIndex:
    """Convert a pandas DatetimeIndex to JalaliDatetimeIndex."""
    results: list[Any] = []

    for ts in index:
        try:
            if pd.isna(ts):
                results.append(pd.NaT)
            else:
                results.append(JalaliTimestamp.from_gregorian(ts))
        except (ValueError, TypeError):
            if errors == "raise":
                raise
            if errors == "coerce":
                results.append(pd.NaT)
            else:
                raise ValueError(
                    "Cannot use errors='ignore' with DatetimeIndex"
                ) from None

    dtype = JalaliDatetimeDtype()
    array = JalaliDatetimeArray._from_sequence(results, dtype=dtype)
    return JalaliDatetimeIndex._simple_new(array, name=index.name)


def _convert_sequence(
    items: list[Any],
    format: str | None,
    errors: ErrorsType,
) -> JalaliDatetimeIndex:
    """Convert a sequence to JalaliDatetimeIndex."""
    results: list[Any] = []

    for item in items:
        try:
            if pd.isna(item):
                results.append(pd.NaT)
            elif isinstance(item, JalaliTimestamp):
                results.append(item)
            elif isinstance(item, str):
                results.append(_parse_string_scalar(item, format, "raise"))
            elif isinstance(item, pd.Timestamp):
                results.append(JalaliTimestamp.from_gregorian(item))
            else:
                # Try to convert via pandas Timestamp
                ts = pd.Timestamp(item)
                results.append(JalaliTimestamp.from_gregorian(ts))
        except (ValueError, TypeError):
            if errors == "raise":
                raise
            if errors == "coerce":
                results.append(pd.NaT)
            else:
                raise ValueError("Cannot use errors='ignore' with sequence") from None

    dtype = JalaliDatetimeDtype()
    array = JalaliDatetimeArray._from_sequence(results, dtype=dtype)
    return JalaliDatetimeIndex._simple_new(array)


def to_gregorian_datetime(
    arg: JalaliTimestamp | JalaliDatetimeIndex | pd.Series,
) -> pd.Timestamp | pd.DatetimeIndex | pd.Series:
    """Convert Jalali datetime to Gregorian datetime.

    Parameters:
        arg: The Jalali datetime object to convert. Can be:
            - JalaliTimestamp: Returns pd.Timestamp
            - JalaliDatetimeIndex: Returns pd.DatetimeIndex
            - pd.Series with Jalali data: Returns pd.Series with Gregorian data

    Returns:
        - pd.Timestamp for JalaliTimestamp input
        - pd.DatetimeIndex for JalaliDatetimeIndex input
        - pd.Series for Series input

    Raises:
        TypeError: If input type is not supported.

    Examples:
        >>> ts = JalaliTimestamp(1402, 6, 15)
        >>> to_gregorian_datetime(ts)
        Timestamp('2023-09-06 00:00:00')

        >>> idx = JalaliDatetimeIndex(["1402-01-01", "1402-01-02"])
        >>> to_gregorian_datetime(idx)
        DatetimeIndex(['2023-03-21', '2023-03-22'], dtype='datetime64[ns]', freq=None)
    """
    if isinstance(arg, JalaliTimestamp):
        return arg.to_gregorian()

    if isinstance(arg, JalaliDatetimeIndex):
        return arg.to_gregorian()

    if isinstance(arg, pd.Series):
        # Check if it's a Jalali series
        if hasattr(arg.dtype, "name") and "jalali" in str(arg.dtype.name).lower():
            greg_vals: list[Any] = []
            for val in arg:
                if pd.isna(val):
                    greg_vals.append(pd.NaT)
                elif isinstance(val, JalaliTimestamp):
                    greg_vals.append(val.to_gregorian())
                else:
                    greg_vals.append(pd.NaT)
            return pd.Series(greg_vals, index=arg.index, name=arg.name)

        # Try to convert each element
        greg_results: list[Any] = []
        for val in arg:
            if pd.isna(val):
                greg_results.append(pd.NaT)
            elif isinstance(val, JalaliTimestamp):
                greg_results.append(val.to_gregorian())
            else:
                raise TypeError(f"Cannot convert {type(val)} to Gregorian datetime")
        return pd.Series(greg_results, index=arg.index, name=arg.name)

    raise TypeError(f"Cannot convert {type(arg)} to Gregorian datetime")


__all__ = ["to_jalali_datetime", "to_gregorian_datetime"]
