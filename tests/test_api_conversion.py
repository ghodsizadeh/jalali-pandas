"""Tests for conversion functions (to_jalali_datetime, to_gregorian_datetime)."""

import pandas as pd
import pytest

from jalali_pandas import (
    JalaliDatetimeIndex,
    JalaliTimestamp,
    to_gregorian_datetime,
    to_jalali_datetime,
)


class TestToJalaliDatetimeScalar:
    """Tests for to_jalali_datetime with scalar inputs."""

    def test_from_string(self):
        """Test conversion from string."""
        result = to_jalali_datetime("1402-06-15")

        assert isinstance(result, JalaliTimestamp)
        assert result.year == 1402
        assert result.month == 6
        assert result.day == 15

    def test_from_string_with_time(self):
        """Test conversion from string with time."""
        result = to_jalali_datetime("1402-06-15 14:30:00")

        assert result.hour == 14
        assert result.minute == 30

    def test_from_string_slash_format(self):
        """Test conversion from string with slash format."""
        result = to_jalali_datetime("1402/06/15")

        assert result.year == 1402
        assert result.month == 6
        assert result.day == 15

    def test_from_jalali_timestamp(self):
        """Test that JalaliTimestamp is returned as-is."""
        ts = JalaliTimestamp(1402, 6, 15)
        result = to_jalali_datetime(ts)

        assert result is ts

    def test_from_pandas_timestamp(self):
        """Test conversion from pandas Timestamp (Gregorian)."""
        # 2023-09-06 = 1402-06-15
        result = to_jalali_datetime(pd.Timestamp("2023-09-06"))

        assert isinstance(result, JalaliTimestamp)
        assert result.year == 1402
        assert result.month == 6
        assert result.day == 15

    def test_from_datetime(self):
        """Test conversion from Python datetime."""
        from datetime import datetime

        dt = datetime(2023, 9, 6, 10, 30, 0)
        result = to_jalali_datetime(dt)

        assert isinstance(result, JalaliTimestamp)
        assert result.year == 1402
        assert result.hour == 10

    def test_with_format(self):
        """Test conversion with explicit format."""
        result = to_jalali_datetime("15-06-1402", format="%d-%m-%Y")

        assert result.year == 1402
        assert result.month == 6
        assert result.day == 15

    def test_invalid_string_raises(self):
        """Test that invalid string raises ValueError."""
        with pytest.raises(ValueError):
            to_jalali_datetime("invalid-date")

    def test_invalid_string_coerce(self):
        """Test that invalid string with errors='coerce' returns NaT."""
        result = to_jalali_datetime("invalid-date", errors="coerce")

        assert pd.isna(result)

    def test_invalid_string_ignore_raises(self):
        """Test that invalid string with errors='ignore' raises TypeError."""
        with pytest.raises(TypeError, match="errors='ignore'"):
            to_jalali_datetime("invalid-date", errors="ignore")

    def test_invalid_type_raises(self):
        """Test invalid input type raises TypeError."""
        with pytest.raises(TypeError):
            to_jalali_datetime(123)  # type: ignore[arg-type]


