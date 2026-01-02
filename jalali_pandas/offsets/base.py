"""Base class for Jalali calendar offsets."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from jalali_pandas.core.timestamp import JalaliTimestamp


class JalaliOffset(ABC):
    """Abstract base class for Jalali calendar-aware offsets.

    This class provides the foundation for implementing calendar-aware
    date offsets that respect Jalali calendar rules.

    Attributes:
        n: Number of periods.
        normalize: Whether to normalize to midnight.
    """

    _prefix: str = "J"
    _attributes: tuple[str, ...] = ("n", "normalize")

    def __init__(self, n: int = 1, normalize: bool = False) -> None:
        """Initialize JalaliOffset.

        Args:
            n: Number of periods. Defaults to 1.
            normalize: Whether to normalize to midnight. Defaults to False.
        """
        self._n = n
        self._normalize = normalize

    @property
    def n(self) -> int:
        """Number of periods."""
        return self._n

    @property
    def normalize(self) -> bool:
        """Whether to normalize to midnight."""
        return self._normalize

    @property
    def name(self) -> str:
        """Return the name of the offset."""
        return f"{self._prefix}{abs(self._n)}"

    @property
    def freqstr(self) -> str:
        """Return the frequency string."""
        return self.name

    def __repr__(self) -> str:
        """String representation."""
        return f"<{self.__class__.__name__}: n={self._n}>"

    def __eq__(self, other: object) -> bool:
        """Check equality."""
        if isinstance(other, JalaliOffset):
            return type(self) is type(other) and self._n == other._n
        return False

    def __hash__(self) -> int:
        """Hash for use in sets and dicts."""
        return hash((type(self).__name__, self._n))

    def __neg__(self) -> JalaliOffset:
        """Return negated offset."""
        return type(self)(n=-self._n, normalize=self._normalize)

    def __mul__(self, other: int) -> JalaliOffset:
        """Multiply offset by integer."""
        if isinstance(other, int):
            return type(self)(n=self._n * other, normalize=self._normalize)
        return NotImplemented

    def __rmul__(self, other: int) -> JalaliOffset:
        """Right multiply offset by integer."""
        return self.__mul__(other)

    @abstractmethod
    def __add__(self, other: JalaliTimestamp) -> JalaliTimestamp:
        """Add offset to a JalaliTimestamp."""
        ...

    def __radd__(self, other: JalaliTimestamp) -> JalaliTimestamp:
        """Right add offset to a JalaliTimestamp."""
        return self.__add__(other)

    @abstractmethod
    def __sub__(self, other: JalaliTimestamp) -> JalaliTimestamp:
        """Subtract offset from a JalaliTimestamp."""
        ...

    @abstractmethod
    def rollforward(self, dt: JalaliTimestamp) -> JalaliTimestamp:
        """Roll forward to next valid date.

        Args:
            dt: JalaliTimestamp to roll forward.

        Returns:
            Rolled forward JalaliTimestamp.
        """
        ...

    @abstractmethod
    def rollback(self, dt: JalaliTimestamp) -> JalaliTimestamp:
        """Roll back to previous valid date.

        Args:
            dt: JalaliTimestamp to roll back.

        Returns:
            Rolled back JalaliTimestamp.
        """
        ...

    @abstractmethod
    def is_on_offset(self, dt: JalaliTimestamp) -> bool:
        """Check if date is on offset boundary.

        Args:
            dt: JalaliTimestamp to check.

        Returns:
            True if on offset boundary.
        """
        ...

    def _apply(self, other: JalaliTimestamp) -> JalaliTimestamp:
        """Apply offset to timestamp.

        Args:
            other: JalaliTimestamp to apply offset to.

        Returns:
            New JalaliTimestamp with offset applied.
        """
        result = self.__add__(other)
        if self._normalize:
            result = result.normalize()
        return result


__all__ = ["JalaliOffset"]
