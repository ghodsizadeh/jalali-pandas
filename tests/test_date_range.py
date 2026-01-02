"""Tests for jalali_date_range function."""

import pytest

from jalali_pandas import JalaliDatetimeIndex, JalaliTimestamp, jalali_date_range
from jalali_pandas.offsets import JalaliMonthEnd


class TestJalaliDateRangeBasic:
    """Basic tests for jalali_date_range."""

    def test_start_and_periods_daily(self):
        """Test with start and periods, daily frequency."""
        idx = jalali_date_range("1402-01-01", periods=5, freq="D")

        assert isinstance(idx, JalaliDatetimeIndex)
        assert len(idx) == 5
        assert idx[0] == JalaliTimestamp(1402, 1, 1)
        assert idx[1] == JalaliTimestamp(1402, 1, 2)
        assert idx[4] == JalaliTimestamp(1402, 1, 5)

    def test_start_and_end_daily(self):
        """Test with start and end, daily frequency."""
        idx = jalali_date_range("1402-01-01", "1402-01-05", freq="D")

        assert len(idx) == 5
        assert idx[0] == JalaliTimestamp(1402, 1, 1)
        assert idx[-1] == JalaliTimestamp(1402, 1, 5)

    def test_end_and_periods_daily(self):
        """Test with end and periods, daily frequency."""
        idx = jalali_date_range(end="1402-01-05", periods=3, freq="D")

        assert len(idx) == 3
        assert idx[-1] == JalaliTimestamp(1402, 1, 5)

    def test_default_frequency_is_daily(self):
        """Test that default frequency is daily."""
        idx = jalali_date_range("1402-01-01", periods=3)

        assert len(idx) == 3
        assert idx[1] == JalaliTimestamp(1402, 1, 2)


class TestJalaliDateRangeFrequencies:
    """Tests for different frequency strings."""

    def test_hourly_frequency(self):
        """Test hourly frequency."""
        idx = jalali_date_range("1402-01-01", periods=3, freq="H")

        assert len(idx) == 3
        assert idx[0].hour == 0
        assert idx[1].hour == 1
        assert idx[2].hour == 2

    def test_jalali_month_end(self):
        """Test Jalali month end frequency."""
        idx = jalali_date_range("1402-01-01", periods=3, freq="JME")

        assert len(idx) == 3
        # First month end should be 1402-01-31
        assert idx[0].day == 31
        assert idx[0].month == 1
        # Second month end should be 1402-02-31
        assert idx[1].day == 31
        assert idx[1].month == 2

    def test_jalali_quarter_end(self):
        """Test Jalali quarter end frequency."""
        idx = jalali_date_range("1402-01-01", periods=4, freq="JQE")

        assert len(idx) == 4
        # Q1 ends on 3rd month (Khordad)
        assert idx[0].month == 3
        # Q2 ends on 6th month (Shahrivar)
        assert idx[1].month == 6

    def test_jalali_year_end(self):
        """Test Jalali year end frequency."""
        idx = jalali_date_range("1400-01-01", periods=3, freq="JYE")

        assert len(idx) == 3
        # All should be month 12 (Esfand)
        assert all(ts.month == 12 for ts in idx)

    def test_with_offset_object(self):
        """Test with JalaliOffset object."""
        idx = jalali_date_range("1402-01-01", periods=3, freq=JalaliMonthEnd())

        assert len(idx) == 3
        assert idx[0].is_month_end

    def test_multiplied_frequency(self):
        """Test multiplied frequency string."""
        idx = jalali_date_range("1402-01-01", periods=3, freq="2D")

        assert len(idx) == 3
        assert idx[0] == JalaliTimestamp(1402, 1, 1)
        assert idx[1] == JalaliTimestamp(1402, 1, 3)
        assert idx[2] == JalaliTimestamp(1402, 1, 5)


