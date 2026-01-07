"""Hypothesis strategies for Jalali datetime testing."""

from __future__ import annotations

from hypothesis import strategies as st

from jalali_pandas import JalaliTimestamp
from jalali_pandas.core.calendar import days_in_month


@st.composite
def jalali_years(draw: st.DrawFn, min_year: int = 1300, max_year: int = 1500) -> int:
    """Generate valid Jalali years."""
    return draw(st.integers(min_value=min_year, max_value=max_year))


@st.composite
def jalali_months(draw: st.DrawFn) -> int:
    """Generate valid Jalali months (1-12)."""
    return draw(st.integers(min_value=1, max_value=12))


@st.composite
def jalali_dates(
    draw: st.DrawFn, min_year: int = 1300, max_year: int = 1500
) -> tuple[int, int, int]:
    """Generate valid Jalali date tuples (year, month, day)."""
    year = draw(st.integers(min_value=min_year, max_value=max_year))
    month = draw(st.integers(min_value=1, max_value=12))
    max_day = days_in_month(year, month)
    day = draw(st.integers(min_value=1, max_value=max_day))
    return (year, month, day)


@st.composite
def jalali_timestamps(
    draw: st.DrawFn, min_year: int = 1300, max_year: int = 1500
) -> JalaliTimestamp:
    """Generate valid JalaliTimestamp instances."""
    year = draw(st.integers(min_value=min_year, max_value=max_year))
    month = draw(st.integers(min_value=1, max_value=12))
    day = draw(st.integers(min_value=1, max_value=days_in_month(year, month)))
    hour = draw(st.integers(min_value=0, max_value=23))
    minute = draw(st.integers(min_value=0, max_value=59))
    second = draw(st.integers(min_value=0, max_value=59))
    microsecond = draw(st.integers(min_value=0, max_value=999999))
    return JalaliTimestamp(year, month, day, hour, minute, second, microsecond)


@st.composite
def jalali_timestamps_midnight(
    draw: st.DrawFn, min_year: int = 1300, max_year: int = 1500
) -> JalaliTimestamp:
    """Generate valid JalaliTimestamp instances at midnight."""
    year = draw(st.integers(min_value=min_year, max_value=max_year))
    month = draw(st.integers(min_value=1, max_value=12))
    day = draw(st.integers(min_value=1, max_value=days_in_month(year, month)))
    return JalaliTimestamp(year, month, day)


@st.composite
def offset_multipliers(draw: st.DrawFn) -> int:
    """Generate offset multipliers (positive and negative)."""
    return draw(st.integers(min_value=-50, max_value=50).filter(lambda x: x != 0))


@st.composite
def small_offset_multipliers(draw: st.DrawFn) -> int:
    """Generate small offset multipliers for testing."""
    return draw(st.integers(min_value=-10, max_value=10).filter(lambda x: x != 0))
