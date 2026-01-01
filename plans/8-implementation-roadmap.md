# Implementation Roadmap

## Overview

This document outlines the phased implementation plan for building full Jalali calendar support in pandas. Each phase builds on the previous one, with clear milestones and deliverables.

---

## Phase 0: Foundation (Week 1-2)

### Goals
- Set up modern project infrastructure
- Establish type system foundation
- Create compatibility layer

### Tasks

#### 0.1 Project Infrastructure
- [ ] Update `pyproject.toml` with new dependencies and configuration
- [ ] Add `py.typed` marker
- [ ] Configure mypy and pyright and (Astral ty)
- [ ] Set up ruff for linting/formatting
- [ ] Update pre-commit hooks
- [ ] Set up GitHub Actions CI pipeline

#### 0.2 Type System Foundation
- [ ] Create `jalali_pandas/_typing.py` with type aliases
- [ ] Define protocols for Jalali types
- [ ] Add type stubs for jdatetime if needed

#### 0.3 Compatibility Layer
- [ ] Create `jalali_pandas/compat/pandas_compat.py`
- [ ] Detect pandas version and provide compatibility shims
- [ ] Create `jalali_pandas/compat/legacy.py` for v0.x API

#### 0.4 Calendar Rules Module
- [ ] Create `jalali_pandas/core/calendar.py`
- [ ] Implement leap year detection (2820-year cycle)
- [ ] Implement month length calculation
- [ ] Define week start (Saturday) and quarter boundaries
- [ ] Add comprehensive tests for calendar rules

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
- [ ] Create `jalali_pandas/core/timestamp.py`
- [ ] Implement construction from components
- [ ] Implement construction from string (parsing)
- [ ] Implement `from_gregorian()` class method
- [ ] Implement `to_gregorian()` method
- [ ] Implement all properties (year, month, day, etc.)
- [ ] Implement all boolean properties (is_leap_year, is_month_end, etc.)
- [ ] Implement `strftime()` method
- [ ] Implement `normalize()`, `floor()`, `ceil()`, `round()`
- [ ] Implement `replace()` method
- [ ] Implement arithmetic operators (+, -, with Timedelta)
- [ ] Implement comparison operators
- [ ] Implement `__hash__` for use as dict key
- [ ] Add NaT handling
- [ ] Add timezone support (tz_localize, tz_convert)

#### 1.2 Conversion Module
- [ ] Create `jalali_pandas/core/conversion.py`
- [ ] Implement scalar Jalali → Gregorian conversion
- [ ] Implement scalar Gregorian → Jalali conversion
- [ ] Implement vectorized conversions using NumPy
- [ ] Optimize with lookup tables for common ranges
- [ ] Add comprehensive round-trip tests

#### 1.3 JalaliDatetimeDtype
- [ ] Create `jalali_pandas/core/dtypes.py`
- [ ] Inherit from `pandas.api.extensions.ExtensionDtype`
- [ ] Implement `name` property
- [ ] Implement `type` property (returns JalaliTimestamp)
- [ ] Implement `na_value` (returns pd.NaT)
- [ ] Implement `construct_array_type()`
- [ ] Implement `construct_from_string()`
- [ ] Register dtype with pandas

#### 1.4 JalaliDatetimeArray
- [ ] Create `jalali_pandas/core/arrays.py`
- [ ] Inherit from `pandas.api.extensions.ExtensionArray`
- [ ] Choose internal storage format (int64 nanoseconds)
- [ ] Implement `_from_sequence()`
- [ ] Implement `_from_sequence_of_strings()`
- [ ] Implement `_from_factorized()`
- [ ] Implement `__len__`, `__getitem__`, `__setitem__`
- [ ] Implement `__iter__`
- [ ] Implement `isna()`
- [ ] Implement `copy()`
- [ ] Implement `_concat_same_type()`
- [ ] Implement vectorized properties (year, month, etc.)
- [ ] Implement vectorized methods (strftime, normalize, etc.)
- [ ] Implement `to_gregorian()` returning DatetimeArray

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
- [ ] Create `jalali_pandas/core/indexes.py`
- [ ] Inherit from `pandas.Index`
- [ ] Wrap `JalaliDatetimeArray` as `_data`
- [ ] Implement construction from various inputs
- [ ] Implement `freq` property
- [ ] Implement frequency inference
- [ ] Implement string indexing ("1402-06-15")
- [ ] Implement partial string indexing ("1402-06", "1402")
- [ ] Implement slice indexing
- [ ] Implement `shift()` method
- [ ] Implement `snap()` method
- [ ] Implement set operations (union, intersection, difference)
- [ ] Implement `to_gregorian()` returning DatetimeIndex

#### 2.2 Date Range Generation
- [ ] Create `jalali_pandas/api/date_range.py`
- [ ] Implement `jalali_date_range()` function
- [ ] Support start/end/periods combinations
- [ ] Support all frequency strings (D, h, min, s, JME, JQE, JYE, etc.)
- [ ] Support timezone parameter
- [ ] Support normalize parameter
- [ ] Support inclusive parameter
- [ ] Validate parameter combinations

