"""Frequency alias registration for Jalali offsets.

This module provides frequency alias registration and parsing for Jalali
calendar offsets, enabling string-based frequency specifications like
"JME", "2JQE", etc.
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from jalali_pandas.offsets.base import JalaliOffset

# Registry of frequency aliases to offset classes
_JALALI_OFFSET_ALIASES: dict[str, type[JalaliOffset]] = {}

# Reverse mapping from offset class to alias
_JALALI_OFFSET_TO_ALIAS: dict[type[JalaliOffset], str] = {}


def register_jalali_alias(alias: str, offset_class: type[JalaliOffset]) -> None:
    """Register a frequency alias for a Jalali offset class.

    Args:
        alias: The frequency alias string (e.g., "JME", "JQS").
        offset_class: The offset class to register.
    """
    _JALALI_OFFSET_ALIASES[alias] = offset_class
    _JALALI_OFFSET_TO_ALIAS[offset_class] = alias


def get_jalali_offset(alias: str) -> type[JalaliOffset] | None:
    """Get the offset class for a frequency alias.

    Args:
        alias: The frequency alias string.

    Returns:
        The offset class, or None if not found.
    """
    return _JALALI_OFFSET_ALIASES.get(alias)


def get_jalali_alias(offset_class: type[JalaliOffset]) -> str | None:
    """Get the frequency alias for an offset class.

    Args:
        offset_class: The offset class.

    Returns:
        The frequency alias, or None if not registered.
    """
    return _JALALI_OFFSET_TO_ALIAS.get(offset_class)


def parse_jalali_frequency(freq_str: str) -> JalaliOffset:
    """Parse a frequency string into a Jalali offset instance.

    Supports formats like:
    - "JME" -> JalaliMonthEnd(n=1)
    - "2JME" -> JalaliMonthEnd(n=2)
    - "-1JQS" -> JalaliQuarterBegin(n=-1)

    Args:
        freq_str: The frequency string to parse.

    Returns:
        A Jalali offset instance.

    Raises:
        ValueError: If the frequency string is not recognized.
    """
    # Pattern: optional sign, optional number, alias
    pattern = r"^(-?)(\d*)([A-Z]+)$"
    match = re.match(pattern, freq_str.strip().upper())

    if not match:
        raise ValueError(f"Cannot parse frequency string: '{freq_str}'")

    sign, num_str, alias = match.groups()

    # Get the offset class
    offset_class = get_jalali_offset(alias)
    if offset_class is None:
        raise ValueError(f"Unknown Jalali frequency alias: '{alias}'")

    # Parse the multiplier
    n = int(num_str) if num_str else 1
    if sign == "-":
        n = -n

    return offset_class(n=n)


def list_jalali_aliases() -> dict[str, str]:
    """List all registered Jalali frequency aliases.

    Returns:
        Dictionary mapping aliases to offset class names.
    """
    return {alias: cls.__name__ for alias, cls in _JALALI_OFFSET_ALIASES.items()}


def _register_default_aliases() -> None:
    """Register the default Jalali frequency aliases.

    This is called automatically when the module is imported.
    """
    from jalali_pandas.offsets.month import JalaliMonthBegin, JalaliMonthEnd
    from jalali_pandas.offsets.quarter import JalaliQuarterBegin, JalaliQuarterEnd
    from jalali_pandas.offsets.week import JalaliWeek
    from jalali_pandas.offsets.year import JalaliYearBegin, JalaliYearEnd

    # Month offsets
    register_jalali_alias("JME", JalaliMonthEnd)
    register_jalali_alias("JMS", JalaliMonthBegin)

    # Quarter offsets
    register_jalali_alias("JQE", JalaliQuarterEnd)
    register_jalali_alias("JQS", JalaliQuarterBegin)

    # Year offsets
    register_jalali_alias("JYE", JalaliYearEnd)
    register_jalali_alias("JYS", JalaliYearBegin)

    # Week offsets
    register_jalali_alias("JW", JalaliWeek)


# Register default aliases on module import
_register_default_aliases()


__all__ = [
    "register_jalali_alias",
    "get_jalali_offset",
    "get_jalali_alias",
    "parse_jalali_frequency",
    "list_jalali_aliases",
]
