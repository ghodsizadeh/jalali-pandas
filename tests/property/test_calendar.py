"""Property-based tests for Jalali calendar functions."""

from __future__ import annotations

from hypothesis import given, settings
from hypothesis import strategies as st

from jalali_pandas.core.calendar import (
    days_in_month,
    days_in_year,
    is_leap_year,
    jalali_to_jdn,
    jdn_to_jalali,
    quarter_of_month,
    validate_jalali_date,
    week_of_year,
    weekday_of_jalali,
)

from .strategies import jalali_dates, jalali_months, jalali_years


class TestLeapYearProperties:
    """Property-based tests for leap year functions."""

    @settings(max_examples=200)
    @given(jalali_years())
    def test_leap_year_days_in_year_consistency(self, year: int) -> None:
        """Leap years have 366 days, non-leap years have 365."""
        if is_leap_year(year):
            assert days_in_year(year) == 366
        else:
            assert days_in_year(year) == 365

    @settings(max_examples=200)
    @given(jalali_years())
    def test_leap_year_esfand_days(self, year: int) -> None:
        """Esfand (month 12) has 30 days in leap years, 29 otherwise."""
        if is_leap_year(year):
            assert days_in_month(year, 12) == 30
        else:
            assert days_in_month(year, 12) == 29

    @settings(max_examples=100)
    @given(jalali_years())
    def test_leap_year_33_cycle(self, year: int) -> None:
        """Leap years follow the 33-year cycle pattern."""
        remainder = year % 33
        expected_leap_remainders = (1, 5, 9, 13, 17, 22, 26, 30)
        assert is_leap_year(year) == (remainder in expected_leap_remainders)


class TestDaysInMonthProperties:
    """Property-based tests for days_in_month function."""

    @settings(max_examples=200)
    @given(jalali_years(), jalali_months())
    def test_days_in_month_range(self, year: int, month: int) -> None:
        """Days in month is always between 29 and 31."""
        days = days_in_month(year, month)
        assert 29 <= days <= 31

    @settings(max_examples=200)
    @given(jalali_years())
    def test_first_six_months_have_31_days(self, year: int) -> None:
        """First 6 months always have 31 days."""
        for month in range(1, 7):
            assert days_in_month(year, month) == 31

    @settings(max_examples=200)
    @given(jalali_years())
    def test_months_7_to_11_have_30_days(self, year: int) -> None:
        """Months 7-11 always have 30 days."""
        for month in range(7, 12):
            assert days_in_month(year, month) == 30

    @settings(max_examples=200)
    @given(jalali_years())
    def test_total_days_in_year(self, year: int) -> None:
        """Sum of days in all months equals days_in_year."""
        total = sum(days_in_month(year, m) for m in range(1, 13))
        assert total == days_in_year(year)


class TestJDNConversionProperties:
    """Property-based tests for Julian Day Number conversions."""

    @settings(max_examples=200)
    @given(jalali_dates())
    def test_jdn_roundtrip(self, date: tuple[int, int, int]) -> None:
        """Converting to JDN and back preserves the date."""
        year, month, day = date
        jdn = jalali_to_jdn(year, month, day)
        restored = jdn_to_jalali(jdn)
        assert restored == (year, month, day)

    @settings(max_examples=200)
    @given(jalali_dates(), jalali_dates())
    def test_jdn_ordering(
        self, date1: tuple[int, int, int], date2: tuple[int, int, int]
    ) -> None:
        """JDN ordering matches date ordering."""
        y1, m1, d1 = date1
        y2, m2, d2 = date2
        jdn1 = jalali_to_jdn(y1, m1, d1)
        jdn2 = jalali_to_jdn(y2, m2, d2)

        if (y1, m1, d1) < (y2, m2, d2):
            assert jdn1 < jdn2
        elif (y1, m1, d1) > (y2, m2, d2):
            assert jdn1 > jdn2
        else:
            assert jdn1 == jdn2

    @settings(max_examples=200)
    @given(jalali_dates())
    def test_consecutive_days_jdn_differ_by_one(
        self, date: tuple[int, int, int]
    ) -> None:
        """Consecutive days have JDN differing by 1."""
        year, month, day = date
        jdn = jalali_to_jdn(year, month, day)

        # Get next day
        max_day = days_in_month(year, month)
        if day < max_day:
            next_year, next_month, next_day = year, month, day + 1
        elif month < 12:
            next_year, next_month, next_day = year, month + 1, 1
        else:
            next_year, next_month, next_day = year + 1, 1, 1

        next_jdn = jalali_to_jdn(next_year, next_month, next_day)
        assert next_jdn == jdn + 1


