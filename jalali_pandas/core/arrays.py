"""JalaliDatetimeArray - ExtensionArray for Jalali datetime."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import Any, cast, overload

import numpy as np
import numpy.typing as npt
import pandas as pd
from pandas.api.extensions import ExtensionArray

from jalali_pandas._typing import NaTType
from jalali_pandas.core.dtypes import JalaliDatetimeDtype
from jalali_pandas.core.timestamp import JalaliTimestamp


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
    _data: npt.NDArray[np.object_]  # Object array of JalaliTimestamp or NaT

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
        return int(self._data.nbytes)

    def __len__(self) -> int:
        """Return the length of the array."""
        return len(self._data)

    @overload
    def __getitem__(self, key: int) -> JalaliTimestamp | NaTType: ...

    @overload
    def __getitem__(
        self, key: slice | Sequence[int] | npt.NDArray[np.bool_]
    ) -> JalaliDatetimeArray: ...

    def __getitem__(self, key: Any) -> Any:
        """Get item(s) from the array."""
        result = self._data[key]

        if isinstance(result, np.ndarray):
            return type(self)(cast(npt.NDArray[np.object_], result), dtype=self._dtype)

        return result

    def __setitem__(self, key: Any, value: Any) -> None:
        """Set item(s) in the array."""
        if isinstance(value, JalaliTimestamp):
            self._data[key] = value
        elif isinstance(value, JalaliDatetimeArray):
            self._data[key] = value._data
        elif isinstance(value, (list, np.ndarray)):
            values = self._from_sequence(cast(Sequence[Any], value), dtype=self._dtype)
            self._data[key] = values._data
        elif pd.isna(value):
            self._data[key] = pd.NaT
        else:
            raise TypeError(f"Cannot set {type(value)} in JalaliDatetimeArray")

    def __iter__(self) -> Iterator[Any]:
        """Iterate over the array."""
        return iter(self._data)

    def __eq__(self, other: Any) -> Any:
        """Element-wise equality comparison."""
        if isinstance(other, JalaliDatetimeArray):
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
        result: list[JalaliTimestamp | NaTType] = []
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

        data = cast(npt.NDArray[np.object_], np.array(result, dtype=object))
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
        cls, values: npt.NDArray[np.object_], original: JalaliDatetimeArray
    ) -> JalaliDatetimeArray:
        """Reconstruct array from factorized values.

        Args:
            values: Unique values array.
            original: Original array for dtype.

        Returns:
            JalaliDatetimeArray instance.
        """
        return cls(values, dtype=original.dtype)

    def _values_for_factorize(self) -> tuple[npt.NDArray[np.object_], NaTType]:
        """Return values and NA value for factorization."""
        return self._data, pd.NaT

    def isna(self) -> npt.NDArray[np.bool_]:
        """Return boolean array indicating NA values."""
        return cast(
            npt.NDArray[np.bool_],
            np.array([pd.isna(x) for x in self._data], dtype=bool),
        )

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

            result: list[object] = []
            for i in indices:
                if i == -1:
                    result.append(fill_value)
                else:
                    result.append(self._data[i])
            data = cast(npt.NDArray[np.object_], np.array(result, dtype=object))
        else:
            data = cast(npt.NDArray[np.object_], self._data[list(indices)])

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
        data = cast(
            npt.NDArray[np.object_], np.concatenate([arr._data for arr in to_concat])
        )
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
    def year(self) -> npt.NDArray[np.float64]:
        """Return array of years."""
        return cast(
            npt.NDArray[np.float64],
            np.array(
                [x.year if not pd.isna(x) else np.nan for x in self._data],
                dtype=float,
            ),
        )

    @property
    def month(self) -> npt.NDArray[np.float64]:
        """Return array of months."""
        return cast(
            npt.NDArray[np.float64],
            np.array(
                [x.month if not pd.isna(x) else np.nan for x in self._data],
                dtype=float,
            ),
        )

    @property
    def day(self) -> npt.NDArray[np.float64]:
        """Return array of days."""
        return cast(
            npt.NDArray[np.float64],
            np.array(
                [x.day if not pd.isna(x) else np.nan for x in self._data],
                dtype=float,
            ),
        )

    @property
    def hour(self) -> npt.NDArray[np.float64]:
        """Return array of hours."""
        return cast(
            npt.NDArray[np.float64],
            np.array(
                [x.hour if not pd.isna(x) else np.nan for x in self._data],
                dtype=float,
            ),
        )

    @property
    def minute(self) -> npt.NDArray[np.float64]:
        """Return array of minutes."""
        return cast(
            npt.NDArray[np.float64],
            np.array(
                [x.minute if not pd.isna(x) else np.nan for x in self._data],
                dtype=float,
            ),
        )

    @property
    def second(self) -> npt.NDArray[np.float64]:
        """Return array of seconds."""
        return cast(
            npt.NDArray[np.float64],
            np.array(
                [x.second if not pd.isna(x) else np.nan for x in self._data],
                dtype=float,
            ),
        )

    @property
    def quarter(self) -> npt.NDArray[np.float64]:
        """Return array of quarters."""
        return cast(
            npt.NDArray[np.float64],
            np.array(
                [x.quarter if not pd.isna(x) else np.nan for x in self._data],
                dtype=float,
            ),
        )

    @property
    def dayofweek(self) -> npt.NDArray[np.float64]:
        """Return array of day of week values."""
        return cast(
            npt.NDArray[np.float64],
            np.array(
                [x.dayofweek if not pd.isna(x) else np.nan for x in self._data],
                dtype=float,
            ),
        )

    @property
    def dayofyear(self) -> npt.NDArray[np.float64]:
        """Return array of day of year values."""
        return cast(
            npt.NDArray[np.float64],
            np.array(
                [x.dayofyear if not pd.isna(x) else np.nan for x in self._data],
                dtype=float,
            ),
        )

    @property
    def week(self) -> npt.NDArray[np.float64]:
        """Return array of week numbers."""
        return cast(
            npt.NDArray[np.float64],
            np.array(
                [x.week if not pd.isna(x) else np.nan for x in self._data],
                dtype=float,
            ),
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

    def strftime(self, fmt: str) -> npt.NDArray[np.object_]:
        """Format timestamps as strings.

        Args:
            fmt: Format string.

        Returns:
            Array of formatted strings.
        """
        return cast(
            npt.NDArray[np.object_],
            np.array(
                [x.strftime(fmt) if not pd.isna(x) else None for x in self._data],
                dtype=object,
            ),
        )


__all__ = ["JalaliDatetimeArray"]
