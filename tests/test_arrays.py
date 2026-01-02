"""Tests for JalaliDatetimeArray."""

import numpy as np
import pandas as pd
import pytest

from jalali_pandas import JalaliTimestamp
from jalali_pandas.core.arrays import JalaliDatetimeArray
from jalali_pandas.core.dtypes import JalaliDatetimeDtype


class TestJalaliDatetimeArrayCreation:
    """Tests for JalaliDatetimeArray creation."""

    def test_from_sequence(self):
        """Test creating array from sequence of JalaliTimestamp."""
        ts1 = JalaliTimestamp(1402, 1, 1)
        ts2 = JalaliTimestamp(1402, 1, 2)
        arr = JalaliDatetimeArray._from_sequence([ts1, ts2])
        assert len(arr) == 2
        assert arr[0] == ts1
        assert arr[1] == ts2

    def test_from_sequence_with_nat(self):
        """Test creating array with NaT values."""
        ts1 = JalaliTimestamp(1402, 1, 1)
        arr = JalaliDatetimeArray._from_sequence([ts1, pd.NaT, None])
        assert len(arr) == 3
        assert arr[0] == ts1
        assert pd.isna(arr[1])
        assert pd.isna(arr[2])

    def test_from_sequence_of_strings(self):
        """Test creating array from strings."""
        arr = JalaliDatetimeArray._from_sequence_of_strings(
            ["1402-01-01", "1402-01-02"]
        )
        assert len(arr) == 2
        assert arr[0].year == 1402
        assert arr[0].month == 1
        assert arr[0].day == 1

    def test_from_sequence_with_time_string(self):
        """Test creating array from datetime strings with time."""
        arr = JalaliDatetimeArray._from_sequence(["1402-01-01 10:30:00"])
        assert arr[0].day == 1
        assert arr[0].hour == 0

    def test_from_sequence_with_invalid_string(self):
        """Test invalid string values become NaT."""
        arr = JalaliDatetimeArray._from_sequence(["invalid-date"])
        assert pd.isna(arr[0])

    def test_from_sequence_with_unknown_type(self):
        """Test unknown value types become NaT."""
        arr = JalaliDatetimeArray._from_sequence([123])
        assert pd.isna(arr[0])

    def test_init_copy(self):
        """Test constructor copy behavior."""
        data = np.array([JalaliTimestamp(1402, 1, 1)], dtype=object)
        arr = JalaliDatetimeArray(data, copy=True)
        assert arr._data is not data

    def test_from_sequence_with_timestamps(self):
        """Test creating array from pandas Timestamps."""
        ts = pd.Timestamp("2023-03-21")
        arr = JalaliDatetimeArray._from_sequence([ts])
        assert len(arr) == 1
        assert arr[0].year == 1402
        assert arr[0].month == 1
        assert arr[0].day == 1

    def test_from_factorized(self):
        """Test _from_factorized reconstruction."""
        ts1 = JalaliTimestamp(1402, 1, 1)
        ts2 = JalaliTimestamp(1402, 1, 2)
        original = JalaliDatetimeArray._from_sequence([ts1, ts2])
        values = np.array([ts1, ts2], dtype=object)
        reconstructed = JalaliDatetimeArray._from_factorized(values, original)
        assert len(reconstructed) == 2


class TestJalaliDatetimeArrayProperties:
    """Tests for JalaliDatetimeArray properties."""

    @pytest.fixture
    def sample_array(self):
        """Create a sample array for testing."""
        return JalaliDatetimeArray._from_sequence(
            [
                JalaliTimestamp(1402, 1, 1),
                JalaliTimestamp(1402, 6, 15, 10, 30, 45),
                JalaliTimestamp(1403, 12, 30),
            ]
        )

    def test_dtype(self, sample_array):
        """Test dtype property."""
        assert isinstance(sample_array.dtype, JalaliDatetimeDtype)

    def test_nbytes(self, sample_array):
        """Test nbytes property."""
        assert sample_array.nbytes > 0

    def test_year(self, sample_array):
        """Test year property."""
        years = sample_array.year
        assert len(years) == 3
        assert years[0] == 1402
        assert years[2] == 1403

    def test_month(self, sample_array):
        """Test month property."""
        months = sample_array.month
        assert months[0] == 1
        assert months[1] == 6
        assert months[2] == 12

    def test_day(self, sample_array):
        """Test day property."""
        days = sample_array.day
        assert days[0] == 1
        assert days[1] == 15
        assert days[2] == 30

    def test_hour(self, sample_array):
        """Test hour property."""
        hours = sample_array.hour
        assert hours[0] == 0
        assert hours[1] == 10

    def test_minute(self, sample_array):
        """Test minute property."""
        minutes = sample_array.minute
        assert minutes[0] == 0
        assert minutes[1] == 30

    def test_second(self, sample_array):
        """Test second property."""
        seconds = sample_array.second
        assert seconds[0] == 0
        assert seconds[1] == 45

    def test_quarter(self, sample_array):
        """Test quarter property."""
        quarters = sample_array.quarter
        assert quarters[0] == 1
        assert quarters[1] == 2
        assert quarters[2] == 4

    def test_dayofweek(self, sample_array):
        """Test dayofweek property."""
        dow = sample_array.dayofweek
        assert len(dow) == 3
        assert all(0 <= d <= 6 or np.isnan(d) for d in dow)

    def test_dayofyear(self, sample_array):
        """Test dayofyear property."""
        doy = sample_array.dayofyear
        assert doy[0] == 1
        assert doy[2] == 366  # Leap year

    def test_week(self, sample_array):
        """Test week property."""
        weeks = sample_array.week
        assert len(weeks) == 3


