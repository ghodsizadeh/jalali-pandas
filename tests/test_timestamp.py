"""Tests for JalaliTimestamp."""

from datetime import timedelta

import pandas as pd
import pytest

from jalali_pandas import JalaliTimestamp


class TestJalaliTimestampCreation:
    """Tests for JalaliTimestamp creation."""

    def test_basic_creation(self):
        """Test basic timestamp creation."""
        ts = JalaliTimestamp(1402, 6, 15)
        assert ts.year == 1402
        assert ts.month == 6
        assert ts.day == 15
        assert ts.hour == 0
        assert ts.minute == 0
        assert ts.second == 0

    def test_full_creation(self):
        """Test timestamp creation with all components."""
        ts = JalaliTimestamp(1402, 6, 15, 10, 30, 45, 123456, 789)
        assert ts.year == 1402
        assert ts.month == 6
        assert ts.day == 15
        assert ts.hour == 10
        assert ts.minute == 30
        assert ts.second == 45
        assert ts.microsecond == 123456
        assert ts.nanosecond == 789

    def test_invalid_month(self):
        """Test that invalid month raises ValueError."""
        with pytest.raises(ValueError):
            JalaliTimestamp(1402, 13, 1)

    def test_invalid_day(self):
        """Test that invalid day raises ValueError."""
        with pytest.raises(ValueError):
            JalaliTimestamp(1402, 1, 32)

    def test_invalid_esfand_day(self):
        """Test that day 30 in Esfand of non-leap year raises ValueError."""
        # 1401 is a leap year, 1402 is not
        with pytest.raises(ValueError):
            JalaliTimestamp(1402, 12, 30)

    def test_valid_esfand_leap_year(self):
        """Test that day 30 in Esfand of leap year is valid."""
        ts = JalaliTimestamp(1403, 12, 30)  # 1403 is a leap year
        assert ts.day == 30


class TestJalaliTimestampProperties:
    """Tests for JalaliTimestamp derived properties."""

    def test_quarter(self):
        """Test quarter property."""
        assert JalaliTimestamp(1402, 1, 1).quarter == 1
        assert JalaliTimestamp(1402, 4, 1).quarter == 2
        assert JalaliTimestamp(1402, 7, 1).quarter == 3
        assert JalaliTimestamp(1402, 10, 1).quarter == 4

    def test_is_leap_year(self):
        """Test is_leap_year property."""
        assert JalaliTimestamp(1403, 1, 1).is_leap_year is True
        assert JalaliTimestamp(1402, 1, 1).is_leap_year is False

    def test_days_in_month(self):
        """Test days_in_month property."""
        assert JalaliTimestamp(1402, 1, 1).days_in_month == 31
        assert JalaliTimestamp(1402, 7, 1).days_in_month == 30
        assert JalaliTimestamp(1402, 12, 1).days_in_month == 29
        assert JalaliTimestamp(1403, 12, 1).days_in_month == 30

    def test_is_month_start(self):
        """Test is_month_start property."""
        assert JalaliTimestamp(1402, 1, 1).is_month_start is True
        assert JalaliTimestamp(1402, 1, 15).is_month_start is False

    def test_is_month_end(self):
        """Test is_month_end property."""
        assert JalaliTimestamp(1402, 1, 31).is_month_end is True
        assert JalaliTimestamp(1402, 1, 15).is_month_end is False

    def test_is_year_start(self):
        """Test is_year_start property (Nowruz)."""
        assert JalaliTimestamp(1402, 1, 1).is_year_start is True
        assert JalaliTimestamp(1402, 2, 1).is_year_start is False

    def test_is_year_end(self):
        """Test is_year_end property."""
        assert JalaliTimestamp(1402, 12, 29).is_year_end is True
        assert JalaliTimestamp(1403, 12, 30).is_year_end is True
        assert JalaliTimestamp(1402, 12, 28).is_year_end is False


