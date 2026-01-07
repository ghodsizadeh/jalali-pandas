"""Tests for JalaliWeek offset."""

from __future__ import annotations

import pytest

from jalali_pandas import JalaliTimestamp
from jalali_pandas.offsets import (
    FRIDAY,
    SATURDAY,
    JalaliWeek,
)


class TestJalaliWeekCreation:
    """Tests for JalaliWeek creation."""

    def test_default_creation(self):
        """Test default creation (Saturday)."""
        offset = JalaliWeek()
        assert offset.n == 1
        assert offset.weekday == SATURDAY
        assert offset.normalize is False

    def test_custom_weekday(self):
        """Test creation with custom weekday."""
        offset = JalaliWeek(weekday=FRIDAY)
        assert offset.weekday == FRIDAY

    def test_invalid_weekday_raises(self):
        """Test that invalid weekday raises ValueError."""
        with pytest.raises(ValueError, match="weekday must be 0-6"):
            JalaliWeek(weekday=7)
        with pytest.raises(ValueError, match="weekday must be 0-6"):
            JalaliWeek(weekday=-1)

    def test_repr(self):
        """Test string representation."""
        offset = JalaliWeek(n=2, weekday=FRIDAY)
        assert "n=2" in repr(offset)
        assert "weekday=6" in repr(offset)


class TestJalaliWeekArithmetic:
    """Tests for JalaliWeek arithmetic operations."""

    def test_add_one_week_from_saturday(self):
        """Test adding one week from a Saturday."""
        # 1402/6/11 is a Saturday (weekday=0)
        ts = JalaliTimestamp(1402, 6, 11)
        assert ts.dayofweek == SATURDAY

        result = ts + JalaliWeek(n=1)
        # Should move to next Saturday (7 days later)
        assert result.dayofweek == SATURDAY
        assert result.day == 18

    def test_add_one_week_from_non_saturday(self):
        """Test adding one week from a non-Saturday."""
        # 1402/6/13 is a Monday (weekday=2)
        ts = JalaliTimestamp(1402, 6, 13)
        assert ts.dayofweek == 2  # Monday in Jalali week

        result = ts + JalaliWeek(n=1)
        # Should move to next Saturday (5 days back in week, so forward to next Sat)
        assert result.dayofweek == SATURDAY
        assert result.day == 18  # Next Saturday

    def test_add_two_weeks(self):
        """Test adding two weeks."""
        ts = JalaliTimestamp(1402, 6, 13)  # Monday
        result = ts + JalaliWeek(n=2)
        # Should move to Saturday 2 weeks from now
        assert result.dayofweek == SATURDAY
        assert result.day == 25  # 5 days to Sat + 7 days

    def test_subtract_one_week(self):
        """Test subtracting one week."""
        ts = JalaliTimestamp(1402, 6, 11)  # Saturday
        result = ts + JalaliWeek(n=-1)
        # Should move to previous Saturday
        assert result.dayofweek == SATURDAY
        assert result.day == 4

    def test_add_week_with_custom_weekday(self):
        """Test adding week with custom weekday target."""
        ts = JalaliTimestamp(1402, 6, 13)  # Monday (weekday=2)
        result = ts + JalaliWeek(n=1, weekday=FRIDAY)
        # Friday is weekday=6, so move forward 4 days
        assert result.dayofweek == FRIDAY
        assert result.day == 17

    def test_negation(self):
        """Test negation of offset."""
        offset = JalaliWeek(n=2, weekday=FRIDAY)
        neg_offset = -offset
        assert neg_offset.n == -2
        assert neg_offset.weekday == FRIDAY

    def test_multiplication(self):
        """Test multiplication of offset."""
        offset = JalaliWeek(n=1, weekday=FRIDAY)
        mult_offset = offset * 3
        assert mult_offset.n == 3
        assert mult_offset.weekday == FRIDAY


