"""Tests for Jalali calendar offsets."""

from jalali_pandas import JalaliTimestamp
from jalali_pandas.offsets import (
    JalaliMonthBegin,
    JalaliMonthEnd,
    JalaliQuarterBegin,
    JalaliQuarterEnd,
    JalaliYearBegin,
    JalaliYearEnd,
)


class TestJalaliOffsetBase:
    """Tests for JalaliOffset base class."""

    def test_offset_properties(self):
        """Test basic offset properties."""
        offset = JalaliMonthEnd(n=2, normalize=True)
        assert offset.n == 2
        assert offset.normalize is True

    def test_offset_name(self):
        """Test offset name property."""
        offset = JalaliMonthEnd(n=2)
        assert "JME" in offset.name

    def test_offset_freqstr(self):
        """Test offset freqstr property."""
        offset = JalaliMonthEnd()
        assert offset.freqstr == offset.name

    def test_offset_repr(self):
        """Test offset repr."""
        offset = JalaliMonthEnd(n=2)
        assert "JalaliMonthEnd" in repr(offset)
        assert "n=2" in repr(offset)

    def test_offset_equality(self):
        """Test offset equality."""
        offset1 = JalaliMonthEnd(n=1)
        offset2 = JalaliMonthEnd(n=1)
        offset3 = JalaliMonthEnd(n=2)
        assert offset1 == offset2
        assert offset1 != offset3

    def test_offset_equality_different_types(self):
        """Test offset inequality with different types."""
        offset1 = JalaliMonthEnd(n=1)
        offset2 = JalaliMonthBegin(n=1)
        assert offset1 != offset2

    def test_offset_equality_non_offset(self):
        """Test offset inequality with non-offset."""
        offset = JalaliMonthEnd()
        assert offset != "JME"
        assert offset != 1

    def test_offset_hash(self):
        """Test offset hash."""
        offset1 = JalaliMonthEnd(n=1)
        offset2 = JalaliMonthEnd(n=1)
        assert hash(offset1) == hash(offset2)

    def test_offset_negation(self):
        """Test offset negation."""
        offset = JalaliMonthEnd(n=2)
        neg_offset = -offset
        assert neg_offset.n == -2

    def test_offset_multiplication(self):
        """Test offset multiplication."""
        offset = JalaliMonthEnd(n=1)
        result = offset * 3
        assert result.n == 3

    def test_offset_rmul(self):
        """Test offset right multiplication."""
        offset = JalaliMonthEnd(n=1)
        result = 3 * offset
        assert result.n == 3

    def test_offset_mul_invalid(self):
        """Test offset multiplication with invalid type."""
        offset = JalaliMonthEnd(n=1)
        result = offset.__mul__("invalid")
        assert result is NotImplemented


class TestJalaliMonthBegin:
    """Tests for JalaliMonthBegin offset."""

    def test_add_to_timestamp(self):
        """Test adding month begin offset."""
        ts = JalaliTimestamp(1402, 6, 15)
        offset = JalaliMonthBegin(n=1)
        result = offset + ts
        assert result.year == 1402
        assert result.month == 7
        assert result.day == 1

    def test_add_multiple_months(self):
        """Test adding multiple months."""
        ts = JalaliTimestamp(1402, 10, 15)
        offset = JalaliMonthBegin(n=5)
        result = offset + ts
        assert result.year == 1403
        assert result.month == 3
        assert result.day == 1

    def test_radd(self):
        """Test right add."""
        ts = JalaliTimestamp(1402, 6, 15)
        offset = JalaliMonthBegin(n=1)
        result = ts + offset
        assert result.month == 7
        assert result.day == 1

    def test_sub(self):
        """Test subtraction."""
        ts = JalaliTimestamp(1402, 6, 15)
        offset = JalaliMonthBegin(n=1)
        result = offset.__sub__(ts)
        assert result.month == 5
        assert result.day == 1

    def test_add_invalid_type(self):
        """Test add with invalid type."""
        offset = JalaliMonthBegin(n=1)
        result = offset.__add__("invalid")
        assert result is NotImplemented

    def test_rollforward_on_offset(self):
        """Test rollforward when already on offset."""
        ts = JalaliTimestamp(1402, 6, 1)
        offset = JalaliMonthBegin()
        result = offset.rollforward(ts)
        assert result == ts

    def test_rollforward_not_on_offset(self):
        """Test rollforward when not on offset."""
        ts = JalaliTimestamp(1402, 6, 15)
        offset = JalaliMonthBegin()
        result = offset.rollforward(ts)
        assert result.month == 7
        assert result.day == 1

    def test_rollback_on_offset(self):
        """Test rollback when already on offset."""
        ts = JalaliTimestamp(1402, 6, 1)
        offset = JalaliMonthBegin()
        result = offset.rollback(ts)
        assert result == ts

    def test_rollback_not_on_offset(self):
        """Test rollback when not on offset."""
        ts = JalaliTimestamp(1402, 6, 15)
        offset = JalaliMonthBegin()
        result = offset.rollback(ts)
        assert result.month == 6
        assert result.day == 1

    def test_is_on_offset(self):
        """Test is_on_offset."""
        offset = JalaliMonthBegin()
        assert offset.is_on_offset(JalaliTimestamp(1402, 6, 1)) is True
        assert offset.is_on_offset(JalaliTimestamp(1402, 6, 15)) is False

    def test_normalize(self):
        """Test normalize parameter."""
        ts = JalaliTimestamp(1402, 6, 15, 10, 30)
        offset = JalaliMonthBegin(n=1, normalize=True)
        result = offset + ts
        assert result.hour == 0
        assert result.minute == 0


