"""JalaliGrouper - Grouper for Jalali calendar-based grouping.

This module provides a Grouper class that enables grouping pandas DataFrames
by Jalali calendar periods (month, quarter, year).
"""

from __future__ import annotations

import contextlib
from typing import TYPE_CHECKING, Any, Literal

import pandas as pd

from jalali_pandas.core.timestamp import JalaliTimestamp
from jalali_pandas.offsets.aliases import parse_jalali_frequency

if TYPE_CHECKING:
    from jalali_pandas.offsets.base import JalaliOffset


class JalaliGrouper:
    """Grouper for Jalali calendar-based grouping.

    This class provides grouping by Jalali calendar periods such as
    month end (JME), quarter end (JQE), year end (JYE), etc.

    Parameters:
        key: Column name containing datetime values to group by.
        freq: Jalali frequency string (e.g., 'JME', 'JQE', 'JYE') or JalaliOffset.
        closed: Which side of bin interval is closed ('left' or 'right').
        label: Which bin edge label to use ('left' or 'right').
        sort: Whether to sort the resulting groups.

    Examples:
        >>> df = pd.DataFrame({
        ...     'date': pd.date_range('2023-03-21', periods=90, freq='D'),
        ...     'value': range(90)
        ... })
        >>> grouper = JalaliGrouper(key='date', freq='JME')
        >>> df.groupby(grouper.get_grouper(df)).sum()
    """

    def __init__(
        self,
        key: str | None = None,
        freq: str | JalaliOffset | None = None,
        closed: str | None = None,
        label: str | None = None,
        sort: bool = True,
    ) -> None:
        """Initialize JalaliGrouper.

        Args:
            key: Column name containing datetime values.
            freq: Jalali frequency string or offset.
            closed: Which side of bin interval is closed.
            label: Which bin edge label to use.
            sort: Whether to sort results.
        """
        self._jalali_freq = freq
        self._jalali_offset: JalaliOffset | None = None
        self._closed = closed
        self._label = label
        self._sort = sort

        # Parse frequency if string
        if isinstance(freq, str):
            with contextlib.suppress(ValueError):
                self._jalali_offset = parse_jalali_frequency(freq)

        # Store key and sort for our use
        self._key = key
        self._sort_groups = sort

    @property
    def key(self) -> str | None:
        """Return the key column name."""
        return self._key

    def get_grouper(self, obj: pd.DataFrame | pd.Series[Any]) -> pd.Series[Any]:
        """Get the grouper Series for groupby operations.

        Args:
            obj: DataFrame or Series to group.

        Returns:
            Series of group labels.
        """
        # Get the datetime column
        if self._key is not None:
            datetime_col = obj[self._key]
        elif isinstance(obj.index, pd.DatetimeIndex):
            datetime_col = obj.index.to_series()
        else:
            raise ValueError(
                "JalaliGrouper requires either a 'key' parameter or a DatetimeIndex"
            )

        # Convert to Jalali and compute group labels
        return self._compute_jalali_groups(datetime_col)

    def _compute_jalali_groups(self, datetime_col: pd.Series[Any]) -> pd.Series[Any]:
        """Compute Jalali-based group labels for datetime values.

        Args:
            datetime_col: Series of datetime values.

        Returns:
            Series of group labels (Jalali period boundaries).
        """
        labels: list[Any] = []

        for dt in datetime_col:
            if pd.isna(dt):
                labels.append(pd.NaT)
                continue

            # Convert to JalaliTimestamp
            if isinstance(dt, pd.Timestamp):
                jts = JalaliTimestamp.from_gregorian(dt)
            elif isinstance(dt, JalaliTimestamp):
                jts = dt
            else:
                # Try to convert
                jts = JalaliTimestamp.from_gregorian(pd.Timestamp(dt))

            # Get the period boundary using rollforward
            if self._jalali_offset is not None:
                boundary = self._jalali_offset.rollforward(jts)
                # Convert back to Gregorian for grouping
                labels.append(boundary.to_gregorian())
            else:
                labels.append(jts.to_gregorian())

        return pd.Series(labels, index=datetime_col.index)


def jalali_groupby(
    df: pd.DataFrame,
    key: str,
    freq: str | JalaliOffset,
    **kwargs: Any,
) -> pd.core.groupby.DataFrameGroupBy:  # type: ignore[type-arg]
    """Group a DataFrame by Jalali calendar periods.

    This is a convenience function that creates a JalaliGrouper and applies
    it to the DataFrame.

    Args:
        df: DataFrame to group.
        key: Column name containing datetime values.
        freq: Jalali frequency string (e.g., 'JME', 'JQE', 'JYE').
        **kwargs: Additional arguments passed to JalaliGrouper.

    Returns:
        DataFrameGroupBy object.

    Examples:
        >>> df = pd.DataFrame({
        ...     'date': pd.date_range('2023-03-21', periods=90, freq='D'),
        ...     'value': range(90)
        ... })
        >>> jalali_groupby(df, 'date', 'JME').sum()
    """
    grouper = JalaliGrouper(key=key, freq=freq, **kwargs)
    return df.groupby(grouper)


