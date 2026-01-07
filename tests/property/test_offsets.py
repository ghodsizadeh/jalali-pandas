"""Property-based tests for Jalali calendar offsets."""

from __future__ import annotations

from hypothesis import assume, given, settings
from hypothesis import strategies as st

from jalali_pandas import JalaliTimestamp
from jalali_pandas.core.calendar import days_in_month, is_leap_year
from jalali_pandas.offsets import (
    JalaliMonthBegin,
    JalaliMonthEnd,
    JalaliQuarterBegin,
    JalaliQuarterEnd,
    JalaliYearBegin,
    JalaliYearEnd,
)

from .strategies import jalali_timestamps, small_offset_multipliers


class TestMonthOffsetProperties:
    """Property-based tests for month offset invariants."""

    @settings(max_examples=100)
    @given(jalali_timestamps(), small_offset_multipliers())
    def test_month_begin_lands_on_day_1(self, ts: JalaliTimestamp, n: int) -> None:
        """JalaliMonthBegin always lands on day 1."""
        offset = JalaliMonthBegin(n=n)
        result = offset + ts
        assert result.day == 1

    @settings(max_examples=100)
    @given(jalali_timestamps(), small_offset_multipliers())
    def test_month_end_lands_on_last_day(self, ts: JalaliTimestamp, n: int) -> None:
        """JalaliMonthEnd always lands on the last day of the month."""
        offset = JalaliMonthEnd(n=n)
        result = offset + ts
        expected_last_day = days_in_month(result.year, result.month)
        assert result.day == expected_last_day

    @settings(max_examples=100)
    @given(jalali_timestamps(), small_offset_multipliers())
    def test_month_begin_add_subtract_inverse(
        self, ts: JalaliTimestamp, n: int
    ) -> None:
        """Adding and subtracting same month offset returns to same month."""
        offset = JalaliMonthBegin(n=n)
        neg_offset = JalaliMonthBegin(n=-n)
        result = neg_offset + (offset + ts)
        # Should return to same year/month, day is always 1
        assert result.year == ts.year
        assert result.month == ts.month
        assert result.day == 1

    @settings(max_examples=100)
    @given(jalali_timestamps())
    def test_month_begin_is_on_offset(self, ts: JalaliTimestamp) -> None:
        """is_on_offset correctly identifies month starts."""
        offset = JalaliMonthBegin()
        assert offset.is_on_offset(ts) == (ts.day == 1)

    @settings(max_examples=100)
    @given(jalali_timestamps())
    def test_month_end_is_on_offset(self, ts: JalaliTimestamp) -> None:
        """is_on_offset correctly identifies month ends."""
        offset = JalaliMonthEnd()
        expected = ts.day == days_in_month(ts.year, ts.month)
        assert offset.is_on_offset(ts) == expected

    @settings(max_examples=100)
    @given(jalali_timestamps())
    def test_month_begin_rollforward_idempotent(self, ts: JalaliTimestamp) -> None:
        """Rolling forward twice is same as rolling forward once."""
        offset = JalaliMonthBegin()
        once = offset.rollforward(ts)
        twice = offset.rollforward(once)
        assert once == twice

    @settings(max_examples=100)
    @given(jalali_timestamps())
    def test_month_end_rollforward_idempotent(self, ts: JalaliTimestamp) -> None:
        """Rolling forward twice is same as rolling forward once."""
        offset = JalaliMonthEnd()
        once = offset.rollforward(ts)
        twice = offset.rollforward(once)
        assert once == twice

    @settings(max_examples=100)
    @given(jalali_timestamps())
    def test_month_begin_rollback_idempotent(self, ts: JalaliTimestamp) -> None:
        """Rolling back twice is same as rolling back once."""
        offset = JalaliMonthBegin()
        once = offset.rollback(ts)
        twice = offset.rollback(once)
        assert once == twice

    @settings(max_examples=100)
    @given(jalali_timestamps())
    def test_month_end_rollback_idempotent(self, ts: JalaliTimestamp) -> None:
        """Rolling back twice is same as rolling back once."""
        offset = JalaliMonthEnd()
        once = offset.rollback(ts)
        twice = offset.rollback(once)
        assert once == twice


