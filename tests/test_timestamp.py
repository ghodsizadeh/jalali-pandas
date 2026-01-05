"""Tests for JalaliTimestamp."""

from __future__ import annotations

import math
from datetime import timedelta

import numpy as np
import pandas as pd
import pytest

from jalali_pandas import JalaliTimestamp
from jalali_pandas.core.timestamp import JalaliNaT, isna_jalali


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

    @pytest.mark.parametrize(
        ("kwargs", "message"),
        [
            ({"hour": 24}, "Hour must be 0-23"),
            ({"minute": 60}, "Minute must be 0-59"),
            ({"second": 60}, "Second must be 0-59"),
            ({"microsecond": 1_000_000}, "Microsecond must be"),
            ({"nanosecond": 1000}, "Nanosecond must be"),
        ],
    )
    def test_invalid_time_components(self, kwargs, message):
        """Test invalid time components raise ValueError."""
        with pytest.raises(ValueError, match=message):
            JalaliTimestamp(1402, 1, 1, **kwargs)


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

    def test_to_pydatetime(self):
        """Test conversion to Python datetime."""
        ts = JalaliTimestamp(1402, 1, 1, 10, 30, 0)
        py_dt = ts.to_pydatetime()

        assert py_dt.year == 2023
        assert py_dt.hour == 10

    def test_to_datetime64(self):
        """Test conversion to numpy datetime64."""
        ts = JalaliTimestamp(1402, 1, 1)
        dt64 = ts.to_datetime64()

        assert isinstance(dt64, np.datetime64)

    def test_from_gregorian_with_timezone(self):
        """Test from_gregorian applies timezone."""
        ts = JalaliTimestamp.from_gregorian(pd.Timestamp("2023-03-21"), tz="UTC")
        assert ts.tzinfo is not None

    def test_now_and_today(self):
        """Test now() and today() helpers."""
        now = JalaliTimestamp.now()
        today = JalaliTimestamp.today()

        assert isinstance(now, JalaliTimestamp)
        assert today.hour == 0


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

    def test_radd_timedelta(self):
        """Test right add for timedelta."""
        ts = JalaliTimestamp(1402, 1, 1)
        result = timedelta(days=1) + ts
        assert result == JalaliTimestamp(1402, 1, 2)


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

    def test_less_than_or_equal(self):
        """Test less than or equal comparison."""
        ts1 = JalaliTimestamp(1402, 6, 15)
        ts2 = JalaliTimestamp(1402, 6, 16)
        assert ts1 <= ts2

    def test_greater_than_or_equal(self):
        """Test greater than or equal comparison."""
        ts1 = JalaliTimestamp(1402, 6, 16)
        ts2 = JalaliTimestamp(1402, 6, 15)
        assert ts1 >= ts2


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

    def test_strptime_two_digit_year(self):
        """Test strptime handles two-digit years."""
        ts = JalaliTimestamp.strptime("02-01-01", "%y-%m-%d")
        assert ts.year == 1302

    def test_isoformat_with_timezone(self):
        """Test isoformat includes timezone offset."""
        from datetime import timedelta, timezone

        tz = timezone(timedelta(hours=3, minutes=30))
        ts = JalaliTimestamp(1402, 6, 15, 10, 0, 0, tzinfo=tz)
        assert ts.isoformat().endswith("+03:30")

    def test_isoformat_with_microsecond(self):
        """Test isoformat includes fractional seconds."""
        ts = JalaliTimestamp(1402, 6, 15, 10, 0, 0, 123456)
        assert ".123456" in ts.isoformat()


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

    def test_date_and_time_methods(self):
        """Test date() and time() methods."""
        ts = JalaliTimestamp(1402, 6, 15, 10, 30, 45, 123456)
        date_only = ts.date()
        time_only = ts.time()

        assert date_only.hour == 0
        assert time_only.hour == 10
        assert time_only.minute == 30


