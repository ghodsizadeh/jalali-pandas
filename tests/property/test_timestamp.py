"""Property-based tests for JalaliTimestamp."""

from __future__ import annotations

from datetime import timedelta

import pandas as pd
from hypothesis import given, settings
from hypothesis import strategies as st

from jalali_pandas import JalaliTimestamp, to_gregorian_datetime, to_jalali_datetime
from jalali_pandas.core.calendar import days_in_month

from .strategies import jalali_timestamps, jalali_timestamps_midnight


class TestTimestampConversionProperties:
    """Property-based tests for timestamp conversions."""

    @settings(max_examples=100)
    @given(jalali_timestamps())
    def test_gregorian_roundtrip(self, ts: JalaliTimestamp) -> None:
        """Converting to Gregorian and back preserves the timestamp."""
        gregorian = ts.to_gregorian()
        restored = JalaliTimestamp.from_gregorian(gregorian)

        assert restored.year == ts.year
        assert restored.month == ts.month
        assert restored.day == ts.day
        assert restored.hour == ts.hour
        assert restored.minute == ts.minute
        assert restored.second == ts.second
        assert restored.microsecond == ts.microsecond

    @settings(max_examples=100)
    @given(jalali_timestamps())
    def test_to_jalali_to_gregorian_roundtrip(self, ts: JalaliTimestamp) -> None:
        """to_jalali_datetime and to_gregorian_datetime are inverses."""
        gregorian = to_gregorian_datetime(ts)
        restored = to_jalali_datetime(gregorian)

        assert restored == ts

    @settings(max_examples=100)
    @given(jalali_timestamps_midnight())
    def test_string_roundtrip(self, ts: JalaliTimestamp) -> None:
        """String formatting and parsing preserves date components."""
        date_str = ts.strftime("%Y-%m-%d")
        parsed = to_jalali_datetime(date_str)

        assert parsed.year == ts.year
        assert parsed.month == ts.month
        assert parsed.day == ts.day


class TestTimestampArithmeticProperties:
    """Property-based tests for timestamp arithmetic."""

    @settings(max_examples=100)
    @given(jalali_timestamps(), st.integers(min_value=-1000, max_value=1000))
    def test_add_subtract_days_inverse(self, ts: JalaliTimestamp, days: int) -> None:
        """Adding and subtracting the same timedelta is identity."""
        delta = timedelta(days=days)
        result = ts + delta - delta

        assert result.year == ts.year
        assert result.month == ts.month
        assert result.day == ts.day
        assert result.hour == ts.hour
        assert result.minute == ts.minute
        assert result.second == ts.second

    @settings(max_examples=100)
    @given(jalali_timestamps(), st.integers(min_value=1, max_value=1000))
    def test_add_positive_days_increases(self, ts: JalaliTimestamp, days: int) -> None:
        """Adding positive days results in a later timestamp."""
        delta = timedelta(days=days)
        result = ts + delta
        assert result > ts

    @settings(max_examples=100)
    @given(jalali_timestamps(), st.integers(min_value=1, max_value=1000))
    def test_subtract_positive_days_decreases(
        self, ts: JalaliTimestamp, days: int
    ) -> None:
        """Subtracting positive days results in an earlier timestamp."""
        delta = timedelta(days=days)
        result = ts - delta
        assert result < ts

    @settings(max_examples=100)
    @given(jalali_timestamps(), jalali_timestamps())
    def test_subtraction_gives_timedelta(
        self, ts1: JalaliTimestamp, ts2: JalaliTimestamp
    ) -> None:
        """Subtracting two timestamps gives a Timedelta."""
        diff = ts1 - ts2
        assert isinstance(diff, pd.Timedelta)

    @settings(max_examples=100)
    @given(jalali_timestamps(), jalali_timestamps())
    def test_subtraction_and_addition_inverse(
        self, ts1: JalaliTimestamp, ts2: JalaliTimestamp
    ) -> None:
        """ts1 - ts2 + ts2 == ts1 (approximately, due to precision)."""
        diff = ts1 - ts2
        restored = ts2 + diff

        assert restored.year == ts1.year
        assert restored.month == ts1.month
        assert restored.day == ts1.day
        assert restored.hour == ts1.hour
        assert restored.minute == ts1.minute
        assert restored.second == ts1.second


