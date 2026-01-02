"""Tests for JalaliDatetimeIndex."""

import numpy as np
import pandas as pd
import pytest

from jalali_pandas import JalaliDatetimeIndex, JalaliMonthEnd, JalaliTimestamp
from jalali_pandas.core.arrays import JalaliDatetimeArray


class TestJalaliDatetimeIndexConstruction:
    """Tests for JalaliDatetimeIndex construction."""

    def test_from_list_of_timestamps(self):
        """Test construction from list of JalaliTimestamp."""
        ts1 = JalaliTimestamp(1402, 1, 1)
        ts2 = JalaliTimestamp(1402, 1, 2)
        ts3 = JalaliTimestamp(1402, 1, 3)

        idx = JalaliDatetimeIndex([ts1, ts2, ts3])

        assert len(idx) == 3
        assert idx[0] == ts1
        assert idx[1] == ts2
        assert idx[2] == ts3

    def test_from_list_of_strings(self):
        """Test construction from list of strings."""
        idx = JalaliDatetimeIndex(["1402-01-01", "1402-01-02", "1402-01-03"])

        assert len(idx) == 3
        assert idx[0] == JalaliTimestamp(1402, 1, 1)
        assert idx[1] == JalaliTimestamp(1402, 1, 2)
        assert idx[2] == JalaliTimestamp(1402, 1, 3)

    def test_from_jalali_datetime_array(self):
        """Test construction from JalaliDatetimeArray."""
        arr = JalaliDatetimeArray._from_sequence(
            [
                JalaliTimestamp(1402, 1, 1),
                JalaliTimestamp(1402, 1, 2),
            ]
        )
        idx = JalaliDatetimeIndex(arr)

        assert len(idx) == 2
        assert idx[0] == JalaliTimestamp(1402, 1, 1)

    def test_from_another_index(self):
        """Test construction from another JalaliDatetimeIndex."""
        idx1 = JalaliDatetimeIndex(["1402-01-01", "1402-01-02"])
        idx2 = JalaliDatetimeIndex(idx1)

        assert len(idx2) == 2
        assert idx2.equals(idx1)

    def test_with_name(self):
        """Test construction with name."""
        idx = JalaliDatetimeIndex(["1402-01-01", "1402-01-02"], name="dates")

        assert idx._name == "dates"

    def test_with_freq(self):
        """Test construction with frequency."""
        idx = JalaliDatetimeIndex(["1402-01-01", "1402-01-02"], freq="D")

        assert idx.freq == "D"
        assert idx.freqstr == "D"

    def test_empty_index(self):
        """Test construction of empty index."""
        idx = JalaliDatetimeIndex([])

        assert len(idx) == 0

    def test_from_none(self):
        """Test construction from None."""
        idx = JalaliDatetimeIndex(None)
        assert len(idx) == 0

    def test_copy_from_index(self):
        """Test copy behavior when constructing from another index."""
        idx = JalaliDatetimeIndex(["1402-01-01", "1402-01-02"])
        copied = JalaliDatetimeIndex(idx, copy=True)

        assert copied.equals(idx)
        assert copied._data is not idx._data

    def test_copy_from_array(self):
        """Test copy behavior when constructing from array."""
        arr = JalaliDatetimeArray._from_sequence(
            [JalaliTimestamp(1402, 1, 1), JalaliTimestamp(1402, 1, 2)]
        )
        idx = JalaliDatetimeIndex(arr, copy=True)

        assert idx._data is not arr


class TestJalaliDatetimeIndexProperties:
    """Tests for JalaliDatetimeIndex properties."""

    @pytest.fixture
    def sample_index(self):
        """Create a sample index for testing."""
        return JalaliDatetimeIndex(
            [
                "1402-01-15",
                "1402-06-20",
                "1402-12-29",
            ]
        )

    def test_year(self, sample_index):
        """Test year property."""
        years = sample_index.year
        assert list(years) == [1402.0, 1402.0, 1402.0]

    def test_month(self, sample_index):
        """Test month property."""
        months = sample_index.month
        assert list(months) == [1.0, 6.0, 12.0]

    def test_day(self, sample_index):
        """Test day property."""
        days = sample_index.day
        assert list(days) == [15.0, 20.0, 29.0]

    def test_quarter(self, sample_index):
        """Test quarter property."""
        quarters = sample_index.quarter
        assert list(quarters) == [1.0, 2.0, 4.0]

    def test_dayofweek(self, sample_index):
        """Test dayofweek property."""
        dow = sample_index.dayofweek
        assert len(dow) == 3
        # All values should be 0-6
        assert all(0 <= d <= 6 for d in dow if not pd.isna(d))

    def test_dtype(self, sample_index):
        """Test dtype property."""
        assert sample_index.dtype.name == "jalali_datetime"

    def test_freq_setter_and_freqstr(self):
        """Test freq setter and freqstr output."""
        idx = JalaliDatetimeIndex(["1402-01-01"])
        idx.freq = "D"
        assert idx.freqstr == "D"

        idx.freq = JalaliMonthEnd()
        assert idx.freqstr == str(idx.freq)

    def test_inferred_frequency(self):
        """Test inferred frequency from data."""
        daily = JalaliDatetimeIndex(["1402-01-01", "1402-01-02", "1402-01-03"])
        hourly = JalaliDatetimeIndex(
            [
                JalaliTimestamp(1402, 1, 1, 0, 0, 0),
                JalaliTimestamp(1402, 1, 1, 1, 0, 0),
                JalaliTimestamp(1402, 1, 1, 2, 0, 0),
            ]
        )
        short = JalaliDatetimeIndex(["1402-01-01", "1402-01-02"])

        assert daily.inferred_freq == "D"
        assert hourly.inferred_freq == "h"
        assert short.inferred_freq is None