class TestJalaliTimestampConversion:
    """Tests for JalaliTimestamp conversion methods."""

    def test_to_gregorian(self):
        """Test conversion to Gregorian."""
        ts = JalaliTimestamp(1402, 1, 1)
        gregorian = ts.to_gregorian()
        assert isinstance(gregorian, pd.Timestamp)
        # 1402/1/1 = 2023/3/21
        assert gregorian.year == 2023
        assert gregorian.month == 3
        assert gregorian.day == 21

    def test_from_gregorian(self):
        """Test creation from Gregorian."""
        gregorian = pd.Timestamp("2023-03-21")
        ts = JalaliTimestamp.from_gregorian(gregorian)
        assert ts.year == 1402
        assert ts.month == 1
        assert ts.day == 1

    def test_roundtrip_conversion(self):
        """Test that Jalali -> Gregorian -> Jalali preserves date."""
        original = JalaliTimestamp(1402, 6, 15, 10, 30, 45)
        gregorian = original.to_gregorian()
        restored = JalaliTimestamp.from_gregorian(gregorian)
        assert original == restored


class TestJalaliTimestampArithmetic:
    """Tests for JalaliTimestamp arithmetic operations."""

    def test_add_timedelta(self):
        """Test adding timedelta."""
        ts = JalaliTimestamp(1402, 1, 1)
        result = ts + timedelta(days=10)
        assert result.year == 1402
        assert result.month == 1
        assert result.day == 11

    def test_subtract_timedelta(self):
        """Test subtracting timedelta."""
        ts = JalaliTimestamp(1402, 1, 15)
        result = ts - timedelta(days=10)
        assert result.year == 1402
        assert result.month == 1
        assert result.day == 5

    def test_subtract_timestamps(self):
        """Test subtracting two timestamps."""
        ts1 = JalaliTimestamp(1402, 1, 15)
        ts2 = JalaliTimestamp(1402, 1, 10)
        result = ts1 - ts2
        assert isinstance(result, pd.Timedelta)
        assert result.days == 5


class TestJalaliTimestampComparison:
    """Tests for JalaliTimestamp comparison operations."""

    def test_equality(self):
        """Test equality comparison."""
        ts1 = JalaliTimestamp(1402, 6, 15)
        ts2 = JalaliTimestamp(1402, 6, 15)
        ts3 = JalaliTimestamp(1402, 6, 16)
        assert ts1 == ts2
        assert ts1 != ts3

    def test_less_than(self):
        """Test less than comparison."""
        ts1 = JalaliTimestamp(1402, 6, 15)
        ts2 = JalaliTimestamp(1402, 6, 16)
        assert ts1 < ts2
        assert not ts2 < ts1

    def test_greater_than(self):
        """Test greater than comparison."""
        ts1 = JalaliTimestamp(1402, 6, 16)
        ts2 = JalaliTimestamp(1402, 6, 15)
        assert ts1 > ts2
        assert not ts2 > ts1


class TestJalaliTimestampFormatting:
    """Tests for JalaliTimestamp formatting methods."""

    def test_strftime(self):
        """Test strftime formatting."""
        ts = JalaliTimestamp(1402, 6, 15, 10, 30, 45)
        assert ts.strftime("%Y-%m-%d") == "1402-06-15"
        assert ts.strftime("%H:%M:%S") == "10:30:45"

    def test_isoformat(self):
        """Test isoformat output."""
        ts = JalaliTimestamp(1402, 6, 15, 10, 30, 45)
        assert ts.isoformat() == "1402-06-15T10:30:45"

    def test_str(self):
        """Test string representation."""
        ts = JalaliTimestamp(1402, 6, 15, 10, 30, 45)
        assert str(ts) == "1402-06-15 10:30:45"

    def test_repr(self):
        """Test repr output."""
        ts = JalaliTimestamp(1402, 6, 15)
        assert "JalaliTimestamp" in repr(ts)


class TestJalaliTimestampReplace:
    """Tests for JalaliTimestamp replace method."""

    def test_replace_year(self):
        """Test replacing year."""
        ts = JalaliTimestamp(1402, 6, 15)
        new_ts = ts.replace(year=1403)
        assert new_ts.year == 1403
        assert new_ts.month == 6
        assert new_ts.day == 15

    def test_replace_multiple(self):
        """Test replacing multiple components."""
        ts = JalaliTimestamp(1402, 6, 15, 10, 30)
        new_ts = ts.replace(month=7, hour=12)
        assert new_ts.year == 1402
        assert new_ts.month == 7
        assert new_ts.day == 15
        assert new_ts.hour == 12
        assert new_ts.minute == 30

    def test_normalize(self):
        """Test normalize method."""
        ts = JalaliTimestamp(1402, 6, 15, 10, 30, 45)
        normalized = ts.normalize()
        assert normalized.hour == 0
        assert normalized.minute == 0
        assert normalized.second == 0
