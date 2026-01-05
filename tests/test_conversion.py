"""Tests for conversion module."""

from __future__ import annotations

import numpy as np
import pandas as pd

from jalali_pandas.core.conversion import (
    datetime64_to_jalali,
    gregorian_to_jalali_scalar,
    gregorian_to_jalali_vectorized,
    jalali_to_datetime64,
    jalali_to_gregorian_scalar,
    jalali_to_gregorian_vectorized,
)


class TestScalarConversions:
    """Tests for scalar conversion functions."""

    def test_jalali_to_gregorian_nowruz(self):
        """Test conversion of Nowruz (1 Farvardin)."""
        # 1402/1/1 = 2023/3/21
        g_year, g_month, g_day = jalali_to_gregorian_scalar(1402, 1, 1)
        assert g_year == 2023
        assert g_month == 3
        assert g_day == 21

    def test_jalali_to_gregorian_various_dates(self):
        """Test conversion of various dates."""
        # 1402/6/15 = 2023/9/6
        g_year, g_month, g_day = jalali_to_gregorian_scalar(1402, 6, 15)
        assert g_year == 2023
        assert g_month == 9
        assert g_day == 6

        # 1400/1/1 = 2021/3/21
        g_year, g_month, g_day = jalali_to_gregorian_scalar(1400, 1, 1)
        assert g_year == 2021
        assert g_month == 3
        assert g_day == 21

    def test_gregorian_to_jalali_nowruz(self):
        """Test conversion to Nowruz."""
        # 2023/3/21 = 1402/1/1
        j_year, j_month, j_day = gregorian_to_jalali_scalar(2023, 3, 21)
        assert j_year == 1402
        assert j_month == 1
        assert j_day == 1

    def test_gregorian_to_jalali_various_dates(self):
        """Test conversion of various Gregorian dates."""
        # 2023/9/6 = 1402/6/15
        j_year, j_month, j_day = gregorian_to_jalali_scalar(2023, 9, 6)
        assert j_year == 1402
        assert j_month == 6
        assert j_day == 15

    def test_roundtrip_conversion(self):
        """Test that Jalali -> Gregorian -> Jalali preserves date."""
        original = (1402, 6, 15)
        g_date = jalali_to_gregorian_scalar(*original)
        restored = gregorian_to_jalali_scalar(*g_date)
        assert restored == original

    def test_roundtrip_gregorian(self):
        """Test that Gregorian -> Jalali -> Gregorian preserves date."""
        original = (2023, 9, 6)
        j_date = gregorian_to_jalali_scalar(*original)
        restored = jalali_to_gregorian_scalar(*j_date)
        assert restored == original

    def test_leap_year_esfand(self):
        """Test conversion of leap year Esfand 30."""
        # 1403 is a leap year, Esfand 30 exists
        g_year, g_month, g_day = jalali_to_gregorian_scalar(1403, 12, 30)
        # Should be March 20, 2025
        assert g_year == 2025
        assert g_month == 3
        assert g_day == 20