class TestJalaliMonthEnd:
    """Tests for JalaliMonthEnd offset."""

    def test_add_to_timestamp(self):
        """Test adding month end offset."""
        ts = JalaliTimestamp(1402, 6, 15)
        offset = JalaliMonthEnd(n=1)
        result = offset + ts
        assert result.year == 1402
        assert result.month == 7
        assert result.day == 30  # Month 7 has 30 days

    def test_add_to_esfand(self):
        """Test adding to Esfand (handles leap year)."""
        ts = JalaliTimestamp(1402, 11, 15)
        offset = JalaliMonthEnd(n=1)
        result = offset + ts
        assert result.month == 12
        assert result.day == 29  # 1402 is not a leap year

    def test_add_to_esfand_leap(self):
        """Test adding to Esfand in leap year."""
        ts = JalaliTimestamp(1403, 11, 15)
        offset = JalaliMonthEnd(n=1)
        result = offset + ts
        assert result.month == 12
        assert result.day == 30  # 1403 is a leap year

    def test_rollforward_on_offset(self):
        """Test rollforward when already on offset."""
        ts = JalaliTimestamp(1402, 6, 31)
        offset = JalaliMonthEnd()
        result = offset.rollforward(ts)
        assert result == ts

    def test_rollforward_not_on_offset(self):
        """Test rollforward when not on offset."""
        ts = JalaliTimestamp(1402, 6, 15)
        offset = JalaliMonthEnd()
        result = offset.rollforward(ts)
        assert result.month == 6
        assert result.day == 31

    def test_rollback_on_offset(self):
        """Test rollback when already on offset."""
        ts = JalaliTimestamp(1402, 6, 31)
        offset = JalaliMonthEnd()
        result = offset.rollback(ts)
        assert result == ts

    def test_rollback_not_on_offset(self):
        """Test rollback when not on offset."""
        ts = JalaliTimestamp(1402, 6, 15)
        offset = JalaliMonthEnd()
        result = offset.rollback(ts)
        assert result.month == 5
        assert result.day == 31

    def test_rollback_first_month(self):
        """Test rollback in first month."""
        ts = JalaliTimestamp(1402, 1, 15)
        offset = JalaliMonthEnd()
        result = offset.rollback(ts)
        assert result.year == 1401
        assert result.month == 12

    def test_is_on_offset(self):
        """Test is_on_offset."""
        offset = JalaliMonthEnd()
        assert offset.is_on_offset(JalaliTimestamp(1402, 6, 31)) is True
        assert offset.is_on_offset(JalaliTimestamp(1402, 6, 15)) is False


