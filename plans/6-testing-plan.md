# Testing Plan

## Testing Philosophy

1. **Comprehensive Coverage**: Every public API must have tests
2. **Edge Case Focus**: Calendar boundaries, leap years, NaT handling
3. **Property-Based Testing**: Use Hypothesis for invariant testing
4. **Performance Regression**: Track performance with benchmarks
5. **Cross-Version Compatibility**: Test against multiple pandas versions

---

## Test Categories

### 1. Unit Tests

Test individual components in isolation.

#### Core Module Tests

**`tests/core/test_timestamp.py`**
```python
class TestJalaliTimestampConstruction:
    """Test JalaliTimestamp creation."""

    def test_from_components(self):
        """Create from year, month, day, etc."""

    def test_from_string(self):
        """Parse from string with various formats."""

    def test_from_gregorian(self):
        """Convert from Gregorian datetime."""

    def test_now(self):
        """JalaliTimestamp.now() returns current time."""

    def test_today(self):
        """JalaliTimestamp.today() returns today at midnight."""

    def test_invalid_date_raises(self):
        """Invalid dates raise ValueError."""

    def test_out_of_range_raises(self):
        """Dates outside valid range raise OverflowError."""


class TestJalaliTimestampProperties:
    """Test JalaliTimestamp properties."""

    def test_year_month_day(self):
        """Basic date components."""

    def test_hour_minute_second(self):
        """Time components."""

    def test_microsecond_nanosecond(self):
        """Sub-second components."""

    def test_dayofweek(self):
        """Day of week (Saturday=0)."""

    def test_dayofyear(self):
        """Day of year (1-366)."""

    def test_weekofyear(self):
        """Week of year."""

    def test_quarter(self):
        """Quarter (1-4)."""

    def test_daysinmonth(self):
        """Days in current month."""

    def test_is_leap_year(self):
        """Leap year detection."""

    def test_is_month_start(self):
        """First day of month."""

    def test_is_month_end(self):
        """Last day of month."""

    def test_is_quarter_start(self):
        """First day of quarter."""

    def test_is_quarter_end(self):
        """Last day of quarter."""

    def test_is_year_start(self):
        """First day of year (1 Farvardin)."""

    def test_is_year_end(self):
        """Last day of year (29/30 Esfand)."""


class TestJalaliTimestampMethods:
    """Test JalaliTimestamp methods."""

    def test_to_gregorian(self):
        """Convert to Gregorian."""

    def test_strftime(self):
        """Format to string."""

    def test_isoformat(self):
        """ISO format string."""

    def test_date(self):
        """Extract date part."""

    def test_time(self):
        """Extract time part."""

    def test_normalize(self):
        """Set time to midnight."""

    def test_replace(self):
        """Replace components."""

    def test_floor(self):
        """Floor to frequency."""

    def test_ceil(self):
        """Ceil to frequency."""

    def test_round(self):
        """Round to frequency."""


class TestJalaliTimestampArithmetic:
    """Test arithmetic operations."""

    def test_add_timedelta(self):
        """Add pd.Timedelta."""

    def test_subtract_timedelta(self):
        """Subtract pd.Timedelta."""

    def test_subtract_timestamp(self):
        """Subtract another JalaliTimestamp."""

    def test_add_offset(self):
        """Add JalaliOffset."""


class TestJalaliTimestampComparison:
    """Test comparison operations."""

    def test_equality(self):
        """Equal timestamps."""

    def test_inequality(self):
        """Unequal timestamps."""

    def test_less_than(self):
        """Less than comparison."""

    def test_greater_than(self):
        """Greater than comparison."""

    def test_nat_comparison(self):
        """Comparison with NaT returns False."""


class TestJalaliTimestampTimezone:
    """Test timezone operations."""

    def test_tz_localize(self):
        """Localize naive timestamp."""

    def test_tz_convert(self):
        """Convert between timezones."""

    def test_tehran_timezone(self):
        """Asia/Tehran specific tests."""

    def test_dst_transitions(self):
        """DST transition handling."""
```

