# Implementation Roadmap

## Overview

This document outlines the phased implementation plan for building full Jalali calendar support in pandas. Each phase builds on the previous one, with clear milestones and deliverables.

---

## Current Status (Updated: 2026-01-02)

**Test Coverage: 86%** (Target: 90%+)

### Phase 0: Foundation - ✅ COMPLETE
- All infrastructure tasks completed
- Calendar rules module with comprehensive tests

### Phase 1: Core Types - ✅ COMPLETE
- JalaliTimestamp fully functional
- JalaliDatetimeDtype registered with pandas
- JalaliDatetimeArray with all required methods
- JalaliNaT singleton for NaT handling
- Timezone support (tz_localize, tz_convert)
- Conversion module with vectorized operations

### Phase 2: Index & Range Generation - ✅ COMPLETE
- JalaliDatetimeIndex with full functionality
- jalali_date_range() for generating date ranges
- to_jalali_datetime() and to_gregorian_datetime() conversion functions
- String and partial string indexing support
- Set operations (union, intersection, difference)
- Shift and snap operations

### Phase 3: Frequency Offsets - ✅ COMPLETE
- Base offset class implemented
- Month, Quarter, Year offsets working
- Week offset (JalaliWeek) with custom weekday support
- Frequency alias registration (JME, JMS, JQE, JQS, JYE, JYS, JW)
- parse_jalali_frequency() for string parsing

### Phase 4: Time Series Operations - ✅ COMPLETE
- JalaliGrouper class for Jalali calendar-based grouping
- JalaliResampler class for resampling with Jalali boundaries
- resample_jalali() function for easy resampling
- DataFrame accessor resample() method (month, quarter, year)
- Rolling/expanding operations work with Gregorian index
- Shifting works with JalaliDatetimeIndex and Timedelta/JalaliOffset
- Comprehensive tests for all time series operations

### Phase 5: Enhanced Accessors - ✅ COMPLETE
- JalaliSeriesAccessor with all properties (dayofyear, daysinmonth, is_* flags)
- JalaliSeriesAccessor with all methods (strftime, normalize, floor/ceil/round, tz_localize/tz_convert, month_name/day_name)
- JalaliDataFrameAccessor with enhanced groupby, resample, convert_columns, filter methods
- Full type annotations on both accessors
- 76 new tests for accessor functionality

### Examples Created
- `examples/01_basic_usage.py` - JalaliTimestamp basics
- `examples/02_series_operations.py` - Series accessor usage
- `examples/03_dataframe_operations.py` - DataFrame groupby
- `examples/04_offsets.py` - Calendar offsets (updated with week offset and aliases)
- `examples/05_index_and_date_range.py` - JalaliDatetimeIndex and date range generation

---

## Phase 0: Foundation (Week 1-2)

### Goals
- Set up modern project infrastructure
- Establish type system foundation

### Tasks

#### 0.1 Project Infrastructure
- [x] Update `pyproject.toml` with new dependencies and configuration
- [x] Add `py.typed` marker
- [x] Configure mypy and pyright and (Astral ty)
- [x] Set up ruff for linting/formatting
- [x] Update pre-commit hooks
- [x] Set up GitHub Actions CI pipeline

#### 0.2 Type System Foundation
- [x] Create `jalali_pandas/_typing.py` with type aliases
- [x] Define protocols for Jalali types
- [x] Add type stubs for jdatetime if needed (not needed - jdatetime has inline types)

#### 0.3 Calendar Rules Module
- [x] Create `jalali_pandas/core/calendar.py`
- [x] Implement leap year detection (2820-year cycle)
- [x] Implement month length calculation
- [x] Define week start (Saturday) and quarter boundaries
- [x] Add comprehensive tests for calendar rules
  - Completed: tests/test_calendar.py with 90%+ coverage

### Deliverables
- Modern project setup with CI/CD
- Type checking passes
- Calendar rules with 100% test coverage

---

## Phase 1: Core Types (Week 3-5)

### Goals
- Implement `JalaliTimestamp` scalar
- Implement `JalaliDatetimeDtype`
- Implement `JalaliDatetimeArray`

### Tasks

#### 1.1 JalaliTimestamp Scalar
- [x] Create `jalali_pandas/core/timestamp.py`
- [x] Implement construction from components
- [x] Implement construction from string (parsing)
- [x] Implement `from_gregorian()` class method
- [x] Implement `to_gregorian()` method
- [x] Implement all properties (year, month, day, etc.)
- [x] Implement all boolean properties (is_leap_year, is_month_end, etc.)
- [x] Implement `strftime()` method
- [x] Implement `normalize()`, `floor()`, `ceil()`, `round()`
- [x] Implement `replace()` method
- [x] Implement arithmetic operators (+, -, with Timedelta)
- [x] Implement comparison operators
- [x] Implement `__hash__` for use as dict key
- [x] Add NaT handling (JalaliNaT singleton, isna_jalali helper)
- [x] Add timezone support (tz_localize, tz_convert)