class TestJalaliQuarterBegin:
    """Tests for JalaliQuarterBegin offset."""

    def test_add_to_timestamp(self):
        """Test adding quarter begin offset."""
        ts = JalaliTimestamp(1402, 2, 15)
        offset = JalaliQuarterBegin(n=1)
        result = offset + ts
        assert result.month == 4
        assert result.day == 1

    def test_add_multiple_quarters(self):
        """Test adding multiple quarters."""
        ts = JalaliTimestamp(1402, 1, 15)
        offset = JalaliQuarterBegin(n=4)
        result = offset + ts
        assert result.year == 1403
        assert result.month == 1
        assert result.day == 1

    def test_rollforward_on_offset(self):
        """Test rollforward when on offset."""
        ts = JalaliTimestamp(1402, 1, 1)
        offset = JalaliQuarterBegin()
        result = offset.rollforward(ts)
        assert result == ts

    def test_rollforward_not_on_offset(self):
        """Test rollforward when not on offset."""
        ts = JalaliTimestamp(1402, 2, 15)
        offset = JalaliQuarterBegin()
        result = offset.rollforward(ts)
        assert result.month == 4
        assert result.day == 1

    def test_rollback_on_offset(self):
        """Test rollback when on offset."""
        ts = JalaliTimestamp(1402, 4, 1)
        offset = JalaliQuarterBegin()
        result = offset.rollback(ts)
        assert result == ts

    def test_rollback_not_on_offset(self):
        """Test rollback when not on offset."""
        ts = JalaliTimestamp(1402, 5, 15)
        offset = JalaliQuarterBegin()
        result = offset.rollback(ts)
        assert result.month == 4
        assert result.day == 1

    def test_is_on_offset(self):
        """Test is_on_offset."""
        offset = JalaliQuarterBegin()
        assert offset.is_on_offset(JalaliTimestamp(1402, 1, 1)) is True
        assert offset.is_on_offset(JalaliTimestamp(1402, 4, 1)) is True
        assert offset.is_on_offset(JalaliTimestamp(1402, 7, 1)) is True
        assert offset.is_on_offset(JalaliTimestamp(1402, 10, 1)) is True
        assert offset.is_on_offset(JalaliTimestamp(1402, 2, 1)) is False


class TestJalaliQuarterEnd:
    """Tests for JalaliQuarterEnd offset."""

    def test_add_to_timestamp(self):
        """Test adding quarter end offset."""
        ts = JalaliTimestamp(1402, 2, 15)
        offset = JalaliQuarterEnd(n=1)
        result = offset + ts
        assert result.month == 6
        assert result.day == 31

    def test_add_to_q4(self):
        """Test adding to Q4 (goes to next year Q1 end)."""
        ts = JalaliTimestamp(1402, 10, 15)
        offset = JalaliQuarterEnd(n=1)
        result = offset + ts
        # Adding 1 quarter from Q4 goes to Q1 of next year
        assert result.year == 1403
        assert result.month == 3
        assert result.day == 31

    def test_rollforward_on_offset(self):
        """Test rollforward when on offset."""
        ts = JalaliTimestamp(1402, 3, 31)
        offset = JalaliQuarterEnd()
        result = offset.rollforward(ts)
        assert result == ts

    def test_rollforward_not_on_offset(self):
        """Test rollforward when not on offset."""
        ts = JalaliTimestamp(1402, 2, 15)
        offset = JalaliQuarterEnd()
        result = offset.rollforward(ts)
        assert result.month == 3
        assert result.day == 31

    def test_rollback_on_offset(self):
        """Test rollback when on offset."""
        ts = JalaliTimestamp(1402, 6, 31)
        offset = JalaliQuarterEnd()
        result = offset.rollback(ts)
        assert result == ts

    def test_rollback_not_on_offset(self):
        """Test rollback when not on offset."""
        ts = JalaliTimestamp(1402, 5, 15)
        offset = JalaliQuarterEnd()
        result = offset.rollback(ts)
        assert result.month == 3
        assert result.day == 31

    def test_rollback_first_quarter(self):
        """Test rollback in first quarter."""
        ts = JalaliTimestamp(1402, 2, 15)
        offset = JalaliQuarterEnd()
        result = offset.rollback(ts)
        assert result.year == 1401
        assert result.month == 12

    def test_is_on_offset(self):
        """Test is_on_offset."""
        offset = JalaliQuarterEnd()
        assert offset.is_on_offset(JalaliTimestamp(1402, 3, 31)) is True
        assert offset.is_on_offset(JalaliTimestamp(1402, 6, 31)) is True
        assert offset.is_on_offset(JalaliTimestamp(1402, 9, 30)) is True
        assert offset.is_on_offset(JalaliTimestamp(1402, 12, 29)) is True
        assert offset.is_on_offset(JalaliTimestamp(1402, 2, 28)) is False