**`tests/core/test_arrays.py`**
```python
class TestJalaliDatetimeArrayConstruction:
    """Test array construction."""

    def test_from_sequence(self):
        """Create from sequence of timestamps."""

    def test_from_strings(self):
        """Create from sequence of strings."""

    def test_from_mixed(self):
        """Create from mixed types."""

    def test_with_nat(self):
        """Handle NaT values."""

    def test_empty_array(self):
        """Empty array creation."""


class TestJalaliDatetimeArrayProperties:
    """Test vectorized properties."""

    def test_year(self):
        """Vectorized year extraction."""

    def test_month(self):
        """Vectorized month extraction."""

    # ... all properties


class TestJalaliDatetimeArrayMethods:
    """Test vectorized methods."""

    def test_to_gregorian(self):
        """Vectorized Gregorian conversion."""

    def test_strftime(self):
        """Vectorized string formatting."""

    def test_normalize(self):
        """Vectorized normalization."""

    # ... all methods


class TestJalaliDatetimeArrayIndexing:
    """Test array indexing."""

    def test_getitem_int(self):
        """Integer indexing returns scalar."""

    def test_getitem_slice(self):
        """Slice indexing returns array."""

    def test_getitem_bool_mask(self):
        """Boolean mask indexing."""

    def test_setitem(self):
        """Item assignment."""


class TestJalaliDatetimeArrayNA:
    """Test NA handling."""

    def test_isna(self):
        """Detect NA values."""

    def test_dropna(self):
        """Drop NA values."""

    def test_fillna(self):
        """Fill NA values."""
```

**`tests/core/test_indexes.py`**
```python
class TestJalaliDatetimeIndexConstruction:
    """Test index construction."""

    def test_from_timestamps(self):
        """Create from timestamps."""

    def test_from_strings(self):
        """Create from strings."""

    def test_with_freq(self):
        """Create with frequency."""

    def test_infer_freq(self):
        """Infer frequency from data."""


class TestJalaliDatetimeIndexSlicing:
    """Test index slicing."""

    def test_string_indexing(self):
        """Index with string like '1402-06-15'."""

    def test_partial_string_month(self):
        """Partial string '1402-06' selects month."""

    def test_partial_string_year(self):
        """Partial string '1402' selects year."""

    def test_slice_strings(self):
        """Slice with string bounds."""

    def test_timestamp_indexing(self):
        """Index with JalaliTimestamp."""


class TestJalaliDatetimeIndexOperations:
    """Test index operations."""

    def test_union(self):
        """Union of indexes."""

    def test_intersection(self):
        """Intersection of indexes."""

    def test_difference(self):
        """Difference of indexes."""

    def test_shift(self):
        """Shift index."""

    def test_snap(self):
        """Snap to frequency."""
```

**`tests/core/test_conversion.py`**
```python
class TestJalaliGregorianConversion:
    """Test Jalali <-> Gregorian conversion."""

    def test_known_dates(self):
        """Test known date conversions."""
        # 1 Farvardin 1402 = 21 March 2023
        # 29 Esfand 1402 = 19 March 2024

    def test_roundtrip(self):
        """Jalali -> Gregorian -> Jalali is identity."""

    def test_leap_year_boundary(self):
        """Conversion around leap year boundaries."""

    def test_vectorized_conversion(self):
        """Vectorized conversion performance."""


class TestConversionEdgeCases:
    """Test edge cases in conversion."""

    def test_esfand_29_leap(self):
        """29 Esfand in leap year."""

    def test_esfand_30_leap(self):
        """30 Esfand in leap year."""

    def test_esfand_29_non_leap(self):
        """29 Esfand in non-leap year (last day)."""

    def test_farvardin_1(self):
        """1 Farvardin (Nowruz)."""
```

**`tests/core/test_calendar.py`**
```python
class TestJalaliCalendarRules:
    """Test Jalali calendar rules."""

    def test_month_lengths(self):
        """Months 1-6 have 31 days, 7-11 have 30, 12 has 29/30."""

    def test_leap_year_cycle(self):
        """Leap year follows 2820-year cycle."""

    def test_known_leap_years(self):
        """Test known leap years."""
        # 1399, 1403, 1408, ... are leap years

    def test_week_start(self):
        """Week starts on Saturday."""

    def test_quarter_definitions(self):
        """Q1: Farvardin-Khordad, Q2: Tir-Shahrivar, etc."""
```

#### Offset Tests

**`tests/offsets/test_month.py`**
```python
class TestJalaliMonthEnd:
    """Test JalaliMonthEnd offset."""

    def test_add_to_mid_month(self):
        """Adding to mid-month goes to month end."""

    def test_add_to_month_end(self):
        """Adding to month end goes to next month end."""

    def test_rollforward(self):
        """Roll forward to month end."""

    def test_rollback(self):
        """Roll back to previous month end."""

    def test_is_on_offset(self):
        """Check if date is on month end."""

    def test_month_31_days(self):
        """Months with 31 days (1-6)."""

    def test_month_30_days(self):
        """Months with 30 days (7-11)."""

    def test_esfand_leap(self):
        """Esfand in leap year (30 days)."""

    def test_esfand_non_leap(self):
        """Esfand in non-leap year (29 days)."""


class TestJalaliMonthBegin:
    """Test JalaliMonthBegin offset."""

    def test_add_to_mid_month(self):
        """Adding to mid-month goes to next month start."""

    def test_add_to_month_start(self):
        """Adding to month start goes to next month start."""

    def test_rollforward(self):
        """Roll forward to month start."""

    def test_rollback(self):
        """Roll back to current/previous month start."""
```