class TestJalaliDateRangeParameters:
    """Tests for various parameter combinations."""

    def test_with_name(self):
        """Test with name parameter."""
        idx = jalali_date_range("1402-01-01", periods=3, name="my_dates")

        assert idx._name == "my_dates"

    def test_normalize(self):
        """Test normalize parameter."""
        idx = jalali_date_range(
            JalaliTimestamp(1402, 1, 1, 10, 30, 0),
            periods=3,
            normalize=True,
        )

        assert all(ts.hour == 0 and ts.minute == 0 for ts in idx)

    def test_normalize_with_end(self):
        """Test normalize applies to end date."""
        idx = jalali_date_range(
            "1402-01-01 10:00:00",
            "1402-01-03 22:00:00",
            freq="D",
            normalize=True,
        )

        assert all(ts.hour == 0 for ts in idx)

    def test_inclusive_both(self):
        """Test inclusive='both' (default)."""
        idx = jalali_date_range("1402-01-01", "1402-01-05", freq="D", inclusive="both")

        assert len(idx) == 5
        assert idx[0] == JalaliTimestamp(1402, 1, 1)
        assert idx[-1] == JalaliTimestamp(1402, 1, 5)

    def test_inclusive_left(self):
        """Test inclusive='left'."""
        idx = jalali_date_range("1402-01-01", "1402-01-05", freq="D", inclusive="left")

        assert len(idx) == 4
        assert idx[0] == JalaliTimestamp(1402, 1, 1)
        assert idx[-1] == JalaliTimestamp(1402, 1, 4)

    def test_inclusive_right(self):
        """Test inclusive='right'."""
        idx = jalali_date_range("1402-01-01", "1402-01-05", freq="D", inclusive="right")

        assert len(idx) == 4
        assert idx[0] == JalaliTimestamp(1402, 1, 2)
        assert idx[-1] == JalaliTimestamp(1402, 1, 5)

    def test_inclusive_neither(self):
        """Test inclusive='neither'."""
        idx = jalali_date_range(
            "1402-01-01", "1402-01-05", freq="D", inclusive="neither"
        )

        assert len(idx) == 3
        assert idx[0] == JalaliTimestamp(1402, 1, 2)
        assert idx[-1] == JalaliTimestamp(1402, 1, 4)

    def test_with_jalali_timestamp_start(self):
        """Test with JalaliTimestamp as start."""
        start = JalaliTimestamp(1402, 6, 15)
        idx = jalali_date_range(start, periods=3)

        assert idx[0] == start


class TestJalaliDateRangeValidation:
    """Tests for parameter validation."""

    def test_missing_parameters(self):
        """Test that missing parameters raise ValueError."""
        with pytest.raises(ValueError, match="exactly three must be specified"):
            jalali_date_range("1402-01-01")

    def test_negative_periods(self):
        """Test that negative periods raise ValueError."""
        with pytest.raises(ValueError, match="non-negative"):
            jalali_date_range("1402-01-01", periods=-5)

    def test_unknown_frequency(self):
        """Test that unknown frequency raises ValueError."""
        with pytest.raises(ValueError, match="Unknown frequency"):
            jalali_date_range("1402-01-01", periods=3, freq="INVALID")

    def test_missing_freq_with_all_params(self):
        """Test missing freq raises when start/end/periods are set."""
        with pytest.raises(ValueError, match="freq must be specified"):
            jalali_date_range("1402-01-01", "1402-01-05", periods=3)

    def test_invalid_start_type(self):
        """Test invalid start type raises TypeError."""
        with pytest.raises(TypeError, match="Expected str or JalaliTimestamp"):
            jalali_date_range(123, periods=3)  # type: ignore[arg-type]

    def test_unparseable_start_string(self):
        """Test invalid start string raises ValueError."""
        with pytest.raises(ValueError, match="Cannot parse"):
            jalali_date_range("invalid", periods=2)


class TestJalaliDateRangeEdgeCases:
    """Edge case tests for jalali_date_range."""

    def test_single_period(self):
        """Test with single period."""
        idx = jalali_date_range("1402-01-01", periods=1)

        assert len(idx) == 1
        assert idx[0] == JalaliTimestamp(1402, 1, 1)

    def test_leap_year_boundary(self):
        """Test date range crossing leap year boundary."""
        # 1403 is a leap year
        idx = jalali_date_range("1403-12-28", periods=5, freq="D")

        assert len(idx) == 5
        # Should include 1403-12-30 (leap year has 30 days in Esfand)
        assert idx[2] == JalaliTimestamp(1403, 12, 30)

    def test_month_boundary(self):
        """Test date range crossing month boundary."""
        idx = jalali_date_range("1402-01-30", periods=3, freq="D")

        assert len(idx) == 3
        assert idx[0] == JalaliTimestamp(1402, 1, 30)
        assert idx[1] == JalaliTimestamp(1402, 1, 31)
        assert idx[2] == JalaliTimestamp(1402, 2, 1)

    def test_year_boundary(self):
        """Test date range crossing year boundary."""
        idx = jalali_date_range("1402-12-28", periods=5, freq="D")

        assert len(idx) == 5
        # 1402 is not a leap year, so Esfand has 29 days
        assert idx[1] == JalaliTimestamp(1402, 12, 29)
        assert idx[2] == JalaliTimestamp(1403, 1, 1)

    def test_end_and_periods_with_jalali_offset(self):
        """Test backward generation with Jalali offsets."""
        idx = jalali_date_range(end="1402-03-31", periods=2, freq="JME")

        assert len(idx) == 2
        assert idx[-1].month == 3

    def test_start_and_end_with_jalali_offset(self):
        """Test start/end generation with Jalali offsets."""
        idx = jalali_date_range("1402-01-01", "1402-03-31", freq="JME")

        assert idx[0].is_month_end
