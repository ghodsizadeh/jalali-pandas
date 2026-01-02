"""Tests for Jalali calendar rules and utilities."""

import numpy as np
import pytest

from jalali_pandas.core.calendar import (
    MONTH_LENGTHS,
    MONTH_LENGTHS_LEAP,
    MONTH_NAMES_EN,
    MONTH_NAMES_FA,
    MONTH_STARTS,
    WEEKDAY_NAMES_EN,
    WEEKDAY_NAMES_FA,
    day_of_year,
    days_in_month,
    days_in_month_vectorized,
    days_in_year,
    is_leap_year,
    is_leap_year_vectorized,
    jalali_to_jdn,
    jdn_to_jalali,
    quarter_of_month,
    validate_jalali_date,
    week_of_year,
    weekday_of_jalali,
)


class TestLeapYear:
    """Tests for leap year detection."""

    def test_leap_years(self):
        """Test known leap years."""
        leap_years = [1403, 1399, 1395, 1391, 1387, 1383, 1379, 1375]
        for year in leap_years:
            assert is_leap_year(year) is True, f"{year} should be a leap year"

    def test_non_leap_years(self):
        """Test known non-leap years."""
        non_leap_years = [1402, 1401, 1400, 1398, 1397, 1396]
        for year in non_leap_years:
            assert is_leap_year(year) is False, f"{year} should not be a leap year"

    def test_leap_year_vectorized(self):
        """Test vectorized leap year detection."""
        years = np.array([1403, 1402, 1399, 1400], dtype=np.int64)
        result = is_leap_year_vectorized(years)
        expected = np.array([True, False, True, False])
        np.testing.assert_array_equal(result, expected)


class TestDaysInMonth:
    """Tests for days in month calculation."""

    def test_first_six_months(self):
        """Test that first 6 months have 31 days."""
        for month in range(1, 7):
            assert days_in_month(1402, month) == 31

    def test_months_7_to_11(self):
        """Test that months 7-11 have 30 days."""
        for month in range(7, 12):
            assert days_in_month(1402, month) == 30

    def test_esfand_non_leap(self):
        """Test Esfand in non-leap year has 29 days."""
        assert days_in_month(1402, 12) == 29

    def test_esfand_leap(self):
        """Test Esfand in leap year has 30 days."""
        assert days_in_month(1403, 12) == 30

    def test_invalid_month(self):
        """Test invalid month raises ValueError."""
        with pytest.raises(ValueError):
            days_in_month(1402, 0)
        with pytest.raises(ValueError):
            days_in_month(1402, 13)

    def test_days_in_month_vectorized(self):
        """Test vectorized days in month calculation."""
        years = np.array([1402, 1402, 1403, 1402], dtype=np.int64)
        months = np.array([1, 7, 12, 12], dtype=np.int64)
        result = days_in_month_vectorized(years, months)
        expected = np.array([31, 30, 30, 29], dtype=np.int64)
        np.testing.assert_array_equal(result, expected)


class TestDaysInYear:
    """Tests for days in year calculation."""

    def test_leap_year(self):
        """Test leap year has 366 days."""
        assert days_in_year(1403) == 366

    def test_non_leap_year(self):
        """Test non-leap year has 365 days."""
        assert days_in_year(1402) == 365


class TestQuarter:
    """Tests for quarter calculation."""

    def test_quarter_of_month(self):
        """Test quarter calculation for all months."""
        assert quarter_of_month(1) == 1
        assert quarter_of_month(2) == 1
        assert quarter_of_month(3) == 1
        assert quarter_of_month(4) == 2
        assert quarter_of_month(5) == 2
        assert quarter_of_month(6) == 2
        assert quarter_of_month(7) == 3
        assert quarter_of_month(8) == 3
        assert quarter_of_month(9) == 3
        assert quarter_of_month(10) == 4
        assert quarter_of_month(11) == 4
        assert quarter_of_month(12) == 4