class TestJalaliYearBegin:
    """Tests for JalaliYearBegin offset."""

    def test_add_to_timestamp(self):
        """Test adding year begin offset."""
        ts = JalaliTimestamp(1402, 6, 15)
        offset = JalaliYearBegin(n=1)
        result = offset + ts
        assert result.year == 1403
        assert result.month == 1
        assert result.day == 1

    def test_add_multiple_years(self):
        """Test adding multiple years."""
        ts = JalaliTimestamp(1402, 6, 15)
        offset = JalaliYearBegin(n=3)
        result = offset + ts
        assert result.year == 1405
        assert result.month == 1
        assert result.day == 1

    def test_rollforward_on_offset(self):
        """Test rollforward when on offset (Nowruz)."""
        ts = JalaliTimestamp(1402, 1, 1)
        offset = JalaliYearBegin()
        result = offset.rollforward(ts)
        assert result == ts

    def test_rollforward_not_on_offset(self):
        """Test rollforward when not on offset."""
        ts = JalaliTimestamp(1402, 6, 15)
        offset = JalaliYearBegin()
        result = offset.rollforward(ts)
        assert result.year == 1403
        assert result.month == 1
        assert result.day == 1

    def test_rollback_on_offset(self):
        """Test rollback when on offset."""
        ts = JalaliTimestamp(1402, 1, 1)
        offset = JalaliYearBegin()
        result = offset.rollback(ts)
        assert result == ts

    def test_rollback_not_on_offset(self):
        """Test rollback when not on offset."""
        ts = JalaliTimestamp(1402, 6, 15)
        offset = JalaliYearBegin()
        result = offset.rollback(ts)
        assert result.year == 1402
        assert result.month == 1
        assert result.day == 1

    def test_is_on_offset(self):
        """Test is_on_offset."""
        offset = JalaliYearBegin()
        assert offset.is_on_offset(JalaliTimestamp(1402, 1, 1)) is True
        assert offset.is_on_offset(JalaliTimestamp(1402, 1, 2)) is False
        assert offset.is_on_offset(JalaliTimestamp(1402, 2, 1)) is False


class TestJalaliYearEnd:
    """Tests for JalaliYearEnd offset."""

    def test_add_to_timestamp(self):
        """Test adding year end offset."""
        ts = JalaliTimestamp(1402, 6, 15)
        offset = JalaliYearEnd(n=1)
        result = offset + ts
        assert result.year == 1403
        assert result.month == 12
        assert result.day == 30  # 1403 is a leap year

    def test_add_non_leap_year(self):
        """Test adding to non-leap year."""
        ts = JalaliTimestamp(1401, 6, 15)
        offset = JalaliYearEnd(n=1)
        result = offset + ts
        assert result.year == 1402
        assert result.month == 12
        assert result.day == 29  # 1402 is not a leap year

    def test_rollforward_on_offset(self):
        """Test rollforward when on offset."""
        ts = JalaliTimestamp(1402, 12, 29)
        offset = JalaliYearEnd()
        result = offset.rollforward(ts)
        assert result == ts

    def test_rollforward_not_on_offset(self):
        """Test rollforward when not on offset."""
        ts = JalaliTimestamp(1402, 6, 15)
        offset = JalaliYearEnd()
        result = offset.rollforward(ts)
        assert result.year == 1402
        assert result.month == 12
        assert result.day == 29

    def test_rollback_on_offset(self):
        """Test rollback when on offset."""
        ts = JalaliTimestamp(1402, 12, 29)
        offset = JalaliYearEnd()
        result = offset.rollback(ts)
        assert result == ts

    def test_rollback_not_on_offset(self):
        """Test rollback when not on offset."""
        ts = JalaliTimestamp(1402, 6, 15)
        offset = JalaliYearEnd()
        result = offset.rollback(ts)
        assert result.year == 1401
        assert result.month == 12

    def test_is_on_offset(self):
        """Test is_on_offset."""
        offset = JalaliYearEnd()
        assert offset.is_on_offset(JalaliTimestamp(1402, 12, 29)) is True
        assert offset.is_on_offset(JalaliTimestamp(1403, 12, 30)) is True
        assert offset.is_on_offset(JalaliTimestamp(1402, 12, 28)) is False
        assert offset.is_on_offset(JalaliTimestamp(1402, 11, 30)) is False