**`tests/offsets/test_quarter.py`**
```python
class TestJalaliQuarterEnd:
    """Test JalaliQuarterEnd offset."""

    def test_q1_end(self):
        """Q1 ends on 31 Khordad."""

    def test_q2_end(self):
        """Q2 ends on 31 Shahrivar."""

    def test_q3_end(self):
        """Q3 ends on 30 Azar."""

    def test_q4_end(self):
        """Q4 ends on 29/30 Esfand."""

    def test_rollforward(self):
        """Roll forward to quarter end."""

    def test_rollback(self):
        """Roll back to previous quarter end."""
```

**`tests/offsets/test_year.py`**
```python
class TestJalaliYearEnd:
    """Test JalaliYearEnd offset."""

    def test_year_end_leap(self):
        """Year end is 30 Esfand in leap year."""

    def test_year_end_non_leap(self):
        """Year end is 29 Esfand in non-leap year."""

    def test_rollforward(self):
        """Roll forward to year end."""

    def test_rollback(self):
        """Roll back to previous year end."""


class TestJalaliYearBegin:
    """Test JalaliYearBegin offset."""

    def test_year_begin(self):
        """Year begins on 1 Farvardin."""

    def test_rollforward(self):
        """Roll forward to year begin."""

    def test_rollback(self):
        """Roll back to current/previous year begin."""
```

**`tests/offsets/test_week.py`**
```python
class TestJalaliWeek:
    """Test JalaliWeek offset."""

    def test_default_saturday(self):
        """Default week ends on Friday (starts Saturday)."""

    def test_custom_weekday(self):
        """Custom week ending day."""

    def test_rollforward(self):
        """Roll forward to week end."""

    def test_rollback(self):
        """Roll back to previous week end."""
```

#### Accessor Tests

**`tests/accessors/test_series.py`**
```python
class TestJalaliSeriesAccessorConversion:
    """Test Series accessor conversion methods."""

    def test_to_jalali(self):
        """Convert Gregorian Series to Jalali."""

    def test_to_gregorian(self):
        """Convert Jalali Series to Gregorian."""

    def test_parse_jalali(self):
        """Parse string Series to Jalali."""

    def test_parse_jalali_formats(self):
        """Various format strings."""


class TestJalaliSeriesAccessorProperties:
    """Test Series accessor properties."""

    def test_year(self):
        """Extract year."""

    def test_month(self):
        """Extract month."""

    # ... all properties


class TestJalaliSeriesAccessorMethods:
    """Test Series accessor methods."""

    def test_strftime(self):
        """Format to string."""

    def test_normalize(self):
        """Normalize to midnight."""

    def test_floor(self):
        """Floor to frequency."""

    def test_ceil(self):
        """Ceil to frequency."""

    def test_round(self):
        """Round to frequency."""

    def test_month_name(self):
        """Get Persian month names."""

    def test_day_name(self):
        """Get Persian day names."""
```

**`tests/accessors/test_dataframe.py`**
```python
class TestJalaliDataFrameAccessorGroupby:
    """Test DataFrame accessor groupby."""

    def test_groupby_year(self):
        """Group by Jalali year."""

    def test_groupby_month(self):
        """Group by Jalali month."""

    def test_groupby_quarter(self):
        """Group by Jalali quarter."""

    def test_groupby_shortcuts(self):
        """Test ym, yq, ymd, md shortcuts."""

    def test_groupby_invalid(self):
        """Invalid groupby raises ValueError."""


class TestJalaliDataFrameAccessorResample:
    """Test DataFrame accessor resample."""

    def test_resample_month(self):
        """Resample to Jalali month."""

    def test_resample_quarter(self):
        """Resample to Jalali quarter."""

    def test_resample_year(self):
        """Resample to Jalali year."""

    def test_resample_aggregations(self):
        """Various aggregation methods."""
```

#### API Function Tests