#### 1.2 Conversion Module
- [x] Create `jalali_pandas/core/conversion.py`
- [x] Implement scalar Jalali → Gregorian conversion
- [x] Implement scalar Gregorian → Jalali conversion
- [x] Implement vectorized conversions using NumPy
- [x] Optimize with lookup tables for common ranges (using jdatetime)
- [x] Add comprehensive round-trip tests

#### 1.3 JalaliDatetimeDtype
- [x] Create `jalali_pandas/core/dtypes.py`
- [x] Inherit from `pandas.api.extensions.ExtensionDtype`
- [x] Implement `name` property
- [x] Implement `type` property (returns JalaliTimestamp)
- [x] Implement `na_value` (returns pd.NaT)
- [x] Implement `construct_array_type()`
- [x] Implement `construct_from_string()`
- [x] Register dtype with pandas

#### 1.4 JalaliDatetimeArray
- [x] Create `jalali_pandas/core/arrays.py`
- [x] Inherit from `pandas.api.extensions.ExtensionArray`
- [x] Choose internal storage format (int64 nanoseconds)
- [x] Implement `_from_sequence()`
- [x] Implement `_from_sequence_of_strings()`
- [x] Implement `_from_factorized()`
- [x] Implement `__len__`, `__getitem__`, `__setitem__`
- [x] Implement `__iter__`
- [x] Implement `isna()`
- [x] Implement `copy()`
- [x] Implement `_concat_same_type()`
- [x] Implement vectorized properties (year, month, etc.)
- [x] Implement vectorized methods (strftime, normalize, etc.)
- [x] Implement `to_gregorian()` returning DatetimeArray
  - Completed: tests/test_arrays.py with comprehensive tests

### Deliverables
- Working `JalaliTimestamp` with full functionality
- Working `JalaliDatetimeArray` for Series storage
- Pandas recognizes `jalali_datetime64[ns]` dtype

---

## Phase 2: Index & Range Generation (Week 6-7)

### Goals
- Implement `JalaliDatetimeIndex`
- Implement `jalali_date_range()`
- Enable time series indexing

### Tasks

#### 2.1 JalaliDatetimeIndex
- [x] Create `jalali_pandas/core/indexes.py`
- [x] Inherit from `pandas.Index`
- [x] Wrap `JalaliDatetimeArray` as `_data`
- [x] Implement construction from various inputs
- [x] Implement `freq` property
- [x] Implement frequency inference
- [x] Implement string indexing ("1402-06-15")
- [x] Implement partial string indexing ("1402-06", "1402")
- [x] Implement slice indexing
- [x] Implement `shift()` method
- [x] Implement `snap()` method
- [x] Implement set operations (union, intersection, difference)
- [x] Implement `to_gregorian()` returning DatetimeIndex

#### 2.2 Date Range Generation
- [x] Create `jalali_pandas/api/date_range.py`
- [x] Implement `jalali_date_range()` function
- [x] Support start/end/periods combinations
- [x] Support all frequency strings (D, h, min, s, JME, JQE, JYE, etc.)
- [x] Support timezone parameter
- [x] Support normalize parameter
- [x] Support inclusive parameter
- [x] Validate parameter combinations

#### 2.3 Conversion Functions
- [x] Create `jalali_pandas/api/conversion.py`
- [x] Implement `to_jalali_datetime()` function
- [x] Support string, list, Series, DatetimeIndex inputs
- [x] Support format parameter
- [x] Support errors parameter (raise, coerce, ignore)
- [x] Implement `to_gregorian_datetime()` function

### Deliverables
- Working `JalaliDatetimeIndex` for time series
- `jalali_date_range()` generates Jalali date ranges
- Conversion functions work with all input types

---

## Phase 3: Frequency Offsets (Week 8-9)

### Goals
- Implement Jalali-aware frequency offsets
- Enable resampling and shifting with Jalali boundaries

### Tasks

#### 3.1 Base Offset
- [x] Create `jalali_pandas/offsets/base.py`
- [x] Implement `JalaliOffset` base class
- [x] Define interface: `__add__`, `__radd__`, `rollforward`, `rollback`, `is_on_offset`
- [x] Implement `n` multiplier support
- [x] Implement `normalize` parameter
  - Completed: tests/test_offsets.py with comprehensive tests