class TestJalaliDatetimeArrayWithNaT:
    """Tests for JalaliDatetimeArray with NaT values."""

    @pytest.fixture
    def array_with_nat(self):
        """Create array with NaT."""
        return JalaliDatetimeArray._from_sequence(
            [
                JalaliTimestamp(1402, 1, 1),
                pd.NaT,
                JalaliTimestamp(1402, 6, 15),
            ]
        )

    def test_isna(self, array_with_nat):
        """Test isna method."""
        result = array_with_nat.isna()
        expected = np.array([False, True, False])
        np.testing.assert_array_equal(result, expected)

    def test_properties_with_nat(self, array_with_nat):
        """Test that properties handle NaT correctly."""
        years = array_with_nat.year
        assert years[0] == 1402
        assert np.isnan(years[1])
        assert years[2] == 1402


class TestJalaliDatetimeArrayMethods:
    """Tests for JalaliDatetimeArray methods."""

    @pytest.fixture
    def sample_array(self):
        """Create a sample array for testing."""
        return JalaliDatetimeArray._from_sequence(
            [
                JalaliTimestamp(1402, 1, 1),
                JalaliTimestamp(1402, 6, 15),
            ]
        )

    def test_len(self, sample_array):
        """Test __len__."""
        assert len(sample_array) == 2

    def test_getitem_int(self, sample_array):
        """Test __getitem__ with integer."""
        item = sample_array[0]
        assert isinstance(item, JalaliTimestamp)
        assert item.year == 1402

    def test_getitem_slice(self, sample_array):
        """Test __getitem__ with slice."""
        sliced = sample_array[0:1]
        assert isinstance(sliced, JalaliDatetimeArray)
        assert len(sliced) == 1

    def test_setitem(self, sample_array):
        """Test __setitem__."""
        new_ts = JalaliTimestamp(1403, 1, 1)
        sample_array[0] = new_ts
        assert sample_array[0] == new_ts

    def test_setitem_nat(self, sample_array):
        """Test __setitem__ with NaT."""
        sample_array[0] = pd.NaT
        assert pd.isna(sample_array[0])

    def test_setitem_array(self):
        """Test __setitem__ with array."""
        arr = JalaliDatetimeArray._from_sequence(
            [
                JalaliTimestamp(1402, 1, 1),
                JalaliTimestamp(1402, 1, 2),
                JalaliTimestamp(1402, 1, 3),
            ]
        )
        new_arr = JalaliDatetimeArray._from_sequence(
            [
                JalaliTimestamp(1403, 1, 1),
                JalaliTimestamp(1403, 1, 2),
            ]
        )
        arr[0:2] = new_arr
        assert arr[0].year == 1403

    def test_setitem_list(self):
        """Test __setitem__ with list."""
        arr = JalaliDatetimeArray._from_sequence(
            [
                JalaliTimestamp(1402, 1, 1),
                JalaliTimestamp(1402, 1, 2),
            ]
        )
        arr[0:2] = [JalaliTimestamp(1403, 1, 1), JalaliTimestamp(1403, 1, 2)]
        assert arr[0].year == 1403

    def test_setitem_invalid(self):
        """Test __setitem__ with invalid type."""
        arr = JalaliDatetimeArray._from_sequence([JalaliTimestamp(1402, 1, 1)])
        with pytest.raises(TypeError):
            arr[0] = "invalid"

    def test_iter(self, sample_array):
        """Test __iter__."""
        items = list(sample_array)
        assert len(items) == 2
        assert all(isinstance(item, JalaliTimestamp) for item in items)

    def test_copy(self, sample_array):
        """Test copy method."""
        copied = sample_array.copy()
        assert len(copied) == len(sample_array)
        assert copied[0] == sample_array[0]
        # Ensure it's a copy
        copied[0] = JalaliTimestamp(1403, 1, 1)
        assert copied[0] != sample_array[0]

    def test_take(self, sample_array):
        """Test take method."""
        taken = sample_array.take([0, 1, 0])
        assert len(taken) == 3
        assert taken[0] == sample_array[0]
        assert taken[2] == sample_array[0]

    def test_take_with_fill(self, sample_array):
        """Test take with allow_fill."""
        taken = sample_array.take([0, -1], allow_fill=True)
        assert len(taken) == 2
        assert taken[0] == sample_array[0]
        assert pd.isna(taken[1])

    def test_concat_same_type(self):
        """Test _concat_same_type."""
        arr1 = JalaliDatetimeArray._from_sequence([JalaliTimestamp(1402, 1, 1)])
        arr2 = JalaliDatetimeArray._from_sequence([JalaliTimestamp(1402, 1, 2)])
        result = JalaliDatetimeArray._concat_same_type([arr1, arr2])
        assert len(result) == 2

    def test_values_for_factorize(self, sample_array):
        """Test _values_for_factorize."""
        values, na_value = sample_array._values_for_factorize()
        assert len(values) == 2
        assert pd.isna(na_value)


