"""JalaliDatetimeIndex - Index for Jalali datetime data."""

from __future__ import annotations

import re
from collections.abc import Hashable, Sequence
from typing import TYPE_CHECKING, Any, cast

import numpy as np
import numpy.typing as npt
import pandas as pd
from pandas import Index

from jalali_pandas.core.arrays import JalaliDatetimeArray
from jalali_pandas.core.dtypes import JalaliDatetimeDtype
from jalali_pandas.core.timestamp import JalaliTimestamp

if TYPE_CHECKING:
    from datetime import tzinfo

    from jalali_pandas.offsets.base import JalaliOffset


class JalaliDatetimeIndex(Index):
    """Index for Jalali datetime data.

    A JalaliDatetimeIndex is an immutable array of Jalali timestamps,
    suitable for use as an index in pandas DataFrames and Series.

    Examples:
        >>> idx = JalaliDatetimeIndex(["1402-01-01", "1402-01-02", "1402-01-03"])
        >>> idx
        JalaliDatetimeIndex(['1402-01-01', '1402-01-02', '1402-01-03'],
                           dtype='jalali_datetime64[ns]', freq=None)

        >>> idx.year
        Index([1402, 1402, 1402], dtype='float64')
    """

    _typ = "jalalidatetimeindex"
    _data: JalaliDatetimeArray
    _freq: JalaliOffset | str | None
    _name: Hashable
    _cache: dict[str, Any]

    # -------------------------------------------------------------------------
    # Construction
    # -------------------------------------------------------------------------

    def __new__(
        cls,
        data: Sequence[Any] | JalaliDatetimeArray | JalaliDatetimeIndex | None = None,
        freq: str | JalaliOffset | None = None,
        tz: tzinfo | str | None = None,
        dtype: JalaliDatetimeDtype | None = None,
        copy: bool = False,
        name: Hashable = None,
    ) -> JalaliDatetimeIndex:
        """Create a new JalaliDatetimeIndex."""
        if dtype is None:
            # Convert tzinfo to string if needed
            tz_str = str(tz) if tz is not None and not isinstance(tz, str) else tz
            dtype = JalaliDatetimeDtype(tz=tz_str)

        if data is None:
            data = []

        if isinstance(data, JalaliDatetimeIndex):
            data = data._data.copy() if copy else data._data
        elif isinstance(data, JalaliDatetimeArray):
            if copy:
                data = data.copy()
        else:
            data = JalaliDatetimeArray._from_sequence(
                list(data), dtype=dtype, copy=copy
            )

        # Create the index
        result = object.__new__(cls)
        result._data = data
        result._name = name
        result._freq = freq
        result._cache = {}

        return result

    @classmethod
    def _simple_new(
        cls,
        values: JalaliDatetimeArray,
        name: Hashable = None,
        freq: str | JalaliOffset | None = None,
        refs: Any = None,  # noqa: ARG003 - pandas compatibility
    ) -> JalaliDatetimeIndex:
        """Create a new JalaliDatetimeIndex from values without validation."""
        result = object.__new__(cls)
        result._data = values
        result._name = name
        result._freq = freq
        result._cache = {}
        return result

    # -------------------------------------------------------------------------
    # Index Properties
    # -------------------------------------------------------------------------

    @property
    def dtype(self) -> JalaliDatetimeDtype:
        """Return the dtype of the index."""
        return self._data.dtype

    @property
    def freq(self) -> JalaliOffset | str | None:
        """Return the frequency of the index."""
        return self._freq

    @freq.setter
    def freq(self, value: JalaliOffset | str | None) -> None:
        """Set the frequency of the index."""
        self._freq = value

    @property
    def freqstr(self) -> str | None:
        """Return the frequency as a string."""
        if self._freq is None:
            return None
        if isinstance(self._freq, str):
            return self._freq
        return str(self._freq)

    @property
    def inferred_freq(self) -> str | None:
        """Try to infer the frequency from the data."""
        if len(self) < 3:
            return None

        # Get differences between consecutive timestamps
        diffs = []
        for i in range(1, min(len(self), 10)):
            diff = self[i].to_gregorian() - self[i - 1].to_gregorian()
            diffs.append(diff)

        # Check if all differences are the same
        if len(set(diffs)) == 1:
            diff = diffs[0]
            if diff == pd.Timedelta(days=1):
                return "D"
            elif diff == pd.Timedelta(hours=1):
                return "h"
            elif diff == pd.Timedelta(minutes=1):
                return "min"
            elif diff == pd.Timedelta(seconds=1):
                return "s"

        return None

    def __len__(self) -> int:
        """Return the length of the index."""
        return len(self._data)

    def __getitem__(self, key: Any) -> Any:
        """Get item(s) from the index."""
        result = self._data[key]

        if isinstance(result, JalaliDatetimeArray):
            return type(self)._simple_new(result, name=self._name, freq=None)

        return result

    def __iter__(self) -> Any:
        """Iterate over the index."""
        return iter(self._data)

    def __contains__(self, key: Any) -> bool:
        """Check if key is in the index."""
        try:
            self.get_loc(key)
            return True
        except KeyError:
            return False

    def __repr__(self) -> str:
        """String representation."""
        data_repr = ", ".join(f"'{x.strftime('%Y-%m-%d')}'" for x in self._data[:5])
        if len(self._data) > 5:
            data_repr += ", ..."
        freq_str = f", freq='{self.freqstr}'" if self.freqstr else ", freq=None"
        return (
            f"JalaliDatetimeIndex([{data_repr}], dtype='{self.dtype.name}'{freq_str})"
        )

    # -------------------------------------------------------------------------
    # Jalali Properties (vectorized)
    # -------------------------------------------------------------------------

    @property
    def year(self) -> Any:
        """Return array of years."""
        return pd.Index(self._data.year, name=self._name)

    @property
    def month(self) -> Any:
        """Return array of months."""
        return pd.Index(self._data.month, name=self._name)

    @property
    def day(self) -> Any:
        """Return array of days."""
        return pd.Index(self._data.day, name=self._name)

    @property
    def hour(self) -> Any:
        """Return array of hours."""
        return pd.Index(self._data.hour, name=self._name)

    @property
    def minute(self) -> Any:
        """Return array of minutes."""
        return pd.Index(self._data.minute, name=self._name)

    @property
    def second(self) -> Any:
        """Return array of seconds."""
        return pd.Index(self._data.second, name=self._name)

    @property
    def quarter(self) -> Any:
        """Return array of quarters."""
        return pd.Index(self._data.quarter, name=self._name)

    @property
    def dayofweek(self) -> Any:
        """Return array of day of week values."""
        return pd.Index(self._data.dayofweek, name=self._name)

    @property
    def weekday(self) -> Any:
        """Alias for dayofweek."""
        return self.dayofweek

    @property
    def dayofyear(self) -> Any:
        """Return array of day of year values."""
        return pd.Index(self._data.dayofyear, name=self._name)

    @property
    def week(self) -> Any:
        """Return array of week numbers."""
        return pd.Index(self._data.week, name=self._name)

    @property
    def weekofyear(self) -> Any:
        """Alias for week."""
        return self.week

    # -------------------------------------------------------------------------
    # Conversion Methods
    # -------------------------------------------------------------------------

    def to_gregorian(self) -> pd.DatetimeIndex:
        """Convert to pandas DatetimeIndex (Gregorian).

        Returns:
            DatetimeIndex with Gregorian timestamps.
        """
        return self._data.to_gregorian()

    def strftime(self, fmt: str) -> Any:
        """Format timestamps as strings.

        Args:
            fmt: Format string.

        Returns:
            Index of formatted strings.
        """
        return pd.Index(self._data.strftime(fmt), name=self._name)

    # -------------------------------------------------------------------------
    # Indexing Methods
    # -------------------------------------------------------------------------

    def get_loc(self, key: Any) -> int | slice | npt.NDArray[np.bool_]:
        """Get integer location for requested label.

        Supports:
        - JalaliTimestamp: exact match
        - String: "1402-06-15" for exact date
        - Partial string: "1402-06" for month, "1402" for year

        Args:
            key: Label to look up.

        Returns:
            Integer location, slice, or boolean mask.

        Raises:
            KeyError: If key is not found.
        """
        if isinstance(key, JalaliTimestamp):
            # Exact match
            for i, val in enumerate(self._data):
                if val == key:
                    return i
            raise KeyError(key)

        if isinstance(key, str):
            return self._get_string_loc(key)

        raise KeyError(key)

    def _get_string_loc(self, key: str) -> int | slice | npt.NDArray[np.bool_]:
        """Get location for string key with partial string indexing support."""
        # Try exact date match first
        try:
            ts = JalaliTimestamp.strptime(key, "%Y-%m-%d")
            for i, val in enumerate(self._data):
                if not pd.isna(val) and val == ts:
                    return i
        except ValueError:
            pass

        # Try partial string indexing
        # Year only: "1402"
        year_match = re.match(r"^(\d{4})$", key)
        if year_match:
            year = int(year_match.group(1))
            mask = cast(
                npt.NDArray[np.bool_],
                np.array(
                    [not pd.isna(x) and x.year == year for x in self._data],
                    dtype=bool,
                ),
            )
            if mask.any():
                return mask
            raise KeyError(key)

        # Year-month: "1402-06"
        ym_match = re.match(r"^(\d{4})-(\d{1,2})$", key)
        if ym_match:
            year = int(ym_match.group(1))
            month = int(ym_match.group(2))
            mask = cast(
                npt.NDArray[np.bool_],
                np.array(
                    [
                        not pd.isna(x) and x.year == year and x.month == month
                        for x in self._data
                    ],
                    dtype=bool,
                ),
            )
            if mask.any():
                return mask
            raise KeyError(key)

        raise KeyError(key)

    def slice_locs(
        self,
        start: str | JalaliTimestamp | None = None,
        end: str | JalaliTimestamp | None = None,
        step: int | None = None,  # noqa: ARG002
    ) -> tuple[int, int]:
        """Compute slice locations for input labels.

        Args:
            start: Start label.
            end: End label.
            step: Step size.

        Returns:
            Tuple of (start, end) integer locations.
        """
        start_loc = 0
        end_loc = len(self)

        if start is not None:
            start_ts = self._parse_to_timestamp(start)
            for i, val in enumerate(self._data):
                if not pd.isna(val) and val >= start_ts:
                    start_loc = i
                    break

        if end is not None:
            end_ts = self._parse_to_timestamp(end)
            for i in range(len(self._data) - 1, -1, -1):
                val = self._data[i]
                if not pd.isna(val) and val <= end_ts:
                    end_loc = i + 1
                    break

        return start_loc, end_loc

    def _parse_to_timestamp(self, key: str | JalaliTimestamp) -> JalaliTimestamp:
        """Parse a key to JalaliTimestamp."""
        if isinstance(key, JalaliTimestamp):
            return key
        if isinstance(key, str):
            try:
                return JalaliTimestamp.strptime(key, "%Y-%m-%d")
            except ValueError:
                try:
                    return JalaliTimestamp.strptime(key, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    pass
            # Try partial string - use start of period
            year_match = re.match(r"^(\d{4})$", key)
            if year_match:
                return JalaliTimestamp(int(year_match.group(1)), 1, 1)
            ym_match = re.match(r"^(\d{4})-(\d{1,2})$", key)
            if ym_match:
                return JalaliTimestamp(
                    int(ym_match.group(1)), int(ym_match.group(2)), 1
                )
        raise ValueError(f"Cannot parse '{key}' to JalaliTimestamp")

    # -------------------------------------------------------------------------
    # Shift and Snap Methods
    # -------------------------------------------------------------------------

    def shift(
        self,
        periods: int = 1,
        freq: str | JalaliOffset | pd.Timedelta | None = None,
    ) -> JalaliDatetimeIndex:
        """Shift index by desired number of time frequency increments.

        Args:
            periods: Number of periods to shift.
            freq: Frequency to shift by. If None, uses the index's freq.

        Returns:
            Shifted JalaliDatetimeIndex.
        """
        if freq is None:
            freq = self._freq

        if freq is None:
            raise ValueError("freq must be specified if index has no frequency")

        # Parse string frequency
        if isinstance(freq, str):
            # Check if it's a Jalali frequency
            from jalali_pandas.offsets.aliases import get_jalali_offset

            offset_class = get_jalali_offset(freq.upper())
            if offset_class is not None:
                freq = offset_class(n=periods)
                periods = 1
            else:
                # Use pandas Timedelta for standard frequencies
                freq = pd.Timedelta(freq)

        # Apply the shift
        new_data: list[Any] = []
        for val in self._data:
            if pd.isna(val):
                new_data.append(pd.NaT)
            else:
                if isinstance(freq, pd.Timedelta):
                    new_val = val + freq * periods
                else:
                    # JalaliOffset
                    new_val = val
                    for _ in range(abs(periods)):
                        new_val = freq + new_val if periods > 0 else new_val - freq
                new_data.append(new_val)

        new_array = JalaliDatetimeArray._from_sequence(new_data, dtype=self.dtype)
        return type(self)._simple_new(new_array, name=self._name, freq=self._freq)

    def snap(self, freq: str = "s") -> JalaliDatetimeIndex:
        """Snap time stamps to nearest occurring frequency.

        Args:
            freq: Frequency to snap to (e.g., 's' for second, 'min' for minute).

        Returns:
            Snapped JalaliDatetimeIndex.
        """
        # Convert to Gregorian, snap, convert back
        gregorian = self.to_gregorian()
        snapped = gregorian.snap(freq)

        new_data = [
            JalaliTimestamp.from_gregorian(ts) if not pd.isna(ts) else pd.NaT
            for ts in snapped
        ]
        new_array = JalaliDatetimeArray._from_sequence(new_data, dtype=self.dtype)
        return type(self)._simple_new(new_array, name=self._name, freq=self._freq)

    # -------------------------------------------------------------------------
    # Set Operations
    # -------------------------------------------------------------------------

    def union(  # type: ignore[override]
        self, other: JalaliDatetimeIndex, sort: bool | None = None
    ) -> JalaliDatetimeIndex:
        """Form the union of two JalaliDatetimeIndex objects.

        Args:
            other: Another JalaliDatetimeIndex.
            sort: Whether to sort the result.

        Returns:
            Union of the two indexes.
        """
        if not isinstance(other, JalaliDatetimeIndex):
            raise TypeError("other must be a JalaliDatetimeIndex")

        # Combine and deduplicate
        combined = list(self._data) + list(other._data)
        seen: set[JalaliTimestamp] = set()
        unique: list[Any] = []
        for val in combined:
            if pd.isna(val):
                if pd.NaT not in seen:
                    unique.append(pd.NaT)
                    seen.add(pd.NaT)  # type: ignore
            elif val not in seen:
                unique.append(val)
                seen.add(val)

        if sort is True or (sort is None and len(unique) > 0):
            # Sort by Gregorian equivalent
            unique = sorted(
                unique,
                key=lambda x: x.to_gregorian() if not pd.isna(x) else pd.Timestamp.min,
            )

        new_array = JalaliDatetimeArray._from_sequence(unique, dtype=self.dtype)
        return type(self)._simple_new(new_array, name=self._name)

    def intersection(  # type: ignore[override]
        self, other: JalaliDatetimeIndex, sort: bool = False
    ) -> JalaliDatetimeIndex:
        """Form the intersection of two JalaliDatetimeIndex objects.

        Args:
            other: Another JalaliDatetimeIndex.
            sort: Whether to sort the result.

        Returns:
            Intersection of the two indexes.
        """
        if not isinstance(other, JalaliDatetimeIndex):
            raise TypeError("other must be a JalaliDatetimeIndex")

        other_set = set(other._data)
        common: list[Any] = []
        for val in self._data:
            if pd.isna(val):
                if any(pd.isna(x) for x in other._data):
                    common.append(pd.NaT)
            elif val in other_set:
                common.append(val)

        if sort:
            common = sorted(
                common,
                key=lambda x: x.to_gregorian() if not pd.isna(x) else pd.Timestamp.min,
            )

        new_array = JalaliDatetimeArray._from_sequence(common, dtype=self.dtype)
        return type(self)._simple_new(new_array, name=self._name)

    def difference(  # type: ignore[override]
        self, other: JalaliDatetimeIndex, sort: bool | None = True
    ) -> JalaliDatetimeIndex:
        """Return a new JalaliDatetimeIndex with elements not in other.

        Args:
            other: Another JalaliDatetimeIndex.
            sort: Whether to sort the result.

        Returns:
            Difference of the two indexes.
        """
        if not isinstance(other, JalaliDatetimeIndex):
            raise TypeError("other must be a JalaliDatetimeIndex")

        other_set = set(other._data)
        diff: list[Any] = []
        for val in self._data:
            if pd.isna(val):
                if not any(pd.isna(x) for x in other._data):
                    diff.append(pd.NaT)
            elif val not in other_set:
                diff.append(val)

        if sort:
            diff = sorted(
                diff,
                key=lambda x: x.to_gregorian() if not pd.isna(x) else pd.Timestamp.min,
            )

        new_array = JalaliDatetimeArray._from_sequence(diff, dtype=self.dtype)
        return type(self)._simple_new(new_array, name=self._name)

    # -------------------------------------------------------------------------
    # Required Index Methods
    # -------------------------------------------------------------------------

    def copy(self, name: Hashable = None, deep: bool = True) -> JalaliDatetimeIndex:
        """Make a copy of this object.

        Args:
            name: Name for the new index.
            deep: Whether to make a deep copy.

        Returns:
            Copy of the index.
        """
        new_data = self._data.copy() if deep else self._data
        return type(self)._simple_new(
            new_data,
            name=name if name is not None else self._name,
            freq=self._freq,
        )

    def _shallow_copy(
        self, values: JalaliDatetimeArray | None = None
    ) -> JalaliDatetimeIndex:
        """Create a shallow copy with optional new values."""
        if values is None:
            values = self._data
        return type(self)._simple_new(values, name=self._name, freq=self._freq)

    @property
    def _constructor(self) -> type[JalaliDatetimeIndex]:
        """Return the constructor for this type."""
        return type(self)

    def equals(self, other: object) -> bool:
        """Determine if two Index objects are equal."""
        if not isinstance(other, JalaliDatetimeIndex):
            return False
        if len(self) != len(other):
            return False
        return all(
            (pd.isna(a) and pd.isna(b)) or a == b
            for a, b in zip(self._data, other._data)
        )

    def __eq__(self, other: Any) -> Any:
        """Element-wise equality comparison."""
        if isinstance(other, JalaliDatetimeIndex):
            return cast(npt.NDArray[np.bool_], self._data == other._data)
        if isinstance(other, JalaliTimestamp):
            return cast(
                npt.NDArray[np.bool_],
                np.array([x == other for x in self._data], dtype=bool),
            )
        return NotImplemented

    def __ne__(self, other: Any) -> Any:
        """Element-wise inequality comparison."""
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return ~result

    def _isna(self) -> npt.NDArray[np.bool_]:
        """Return boolean array indicating NA values."""
        return self._data.isna()

    def _notna(self) -> npt.NDArray[np.bool_]:
        """Return boolean array indicating non-NA values."""
        return ~self._isna()

    @property
    def values(self) -> JalaliDatetimeArray:
        """Return the underlying data as a JalaliDatetimeArray."""
        return self._data

    def to_numpy(  # type: ignore[override]
        self,
        dtype: Any = None,
        copy: bool = False,
        na_value: Any = None,  # noqa: ARG002
    ) -> npt.NDArray[Any]:
        """Convert to numpy array."""
        if dtype is None:
            return self._data._data.copy() if copy else self._data._data
        return np.array(self._data._data, dtype=dtype, copy=copy)

    def to_list(self) -> list[JalaliTimestamp]:
        """Return a list of the values."""
        return list(self._data)

    def tolist(self) -> list[JalaliTimestamp]:
        """Return a list of the values."""
        return self.to_list()


__all__ = ["JalaliDatetimeIndex"]