class JalaliResampler:
    """Resampler for Jalali calendar-based resampling.

    This class provides a resampler interface similar to pandas Resampler
    but uses Jalali calendar boundaries for grouping.

    Parameters:
        obj: Series or DataFrame to resample.
        offset: JalaliOffset for determining period boundaries.
        closed: Which side of bin interval is closed.
        label: Which bin edge label to use.
    """

    def __init__(
        self,
        obj: pd.Series[Any] | pd.DataFrame,
        offset: JalaliOffset,
        closed: Literal["right", "left"] | None = None,
        label: Literal["right", "left"] | None = None,
    ) -> None:
        """Initialize JalaliResampler."""
        self._obj = obj
        self._offset = offset
        self._closed = closed or "right"
        self._label = label or "right"
        self._groups = self._compute_groups()

    def _compute_groups(self) -> pd.Series[Any]:
        """Compute group labels based on Jalali period boundaries."""
        if isinstance(self._obj.index, pd.DatetimeIndex):
            index = self._obj.index
        else:
            raise ValueError("Resampling requires a DatetimeIndex")

        labels: list[Any] = []
        for ts in index:
            if pd.isna(ts):
                labels.append(pd.NaT)
                continue

            # Convert to JalaliTimestamp
            jts = JalaliTimestamp.from_gregorian(ts)

            # Get the period boundary using rollforward
            boundary = self._offset.rollforward(jts)

            # Convert back to Gregorian for the label
            labels.append(boundary.to_gregorian())

        return pd.Series(labels, index=index)

    def _apply_agg(self, func: str) -> Any:
        """Apply aggregation function to groups."""
        return getattr(self._obj.groupby(self._groups), func)()

    def sum(self, **kwargs: Any) -> pd.Series[Any] | pd.DataFrame:
        """Compute sum of groups."""
        return self._obj.groupby(self._groups).sum(**kwargs)

    def mean(self, **kwargs: Any) -> pd.Series[Any] | pd.DataFrame:
        """Compute mean of groups."""
        return self._obj.groupby(self._groups).mean(**kwargs)

    def min(self, **kwargs: Any) -> pd.Series[Any] | pd.DataFrame:
        """Compute min of groups."""
        return self._obj.groupby(self._groups).min(**kwargs)

    def max(self, **kwargs: Any) -> pd.Series[Any] | pd.DataFrame:
        """Compute max of groups."""
        return self._obj.groupby(self._groups).max(**kwargs)

    def count(self) -> pd.Series[Any] | pd.DataFrame:
        """Compute count of groups."""
        return self._obj.groupby(self._groups).count()

    def first(self, **kwargs: Any) -> pd.Series[Any] | pd.DataFrame:
        """Compute first value of groups."""
        return self._obj.groupby(self._groups).first(**kwargs)

    def last(self, **kwargs: Any) -> pd.Series[Any] | pd.DataFrame:
        """Compute last value of groups."""
        return self._obj.groupby(self._groups).last(**kwargs)

    def std(self, **kwargs: Any) -> pd.Series[Any] | pd.DataFrame:
        """Compute standard deviation of groups."""
        return self._obj.groupby(self._groups).std(**kwargs)

    def var(self, **kwargs: Any) -> pd.Series[Any] | pd.DataFrame:
        """Compute variance of groups."""
        return self._obj.groupby(self._groups).var(**kwargs)

    def median(self, **kwargs: Any) -> pd.Series[Any] | pd.DataFrame:
        """Compute median of groups."""
        return self._obj.groupby(self._groups).median(**kwargs)

    def agg(self, func: Any, *args: Any, **kwargs: Any) -> Any:
        """Aggregate using one or more operations."""
        return self._obj.groupby(self._groups).agg(func, *args, **kwargs)

    def apply(self, func: Any, *args: Any, **kwargs: Any) -> Any:
        """Apply function to groups."""
        return self._obj.groupby(self._groups).apply(func, *args, **kwargs)


def resample_jalali(
    series_or_df: pd.Series[Any] | pd.DataFrame,
    freq: str | JalaliOffset,
    closed: Literal["right", "left"] | None = None,
    label: Literal["right", "left"] | None = None,
) -> JalaliResampler:
    """Resample a Series or DataFrame using Jalali calendar boundaries.

    This function provides resampling functionality using Jalali calendar
    period boundaries instead of Gregorian.

    Args:
        series_or_df: Series or DataFrame with DatetimeIndex.
        freq: Jalali frequency string or offset.
        closed: Which side of bin interval is closed.
        label: Which bin edge label to use.

    Returns:
        JalaliResampler object with aggregation methods.

    Examples:
        >>> idx = pd.date_range('2023-03-21', periods=90, freq='D')
        >>> s = pd.Series(range(90), index=idx)
        >>> resample_jalali(s, 'JME').sum()
    """
    # Parse frequency
    offset = parse_jalali_frequency(freq) if isinstance(freq, str) else freq

    return JalaliResampler(series_or_df, offset, closed=closed, label=label)


__all__ = ["JalaliGrouper", "jalali_groupby", "resample_jalali"]