class TestQuarterOffsetProperties:
    """Property-based tests for quarter offset invariants."""

    @settings(max_examples=100)
    @given(jalali_timestamps(), small_offset_multipliers())
    def test_quarter_begin_lands_on_quarter_start(
        self, ts: JalaliTimestamp, n: int
    ) -> None:
        """JalaliQuarterBegin lands on month 1, 4, 7, or 10, day 1."""
        offset = JalaliQuarterBegin(n=n)
        result = offset + ts
        assert result.month in (1, 4, 7, 10)
        assert result.day == 1

    @settings(max_examples=100)
    @given(jalali_timestamps(), small_offset_multipliers())
    def test_quarter_end_lands_on_quarter_end(
        self, ts: JalaliTimestamp, n: int
    ) -> None:
        """JalaliQuarterEnd lands on month 3, 6, 9, or 12, last day."""
        offset = JalaliQuarterEnd(n=n)
        result = offset + ts
        assert result.month in (3, 6, 9, 12)
        expected_last_day = days_in_month(result.year, result.month)
        assert result.day == expected_last_day

    @settings(max_examples=100)
    @given(jalali_timestamps())
    def test_quarter_begin_is_on_offset(self, ts: JalaliTimestamp) -> None:
        """is_on_offset correctly identifies quarter starts."""
        offset = JalaliQuarterBegin()
        expected = ts.month in (1, 4, 7, 10) and ts.day == 1
        assert offset.is_on_offset(ts) == expected

    @settings(max_examples=100)
    @given(jalali_timestamps())
    def test_quarter_end_is_on_offset(self, ts: JalaliTimestamp) -> None:
        """is_on_offset correctly identifies quarter ends."""
        offset = JalaliQuarterEnd()
        is_quarter_end_month = ts.month in (3, 6, 9, 12)
        is_last_day = ts.day == days_in_month(ts.year, ts.month)
        expected = is_quarter_end_month and is_last_day
        assert offset.is_on_offset(ts) == expected

    @settings(max_examples=100)
    @given(jalali_timestamps())
    def test_quarter_begin_rollforward_idempotent(self, ts: JalaliTimestamp) -> None:
        """Rolling forward twice is same as rolling forward once."""
        offset = JalaliQuarterBegin()
        once = offset.rollforward(ts)
        twice = offset.rollforward(once)
        assert once == twice

    @settings(max_examples=100)
    @given(jalali_timestamps())
    def test_quarter_end_rollforward_idempotent(self, ts: JalaliTimestamp) -> None:
        """Rolling forward twice is same as rolling forward once."""
        offset = JalaliQuarterEnd()
        once = offset.rollforward(ts)
        twice = offset.rollforward(once)
        assert once == twice


