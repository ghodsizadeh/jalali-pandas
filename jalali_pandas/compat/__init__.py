"""Compatibility layer for jalali-pandas."""

from jalali_pandas.compat.legacy import (
    DeprecatedAlias,
    deprecated,
    emit_deprecation_warning,
)
from jalali_pandas.compat.pandas_compat import (
    PANDAS_VERSION,
    pandas_version_info,
)

__all__ = [
    "PANDAS_VERSION",
    "pandas_version_info",
    "deprecated",
    "DeprecatedAlias",
    "emit_deprecation_warning",
]