class TestTimestampComparisonProperties:
    """Property-based tests for timestamp comparisons."""

    @settings(max_examples=100)
    @given(jalali_timestamps())
    def test_equality_reflexive(self, ts: JalaliTimestamp) -> None:
        """A timestamp equals itself."""
        assert ts == ts

    @settings(max_examples=100)
    @given(jalali_timestamps(), jalali_timestamps())
    def test_equality_symmetric(
        self, ts1: JalaliTimestamp, ts2: JalaliTimestamp
    ) -> None:
        """Equality is symmetric."""
        assert (ts1 == ts2) == (ts2 == ts1)

    @settings(max_examples=100)
    @given(jalali_timestamps(), jalali_timestamps())
    def test_comparison_trichotomy(
        self, ts1: JalaliTimestamp, ts2: JalaliTimestamp
    ) -> None:
        """Exactly one of <, ==, > holds."""
        lt = ts1 < ts2
        eq = ts1 == ts2
        gt = ts1 > ts2
        assert sum([lt, eq, gt]) == 1

    @settings(max_examples=100)
    @given(jalali_timestamps(), jalali_timestamps())
    def test_le_ge_consistency(
        self, ts1: JalaliTimestamp, ts2: JalaliTimestamp
    ) -> None:
        """<= and >= are consistent with < and ==."""
        assert (ts1 <= ts2) == (ts1 < ts2 or ts1 == ts2)
        assert (ts1 >= ts2) == (ts1 > ts2 or ts1 == ts2)

    @settings(max_examples=100)
    @given(jalali_timestamps())
    def test_hash_consistency(self, ts: JalaliTimestamp) -> None:
        """Equal timestamps have equal hashes."""
        ts_copy = JalaliTimestamp(
            ts.year,
            ts.month,
            ts.day,
            ts.hour,
            ts.minute,
            ts.second,
            ts.microsecond,
            ts.nanosecond,
        )
        assert ts == ts_copy
        assert hash(ts) == hash(ts_copy)


class TestTimestampPropertiesInvariants:
    """Property-based tests for timestamp derived properties."""

    @settings(max_examples=100)
    @given(jalali_timestamps())
    def test_quarter_range(self, ts: JalaliTimestamp) -> None:
        """Quarter is always 1-4."""
        assert 1 <= ts.quarter <= 4

    @settings(max_examples=100)
    @given(jalali_timestamps())
    def test_quarter_month_consistency(self, ts: JalaliTimestamp) -> None:
        """Quarter matches month range."""
        if ts.month <= 3:
            assert ts.quarter == 1
        elif ts.month <= 6:
            assert ts.quarter == 2
        elif ts.month <= 9:
            assert ts.quarter == 3
        else:
            assert ts.quarter == 4

    @settings(max_examples=100)
    @given(jalali_timestamps())
    def test_dayofweek_range(self, ts: JalaliTimestamp) -> None:
        """Day of week is always 0-6."""
        assert 0 <= ts.dayofweek <= 6
        assert ts.weekday == ts.dayofweek

    @settings(max_examples=100)
    @given(jalali_timestamps())
    def test_dayofyear_range(self, ts: JalaliTimestamp) -> None:
        """Day of year is 1-365 or 1-366 for leap years."""
        max_doy = 366 if ts.is_leap_year else 365
        assert 1 <= ts.dayofyear <= max_doy

    @settings(max_examples=100)
    @given(jalali_timestamps())
    def test_week_range(self, ts: JalaliTimestamp) -> None:
        """Week of year is 1-53."""
        assert 1 <= ts.week <= 53
        assert ts.weekofyear == ts.week

    @settings(max_examples=100)
    @given(jalali_timestamps())
    def test_days_in_month_consistency(self, ts: JalaliTimestamp) -> None:
        """days_in_month property matches calendar function."""
        assert ts.days_in_month == days_in_month(ts.year, ts.month)
        assert ts.daysinmonth == ts.days_in_month

    @settings(max_examples=100)
    @given(jalali_timestamps())
    def test_is_month_start_consistency(self, ts: JalaliTimestamp) -> None:
        """is_month_start is True iff day == 1."""
        assert ts.is_month_start == (ts.day == 1)

    @settings(max_examples=100)
    @given(jalali_timestamps())
    def test_is_month_end_consistency(self, ts: JalaliTimestamp) -> None:
        """is_month_end is True iff day == days_in_month."""
        assert ts.is_month_end == (ts.day == ts.days_in_month)

    @settings(max_examples=100)
    @given(jalali_timestamps())
    def test_is_year_start_consistency(self, ts: JalaliTimestamp) -> None:
        """is_year_start is True iff month == 1 and day == 1."""
        assert ts.is_year_start == (ts.month == 1 and ts.day == 1)

    @settings(max_examples=100)
    @given(jalali_timestamps())
    def test_is_year_end_consistency(self, ts: JalaliTimestamp) -> None:
        """is_year_end is True iff month == 12 and day == last day."""
        expected = ts.month == 12 and ts.day == ts.days_in_month
        assert ts.is_year_end == expected