class TestYearOffsetProperties:
    """Property-based tests for year offset invariants."""

    @settings(max_examples=100)
    @given(jalali_timestamps(), small_offset_multipliers())
    def test_year_begin_lands_on_nowruz(self, ts: JalaliTimestamp, n: int) -> None:
        """JalaliYearBegin always lands on 1 Farvardin."""
        offset = JalaliYearBegin(n=n)
        result = offset + ts
        assert result.month == 1
        assert result.day == 1

    @settings(max_examples=100)
    @given(jalali_timestamps(), small_offset_multipliers())
    def test_year_end_lands_on_last_day_of_esfand(
        self, ts: JalaliTimestamp, n: int
    ) -> None:
        """JalaliYearEnd always lands on last day of Esfand."""
        offset = JalaliYearEnd(n=n)
        result = offset + ts
        assert result.month == 12
        expected_last_day = 30 if is_leap_year(result.year) else 29
        assert result.day == expected_last_day

    @settings(max_examples=100)
    @given(jalali_timestamps(), small_offset_multipliers())
    def test_year_begin_add_n_years(self, ts: JalaliTimestamp, n: int) -> None:
        """Adding n years via YearBegin changes year by n."""
        offset = JalaliYearBegin(n=n)
        result = offset + ts
        assert result.year == ts.year + n

    @settings(max_examples=100)
    @given(jalali_timestamps(), small_offset_multipliers())
    def test_year_end_add_n_years(self, ts: JalaliTimestamp, n: int) -> None:
        """Adding n years via YearEnd changes year by n."""
        offset = JalaliYearEnd(n=n)
        result = offset + ts
        assert result.year == ts.year + n

    @settings(max_examples=100)
    @given(jalali_timestamps())
    def test_year_begin_is_on_offset(self, ts: JalaliTimestamp) -> None:
        """is_on_offset correctly identifies year starts."""
        offset = JalaliYearBegin()
        expected = ts.month == 1 and ts.day == 1
        assert offset.is_on_offset(ts) == expected

    @settings(max_examples=100)
    @given(jalali_timestamps())
    def test_year_end_is_on_offset(self, ts: JalaliTimestamp) -> None:
        """is_on_offset correctly identifies year ends."""
        offset = JalaliYearEnd()
        expected = ts.month == 12 and ts.day == days_in_month(ts.year, 12)
        assert offset.is_on_offset(ts) == expected

    @settings(max_examples=100)
    @given(jalali_timestamps())
    def test_year_begin_rollforward_idempotent(self, ts: JalaliTimestamp) -> None:
        """Rolling forward twice is same as rolling forward once."""
        offset = JalaliYearBegin()
        once = offset.rollforward(ts)
        twice = offset.rollforward(once)
        assert once == twice

    @settings(max_examples=100)
    @given(jalali_timestamps())
    def test_year_end_rollforward_idempotent(self, ts: JalaliTimestamp) -> None:
        """Rolling forward twice is same as rolling forward once."""
        offset = JalaliYearEnd()
        once = offset.rollforward(ts)
        twice = offset.rollforward(once)
        assert once == twice


class TestOffsetAlgebraProperties:
    """Property-based tests for offset algebraic properties."""

    @settings(max_examples=50)
    @given(st.integers(min_value=-10, max_value=10).filter(lambda x: x != 0))
    def test_offset_negation(self, n: int) -> None:
        """Negating an offset negates its n value."""
        offset = JalaliMonthEnd(n=n)
        neg = -offset
        assert neg.n == -n

    @settings(max_examples=50)
    @given(
        st.integers(min_value=-5, max_value=5).filter(lambda x: x != 0),
        st.integers(min_value=-5, max_value=5).filter(lambda x: x != 0),
    )
    def test_offset_multiplication(self, n: int, mult: int) -> None:
        """Multiplying an offset multiplies its n value."""
        offset = JalaliMonthEnd(n=n)
        result = offset * mult
        assert result.n == n * mult

    @settings(max_examples=50)
    @given(st.integers(min_value=-10, max_value=10).filter(lambda x: x != 0))
    def test_offset_equality(self, n: int) -> None:
        """Offsets with same type and n are equal."""
        offset1 = JalaliMonthEnd(n=n)
        offset2 = JalaliMonthEnd(n=n)
        assert offset1 == offset2
        assert hash(offset1) == hash(offset2)

    @settings(max_examples=50)
    @given(
        st.integers(min_value=-10, max_value=10).filter(lambda x: x != 0),
        st.integers(min_value=-10, max_value=10).filter(lambda x: x != 0),
    )
    def test_offset_inequality(self, n1: int, n2: int) -> None:
        """Offsets with different n are not equal."""
        assume(n1 != n2)
        offset1 = JalaliMonthEnd(n=n1)
        offset2 = JalaliMonthEnd(n=n2)
        assert offset1 != offset2