class TestJalaliDatetimeArrayComparison:
    """Tests for JalaliDatetimeArray comparison operations."""

    def test_eq_array(self):
        """Test equality with another array."""
        arr1 = JalaliDatetimeArray._from_sequence(
            [
                JalaliTimestamp(1402, 1, 1),
                JalaliTimestamp(1402, 1, 2),
            ]
        )
        arr2 = JalaliDatetimeArray._from_sequence(
            [
                JalaliTimestamp(1402, 1, 1),
                JalaliTimestamp(1402, 1, 3),
            ]
        )
        result = arr1 == arr2
        expected = np.array([True, False])
        np.testing.assert_array_equal(result, expected)

    def test_eq_scalar(self):
        """Test equality with scalar."""
        arr = JalaliDatetimeArray._from_sequence(
            [
                JalaliTimestamp(1402, 1, 1),
                JalaliTimestamp(1402, 1, 2),
            ]
        )
        ts = JalaliTimestamp(1402, 1, 1)
        result = arr == ts
        expected = np.array([True, False])
        np.testing.assert_array_equal(result, expected)

    def test_ne_array(self):
        """Test inequality."""
        arr1 = JalaliDatetimeArray._from_sequence(
            [
                JalaliTimestamp(1402, 1, 1),
                JalaliTimestamp(1402, 1, 2),
            ]
        )
        arr2 = JalaliDatetimeArray._from_sequence(
            [
                JalaliTimestamp(1402, 1, 1),
                JalaliTimestamp(1402, 1, 3),
            ]
        )
        result = arr1 != arr2
        expected = np.array([False, True])
        np.testing.assert_array_equal(result, expected)

    def test_eq_invalid_type(self):
        """Test equality with invalid type returns NotImplemented."""
        arr = JalaliDatetimeArray._from_sequence([JalaliTimestamp(1402, 1, 1)])
        result = arr.__eq__("invalid")
        assert result is NotImplemented


class TestJalaliDatetimeArrayConversion:
    """Tests for JalaliDatetimeArray conversion methods."""

    def test_to_gregorian(self):
        """Test to_gregorian method."""
        arr = JalaliDatetimeArray._from_sequence(
            [
                JalaliTimestamp(1402, 1, 1),
                JalaliTimestamp(1402, 6, 15),
            ]
        )
        result = arr.to_gregorian()
        assert isinstance(result, pd.DatetimeIndex)
        assert len(result) == 2
        assert result[0].year == 2023
        assert result[0].month == 3
        assert result[0].day == 21

    def test_to_gregorian_with_nat(self):
        """Test to_gregorian with NaT values."""
        arr = JalaliDatetimeArray._from_sequence(
            [
                JalaliTimestamp(1402, 1, 1),
                pd.NaT,
            ]
        )
        result = arr.to_gregorian()
        assert len(result) == 2
        assert pd.isna(result[1])

    def test_strftime(self):
        """Test strftime method."""
        arr = JalaliDatetimeArray._from_sequence(
            [
                JalaliTimestamp(1402, 1, 1),
                JalaliTimestamp(1402, 6, 15),
            ]
        )
        result = arr.strftime("%Y-%m-%d")
        assert result[0] == "1402-01-01"
        assert result[1] == "1402-06-15"

    def test_strftime_with_nat(self):
        """Test strftime with NaT values."""
        arr = JalaliDatetimeArray._from_sequence(
            [
                JalaliTimestamp(1402, 1, 1),
                pd.NaT,
            ]
        )
        result = arr.strftime("%Y-%m-%d")
        assert result[0] == "1402-01-01"
        assert result[1] is None


class TestJalaliDatetimeArrayRepr:
    """Tests for JalaliDatetimeArray string representation."""

    def test_repr_short(self):
        """Test repr with few elements."""
        arr = JalaliDatetimeArray._from_sequence(
            [
                JalaliTimestamp(1402, 1, 1),
                JalaliTimestamp(1402, 1, 2),
            ]
        )
        repr_str = repr(arr)
        assert "JalaliDatetimeArray" in repr_str

    def test_repr_long(self):
        """Test repr with many elements (truncated)."""
        timestamps = [JalaliTimestamp(1402, 1, i) for i in range(1, 11)]
        arr = JalaliDatetimeArray._from_sequence(timestamps)
        repr_str = repr(arr)
        assert "..." in repr_str