class TestToJalaliDatetimeSequence:
    """Tests for to_jalali_datetime with sequence inputs."""

    def test_from_list_of_strings(self):
        """Test conversion from list of strings."""
        result = to_jalali_datetime(["1402-01-01", "1402-06-15"])

        assert isinstance(result, JalaliDatetimeIndex)
        assert len(result) == 2
        assert result[0] == JalaliTimestamp(1402, 1, 1)
        assert result[1] == JalaliTimestamp(1402, 6, 15)

    def test_from_datetime_index(self):
        """Test conversion from DatetimeIndex."""
        dti = pd.DatetimeIndex(["2023-03-21", "2023-09-06"])
        result = to_jalali_datetime(dti)

        assert isinstance(result, JalaliDatetimeIndex)
        assert len(result) == 2
        # 2023-03-21 = 1402-01-01
        assert result[0] == JalaliTimestamp(1402, 1, 1)

    def test_with_nat_in_sequence(self):
        """Test sequence with NaT values."""
        result = to_jalali_datetime(["1402-01-01", None, "1402-01-03"], errors="coerce")

        assert len(result) == 3
        assert pd.isna(result[1])

    def test_invalid_in_sequence_raises(self):
        """Test that invalid value in sequence raises ValueError."""
        with pytest.raises(ValueError):
            to_jalali_datetime(["1402-01-01", "invalid"])

    def test_invalid_in_sequence_coerce(self):
        """Test that invalid value with errors='coerce' becomes NaT."""
        result = to_jalali_datetime(["1402-01-01", "invalid"], errors="coerce")

        assert len(result) == 2
        assert pd.isna(result[1])

    def test_sequence_with_timestamps(self):
        """Test conversion from list of pandas Timestamps."""
        items = [pd.Timestamp("2023-03-21"), pd.Timestamp("2023-03-22")]
        result = to_jalali_datetime(items)

        assert isinstance(result, JalaliDatetimeIndex)
        assert result[0] == JalaliTimestamp(1402, 1, 1)

    def test_sequence_with_jalali_timestamps(self):
        """Test conversion from list of JalaliTimestamp objects."""
        items = [JalaliTimestamp(1402, 1, 1), JalaliTimestamp(1402, 1, 2)]
        result = to_jalali_datetime(items)

        assert isinstance(result, JalaliDatetimeIndex)
        assert result[1] == JalaliTimestamp(1402, 1, 2)

    def test_invalid_in_sequence_ignore_raises(self):
        """Test that invalid value with errors='ignore' raises ValueError."""
        with pytest.raises(ValueError, match="errors='ignore'"):
            to_jalali_datetime(["1402-01-01", "invalid"], errors="ignore")

    def test_datetime_index_with_nat(self):
        """Test DatetimeIndex conversion preserves NaT values."""
        dti = pd.DatetimeIndex([pd.Timestamp("2023-03-21"), pd.NaT])
        result = to_jalali_datetime(dti)

        assert pd.isna(result[1])


class TestToJalaliDatetimeSeries:
    """Tests for to_jalali_datetime with Series inputs."""

    def test_from_string_series(self):
        """Test conversion from Series of strings."""
        s = pd.Series(["1402-01-01", "1402-06-15"])
        result = to_jalali_datetime(s)

        assert isinstance(result, pd.Series)
        assert len(result) == 2
        assert result.iloc[0] == JalaliTimestamp(1402, 1, 1)

    def test_from_timestamp_series(self):
        """Test conversion from Series of Timestamps."""
        s = pd.Series([pd.Timestamp("2023-03-21"), pd.Timestamp("2023-09-06")])
        result = to_jalali_datetime(s)

        assert isinstance(result, pd.Series)
        assert result.iloc[0] == JalaliTimestamp(1402, 1, 1)

    def test_preserves_index(self):
        """Test that Series index is preserved."""
        s = pd.Series(["1402-01-01", "1402-06-15"], index=["a", "b"])
        result = to_jalali_datetime(s)

        assert list(result.index) == ["a", "b"]

    def test_preserves_name(self):
        """Test that Series name is preserved."""
        s = pd.Series(["1402-01-01", "1402-06-15"], name="dates")
        result = to_jalali_datetime(s)

        assert result.name == "dates"

    def test_with_nat_in_series(self):
        """Test Series with NaT values."""
        s = pd.Series(["1402-01-01", None, "1402-01-03"])
        result = to_jalali_datetime(s, errors="coerce")

        assert len(result) == 3
        assert pd.isna(result.iloc[1])

    def test_series_with_datetime_objects(self):
        """Test Series with Python datetime values."""
        from datetime import datetime

        s = pd.Series([datetime(2023, 3, 21), datetime(2023, 3, 22)])
        result = to_jalali_datetime(s)

        assert result.iloc[0] == JalaliTimestamp(1402, 1, 1)

    def test_series_errors_ignore_returns_original(self):
        """Test errors='ignore' returns the original Series."""
        s = pd.Series(["1402-01-01", "invalid-date"])
        result = to_jalali_datetime(s, errors="ignore")

        assert result is s