**`tests/api/test_date_range.py`**
```python
class TestJalaliDateRange:
    """Test jalali_date_range function."""

    def test_start_periods(self):
        """Generate with start and periods."""

    def test_start_end(self):
        """Generate with start and end."""

    def test_end_periods(self):
        """Generate with end and periods."""

    def test_daily_freq(self):
        """Daily frequency."""

    def test_monthly_freq(self):
        """Monthly frequency (JME, JMS)."""

    def test_quarterly_freq(self):
        """Quarterly frequency (JQE, JQS)."""

    def test_yearly_freq(self):
        """Yearly frequency (JYE, JYS)."""

    def test_hourly_freq(self):
        """Hourly frequency."""

    def test_with_timezone(self):
        """Generate with timezone."""

    def test_normalize(self):
        """Normalize to midnight."""

    def test_inclusive(self):
        """Test inclusive parameter."""

    def test_invalid_params(self):
        """Invalid parameter combinations raise."""
```

**`tests/api/test_conversion.py`**
```python
class TestToJalaliDatetime:
    """Test to_jalali_datetime function."""

    def test_from_string(self):
        """Convert string to JalaliTimestamp."""

    def test_from_strings(self):
        """Convert string list to JalaliDatetimeIndex."""

    def test_from_series(self):
        """Convert Series to Jalali Series."""

    def test_from_datetime_index(self):
        """Convert DatetimeIndex to JalaliDatetimeIndex."""

    def test_format_parameter(self):
        """Custom format string."""

    def test_errors_raise(self):
        """errors='raise' raises on invalid."""

    def test_errors_coerce(self):
        """errors='coerce' returns NaT on invalid."""

    def test_errors_ignore(self):
        """errors='ignore' returns input on invalid."""
```

### 2. Integration Tests

Test components working together.

**`tests/integration/test_resample.py`**
```python
class TestResampleIntegration:
    """Test resampling with Jalali dates."""

    def test_resample_with_jalali_index(self):
        """Resample Series with JalaliDatetimeIndex."""

    def test_resample_with_jalali_column(self):
        """Resample DataFrame with Jalali column."""

    def test_resample_aggregations(self):
        """All aggregation methods work."""

    def test_resample_upsampling(self):
        """Upsampling with fill methods."""

    def test_resample_downsampling(self):
        """Downsampling aggregation."""

    def test_resample_closed_label(self):
        """closed and label parameters."""
```

**`tests/integration/test_groupby.py`**
```python
class TestGroupbyIntegration:
    """Test groupby with Jalali dates."""

    def test_groupby_jalali_grouper(self):
        """Use JalaliGrouper in groupby."""

    def test_groupby_multiple_groupers(self):
        """Multiple groupers including Jalali."""

    def test_groupby_transform(self):
        """Transform with Jalali groupby."""

    def test_groupby_apply(self):
        """Apply with Jalali groupby."""
```

**`tests/integration/test_io.py`**
```python
class TestIOIntegration:
    """Test I/O with Jalali dates."""

    def test_csv_roundtrip(self):
        """Write and read CSV with Jalali dates."""

    def test_parquet_roundtrip(self):
        """Write and read Parquet with Jalali dates."""

    def test_json_roundtrip(self):
        """Write and read JSON with Jalali dates."""

    def test_excel_roundtrip(self):
        """Write and read Excel with Jalali dates."""
```

### 3. Property-Based Tests (Hypothesis)

**`tests/test_properties.py`**
```python
from hypothesis import given, strategies as st

class TestJalaliTimestampProperties:
    """Property-based tests for JalaliTimestamp."""

    @given(st.integers(1, 1500), st.integers(1, 12), st.integers(1, 29))
    def test_roundtrip_conversion(self, year, month, day):
        """Jalali -> Gregorian -> Jalali is identity."""
        jts = JalaliTimestamp(year, month, day)
        roundtrip = JalaliTimestamp.from_gregorian(jts.to_gregorian())
        assert jts == roundtrip

    @given(st.integers(1300, 1500))
    def test_year_has_valid_days(self, year):
        """Every year has valid number of days."""
        days = 366 if JalaliTimestamp(year, 1, 1).is_leap_year else 365
        assert days in (365, 366)

    @given(st.integers(1300, 1500), st.integers(1, 12))
    def test_month_has_valid_days(self, year, month):
        """Every month has valid number of days."""
        jts = JalaliTimestamp(year, month, 1)
        days = jts.daysinmonth
        if month <= 6:
            assert days == 31
        elif month <= 11:
            assert days == 30
        else:
            assert days in (29, 30)
```

### 4. Performance Tests