class TestJalaliDatetimeIndexIndexing:
    """Tests for JalaliDatetimeIndex indexing operations."""

    @pytest.fixture
    def sample_index(self):
        """Create a sample index for testing."""
        return JalaliDatetimeIndex(
            [
                "1402-01-01",
                "1402-01-15",
                "1402-02-01",
                "1402-02-15",
                "1402-03-01",
            ]
        )

    def test_integer_indexing(self, sample_index):
        """Test integer indexing."""
        assert sample_index[0] == JalaliTimestamp(1402, 1, 1)
        assert sample_index[2] == JalaliTimestamp(1402, 2, 1)
        assert sample_index[-1] == JalaliTimestamp(1402, 3, 1)

    def test_slice_indexing(self, sample_index):
        """Test slice indexing."""
        sliced = sample_index[1:3]
        assert len(sliced) == 2
        assert sliced[0] == JalaliTimestamp(1402, 1, 15)
        assert sliced[1] == JalaliTimestamp(1402, 2, 1)

    def test_string_exact_match(self, sample_index):
        """Test string indexing with exact match."""
        loc = sample_index.get_loc("1402-01-15")
        assert loc == 1

    def test_string_partial_year(self, sample_index):
        """Test partial string indexing by year."""
        mask = sample_index.get_loc("1402")
        assert isinstance(mask, np.ndarray)
        assert mask.sum() == 5  # All dates are in 1402

    def test_string_partial_month(self, sample_index):
        """Test partial string indexing by year-month."""
        mask = sample_index.get_loc("1402-01")
        assert isinstance(mask, np.ndarray)
        assert mask.sum() == 2  # Two dates in 1402-01

    def test_contains(self, sample_index):
        """Test __contains__ method."""
        assert JalaliTimestamp(1402, 1, 1) in sample_index
        assert JalaliTimestamp(1402, 1, 10) not in sample_index

    def test_get_loc_not_found(self, sample_index):
        """Test get_loc raises KeyError for missing key."""
        with pytest.raises(KeyError):
            sample_index.get_loc("1402-01-10")

    def test_get_loc_with_jalali_timestamp(self, sample_index):
        """Test get_loc with JalaliTimestamp input."""
        loc = sample_index.get_loc(JalaliTimestamp(1402, 2, 1))
        assert loc == 2

    def test_partial_string_not_found(self, sample_index):
        """Test partial string lookup raises KeyError when no match."""
        with pytest.raises(KeyError):
            sample_index.get_loc("1401")

    def test_repr_truncates(self):
        """Test repr truncates long indexes."""
        idx = JalaliDatetimeIndex([f"1402-01-{day:02d}" for day in range(1, 8)])
        repr_str = repr(idx)

        assert "..." in repr_str

    def test_slice_locs(self):
        """Test slice_locs boundaries."""
        idx = JalaliDatetimeIndex(
            ["1402-01-01", "1402-01-05", "1402-01-10", "1402-01-20"]
        )
        start, end = idx.slice_locs("1402-01-05", "1402-01-10")

        assert (start, end) == (1, 3)

    def test_parse_to_timestamp_variants(self):
        """Test parsing keys to JalaliTimestamp."""
        idx = JalaliDatetimeIndex(["1402-01-01"])

        assert idx._parse_to_timestamp("1402-01-01 01:02:03") == JalaliTimestamp(
            1402, 1, 1
        )
        assert idx._parse_to_timestamp("1402") == JalaliTimestamp(1402, 1, 1)
        assert idx._parse_to_timestamp("1402-02") == JalaliTimestamp(1402, 2, 1)
        with pytest.raises(ValueError):
            idx._parse_to_timestamp("invalid")