class TestJalaliNaT:
    """Tests for JalaliNaT (Not-a-Time) handling."""

    def test_nat_singleton(self):
        """Test that JalaliNaT is a singleton."""
        from jalali_pandas.core.timestamp import _JalaliNaTType

        nat1 = _JalaliNaTType()
        nat2 = _JalaliNaTType()
        assert nat1 is nat2
        assert nat1 is JalaliNaT

    def test_nat_repr(self):
        """Test JalaliNaT string representation."""
        assert repr(JalaliNaT) == "JalaliNaT"
        assert str(JalaliNaT) == "JalaliNaT"

    def test_nat_bool(self):
        """Test JalaliNaT is falsy."""
        assert not JalaliNaT
        assert bool(JalaliNaT) is False

    def test_nat_hash(self):
        """Test JalaliNaT is hashable."""
        assert hash(JalaliNaT) == hash("JalaliNaT")
        # Can be used in sets/dicts
        s = {JalaliNaT}
        assert JalaliNaT in s

    def test_nat_equality(self):
        """Test JalaliNaT equality comparisons."""
        assert JalaliNaT == JalaliNaT
        assert JalaliNaT == pd.NaT
        assert JalaliNaT != JalaliTimestamp(1402, 1, 1)

    def test_nat_inequality(self):
        """Test JalaliNaT inequality comparisons."""
        assert JalaliNaT == JalaliNaT
        assert JalaliNaT != JalaliTimestamp(1402, 1, 1)

    def test_nat_comparisons_return_false(self):
        """Test that NaT comparisons (except ==, !=) return False."""
        ts = JalaliTimestamp(1402, 1, 1)
        assert not (JalaliNaT < ts)
        assert not (JalaliNaT > ts)
        assert not (JalaliNaT < JalaliNaT)
        assert not (JalaliNaT > JalaliNaT)
        assert not (JalaliNaT <= ts)
        assert not (JalaliNaT >= ts)

    def test_nat_arithmetic_returns_nat(self):
        """Test that arithmetic with NaT returns NaT."""
        result = JalaliNaT + timedelta(days=1)
        assert result is JalaliNaT

        result = JalaliNaT - timedelta(days=1)
        assert result is JalaliNaT

        result = timedelta(days=1) + JalaliNaT
        assert result is JalaliNaT

    def test_nat_properties_return_nan(self):
        """Test that NaT properties return NaN."""
        assert math.isnan(JalaliNaT.year)
        assert math.isnan(JalaliNaT.month)
        assert math.isnan(JalaliNaT.day)
        assert math.isnan(JalaliNaT.hour)
        assert math.isnan(JalaliNaT.minute)
        assert math.isnan(JalaliNaT.second)
        assert math.isnan(JalaliNaT.microsecond)
        assert math.isnan(JalaliNaT.nanosecond)
        assert math.isnan(JalaliNaT.quarter)
        assert math.isnan(JalaliNaT.dayofweek)
        assert JalaliNaT.tzinfo is None
        assert JalaliNaT.tz is None

    def test_nat_boolean_properties_return_false(self):
        """Test that NaT boolean properties return False."""
        assert JalaliNaT.is_leap_year is False
        assert JalaliNaT.is_month_start is False
        assert JalaliNaT.is_month_end is False
        assert JalaliNaT.is_quarter_start is False
        assert JalaliNaT.is_quarter_end is False
        assert JalaliNaT.is_year_start is False
        assert JalaliNaT.is_year_end is False

    def test_nat_to_gregorian(self):
        """Test NaT conversion to Gregorian returns pd.NaT."""
        assert JalaliNaT.to_gregorian() is pd.NaT

    def test_nat_to_datetime64(self):
        """Test NaT conversion to datetime64 returns NaT."""
        result = JalaliNaT.to_datetime64()
        assert np.isnat(result)

    def test_nat_to_pydatetime(self):
        """Test NaT conversion to pydatetime returns None."""
        assert JalaliNaT.to_pydatetime() is None

    def test_nat_strftime(self):
        """Test NaT strftime returns 'NaT'."""
        assert JalaliNaT.strftime("%Y-%m-%d") == "NaT"

    def test_nat_isoformat(self):
        """Test NaT isoformat returns 'NaT'."""
        assert JalaliNaT.isoformat() == "NaT"

    def test_nat_normalize(self):
        """Test NaT normalize returns NaT."""
        assert JalaliNaT.normalize() is JalaliNaT

    def test_nat_date_time(self):
        """Test NaT date/time accessors."""
        assert JalaliNaT.date() is JalaliNaT
        assert JalaliNaT.time() is None

    def test_nat_replace(self):
        """Test NaT replace returns NaT."""
        assert JalaliNaT.replace(year=1402) is JalaliNaT

    def test_nat_tz_methods(self):
        """Test NaT timezone methods return NaT."""
        assert JalaliNaT.tz_localize("UTC") is JalaliNaT
        assert JalaliNaT.tz_convert("UTC") is JalaliNaT


