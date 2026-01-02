"""Tests for pandas compatibility layer."""

import pandas as pd

from jalali_pandas.compat.pandas_compat import (
    PANDAS_GE_20,
    PANDAS_GE_21,
    PANDAS_GE_22,
    PANDAS_VERSION,
    check_pandas_version,
    pandas_version_info,
)


class TestPandasVersionInfo:
    """Tests for pandas version detection."""

    def test_pandas_version_string(self):
        """Test PANDAS_VERSION is a string."""
        assert isinstance(PANDAS_VERSION, str)
        assert pd.__version__ == PANDAS_VERSION

    def test_pandas_version_info(self):
        """Test pandas_version_info returns tuple."""
        version = pandas_version_info()
        assert isinstance(version, tuple)
        assert len(version) == 3
        assert all(isinstance(v, int) for v in version)

    def test_version_flags(self):
        """Test version flags are boolean."""
        assert isinstance(PANDAS_GE_20, bool)
        assert isinstance(PANDAS_GE_21, bool)
        assert isinstance(PANDAS_GE_22, bool)

    def test_version_consistency(self):
        """Test version flags are consistent."""
        # If >= 2.2, must also be >= 2.1 and >= 2.0
        if PANDAS_GE_22:
            assert PANDAS_GE_21
            assert PANDAS_GE_20
        # If >= 2.1, must also be >= 2.0
        if PANDAS_GE_21:
            assert PANDAS_GE_20

    def test_check_pandas_version(self):
        """Test check_pandas_version doesn't raise for supported versions."""
        # Should not raise since we require pandas >= 2.0
        check_pandas_version()