class TestJalaliDatetimeIndexConversion:
    """Tests for JalaliDatetimeIndex conversion methods."""

    def test_to_gregorian(self):
        """Test conversion to Gregorian DatetimeIndex."""
        idx = JalaliDatetimeIndex(["1402-01-01", "1402-06-15"])
        gregorian = idx.to_gregorian()

        assert isinstance(gregorian, pd.DatetimeIndex)
        assert len(gregorian) == 2
        # 1402-01-01 = 2023-03-21
        assert gregorian[0] == pd.Timestamp("2023-03-21")

    def test_strftime(self):
        """Test strftime method."""
        idx = JalaliDatetimeIndex(["1402-01-01", "1402-06-15"])
        formatted = idx.strftime("%Y/%m/%d")

        assert list(formatted) == ["1402/01/01", "1402/06/15"]


class TestJalaliDatetimeIndexSetOperations:
    """Tests for JalaliDatetimeIndex set operations."""

    def test_union(self):
        """Test union of two indexes."""
        idx1 = JalaliDatetimeIndex(["1402-01-01", "1402-01-02"])
        idx2 = JalaliDatetimeIndex(["1402-01-02", "1402-01-03"])

        result = idx1.union(idx2)

        assert len(result) == 3
        assert JalaliTimestamp(1402, 1, 1) in result
        assert JalaliTimestamp(1402, 1, 2) in result
        assert JalaliTimestamp(1402, 1, 3) in result

    def test_intersection(self):
        """Test intersection of two indexes."""
        idx1 = JalaliDatetimeIndex(["1402-01-01", "1402-01-02", "1402-01-03"])
        idx2 = JalaliDatetimeIndex(["1402-01-02", "1402-01-03", "1402-01-04"])

        result = idx1.intersection(idx2)

        assert len(result) == 2
        assert JalaliTimestamp(1402, 1, 2) in result
        assert JalaliTimestamp(1402, 1, 3) in result

    def test_difference(self):
        """Test difference of two indexes."""
        idx1 = JalaliDatetimeIndex(["1402-01-01", "1402-01-02", "1402-01-03"])
        idx2 = JalaliDatetimeIndex(["1402-01-02"])

        result = idx1.difference(idx2)

        assert len(result) == 2
        assert JalaliTimestamp(1402, 1, 1) in result
        assert JalaliTimestamp(1402, 1, 3) in result
        assert JalaliTimestamp(1402, 1, 2) not in result

    def test_union_with_nat(self):
        """Test union with NaT values."""
        idx1 = JalaliDatetimeIndex([JalaliTimestamp(1402, 1, 1), pd.NaT])
        idx2 = JalaliDatetimeIndex([JalaliTimestamp(1402, 1, 2), pd.NaT])

        result = idx1.union(idx2)
        assert len(result) == 3
        assert any(pd.isna(val) for val in result)

    def test_intersection_with_nat(self):
        """Test intersection with NaT values."""
        idx1 = JalaliDatetimeIndex([JalaliTimestamp(1402, 1, 1), pd.NaT])
        idx2 = JalaliDatetimeIndex([pd.NaT])

        result = idx1.intersection(idx2)
        assert len(result) == 1
        assert pd.isna(result[0])

    def test_difference_with_nat(self):
        """Test difference with NaT values."""
        idx1 = JalaliDatetimeIndex([JalaliTimestamp(1402, 1, 1), pd.NaT])
        idx2 = JalaliDatetimeIndex([pd.NaT])

        result = idx1.difference(idx2)
        assert len(result) == 1
        assert result[0] == JalaliTimestamp(1402, 1, 1)

    def test_set_ops_type_error(self):
        """Test set operations reject non-index inputs."""
        idx = JalaliDatetimeIndex(["1402-01-01"])
        with pytest.raises(TypeError, match="JalaliDatetimeIndex"):
            idx.union(["1402-01-02"])  # type: ignore[arg-type]
        with pytest.raises(TypeError, match="JalaliDatetimeIndex"):
            idx.intersection(["1402-01-02"])  # type: ignore[arg-type]
        with pytest.raises(TypeError, match="JalaliDatetimeIndex"):
            idx.difference(["1402-01-02"])  # type: ignore[arg-type]


