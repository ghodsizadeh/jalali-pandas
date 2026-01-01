"""JalaliDatetimeArray - ExtensionArray for Jalali datetime."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Sequence

import numpy as np
import pandas as pd
from pandas.api.extensions import ExtensionArray
from pandas.core.arrays import ExtensionArray as ExtensionArrayBase

from jalali_pandas.core.dtypes import JalaliDatetimeDtype
from jalali_pandas.core.timestamp import JalaliTimestamp

if TYPE_CHECKING:
    from pandas._typing import NumpyValueArrayLike


class JalaliDatetimeArray(ExtensionArray):
    """ExtensionArray for Jalali datetime data.

    This array stores Jalali timestamps and integrates with pandas'
    ExtensionArray system for seamless DataFrame/Series operations.

    Attributes:
        dtype: The JalaliDatetimeDtype for this array.

    Examples:
        >>> arr = JalaliDatetimeArray._from_sequence([
        ...     JalaliTimestamp(1402, 1, 1),
        ...     JalaliTimestamp(1402, 1, 2),
        ... ])
        >>> arr[0]
        JalaliTimestamp('1402-01-01T00:00:00')
    """

    _dtype: JalaliDatetimeDtype
    _data: np.ndarray  # Object array of JalaliTimestamp or NaT

    def __init__(
        self,
        data: np.ndarray,
        dtype: JalaliDatetimeDtype | None = None,
        copy: bool = False,
    ) -> None:
        """Initialize JalaliDatetimeArray.

        Args:
            data: Array of JalaliTimestamp objects.
            dtype: JalaliDatetimeDtype instance. Defaults to None.
            copy: Whether to copy the data. Defaults to False.
        """
        if copy:
            data = data.copy()

        self._data = data
        self._dtype = dtype if dtype is not None else JalaliDatetimeDtype()

    @property
    def dtype(self) -> JalaliDatetimeDtype:
        """Return the dtype for this array."""
        return self._dtype

    @property
    def nbytes(self) -> int:
        """Return the number of bytes in the array."""
        return self._data.nbytes

    def __len__(self) -> int:
        """Return the length of the array."""
        return len(self._data)

    def __getitem__(self, key: Any) -> JalaliTimestamp | JalaliDatetimeArray:
        """Get item(s) from the array."""
        result = self._data[key]

        if isinstance(result, np.ndarray):
            return type(self)(result, dtype=self._dtype)

        return result

    def __setitem__(self, key: Any, value: Any) -> None:
        """Set item(s) in the array."""
        if isinstance(value, JalaliTimestamp):
            self._data[key] = value
        elif pd.isna(value):
            self._data[key] = pd.NaT
        elif isinstance(value, (list, np.ndarray, JalaliDatetimeArray)):
            values = self._from_sequence(value, dtype=self._dtype)
            self._data[key] = values._data
        else:
            raise TypeError(f"Cannot set {type(value)} in JalaliDatetimeArray")

    def __iter__(self):
        """Iterate over the array."""
        return iter(self._data)

    def __eq__(self, other: Any) -> np.ndarray:
        """Element-wise equality comparison."""
        if isinstance(other, JalaliDatetimeArray):
            return self._data == other._data
        if isinstance(other, JalaliTimestamp):
            return np.array([x == other for x in self._data])
        return NotImplemented

    def __ne__(self, other: Any) -> np.ndarray:
        """Element-wise inequality comparison."""
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return ~result

    @classmethod
    def _from_sequence(
        cls,
        scalars: Sequence[Any],
        *,
        dtype: JalaliDatetimeDtype | None = None,
        copy: bool = False,
    ) -> JalaliDatetimeArray:
        """Create array from sequence of scalars.

        Args:
            scalars: Sequence of JalaliTimestamp, strings, or NaT values.
            dtype: JalaliDatetimeDtype instance.
            copy: Whether to copy the data.

        Returns:
            JalaliDatetimeArray instance.
        """
        result = []
        for scalar in scalars:
            if isinstance(scalar, JalaliTimestamp):
                result.append(scalar)
            elif pd.isna(scalar):
                result.append(pd.NaT)
            elif isinstance(scalar, str):
                # Try to parse string
                try:
                    result.append(JalaliTimestamp.strptime(scalar, "%Y-%m-%d"))
                except ValueError:
                    try:
                        result.append(
                            JalaliTimestamp.strptime(scalar, "%Y-%m-%d %H:%M:%S")
                        )
                    except ValueError:
                        result.append(pd.NaT)
            elif isinstance(scalar, pd.Timestamp):
                result.append(JalaliTimestamp.from_gregorian(scalar))
            else:
                result.append(pd.NaT)

        data = np.array(result, dtype=object)
        return cls(data, dtype=dtype, copy=copy)

    @classmethod
    def _from_sequence_of_strings(
        cls,
        strings: Sequence[str],
        *,
        dtype: JalaliDatetimeDtype | None = None,
        copy: bool = False,
    ) -> JalaliDatetimeArray:
        """Create array from sequence of strings.

        Args:
            strings: Sequence of date strings.
            dtype: JalaliDatetimeDtype instance.
            copy: Whether to copy the data.

        Returns:
            JalaliDatetimeArray instance.
        """
        return cls._from_sequence(strings, dtype=dtype, copy=copy)

    @classmethod
    def _from_factorized(
        cls, values: np.ndarray, original: JalaliDatetimeArray
    ) -> JalaliDatetimeArray:
        """Reconstruct array from factorized values.

        Args:
            values: Unique values array.
            original: Original array for dtype.

        Returns:
            JalaliDatetimeArray instance.
        """
        return cls(values, dtype=original.dtype)

    def _values_for_factorize(self) -> tuple[np.ndarray, Any]:
        """Return values and NA value for factorization."""
        return self._data, pd.NaT

    def isna(self) -> np.ndarray:
        """Return boolean array indicating NA values."""
        return np.array([pd.isna(x) for x in self._data], dtype=bool)

    def take(
        self,
        indices: Sequence[int],
        *,
        allow_fill: bool = False,
        fill_value: Any = None,
    ) -> JalaliDatetimeArray:
        """Take elements from the array.

        Args:
            indices: Indices to take.
            allow_fill: Whether to allow fill values for -1 indices.
            fill_value: Value to use for -1 indices.

        Returns:
            JalaliDatetimeArray with taken elements.
        """
        if allow_fill:
            if fill_value is None:
                fill_value = pd.NaT

            result = []
            for i in indices:
                if i == -1:
                    result.append(fill_value)
                else:
                    result.append(self._data[i])
            data = np.array(result, dtype=object)
        else:
            data = self._data[list(indices)]

        return type(self)(data, dtype=self._dtype)

    def copy(self) -> JalaliDatetimeArray:
        """Return a copy of the array."""
        return type(self)(self._data.copy(), dtype=self._dtype)

    @classmethod
    def _concat_same_type(
        cls, to_concat: Sequence[JalaliDatetimeArray]
    ) -> JalaliDatetimeArray:
        """Concatenate arrays of the same type.

        Args:
            to_concat: Sequence of arrays to concatenate.

        Returns:
            Concatenated JalaliDatetimeArray.
        """
        data = np.concatenate([arr._data for arr in to_concat])
        return cls(data, dtype=to_concat[0].dtype)

    def __repr__(self) -> str:
        """String representation."""
        data_repr = ", ".join(repr(x) for x in self._data[:5])
        if len(self._data) > 5:
            data_repr += ", ..."
        return f"JalaliDatetimeArray([{data_repr}], dtype={self._dtype})"

    # -------------------------------------------------------------------------
    # Jalali-specific methods
    # -------------------------------------------------------------------------

    @property
    def year(self) -> np.ndarray:
        """Return array of years."""
        return np.array(
            [x.year if not pd.isna(x) else np.nan for x in self._data], dtype=float
        )

    @property
    def month(self) -> np.ndarray:
        """Return array of months."""
        return np.array(
            [x.month if not pd.isna(x) else np.nan for x in self._data], dtype=float
        )

    @property
    def day(self) -> np.ndarray:
        """Return array of days."""
        return np.array(
            [x.day if not pd.isna(x) else np.nan for x in self._data], dtype=float
        )

    @property
    def hour(self) -> np.ndarray:
        """Return array of hours."""
        return np.array(
            [x.hour if not pd.isna(x) else np.nan for x in self._data], dtype=float
        )

    @property
    def minute(self) -> np.ndarray:
        """Return array of minutes."""
        return np.array(
            [x.minute if not pd.isna(x) else np.nan for x in self._data], dtype=float
        )

    @property
    def second(self) -> np.ndarray:
        """Return array of seconds."""
        return np.array(
            [x.second if not pd.isna(x) else np.nan for x in self._data], dtype=float
        )

    @property
    def quarter(self) -> np.ndarray:
        """Return array of quarters."""
        return np.array(
            [x.quarter if not pd.isna(x) else np.nan for x in self._data], dtype=float
        )

    @property
    def dayofweek(self) -> np.ndarray:
        """Return array of day of week values."""
        return np.array(
            [x.dayofweek if not pd.isna(x) else np.nan for x in self._data], dtype=float
        )

    @property
    def dayofyear(self) -> np.ndarray:
        """Return array of day of year values."""
        return np.array(
            [x.dayofyear if not pd.isna(x) else np.nan for x in self._data], dtype=float
        )

    @property
    def week(self) -> np.ndarray:
        """Return array of week numbers."""
        return np.array(
            [x.week if not pd.isna(x) else np.nan for x in self._data], dtype=float
        )

    def to_gregorian(self) -> pd.DatetimeIndex:
        """Convert to pandas DatetimeIndex (Gregorian).

        Returns:
            DatetimeIndex with Gregorian timestamps.
        """
        timestamps = [
            x.to_gregorian() if not pd.isna(x) else pd.NaT for x in self._data
        ]
        return pd.DatetimeIndex(timestamps)

    def strftime(self, fmt: str) -> np.ndarray:
        """Format timestamps as strings.

        Args:
            fmt: Format string.

        Returns:
            Array of formatted strings.
        """
        return np.array(
            [x.strftime(fmt) if not pd.isna(x) else None for x in self._data],
            dtype=object,
        )


__all__ = ["JalaliDatetimeArray"]
