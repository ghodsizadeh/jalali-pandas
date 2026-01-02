"""Pandas version compatibility utilities."""

from __future__ import annotations

import pandas as pd

# Pandas version information
PANDAS_VERSION: str = pd.__version__


def pandas_version_info() -> tuple[int, int, int]:
    """Get pandas version as a tuple of (major, minor, patch).

    Returns:
        Tuple of (major, minor, patch) version numbers.
    """
    parts = PANDAS_VERSION.split(".")
    major = int(parts[0])
    minor = int(parts[1])
    # Handle patch versions like "0rc1" or "0.dev"
    patch_str = parts[2] if len(parts) > 2 else "0"
    patch = int("".join(c for c in patch_str if c.isdigit()) or "0")
    return (major, minor, patch)


# Version checks
_version_info = pandas_version_info()
PANDAS_GE_20 = _version_info >= (2, 0, 0)
PANDAS_GE_21 = _version_info >= (2, 1, 0)
PANDAS_GE_22 = _version_info >= (2, 2, 0)


def check_pandas_version() -> None:
    """Check that pandas version is supported.

    Raises:
        ImportError: If pandas version is not supported.
    """
    if not PANDAS_GE_20:
        raise ImportError(
            f"jalali-pandas requires pandas >= 2.0.0, but found pandas {PANDAS_VERSION}"
        )


# Run version check on import
check_pandas_version()