#### 3.2 Month Offsets
- [x] Create `jalali_pandas/offsets/month.py`
- [x] Implement `JalaliMonthEnd`
  - Handle 31-day months (1-6)
  - Handle 30-day months (7-11)
  - Handle Esfand (29 or 30 days)
- [x] Implement `JalaliMonthBegin`
- [x] Register frequency aliases ("JME", "JMS")

#### 3.3 Quarter Offsets
- [x] Create `jalali_pandas/offsets/quarter.py`
- [x] Implement `JalaliQuarterEnd`
  - Q1 ends 31 Khordad
  - Q2 ends 31 Shahrivar
  - Q3 ends 30 Azar
  - Q4 ends 29/30 Esfand
- [x] Implement `JalaliQuarterBegin`
- [x] Register frequency aliases ("JQE", "JQS")

#### 3.4 Year Offsets
- [x] Create `jalali_pandas/offsets/year.py`
- [x] Implement `JalaliYearEnd` (29/30 Esfand)
- [x] Implement `JalaliYearBegin` (1 Farvardin)
- [x] Register frequency aliases ("JYE", "JYS")

#### 3.5 Week Offset
- [x] Create `jalali_pandas/offsets/week.py`
- [x] Implement `JalaliWeek` (Saturday-based by default)
- [x] Support custom weekday parameter
- [x] Register frequency alias ("JW")

#### 3.6 Offset Integration
- [x] Create `jalali_pandas/offsets/__init__.py`
- [x] Create `jalali_pandas/offsets/aliases.py` for frequency registration
- [x] Enable string frequency parsing ("JME", "2JME", etc.)

### Deliverables
- All Jalali offsets working
- Offsets integrate with pandas frequency system
- String aliases work everywhere

---

## Phase 4: Time Series Operations (Week 10-12)

### Goals
- Implement resampling with Jalali boundaries
- Implement groupby with Jalali components
- Implement rolling/shifting with Jalali offsets

### Tasks

#### 4.1 Resampling
- [x] Implement `resample_jalali()` function for Jalali-aware resampling
- [x] Test all aggregation methods (mean, sum, min, max, etc.)
- [x] Test upsampling with fill methods
- [x] Test downsampling
- [x] Test closed/label parameters
- [x] Document limitations: pandas resample() doesn't accept custom JalaliOffset directly; use resample_jalali() instead

#### 4.2 JalaliGrouper
- [x] Create `jalali_pandas/api/grouper.py`
- [x] Implement `JalaliGrouper` class
- [x] Support `key` parameter for column-based grouping
- [x] Support `freq` parameter for frequency-based grouping
- [x] Integrate with `DataFrame.groupby()` via `get_grouper()` method

#### 4.3 DataFrame Accessor Resample
- [x] Update `JalaliDataFrameAccessor.resample()`
- [x] Remove `NotImplementedError`
- [x] Implement using groupby internally (month, quarter, year)
- [x] Support resample parameters: month, quarter, year

#### 4.4 Rolling/Expanding
- [x] Test rolling with Timedelta windows (works with Gregorian index)
- [x] Test expanding operations
- [x] Document limitations: rolling requires Gregorian DatetimeIndex

#### 4.5 Shifting
- [x] Test `Series.shift(freq=Timedelta)` with Gregorian index
- [x] Test `DataFrame.shift(freq=Timedelta)` with Gregorian index
- [x] Test `JalaliDatetimeIndex.shift()` with JalaliOffset and Timedelta

### Deliverables
- Full resampling support with Jalali boundaries via `resample_jalali()`
- JalaliGrouper for flexible grouping
- Rolling/shifting work with Jalali offsets

### Completion Notes (2026-01-02)
- Created `jalali_pandas/api/grouper.py` with JalaliGrouper and JalaliResampler classes
- Added `resample_jalali()` function for easy Jalali-aware resampling
- Updated DataFrame accessor `resample()` to support month/quarter/year grouping
- Added `refs` parameter to `JalaliDatetimeIndex._simple_new()` for pandas compatibility
- 27 new tests in `tests/test_time_series.py`
- Total: 393 tests passing, 86% coverage

---

## Phase 5: Enhanced Accessors (Week 13-14)

### Goals
- Enhance Series accessor with all properties/methods
- Enhance DataFrame accessor

### Tasks

#### 5.1 Series Accessor Enhancement
- [x] Update `jalali_pandas/accessors/series.py`
- [x] Add all missing properties (dayofyear, daysinmonth, is_* flags)
- [x] Add `strftime()` method
- [x] Add `normalize()` method
- [x] Add `floor()`, `ceil()`, `round()` methods
- [x] Add `tz_localize()`, `tz_convert()` methods
- [x] Add `month_name()`, `day_name()` methods
- [x] Add `date`, `time` properties
- [x] Add full type annotations

