"""Tests for JalaliDatetimeDtype."""

import pytest

from jalali_pandas.core.arrays import JalaliDatetimeArray
from jalali_pandas.core.dtypes import JalaliDatetimeDtype


class TestJalaliDatetimeDtypeCreation:
    """Tests for JalaliDatetimeDtype creation."""

    def test_basic_creation(self):
        """Test basic dtype creation."""
        dtype = JalaliDatetimeDtype()
        assert dtype.name == "jalali_datetime"
        assert dtype.tz is None

    def test_creation_with_tz(self):
        """Test dtype creation with timezone."""
        dtype = JalaliDatetimeDtype(tz="Asia/Tehran")
        assert dtype.tz == "Asia/Tehran"

    def test_construct_from_string(self):
        """Test construct_from_string."""
        dtype = JalaliDatetimeDtype.construct_from_string("jalali_datetime")
        assert isinstance(dtype, JalaliDatetimeDtype)
        assert dtype.tz is None

    def test_construct_from_string_with_tz(self):
        """Test construct_from_string with timezone."""
        dtype = JalaliDatetimeDtype.construct_from_string(
            "jalali_datetime[Asia/Tehran]"
        )
        assert dtype.tz == "Asia/Tehran"

    def test_construct_from_string_empty_tz(self):
        """Test construct_from_string with empty timezone."""
        dtype = JalaliDatetimeDtype.construct_from_string("jalali_datetime[]")
        assert dtype.tz is None

    def test_construct_from_string_invalid(self):
        """Test construct_from_string with invalid string."""
        with pytest.raises(TypeError):
            JalaliDatetimeDtype.construct_from_string("invalid_dtype")

    def test_construct_from_string_not_string(self):
        """Test construct_from_string with non-string."""
        with pytest.raises(TypeError):
            JalaliDatetimeDtype.construct_from_string(123)


class TestJalaliDatetimeDtypeProperties:
    """Tests for JalaliDatetimeDtype properties."""

    def test_name(self):
        """Test name property."""
        dtype = JalaliDatetimeDtype()
        assert dtype.name == "jalali_datetime"

    def test_type(self):
        """Test type property."""
        dtype = JalaliDatetimeDtype()
        assert dtype.type is object

    def test_na_value(self):
        """Test na_value property."""
        import pandas as pd

        dtype = JalaliDatetimeDtype()
        assert dtype.na_value is pd.NaT

    def test_is_numeric(self):
        """Test _is_numeric property."""
        dtype = JalaliDatetimeDtype()
        assert dtype._is_numeric is False

    def test_is_boolean(self):
        """Test _is_boolean property."""
        dtype = JalaliDatetimeDtype()
        assert dtype._is_boolean is False

    def test_construct_array_type(self):
        """Test construct_array_type."""
        dtype = JalaliDatetimeDtype()
        array_type = dtype.construct_array_type()
        assert array_type is JalaliDatetimeArray


class TestJalaliDatetimeDtypeEquality:
    """Tests for JalaliDatetimeDtype equality and hashing."""

    def test_equality_same(self):
        """Test equality with same dtype."""
        dtype1 = JalaliDatetimeDtype()
        dtype2 = JalaliDatetimeDtype()
        assert dtype1 == dtype2

    def test_equality_same_tz(self):
        """Test equality with same timezone."""
        dtype1 = JalaliDatetimeDtype(tz="Asia/Tehran")
        dtype2 = JalaliDatetimeDtype(tz="Asia/Tehran")
        assert dtype1 == dtype2

    def test_equality_different_tz(self):
        """Test inequality with different timezone."""
        dtype1 = JalaliDatetimeDtype(tz="Asia/Tehran")
        dtype2 = JalaliDatetimeDtype(tz="UTC")
        assert dtype1 != dtype2

    def test_equality_with_string(self):
        """Test equality with string."""
        dtype = JalaliDatetimeDtype()
        assert dtype == "jalali_datetime"

    def test_equality_with_string_tz(self):
        """Test equality with string including timezone."""
        dtype = JalaliDatetimeDtype(tz="Asia/Tehran")
        assert dtype == "jalali_datetime[Asia/Tehran]"

    def test_equality_with_invalid_string(self):
        """Test inequality with invalid string."""
        dtype = JalaliDatetimeDtype()
        assert dtype != "invalid"

    def test_equality_with_other_type(self):
        """Test inequality with other type."""
        dtype = JalaliDatetimeDtype()
        assert dtype != 123
        assert dtype is not None

    def test_hash(self):
        """Test hash."""
        dtype1 = JalaliDatetimeDtype()
        dtype2 = JalaliDatetimeDtype()
        assert hash(dtype1) == hash(dtype2)

    def test_hash_with_tz(self):
        """Test hash with timezone."""
        dtype1 = JalaliDatetimeDtype(tz="Asia/Tehran")
        dtype2 = JalaliDatetimeDtype(tz="Asia/Tehran")
        assert hash(dtype1) == hash(dtype2)


class TestJalaliDatetimeDtypeRepr:
    """Tests for JalaliDatetimeDtype string representation."""

    def test_repr_no_tz(self):
        """Test repr without timezone."""
        dtype = JalaliDatetimeDtype()
        assert repr(dtype) == "jalali_datetime"
        assert str(dtype) == "jalali_datetime"

    def test_repr_with_tz(self):
        """Test repr with timezone."""
        dtype = JalaliDatetimeDtype(tz="Asia/Tehran")
        assert repr(dtype) == "jalali_datetime[Asia/Tehran]"
        assert str(dtype) == "jalali_datetime[Asia/Tehran]"