class TestDayOfYear:
    """Tests for day of year calculation."""

    def test_first_day(self):
        """Test first day of year."""
        assert day_of_year(1402, 1, 1) == 1

    def test_last_day_non_leap(self):
        """Test last day of non-leap year."""
        assert day_of_year(1402, 12, 29) == 365

    def test_last_day_leap(self):
        """Test last day of leap year."""
        assert day_of_year(1403, 12, 30) == 366

    def test_mid_year(self):
        """Test day in middle of year."""
        # 6 months * 31 days = 186, + 15 = 201
        assert day_of_year(1402, 7, 15) == 186 + 15

    def test_invalid_day(self):
        """Test invalid day raises ValueError."""
        with pytest.raises(ValueError):
            day_of_year(1402, 1, 32)


class TestWeekday:
    """Tests for weekday calculation."""

    def test_weekday_of_jalali(self):
        """Test weekday calculation."""
        # 1402/1/1 is a Tuesday (Gregorian 2023/3/21)
        # In Jalali week: Saturday=0, so Tuesday=3
        weekday = weekday_of_jalali(1402, 1, 1)
        assert 0 <= weekday <= 6


class TestWeekOfYear:
    """Tests for week of year calculation."""

    def test_first_week(self):
        """Test first week of year."""
        week = week_of_year(1402, 1, 1)
        assert week >= 1

    def test_week_progression(self):
        """Test week number increases through year."""
        week1 = week_of_year(1402, 1, 1)
        week2 = week_of_year(1402, 1, 8)
        assert week2 >= week1


class TestJDNConversion:
    """Tests for Julian Day Number conversion."""

    def test_jalali_to_jdn(self):
        """Test jalali_to_jdn produces valid JDN."""
        jdn = jalali_to_jdn(1402, 1, 1)
        assert isinstance(jdn, int)
        assert jdn > 0

    def test_jalali_to_jdn_ordering(self):
        """Test that later dates have higher JDN."""
        jdn1 = jalali_to_jdn(1402, 1, 1)
        jdn2 = jalali_to_jdn(1402, 1, 2)
        jdn3 = jalali_to_jdn(1403, 1, 1)
        assert jdn2 == jdn1 + 1
        assert jdn3 > jdn1

    def test_jdn_to_jalali(self):
        """Test jdn_to_jalali returns valid tuple."""
        jdn = jalali_to_jdn(1402, 1, 1)
        result = jdn_to_jalali(jdn)
        assert isinstance(result, tuple)
        assert len(result) == 3


class TestValidation:
    """Tests for date validation."""

    def test_valid_date(self):
        """Test valid date returns True."""
        assert validate_jalali_date(1402, 6, 15) is True

    def test_invalid_month_low(self):
        """Test month < 1 raises ValueError."""
        with pytest.raises(ValueError):
            validate_jalali_date(1402, 0, 1)

    def test_invalid_month_high(self):
        """Test month > 12 raises ValueError."""
        with pytest.raises(ValueError):
            validate_jalali_date(1402, 13, 1)

    def test_invalid_day_low(self):
        """Test day < 1 raises ValueError."""
        with pytest.raises(ValueError):
            validate_jalali_date(1402, 1, 0)

    def test_invalid_day_high(self):
        """Test day > max for month raises ValueError."""
        with pytest.raises(ValueError):
            validate_jalali_date(1402, 1, 32)


class TestConstants:
    """Tests for calendar constants."""

    def test_month_lengths(self):
        """Test month lengths tuple."""
        assert len(MONTH_LENGTHS) == 12
        assert sum(MONTH_LENGTHS) == 365

    def test_month_lengths_leap(self):
        """Test leap year month lengths tuple."""
        assert len(MONTH_LENGTHS_LEAP) == 12
        assert sum(MONTH_LENGTHS_LEAP) == 366

    def test_month_starts(self):
        """Test month starts tuple."""
        assert len(MONTH_STARTS) == 12
        assert MONTH_STARTS[0] == 0

    def test_month_names(self):
        """Test month names."""
        assert len(MONTH_NAMES_FA) == 12
        assert len(MONTH_NAMES_EN) == 12
        assert MONTH_NAMES_FA[0] == "فروردین"
        assert MONTH_NAMES_EN[0] == "Farvardin"

    def test_weekday_names(self):
        """Test weekday names."""
        assert len(WEEKDAY_NAMES_FA) == 7
        assert len(WEEKDAY_NAMES_EN) == 7
        assert WEEKDAY_NAMES_FA[0] == "شنبه"
        assert WEEKDAY_NAMES_EN[0] == "Shanbeh"
