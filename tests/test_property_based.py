"""Property-based tests for Jalali datetime behaviors."""

from __future__ import annotations

from hypothesis import given, settings
from hypothesis import strategies as st

from jalali_pandas import JalaliTimestamp, to_gregorian_datetime, to_jalali_datetime
from jalali_pandas.core.calendar import days_in_month


@st.composite
def jalali_datetimes(draw: st.DrawFn) -> JalaliTimestamp:
    """Generate valid JalaliTimestamp instances."""
    year = draw(st.integers(min_value=1300, max_value=1500))
    month = draw(st.integers(min_value=1, max_value=12))
    day = draw(st.integers(min_value=1, max_value=days_in_month(year, month)))
    hour = draw(st.integers(min_value=0, max_value=23))
    minute = draw(st.integers(min_value=0, max_value=59))
    second = draw(st.integers(min_value=0, max_value=59))
    microsecond = draw(st.integers(min_value=0, max_value=999999))
    return JalaliTimestamp(year, month, day, hour, minute, second, microsecond)


@st.composite
def jalali_dates(draw: st.DrawFn) -> JalaliTimestamp:
    """Generate valid JalaliTimestamp instances at midnight."""
    year = draw(st.integers(min_value=1300, max_value=1500))
    month = draw(st.integers(min_value=1, max_value=12))
    day = draw(st.integers(min_value=1, max_value=days_in_month(year, month)))
    return JalaliTimestamp(year, month, day)


@settings(max_examples=50)
@given(jalali_datetimes())
def test_roundtrip_gregorian_conversion(ts: JalaliTimestamp) -> None:
    """Gregorian conversion roundtrip should preserve timestamps."""
    gregorian = to_gregorian_datetime(ts)
    restored = to_jalali_datetime(gregorian)

    assert restored == ts


@settings(max_examples=50)
@given(jalali_dates())
def test_string_roundtrip(ts: JalaliTimestamp) -> None:
    """String parsing should preserve date components."""
    date_str = ts.strftime("%Y-%m-%d")
    parsed = to_jalali_datetime(date_str)

    assert parsed.year == ts.year
    assert parsed.month == ts.month
    assert parsed.day == ts.day
