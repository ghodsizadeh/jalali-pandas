"""Jalali week offset."""

from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING

from jalali_pandas.offsets.base import JalaliOffset

if TYPE_CHECKING:
    from jalali_pandas.core.timestamp import JalaliTimestamp

# Jalali week starts on Saturday (0=Saturday, 6=Friday)
SATURDAY = 0
SUNDAY = 1
MONDAY = 2
TUESDAY = 3
WEDNESDAY = 4
THURSDAY = 5
FRIDAY = 6


class JalaliWeek(JalaliOffset):
    """Offset to a specific day of the Jalali week.

    The Jalali week starts on Saturday (weekday=0) and ends on Friday (weekday=6).

    Attributes:
        weekday: The target weekday (0=Saturday, 6=Friday). Defaults to 0 (Saturday).
    """

    _prefix = "JW"
    _attributes = ("n", "normalize", "weekday")

    def __init__(
        self,
        n: int = 1,
        normalize: bool = False,
        weekday: int = SATURDAY,
    ) -> None:
        """Initialize JalaliWeek offset.

        Args:
            n: Number of weeks. Defaults to 1.
            normalize: Whether to normalize to midnight. Defaults to False.
            weekday: Target weekday (0=Saturday, 6=Friday). Defaults to 0 (Saturday).

        Raises:
            ValueError: If weekday is not in range 0-6.
        """
        super().__init__(n=n, normalize=normalize)
        if not 0 <= weekday <= 6:
            raise ValueError(f"weekday must be 0-6, got {weekday}")
        self._weekday = weekday

    @property
    def weekday(self) -> int:
        """Target weekday (0=Saturday, 6=Friday)."""
        return self._weekday

    def __repr__(self) -> str:
        """String representation."""
        return f"<{self.__class__.__name__}: n={self._n}, weekday={self._weekday}>"

    def __eq__(self, other: object) -> bool:
        """Check equality."""
        if isinstance(other, JalaliWeek):
            return (
                type(self) is type(other)
                and self._n == other._n
                and self._weekday == other._weekday
            )
        return False

    def __hash__(self) -> int:
        """Hash for use in sets and dicts."""
        return hash((type(self).__name__, self._n, self._weekday))

    def __neg__(self) -> JalaliWeek:
        """Return negated offset."""
        return JalaliWeek(n=-self._n, normalize=self._normalize, weekday=self._weekday)

    def __mul__(self, other: int) -> JalaliWeek:
        """Multiply offset by integer."""
        if isinstance(other, int):
            return JalaliWeek(
                n=self._n * other, normalize=self._normalize, weekday=self._weekday
            )
        return NotImplemented

    def __add__(self, other: JalaliTimestamp) -> JalaliTimestamp:
        """Add weeks to timestamp, landing on target weekday."""
        from jalali_pandas.core.timestamp import JalaliTimestamp

        if not isinstance(other, JalaliTimestamp):
            return NotImplemented

        # Get current weekday (0=Saturday, 6=Friday)
        current_weekday = other.dayofweek

        # Calculate days to target weekday
        days_to_target = (self._weekday - current_weekday) % 7

        # If we're already on the target weekday and n > 0, we need to go forward
        # If n < 0, we need to go backward
        if self._n > 0:
            # Move forward n weeks, landing on target weekday
            if days_to_target == 0:
                # Already on target, move n full weeks
                total_days = self._n * 7
            else:
                # Move to next target weekday, then (n-1) more weeks
                total_days = days_to_target + (self._n - 1) * 7
        elif self._n < 0:
            # Move backward |n| weeks, landing on target weekday
            if days_to_target == 0:
                # Already on target, move |n| full weeks back
                total_days = self._n * 7
            else:
                # Move to previous target weekday, then (|n|-1) more weeks back
                days_to_prev_target = days_to_target - 7  # Negative
                total_days = days_to_prev_target + (self._n + 1) * 7
        else:
            # n == 0, just move to nearest target weekday (forward)
            total_days = days_to_target

        # Apply the offset using timedelta
        new_gregorian = other.to_gregorian() + timedelta(days=total_days)
        result = JalaliTimestamp.from_gregorian(new_gregorian)

        if self._normalize:
            result = result.normalize()

        return result

    def __sub__(self, other: JalaliTimestamp) -> JalaliTimestamp:
        """Subtract weeks from timestamp."""
        return self.__neg__().__add__(other)

    def rollforward(self, dt: JalaliTimestamp) -> JalaliTimestamp:
        """Roll forward to next target weekday if not already on one."""
        if self.is_on_offset(dt):
            return dt

        # Calculate days to next target weekday
        current_weekday = dt.dayofweek
        days_forward = (self._weekday - current_weekday) % 7
        if days_forward == 0:
            days_forward = 7  # Move to next week if already on target

        new_gregorian = dt.to_gregorian() + timedelta(days=days_forward)
        result = type(dt).from_gregorian(new_gregorian)

        if self._normalize:
            result = result.normalize()

        return result

    def rollback(self, dt: JalaliTimestamp) -> JalaliTimestamp:
        """Roll back to previous target weekday."""
        if self.is_on_offset(dt):
            return dt

        # Calculate days to previous target weekday
        current_weekday = dt.dayofweek
        days_back = (current_weekday - self._weekday) % 7
        if days_back == 0:
            days_back = 7  # Move to previous week if already on target

        new_gregorian = dt.to_gregorian() - timedelta(days=days_back)
        result = type(dt).from_gregorian(new_gregorian)

        if self._normalize:
            result = result.normalize()

        return result

    def is_on_offset(self, dt: JalaliTimestamp) -> bool:
        """Check if date is on target weekday."""
        return dt.dayofweek == self._weekday


__all__ = [
    "JalaliWeek",
    "SATURDAY",
    "SUNDAY",
    "MONDAY",
    "TUESDAY",
    "WEDNESDAY",
    "THURSDAY",
    "FRIDAY",
]