class TestJalaliDatetimeIndexShift:
    """Tests for JalaliDatetimeIndex shift operations."""

    def test_shift_with_timedelta(self):
        """Test shift with pandas Timedelta."""
        idx = JalaliDatetimeIndex(["1402-01-01", "1402-01-02"], freq="D")
        shifted = idx.shift(1, freq=pd.Timedelta(days=1))

        assert shifted[0] == JalaliTimestamp(1402, 1, 2)
        assert shifted[1] == JalaliTimestamp(1402, 1, 3)

    def test_shift_with_jalali_offset(self):
        """Test shift with Jalali offset."""
        from jalali_pandas import JalaliMonthEnd

        idx = JalaliDatetimeIndex(["1402-01-15", "1402-02-15"], freq="JME")
        shifted = idx.shift(1, freq=JalaliMonthEnd())

        # After shifting by 1 month end
        assert shifted[0].month == 2 or shifted[0].month == 1
        assert shifted[1].month == 3 or shifted[1].month == 2

    def test_shift_requires_freq(self):
        """Test shift raises when freq is missing."""
        idx = JalaliDatetimeIndex(["1402-01-01", "1402-01-02"])
        with pytest.raises(ValueError, match="freq must be specified"):
            idx.shift()

    def test_shift_with_string_offset(self):
        """Test shift with string frequency parsed as Timedelta."""
        idx = JalaliDatetimeIndex(["1402-01-01", "1402-01-02"])
        shifted = idx.shift(2, freq="2D")

        assert shifted[0] == JalaliTimestamp(1402, 1, 5)

    def test_shift_with_jalali_alias(self):
        """Test shift with Jalali frequency alias string."""
        idx = JalaliDatetimeIndex(["1402-01-01"], freq="JME")
        shifted = idx.shift(1, freq="JME")

        assert shifted[0].is_month_end

    def test_snap(self):
        """Test snap to nearest minute."""
        idx = JalaliDatetimeIndex(
            [
                JalaliTimestamp(1402, 1, 1, 12, 0, 30),
                JalaliTimestamp(1402, 1, 1, 12, 1, 0),
            ]
        )
        snapped = idx.snap("min")

        assert snapped[0] == idx[0]


class TestJalaliDatetimeIndexMisc:
    """Miscellaneous tests for JalaliDatetimeIndex."""

    def test_copy(self):
        """Test copy method."""
        idx = JalaliDatetimeIndex(["1402-01-01", "1402-01-02"])
        copied = idx.copy()

        assert copied.equals(idx)
        assert copied is not idx

    def test_equals(self):
        """Test equals method."""
        idx1 = JalaliDatetimeIndex(["1402-01-01", "1402-01-02"])
        idx2 = JalaliDatetimeIndex(["1402-01-01", "1402-01-02"])
        idx3 = JalaliDatetimeIndex(["1402-01-01", "1402-01-03"])

        assert idx1.equals(idx2)
        assert not idx1.equals(idx3)

    def test_isna(self):
        """Test _isna method."""
        idx = JalaliDatetimeIndex(
            [
                JalaliTimestamp(1402, 1, 1),
                pd.NaT,
                JalaliTimestamp(1402, 1, 3),
            ]
        )

        na_mask = idx._isna()
        assert list(na_mask) == [False, True, False]

    def test_notna(self):
        """Test _notna method."""
        idx = JalaliDatetimeIndex(
            [
                JalaliTimestamp(1402, 1, 1),
                pd.NaT,
                JalaliTimestamp(1402, 1, 3),
            ]
        )

        notna_mask = idx._notna()
        assert list(notna_mask) == [True, False, True]

    def test_repr(self):
        """Test string representation."""
        idx = JalaliDatetimeIndex(["1402-01-01", "1402-01-02"])
        repr_str = repr(idx)

        assert "JalaliDatetimeIndex" in repr_str
        assert "1402-01-01" in repr_str

    def test_to_list(self):
        """Test to_list method."""
        idx = JalaliDatetimeIndex(["1402-01-01", "1402-01-02"])
        lst = idx.to_list()

        assert isinstance(lst, list)
        assert len(lst) == 2
        assert lst[0] == JalaliTimestamp(1402, 1, 1)

    def test_values_property(self):
        """Test values property."""
        idx = JalaliDatetimeIndex(["1402-01-01", "1402-01-02"])
        values = idx.values

        assert isinstance(values, JalaliDatetimeArray)
        assert len(values) == 2

    def test_shallow_copy(self):
        """Test _shallow_copy uses existing values when none provided."""
        idx = JalaliDatetimeIndex(["1402-01-01", "1402-01-02"])
        copied = idx._shallow_copy()

        assert copied is not idx
        assert copied.equals(idx)

    def test_eq_with_timestamp(self):
        """Test element-wise equality with JalaliTimestamp."""
        idx = JalaliDatetimeIndex(["1402-01-01", "1402-01-02"])
        mask = idx == JalaliTimestamp(1402, 1, 2)

        assert mask.tolist() == [False, True]

    def test_to_numpy(self):
        """Test to_numpy with and without dtype."""
        idx = JalaliDatetimeIndex(["1402-01-01", "1402-01-02"])
        raw = idx.to_numpy()
        typed = idx.to_numpy(dtype=object)

        assert len(raw) == 2
        assert typed.dtype == object