class TestJalaliWeekRoll:
    """Tests for JalaliWeek roll operations."""

    def test_rollforward_on_target(self):
        """Test rollforward when already on target weekday."""
        ts = JalaliTimestamp(1402, 6, 11)  # Saturday (weekday=0)
        offset = JalaliWeek(weekday=SATURDAY)
        result = offset.rollforward(ts)
        assert result == ts

    def test_rollforward_not_on_target(self):
        """Test rollforward when not on target weekday."""
        ts = JalaliTimestamp(1402, 6, 13)  # Monday (weekday=2)
        offset = JalaliWeek(weekday=SATURDAY)
        result = offset.rollforward(ts)
        assert result.dayofweek == SATURDAY
        assert result.day == 18  # Next Saturday

    def test_rollback_on_target(self):
        """Test rollback when already on target weekday."""
        ts = JalaliTimestamp(1402, 6, 11)  # Saturday (weekday=0)
        offset = JalaliWeek(weekday=SATURDAY)
        result = offset.rollback(ts)
        assert result == ts

    def test_rollback_not_on_target(self):
        """Test rollback when not on target weekday."""
        ts = JalaliTimestamp(1402, 6, 13)  # Monday (weekday=2)
        offset = JalaliWeek(weekday=SATURDAY)
        result = offset.rollback(ts)
        assert result.dayofweek == SATURDAY
        assert result.day == 11  # Previous Saturday


class TestJalaliWeekIsOnOffset:
    """Tests for JalaliWeek is_on_offset method."""

    def test_is_on_offset_saturday(self):
        """Test is_on_offset for Saturday."""
        ts_sat = JalaliTimestamp(1402, 6, 11)  # Saturday (weekday=0)
        ts_mon = JalaliTimestamp(1402, 6, 13)  # Monday (weekday=2)

        offset = JalaliWeek(weekday=SATURDAY)
        assert offset.is_on_offset(ts_sat) is True
        assert offset.is_on_offset(ts_mon) is False

    def test_is_on_offset_friday(self):
        """Test is_on_offset for Friday."""
        ts_fri = JalaliTimestamp(1402, 6, 17)  # Friday (weekday=6)
        ts_sat = JalaliTimestamp(1402, 6, 11)  # Saturday (weekday=0)

        offset = JalaliWeek(weekday=FRIDAY)
        assert offset.is_on_offset(ts_fri) is True
        assert offset.is_on_offset(ts_sat) is False


class TestJalaliWeekEquality:
    """Tests for JalaliWeek equality and hashing."""

    def test_equality(self):
        """Test equality comparison."""
        offset1 = JalaliWeek(n=1, weekday=SATURDAY)
        offset2 = JalaliWeek(n=1, weekday=SATURDAY)
        offset3 = JalaliWeek(n=1, weekday=FRIDAY)
        offset4 = JalaliWeek(n=2, weekday=SATURDAY)

        assert offset1 == offset2
        assert offset1 != offset3
        assert offset1 != offset4

    def test_hash(self):
        """Test hashing."""
        offset1 = JalaliWeek(n=1, weekday=SATURDAY)
        offset2 = JalaliWeek(n=1, weekday=SATURDAY)

        assert hash(offset1) == hash(offset2)
        # Can be used in sets
        s = {offset1, offset2}
        assert len(s) == 1


class TestJalaliWeekNormalize:
    """Tests for JalaliWeek normalize parameter."""

    def test_normalize_true(self):
        """Test that normalize=True sets time to midnight."""
        ts = JalaliTimestamp(1402, 6, 15, 10, 30, 45)
        offset = JalaliWeek(n=1, normalize=True)
        result = ts + offset
        assert result.hour == 0
        assert result.minute == 0
        assert result.second == 0

    def test_normalize_false(self):
        """Test that normalize=False preserves time."""
        ts = JalaliTimestamp(1402, 6, 15, 10, 30, 45)
        offset = JalaliWeek(n=1, normalize=False)
        result = ts + offset
        assert result.hour == 10
        assert result.minute == 30
        assert result.second == 45