#### 2.3 Conversion Functions
- [ ] Create `jalali_pandas/api/conversion.py`
- [ ] Implement `to_jalali_datetime()` function
- [ ] Support string, list, Series, DatetimeIndex inputs
- [ ] Support format parameter
- [ ] Support errors parameter (raise, coerce, ignore)
- [ ] Implement `to_gregorian_datetime()` function

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
- [ ] Create `jalali_pandas/offsets/base.py`
- [ ] Implement `JalaliOffset` base class
- [ ] Define interface: `__add__`, `__radd__`, `rollforward`, `rollback`, `is_on_offset`
- [ ] Implement `n` multiplier support
- [ ] Implement `normalize` parameter

#### 3.2 Month Offsets
- [ ] Create `jalali_pandas/offsets/month.py`
- [ ] Implement `JalaliMonthEnd`
  - Handle 31-day months (1-6)
  - Handle 30-day months (7-11)
  - Handle Esfand (29 or 30 days)
- [ ] Implement `JalaliMonthBegin`
- [ ] Register frequency aliases ("JME", "JMS")

#### 3.3 Quarter Offsets
- [ ] Create `jalali_pandas/offsets/quarter.py`
- [ ] Implement `JalaliQuarterEnd`
  - Q1 ends 31 Khordad
  - Q2 ends 31 Shahrivar
  - Q3 ends 30 Azar
  - Q4 ends 29/30 Esfand
- [ ] Implement `JalaliQuarterBegin`
- [ ] Register frequency aliases ("JQE", "JQS")

#### 3.4 Year Offsets
- [ ] Create `jalali_pandas/offsets/year.py`
- [ ] Implement `JalaliYearEnd` (29/30 Esfand)
- [ ] Implement `JalaliYearBegin` (1 Farvardin)
- [ ] Register frequency aliases ("JYE", "JYS")

#### 3.5 Week Offset
- [ ] Create `jalali_pandas/offsets/week.py`
- [ ] Implement `JalaliWeek` (Saturday-based by default)
- [ ] Support custom weekday parameter
- [ ] Register frequency alias ("JW")

#### 3.6 Offset Integration
- [ ] Create `jalali_pandas/offsets/__init__.py`
- [ ] Register all offsets with pandas frequency system
- [ ] Enable string frequency parsing ("JME", "2JME", etc.)

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
- [ ] Ensure `JalaliDatetimeIndex.resample()` works with Jalali offsets
- [ ] Test all aggregation methods (mean, sum, min, max, etc.)
- [ ] Test upsampling with fill methods
- [ ] Test downsampling
- [ ] Test closed/label parameters
- [ ] Document any limitations

#### 4.2 JalaliGrouper
- [ ] Create `jalali_pandas/api/grouper.py`
- [ ] Implement `JalaliGrouper` class
- [ ] Support `key` parameter for column-based grouping
- [ ] Support `freq` parameter for frequency-based grouping
- [ ] Integrate with `DataFrame.groupby()`

#### 4.3 DataFrame Accessor Resample
- [ ] Update `JalaliDataFrameAccessor.resample()`
- [ ] Remove `NotImplementedError`
- [ ] Implement using JalaliGrouper internally
- [ ] Support all resample parameters

#### 4.4 Rolling/Expanding
- [ ] Test rolling with Jalali offset windows
- [ ] Test expanding operations
- [ ] Document any limitations

#### 4.5 Shifting
- [ ] Test `Series.shift(freq=JalaliOffset)`
- [ ] Test `DataFrame.shift(freq=JalaliOffset)`
- [ ] Test `JalaliDatetimeIndex.shift()`

### Deliverables
- Full resampling support with Jalali boundaries
- JalaliGrouper for flexible grouping
- Rolling/shifting work with Jalali offsets

---

## Phase 5: Enhanced Accessors (Week 13-14)

### Goals
- Enhance Series accessor with all properties/methods
- Enhance DataFrame accessor
- Maintain backward compatibility

### Tasks

#### 5.1 Series Accessor Enhancement
- [ ] Update `jalali_pandas/accessors/series.py`
- [ ] Add all missing properties (dayofyear, daysinmonth, is_* flags)
- [ ] Add `strftime()` method
- [ ] Add `normalize()` method
- [ ] Add `floor()`, `ceil()`, `round()` methods
- [ ] Add `tz_localize()`, `tz_convert()` methods
- [ ] Add `month_name()`, `day_name()` methods
- [ ] Add `date`, `time` properties
- [ ] Add full type annotations
- [ ] Maintain backward compatibility with v0.x

#### 5.2 DataFrame Accessor Enhancement
- [ ] Update `jalali_pandas/accessors/dataframe.py`
- [ ] Add `set_date_column()` method
- [ ] Update `groupby()` to use new infrastructure
- [ ] Implement `resample()` properly
- [ ] Add `convert_columns()` method
- [ ] Add full type annotations
- [ ] Maintain backward compatibility with v0.x

#### 5.3 Backward Compatibility
- [ ] Test all v0.x API still works
- [ ] Add deprecation warnings for changed behavior
- [ ] Document migration path

### Deliverables
- Feature-complete accessors
- Full type annotations
- Backward compatible with v0.x

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
- [ ] Write migration guide
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
| Backward compatibility breaks | Maintain v0.x API, add deprecation warnings |

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
- [ ] Backward compatible with v0.x
- [ ] Performance acceptable (benchmarked)

### Post-Release Goals

- [ ] Community adoption
- [ ] Bug reports addressed within 1 week
- [ ] Monthly patch releases
- [ ] Quarterly feature releases