class TestIsNaJalali:
    """Tests for isna_jalali function."""

    def test_isna_jalali_nat(self):
        """Test isna_jalali with JalaliNaT."""
        assert isna_jalali(JalaliNaT) is True

    def test_isna_jalali_pandas_nat(self):
        """Test isna_jalali with pandas NaT."""
        assert isna_jalali(pd.NaT) is True

    def test_isna_jalali_none(self):
        """Test isna_jalali with None."""
        assert isna_jalali(None) is True

    def test_isna_jalali_timestamp(self):
        """Test isna_jalali with valid timestamp."""
        ts = JalaliTimestamp(1402, 1, 1)
        assert isna_jalali(ts) is False

    def test_isna_jalali_nan(self):
        """Test isna_jalali with float NaN."""
        assert isna_jalali(float("nan")) is True


class TestJalaliTimestampTimezone:
    """Tests for JalaliTimestamp timezone methods."""

    def test_tz_localize(self):
        """Test localizing a tz-naive timestamp."""
        ts = JalaliTimestamp(1402, 6, 15, 10, 30)
        localized = ts.tz_localize("UTC")
        assert localized.tz is not None
        assert str(localized.tz) == "UTC"
        # Date/time components should be unchanged
        assert localized.year == 1402
        assert localized.month == 6
        assert localized.day == 15
        assert localized.hour == 10
        assert localized.minute == 30

    def test_tz_localize_tehran(self):
        """Test localizing to Asia/Tehran timezone."""
        ts = JalaliTimestamp(1402, 6, 15, 10, 30)
        localized = ts.tz_localize("Asia/Tehran")
        assert localized.tz is not None
        assert "Tehran" in str(localized.tz)

    def test_tz_localize_already_aware_raises(self):
        """Test that localizing tz-aware timestamp raises TypeError."""
        ts = JalaliTimestamp(1402, 6, 15, 10, 30)
        localized = ts.tz_localize("UTC")
        with pytest.raises(TypeError, match="Cannot localize tz-aware"):
            localized.tz_localize("Asia/Tehran")

    def test_tz_convert(self):
        """Test converting between timezones."""
        ts = JalaliTimestamp(1402, 6, 15, 10, 30)
        utc_ts = ts.tz_localize("UTC")
        tehran_ts = utc_ts.tz_convert("Asia/Tehran")

        assert tehran_ts.tz is not None
        assert "Tehran" in str(tehran_ts.tz)
        # Tehran is UTC+3:30, so 10:30 UTC = 14:00 Tehran
        assert tehran_ts.hour == 14
        assert tehran_ts.minute == 0

    def test_tz_convert_naive_raises(self):
        """Test that converting tz-naive timestamp raises TypeError."""
        ts = JalaliTimestamp(1402, 6, 15, 10, 30)
        with pytest.raises(TypeError, match="Cannot convert tz-naive"):
            ts.tz_convert("Asia/Tehran")

    def test_tz_localize_none_removes_tz(self):
        """Test that localizing to None removes timezone."""
        ts = JalaliTimestamp(1402, 6, 15, 10, 30)
        localized = ts.tz_localize("UTC")
        # Convert to None timezone (remove tz info)
        naive = localized.tz_convert(None)
        assert naive.tz is None

    def test_roundtrip_tz_conversion(self):
        """Test roundtrip timezone conversion preserves time."""
        ts = JalaliTimestamp(1402, 6, 15, 12, 0)
        utc_ts = ts.tz_localize("UTC")
        tehran_ts = utc_ts.tz_convert("Asia/Tehran")
        back_to_utc = tehran_ts.tz_convert("UTC")

        # Should be back to original UTC time
        assert back_to_utc.hour == 12
        assert back_to_utc.minute == 0
