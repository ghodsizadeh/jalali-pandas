"""JalaliDatetimeDtype - ExtensionDtype for Jalali datetime."""

from __future__ import annotations

import builtins
from typing import TYPE_CHECKING

import pandas as pd
from pandas.api.extensions import ExtensionDtype, register_extension_dtype

if TYPE_CHECKING:
    from jalali_pandas.core.arrays import JalaliDatetimeArray


@register_extension_dtype
class JalaliDatetimeDtype(ExtensionDtype):
    """ExtensionDtype for Jalali datetime data.

    This dtype represents Jalali (Persian/Shamsi) calendar datetimes
    and integrates with pandas' ExtensionArray system.

    Attributes:
        name: String identifier for the dtype.
        type: The scalar type for the array.
        na_value: The missing value sentinel.

    Examples:
        >>> dtype = JalaliDatetimeDtype()
        >>> dtype.name
        'jalali_datetime'
        >>> pd.array([...], dtype='jalali_datetime')
    """

    name = "jalali_datetime"
    type = object  # Will be JalaliTimestamp
    na_value = pd.NaT
    _metadata: tuple[str, ...] = ("tz",)

    def __init__(self, tz: str | None = None) -> None:
        """Initialize JalaliDatetimeDtype.

        Args:
            tz: Timezone string (e.g., 'Asia/Tehran'). Defaults to None.
        """
        self._tz = tz

    @property
    def tz(self) -> str | None:
        """Timezone for this dtype."""
        return self._tz

    @classmethod
    def construct_array_type(cls) -> builtins.type[JalaliDatetimeArray]:
        """Return the array type associated with this dtype.

        Returns:
            JalaliDatetimeArray class.
        """
        from jalali_pandas.core.arrays import JalaliDatetimeArray

        return JalaliDatetimeArray

    @classmethod
    def construct_from_string(cls, string: str) -> JalaliDatetimeDtype:
        """Construct dtype from a string.

        Args:
            string: String representation of the dtype.

        Returns:
            JalaliDatetimeDtype instance.

        Raises:
            TypeError: If string doesn't match expected format.
        """
        if not isinstance(string, str):
            raise TypeError(f"Expected string, got {type(string)}")

        if string == cls.name:
            return cls()

        # Handle timezone specification: jalali_datetime[tz]
        if string.startswith(f"{cls.name}[") and string.endswith("]"):
            tz = string[len(cls.name) + 1 : -1]
            return cls(tz=tz if tz else None)

        raise TypeError(f"Cannot construct {cls.__name__} from '{string}'")

    def __repr__(self) -> str:
        """String representation."""
        if self._tz:
            return f"{self.name}[{self._tz}]"
        return self.name

    def __str__(self) -> str:
        """String representation."""
        return self.__repr__()

    def __hash__(self) -> int:
        """Hash for use in sets and dicts."""
        return hash((self.name, self._tz))

    def __eq__(self, other: object) -> bool:
        """Check equality with another dtype."""
        if isinstance(other, str):
            try:
                other = self.construct_from_string(other)
            except TypeError:
                return False

        if isinstance(other, JalaliDatetimeDtype):
            return self._tz == other._tz

        return False

    @property
    def _is_numeric(self) -> bool:
        """Whether this dtype is numeric."""
        return False

    @property
    def _is_boolean(self) -> bool:
        """Whether this dtype is boolean."""
        return False


__all__ = ["JalaliDatetimeDtype"]