class TestToGregorianDatetime:
    """Tests for to_gregorian_datetime function."""

    def test_from_jalali_timestamp(self):
        """Test conversion from JalaliTimestamp."""
        ts = JalaliTimestamp(1402, 6, 15)
        result = to_gregorian_datetime(ts)

        assert isinstance(result, pd.Timestamp)
        assert result == pd.Timestamp("2023-09-06")

    def test_from_jalali_datetime_index(self):
        """Test conversion from JalaliDatetimeIndex."""
        idx = JalaliDatetimeIndex(["1402-01-01", "1402-06-15"])
        result = to_gregorian_datetime(idx)

        assert isinstance(result, pd.DatetimeIndex)
        assert len(result) == 2
        assert result[0] == pd.Timestamp("2023-03-21")

    def test_from_series(self):
        """Test conversion from Series with Jalali data."""
        idx = JalaliDatetimeIndex(["1402-01-01", "1402-06-15"])
        s = pd.Series([idx[0], idx[1]])
        result = to_gregorian_datetime(s)

        assert isinstance(result, pd.Series)
        assert result.iloc[0] == pd.Timestamp("2023-03-21")

    def test_preserves_index(self):
        """Test that Series index is preserved."""
        idx = JalaliDatetimeIndex(["1402-01-01", "1402-06-15"])
        s = pd.Series([idx[0], idx[1]], index=["a", "b"])
        result = to_gregorian_datetime(s)

        assert list(result.index) == ["a", "b"]

    def test_with_nat(self):
        """Test conversion with NaT values."""
        idx = JalaliDatetimeIndex(
            [
                JalaliTimestamp(1402, 1, 1),
                pd.NaT,
            ]
        )
        result = to_gregorian_datetime(idx)

        assert len(result) == 2
        assert pd.isna(result[1])

    def test_from_jalali_dtype_series(self):
        """Test conversion from Series with Jalali dtype."""
        idx = JalaliDatetimeIndex(["1402-01-01", "1402-01-02"])
        series = pd.Series(idx._data, name="jalali")
        result = to_gregorian_datetime(series)

        assert isinstance(result, pd.Series)
        assert result.iloc[0] == pd.Timestamp("2023-03-21")

    def test_series_invalid_element_raises(self):
        """Test that invalid element types raise TypeError."""
        s = pd.Series([JalaliTimestamp(1402, 1, 1), "not-jalali"])
        with pytest.raises(TypeError, match="Cannot convert"):
            _ = to_gregorian_datetime(s)

    def test_invalid_type_raises(self):
        """Test that invalid type raises TypeError."""
        with pytest.raises(TypeError):
            to_gregorian_datetime("not a jalali type")  # type: ignore[arg-type]


def test_datetime_index_ignore_raises(monkeypatch):
    """Test errors='ignore' for DatetimeIndex raises ValueError."""
    from jalali_pandas.api import conversion

    def _raise(_: object) -> None:
        raise ValueError("boom")

    monkeypatch.setattr(conversion.JalaliTimestamp, "from_gregorian", _raise)
    with pytest.raises(ValueError, match="errors='ignore'"):
        to_jalali_datetime(pd.DatetimeIndex(["2023-03-21"]), errors="ignore")


class TestRoundTrip:
    """Tests for round-trip conversions."""

    def test_gregorian_to_jalali_to_gregorian(self):
        """Test Gregorian -> Jalali -> Gregorian round trip."""
        original = pd.Timestamp("2023-09-06 14:30:00")
        jalali = to_jalali_datetime(original)
        back = to_gregorian_datetime(jalali)

        assert back == original

    def test_jalali_to_gregorian_to_jalali(self):
        """Test Jalali -> Gregorian -> Jalali round trip."""
        original = JalaliTimestamp(1402, 6, 15, 14, 30, 0)
        gregorian = to_gregorian_datetime(original)
        back = to_jalali_datetime(gregorian)

        assert back == original

    def test_index_round_trip(self):
        """Test round trip with index."""
        original = JalaliDatetimeIndex(["1402-01-01", "1402-06-15", "1402-12-29"])
        gregorian = to_gregorian_datetime(original)
        back = to_jalali_datetime(gregorian)

        assert len(back) == len(original)
        for i in range(len(original)):
            assert back[i] == original[i]
