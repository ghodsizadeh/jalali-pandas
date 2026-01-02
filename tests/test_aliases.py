"""Tests for frequency alias registration."""

from __future__ import annotations

import pytest

from jalali_pandas.offsets import (
    JalaliMonthBegin,
    JalaliMonthEnd,
    JalaliQuarterBegin,
    JalaliQuarterEnd,
    JalaliYearBegin,
    JalaliYearEnd,
    get_jalali_alias,
    get_jalali_offset,
    list_jalali_aliases,
    parse_jalali_frequency,
)


class TestAliasRegistration:
    """Tests for alias registration functions."""

    def test_get_jalali_offset_month(self):
        """Test getting month offset classes by alias."""
        assert get_jalali_offset("JME") is JalaliMonthEnd
        assert get_jalali_offset("JMS") is JalaliMonthBegin

    def test_get_jalali_offset_quarter(self):
        """Test getting quarter offset classes by alias."""
        assert get_jalali_offset("JQE") is JalaliQuarterEnd
        assert get_jalali_offset("JQS") is JalaliQuarterBegin

    def test_get_jalali_offset_year(self):
        """Test getting year offset classes by alias."""
        assert get_jalali_offset("JYE") is JalaliYearEnd
        assert get_jalali_offset("JYS") is JalaliYearBegin

    def test_get_jalali_offset_unknown(self):
        """Test getting unknown alias returns None."""
        assert get_jalali_offset("UNKNOWN") is None
        assert get_jalali_offset("XYZ") is None

    def test_get_jalali_alias(self):
        """Test getting alias from offset class."""
        assert get_jalali_alias(JalaliMonthEnd) == "JME"
        assert get_jalali_alias(JalaliMonthBegin) == "JMS"
        assert get_jalali_alias(JalaliQuarterEnd) == "JQE"
        assert get_jalali_alias(JalaliQuarterBegin) == "JQS"
        assert get_jalali_alias(JalaliYearEnd) == "JYE"
        assert get_jalali_alias(JalaliYearBegin) == "JYS"

    def test_list_jalali_aliases(self):
        """Test listing all registered aliases."""
        aliases = list_jalali_aliases()
        assert "JME" in aliases
        assert "JMS" in aliases
        assert "JQE" in aliases
        assert "JQS" in aliases
        assert "JYE" in aliases
        assert "JYS" in aliases
        assert aliases["JME"] == "JalaliMonthEnd"


class TestParseJalaliFrequency:
    """Tests for frequency string parsing."""

    def test_parse_simple_alias(self):
        """Test parsing simple alias without multiplier."""
        offset = parse_jalali_frequency("JME")
        assert isinstance(offset, JalaliMonthEnd)
        assert offset.n == 1

    def test_parse_with_multiplier(self):
        """Test parsing alias with multiplier."""
        offset = parse_jalali_frequency("2JME")
        assert isinstance(offset, JalaliMonthEnd)
        assert offset.n == 2

        offset = parse_jalali_frequency("3JQS")
        assert isinstance(offset, JalaliQuarterBegin)
        assert offset.n == 3

    def test_parse_negative_multiplier(self):
        """Test parsing alias with negative multiplier."""
        offset = parse_jalali_frequency("-1JME")
        assert isinstance(offset, JalaliMonthEnd)
        assert offset.n == -1

        offset = parse_jalali_frequency("-2JYE")
        assert isinstance(offset, JalaliYearEnd)
        assert offset.n == -2

    def test_parse_large_multiplier(self):
        """Test parsing alias with large multiplier."""
        offset = parse_jalali_frequency("12JME")
        assert isinstance(offset, JalaliMonthEnd)
        assert offset.n == 12

    def test_parse_lowercase(self):
        """Test parsing lowercase alias (should be case-insensitive)."""
        offset = parse_jalali_frequency("jme")
        assert isinstance(offset, JalaliMonthEnd)
        assert offset.n == 1

    def test_parse_with_whitespace(self):
        """Test parsing alias with whitespace."""
        offset = parse_jalali_frequency("  JME  ")
        assert isinstance(offset, JalaliMonthEnd)
        assert offset.n == 1

    def test_parse_all_aliases(self):
        """Test parsing all registered aliases."""
        test_cases = [
            ("JME", JalaliMonthEnd),
            ("JMS", JalaliMonthBegin),
            ("JQE", JalaliQuarterEnd),
            ("JQS", JalaliQuarterBegin),
            ("JYE", JalaliYearEnd),
            ("JYS", JalaliYearBegin),
        ]
        for alias, expected_class in test_cases:
            offset = parse_jalali_frequency(alias)
            assert isinstance(offset, expected_class), f"Failed for {alias}"

    def test_parse_unknown_alias_raises(self):
        """Test that parsing unknown alias raises ValueError."""
        with pytest.raises(ValueError, match="Unknown Jalali frequency alias"):
            parse_jalali_frequency("UNKNOWN")

    def test_parse_invalid_format_raises(self):
        """Test that parsing invalid format raises ValueError."""
        with pytest.raises(ValueError, match="Cannot parse frequency string"):
            parse_jalali_frequency("123")

        with pytest.raises(ValueError, match="Cannot parse frequency string"):
            parse_jalali_frequency("")

        with pytest.raises(ValueError, match="Cannot parse frequency string"):
            parse_jalali_frequency("JME2")  # Number after alias