**`tests/performance/benchmarks.py`**
```python
class TimestampBenchmarks:
    """Benchmark JalaliTimestamp operations."""

    def setup(self):
        self.timestamps = [JalaliTimestamp(1402, 6, i) for i in range(1, 29)]

    def time_construction(self):
        """Benchmark timestamp construction."""
        JalaliTimestamp(1402, 6, 15)

    def time_to_gregorian(self):
        """Benchmark Gregorian conversion."""
        for ts in self.timestamps:
            ts.to_gregorian()

    def time_properties(self):
        """Benchmark property access."""
        for ts in self.timestamps:
            _ = ts.year, ts.month, ts.day


class ArrayBenchmarks:
    """Benchmark JalaliDatetimeArray operations."""

    params = [100, 1000, 10000, 100000]

    def setup(self, n):
        self.array = JalaliDatetimeArray._from_sequence(
            [JalaliTimestamp(1402, 1, 1) + pd.Timedelta(days=i) for i in range(n)]
        )

    def time_year_extraction(self, n):
        """Benchmark vectorized year extraction."""
        _ = self.array.year

    def time_to_gregorian(self, n):
        """Benchmark vectorized Gregorian conversion."""
        _ = self.array.to_gregorian()
```

---

## Test Fixtures

**`tests/conftest.py`**
```python
import pytest
import pandas as pd
from jalali_pandas import JalaliTimestamp, JalaliDatetimeIndex, jalali_date_range


@pytest.fixture
def sample_jalali_timestamp():
    """A sample JalaliTimestamp for testing."""
    return JalaliTimestamp(1402, 6, 15, 14, 30, 0)


@pytest.fixture
def sample_jalali_index():
    """A sample JalaliDatetimeIndex for testing."""
    return jalali_date_range("1402-01-01", periods=100, freq="D")


@pytest.fixture
def sample_jalali_series(sample_jalali_index):
    """A sample Series with JalaliDatetimeIndex."""
    return pd.Series(range(100), index=sample_jalali_index)


@pytest.fixture
def sample_jalali_dataframe(sample_jalali_index):
    """A sample DataFrame with JalaliDatetimeIndex."""
    return pd.DataFrame({
        "value": range(100),
        "category": ["A", "B"] * 50,
    }, index=sample_jalali_index)


@pytest.fixture
def leap_years():
    """Known Jalali leap years."""
    return [1399, 1403, 1408, 1412, 1416, 1420, 1424]


@pytest.fixture
def non_leap_years():
    """Known Jalali non-leap years."""
    return [1400, 1401, 1402, 1404, 1405, 1406, 1407]


@pytest.fixture
def known_conversions():
    """Known Jalali <-> Gregorian conversions."""
    return [
        (JalaliTimestamp(1402, 1, 1), pd.Timestamp("2023-03-21")),
        (JalaliTimestamp(1402, 12, 29), pd.Timestamp("2024-03-19")),
        (JalaliTimestamp(1399, 12, 30), pd.Timestamp("2021-03-20")),  # Leap year
        (JalaliTimestamp(1400, 1, 1), pd.Timestamp("2021-03-21")),
    ]
```

---

## Coverage Goals

| Module | Target Coverage |
|--------|-----------------|
| `core/timestamp.py` | 95%+ |
| `core/arrays.py` | 95%+ |
| `core/dtypes.py` | 90%+ |
| `core/indexes.py` | 90%+ |
| `core/conversion.py` | 100% |
| `core/calendar.py` | 100% |
| `offsets/*` | 95%+ |
| `accessors/*` | 90%+ |
| `api/*` | 95%+ |
| **Overall** | **90%+** |

---

## CI Test Matrix

| Python | pandas | OS |
|--------|--------|-----|
| 3.9 | 2.0 | Ubuntu |
| 3.10 | 2.0, 2.1 | Ubuntu |
| 3.11 | 2.0, 2.1, 2.2 | Ubuntu, macOS, Windows |
| 3.12 | 2.1, 2.2 | Ubuntu, macOS, Windows |
| 3.13 | 2.2 | Ubuntu |

---

## Test Commands

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=jalali_pandas --cov-report=html

# Run specific test file
uv run pytest tests/core/test_timestamp.py

# Run specific test class
uv run pytest tests/core/test_timestamp.py::TestJalaliTimestampConstruction

# Run specific test
uv run pytest tests/core/test_timestamp.py::TestJalaliTimestampConstruction::test_from_components

# Run with verbose output
uv run pytest -v

# Run in parallel
uv run pytest -n auto

# Run only fast tests
uv run pytest -m "not slow"

# Run integration tests
uv run pytest -m integration

# Run property-based tests
uv run pytest tests/test_properties.py

# Run benchmarks
uv run asv run
```