class TestVectorizedConversions:
    """Tests for vectorized conversion functions."""

    def test_jalali_to_gregorian_vectorized(self):
        """Test vectorized Jalali to Gregorian conversion."""
        years = np.array([1402, 1402, 1403], dtype=np.int64)
        months = np.array([1, 6, 12], dtype=np.int64)
        days = np.array([1, 15, 30], dtype=np.int64)

        g_years, g_months, g_days = jalali_to_gregorian_vectorized(years, months, days)

        # 1402/1/1 = 2023/3/21
        assert g_years[0] == 2023
        assert g_months[0] == 3
        assert g_days[0] == 21

        # 1402/6/15 = 2023/9/6
        assert g_years[1] == 2023
        assert g_months[1] == 9
        assert g_days[1] == 6

    def test_gregorian_to_jalali_vectorized(self):
        """Test vectorized Gregorian to Jalali conversion."""
        years = np.array([2023, 2023, 2025], dtype=np.int64)
        months = np.array([3, 9, 3], dtype=np.int64)
        days = np.array([21, 6, 20], dtype=np.int64)

        j_years, j_months, j_days = gregorian_to_jalali_vectorized(years, months, days)

        # 2023/3/21 = 1402/1/1
        assert j_years[0] == 1402
        assert j_months[0] == 1
        assert j_days[0] == 1

        # 2023/9/6 = 1402/6/15
        assert j_years[1] == 1402
        assert j_months[1] == 6
        assert j_days[1] == 15

    def test_vectorized_roundtrip(self):
        """Test vectorized roundtrip conversion."""
        years = np.array([1400, 1401, 1402, 1403], dtype=np.int64)
        months = np.array([1, 6, 12, 7], dtype=np.int64)
        days = np.array([1, 15, 29, 30], dtype=np.int64)

        g_years, g_months, g_days = jalali_to_gregorian_vectorized(years, months, days)
        j_years, j_months, j_days = gregorian_to_jalali_vectorized(
            g_years, g_months, g_days
        )

        np.testing.assert_array_equal(j_years, years)
        np.testing.assert_array_equal(j_months, months)
        np.testing.assert_array_equal(j_days, days)


class TestDatetime64Conversions:
    """Tests for datetime64 conversion functions."""

    def test_datetime64_to_jalali(self):
        """Test conversion from datetime64 to Jalali."""
        dt = np.array(["2023-03-21", "2023-09-06"], dtype="datetime64[D]")
        j_years, j_months, j_days = datetime64_to_jalali(dt)

        assert j_years[0] == 1402
        assert j_months[0] == 1
        assert j_days[0] == 1

        assert j_years[1] == 1402
        assert j_months[1] == 6
        assert j_days[1] == 15

    def test_jalali_to_datetime64(self):
        """Test conversion from Jalali to datetime64."""
        years = np.array([1402, 1402], dtype=np.int64)
        months = np.array([1, 6], dtype=np.int64)
        days = np.array([1, 15], dtype=np.int64)

        dt = jalali_to_datetime64(years, months, days)

        # Convert to pandas for easier comparison
        dti = pd.DatetimeIndex(dt)
        assert dti[0].year == 2023
        assert dti[0].month == 3
        assert dti[0].day == 21

        assert dti[1].year == 2023
        assert dti[1].month == 9
        assert dti[1].day == 6

    def test_jalali_to_datetime64_with_time(self):
        """Test conversion with time components."""
        years = np.array([1402], dtype=np.int64)
        months = np.array([6], dtype=np.int64)
        days = np.array([15], dtype=np.int64)
        hours = np.array([10], dtype=np.int64)
        minutes = np.array([30], dtype=np.int64)
        seconds = np.array([45], dtype=np.int64)

        dt = jalali_to_datetime64(years, months, days, hours, minutes, seconds)

        dti = pd.DatetimeIndex(dt)
        assert dti[0].hour == 10
        assert dti[0].minute == 30
        assert dti[0].second == 45

    def test_datetime64_roundtrip(self):
        """Test roundtrip conversion through datetime64."""
        original_dt = np.array(
            ["2023-03-21T10:30:00", "2023-09-06T15:45:30"],
            dtype="datetime64[s]",
        )

        j_years, j_months, j_days = datetime64_to_jalali(original_dt)

        # Extract time components from original
        dti = pd.DatetimeIndex(original_dt)
        hours = dti.hour.to_numpy().astype(np.int64)
        minutes = dti.minute.to_numpy().astype(np.int64)
        seconds = dti.second.to_numpy().astype(np.int64)

        restored_dt = jalali_to_datetime64(
            j_years, j_months, j_days, hours, minutes, seconds
        )

        # Compare as pandas DatetimeIndex
        original_dti = pd.DatetimeIndex(original_dt)
        restored_dti = pd.DatetimeIndex(restored_dt)

        assert original_dti[0] == restored_dti[0]
        assert original_dti[1] == restored_dti[1]