class TestTimestampReplaceProperties:
    """Property-based tests for timestamp replace method."""

    @settings(max_examples=100)
    @given(jalali_timestamps())
    def test_replace_no_args_identity(self, ts: JalaliTimestamp) -> None:
        """Replace with no arguments returns equal timestamp."""
        replaced = ts.replace()
        assert replaced == ts

    @settings(max_examples=100)
    @given(jalali_timestamps(), st.integers(min_value=0, max_value=23))
    def test_replace_hour(self, ts: JalaliTimestamp, new_hour: int) -> None:
        """Replace hour preserves other components."""
        replaced = ts.replace(hour=new_hour)
        assert replaced.year == ts.year
        assert replaced.month == ts.month
        assert replaced.day == ts.day
        assert replaced.hour == new_hour
        assert replaced.minute == ts.minute
        assert replaced.second == ts.second

    @settings(max_examples=100)
    @given(jalali_timestamps())
    def test_normalize_sets_time_to_midnight(self, ts: JalaliTimestamp) -> None:
        """Normalize sets time components to zero."""
        normalized = ts.normalize()
        assert normalized.year == ts.year
        assert normalized.month == ts.month
        assert normalized.day == ts.day
        assert normalized.hour == 0
        assert normalized.minute == 0
        assert normalized.second == 0
        assert normalized.microsecond == 0
        assert normalized.nanosecond == 0

    @settings(max_examples=100)
    @given(jalali_timestamps())
    def test_date_equals_normalize(self, ts: JalaliTimestamp) -> None:
        """date() method returns same as normalize()."""
        assert ts.date() == ts.normalize()


class TestTimestampStringProperties:
    """Property-based tests for timestamp string methods."""

    @settings(max_examples=100)
    @given(jalali_timestamps())
    def test_isoformat_parseable(self, ts: JalaliTimestamp) -> None:
        """isoformat output contains expected components."""
        iso = ts.isoformat()
        assert f"{ts.year:04d}" in iso
        assert f"{ts.month:02d}" in iso
        assert f"{ts.day:02d}" in iso

    @settings(max_examples=100)
    @given(jalali_timestamps())
    def test_str_contains_date_and_time(self, ts: JalaliTimestamp) -> None:
        """String representation contains date and time."""
        s = str(ts)
        assert f"{ts.year:04d}" in s
        assert f"{ts.hour:02d}" in s

    @settings(max_examples=100)
    @given(jalali_timestamps())
    def test_repr_contains_class_name(self, ts: JalaliTimestamp) -> None:
        """Repr contains class name."""
        r = repr(ts)
        assert "JalaliTimestamp" in r