#### 5.2 DataFrame Accessor Enhancement
- [x] Update `jalali_pandas/accessors/dataframe.py`
- [x] Add `set_date_column()` method
- [x] Update `groupby()` to use new infrastructure
- [x] Implement `resample()` properly
- [x] Add `convert_columns()` method
- [x] Add full type annotations

### Deliverables
- Feature-complete accessors
- Full type annotations

### Completion Notes (2026-01-02)
- Created `jalali_pandas/accessors/series.py` with JalaliSeriesAccessor class
- Created `jalali_pandas/accessors/dataframe.py` with JalaliDataFrameAccessor class
- Series accessor includes: all date/time properties, boolean flags (is_leap_year, is_month_start, etc.), strftime, normalize, floor/ceil/round, month_name/day_name, tz_localize/tz_convert
- DataFrame accessor includes: set_date_column, groupby (extended), resample, convert_columns, to_period, filter_by_year/month/quarter/date_range
- 76 new tests in `tests/test_accessors.py`
- Total: 469 tests passing, 83% coverage

---

## Phase 6: Testing & Performance (Week 15-16)

### Goals
- Achieve 90%+ test coverage
- Optimize performance
- Add benchmarks

### Tasks

#### 6.1 Test Coverage
- [ ] Write unit tests for all modules
- [ ] Write integration tests
- [ ] Write property-based tests with Hypothesis
- [ ] Achieve 90%+ coverage
- [ ] Test edge cases (leap years, month boundaries, NaT)

#### 6.2 Performance Optimization
- [ ] Profile conversion operations
- [ ] Optimize vectorized operations
- [ ] Consider Cython for hot paths (future)
- [ ] Add lookup tables for common date ranges

#### 6.3 Benchmarks
- [ ] Set up ASV benchmark suite
- [ ] Benchmark timestamp construction
- [ ] Benchmark conversions
- [ ] Benchmark array operations
- [ ] Benchmark resampling

### Deliverables
- 90%+ test coverage
- Performance benchmarks
- Optimized hot paths

---

## Phase 7: Documentation & Release (Week 17-18)

### Goals
- Complete documentation
- Prepare v1.0 release

### Tasks

#### 7.1 Documentation
- [ ] Set up MkDocs with Material theme
- [ ] Write home page
- [ ] Write installation guide
- [ ] Write quickstart tutorial
- [ ] Write user guide sections
- [ ] Generate API reference
- [ ] Add examples
- [ ] Deploy to GitHub Pages

#### 7.2 Release Preparation
- [ ] Update CHANGELOG.md
- [ ] Update README.md
- [ ] Create release notes
- [ ] Test PyPI upload (TestPyPI)
- [ ] Tag v1.0.0 release
- [ ] Publish to PyPI

#### 7.3 Announcement
- [ ] Write blog post / announcement
- [ ] Update Persian documentation
- [ ] Create demo notebook

### Deliverables
- Complete documentation site
- v1.0.0 released on PyPI
- Announcement published

---

## Timeline Summary

| Phase | Duration | Focus |
|-------|----------|-------|
| Phase 0 | Week 1-2 | Foundation & Infrastructure |
| Phase 1 | Week 3-5 | Core Types (Timestamp, Array, Dtype) |
| Phase 2 | Week 6-7 | Index & Date Range |
| Phase 3 | Week 8-9 | Frequency Offsets |
| Phase 4 | Week 10-12 | Time Series Operations |
| Phase 5 | Week 13-14 | Enhanced Accessors |
| Phase 6 | Week 15-16 | Testing & Performance |
| Phase 7 | Week 17-18 | Documentation & Release |

**Total: ~18 weeks to v1.0**

---

## Risk Mitigation

### Technical Risks

| Risk | Mitigation |
|------|------------|
| pandas ExtensionArray limitations | Research early, design around limitations |
| Performance overhead | Profile early, optimize iteratively |
| Timezone edge cases | Delegate to pandas for tz ops, test thoroughly |

### Schedule Risks

| Risk | Mitigation |
|------|------------|
| Scope creep | Strict MVP focus, defer nice-to-haves |
| Underestimated complexity | Buffer time in each phase |
| Testing takes longer | Parallelize test writing with development |

---

## Success Metrics

### v1.0 Release Criteria

- [ ] All core types implemented and tested
- [ ] All frequency offsets working
- [ ] Resampling works with Jalali boundaries
- [ ] 90%+ test coverage
- [ ] Type checking passes (mypy strict)
- [ ] Documentation complete
- [ ] Performance acceptable (benchmarked)

### Post-Release Goals

- [ ] Community adoption
- [ ] Bug reports addressed within 1 week
- [ ] Monthly patch releases
- [ ] Quarterly feature releases
