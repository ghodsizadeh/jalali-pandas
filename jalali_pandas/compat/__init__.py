"""Compatibility layer for pandas versions and legacy API."""

from jalali_pandas.compat.pandas_compat import (
    PANDAS_VERSION,
    pandas_version_info,
)

__all__ = [
    "PANDAS_VERSION",
    "pandas_version_info",
]