class TestWeekdayProperties:
    """Property-based tests for weekday functions."""

    @settings(max_examples=200)
    @given(jalali_dates())
    def test_weekday_range(self, date: tuple[int, int, int]) -> None:
        """Weekday is always 0-6."""
        year, month, day = date
        weekday = weekday_of_jalali(year, month, day)
        assert 0 <= weekday <= 6

    @settings(max_examples=200)
    @given(jalali_dates())
    def test_weekday_7_day_cycle(self, date: tuple[int, int, int]) -> None:
        """Adding 7 days returns to the same weekday."""
        year, month, day = date
        weekday = weekday_of_jalali(year, month, day)

        # Calculate date 7 days later using JDN
        jdn = jalali_to_jdn(year, month, day)
        future_year, future_month, future_day = jdn_to_jalali(jdn + 7)
        future_weekday = weekday_of_jalali(future_year, future_month, future_day)

        assert weekday == future_weekday


class TestWeekOfYearProperties:
    """Property-based tests for week_of_year function."""

    @settings(max_examples=200)
    @given(jalali_dates())
    def test_week_of_year_range(self, date: tuple[int, int, int]) -> None:
        """Week of year is always 1-53."""
        year, month, day = date
        week = week_of_year(year, month, day)
        assert 1 <= week <= 53


class TestQuarterProperties:
    """Property-based tests for quarter functions."""

    @settings(max_examples=50)
    @given(jalali_months())
    def test_quarter_range(self, month: int) -> None:
        """Quarter is always 1-4."""
        quarter = quarter_of_month(month)
        assert 1 <= quarter <= 4

    @settings(max_examples=50)
    @given(jalali_months())
    def test_quarter_mapping(self, month: int) -> None:
        """Months 1-3 are Q1, 4-6 are Q2, 7-9 are Q3, 10-12 are Q4."""
        quarter = quarter_of_month(month)
        if month <= 3:
            assert quarter == 1
        elif month <= 6:
            assert quarter == 2
        elif month <= 9:
            assert quarter == 3
        else:
            assert quarter == 4


class TestValidateDateProperties:
    """Property-based tests for date validation."""

    @settings(max_examples=200)
    @given(jalali_dates())
    def test_valid_dates_pass_validation(self, date: tuple[int, int, int]) -> None:
        """All generated valid dates pass validation."""
        year, month, day = date
        assert validate_jalali_date(year, month, day) is True

    @settings(max_examples=100)
    @given(jalali_years(), st.integers(min_value=13, max_value=100))
    def test_invalid_month_fails(self, year: int, month: int) -> None:
        """Invalid months fail validation."""
        import pytest

        with pytest.raises(ValueError, match="Month must be 1-12"):
            validate_jalali_date(year, month, 1)

    @settings(max_examples=100)
    @given(jalali_years(), jalali_months())
    def test_day_exceeding_month_fails(self, year: int, month: int) -> None:
        """Days exceeding month length fail validation."""
        import pytest

        max_day = days_in_month(year, month)
        with pytest.raises(ValueError, match="Day must be"):
            validate_jalali_date(year, month, max_day + 1)
