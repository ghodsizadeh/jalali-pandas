# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2026-01-07

### Changed
- **Official 1.0.0 Release**: Moved from beta to production/stable status
- Package now marked as Production/Stable in PyPI classifiers

### Notes
- This is the first stable release of jalali-pandas with full pandas 2.0+ extension API support
- All features from 1.0.0b1 are now considered stable and production-ready
- API is now considered stable and will follow semantic versioning

## [1.0.0b1] - 2026-01-05

### Added
- **JalaliTimestamp**: Full-featured scalar type with all date/time properties and methods
- **JalaliDatetimeDtype**: Registered pandas extension dtype (`jalali_datetime64[ns]`)
- **JalaliDatetimeArray**: Extension array for Series storage with vectorized operations
- **JalaliDatetimeIndex**: Full pandas Index implementation with Jalali awareness
- **jalali_date_range()**: Generate date ranges with all frequency strings
- **Frequency Offsets**: JalaliMonthEnd/Begin, JalaliQuarterEnd/Begin, JalaliYearEnd/Begin, JalaliWeek
- **Frequency aliases**: JME, JMS, JQE, JQS, JYE, JYS, JW
- **resample_jalali()**: Jalali-aware resampling with proper boundaries
- **JalaliGrouper**: Calendar-based grouping by year/month/quarter/day
- **Enhanced Series Accessor**: All date/time properties, strftime, normalize, floor/ceil/round, tz_localize/tz_convert, month_name/day_name
- **Enhanced DataFrame Accessor**: set_date_column, groupby, resample, convert_columns, filter methods
- **Timezone support**: Full tz_localize and tz_convert functionality
- **String indexing**: Support for "1402-06-15", "1402-06", "1402" formats
- **Comprehensive documentation**: MkDocs site with English and Persian versions
- **11 Python examples** + 2 Jupyter notebooks demonstrating all features
- **94% test coverage** with 563 tests (unit, integration, property-based)

### Changed
- **Complete rewrite**: Ground-up implementation using pandas ExtensionArray API
- **Breaking API changes**: New extension-based architecture (see migration guide in docs)
- **Minimum Python version**: Now requires Python 3.9+
- **Minimum pandas version**: Now requires pandas 2.0+

### Performance
- Vectorized conversions using NumPy for bulk operations
- Lookup tables for cached conversions of common date ranges
- Optimized calendar rules with efficient leap year detection

## [1.0.0a1] - 2026-01-01

### Added
- Modern project infrastructure with ruff, mypy, pyright
- `py.typed` marker for PEP 561 compliance
- Comprehensive CI/CD pipeline with GitHub Actions
- Support for Python 3.9-3.13
- Support for pandas 2.0-2.2

### Changed
- Updated dependencies to require pandas>=2.0.0 and numpy>=1.23.0
- Replaced black/pylint with ruff for linting and formatting
- Updated pre-commit hooks configuration

## [0.2.2] - Previous Release

### Features
- Basic Series accessor with `to_jalali()`, `to_gregorian()`, `parse_jalali()`
- Series properties: year, month, day, hour, minute, second, weekday, weeknumber, quarter
- DataFrame accessor with `groupby()` for Jalali date components
- Groupby shortcuts: year, month, day, week, ym, yq, ymd, md

[Unreleased]: https://github.com/ghodsizadeh/jalali-pandas/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/ghodsizadeh/jalali-pandas/compare/v1.0.0b1...v1.0.0
[1.0.0b1]: https://github.com/ghodsizadeh/jalali-pandas/compare/v1.0.0a1...v1.0.0b1
[1.0.0a1]: https://github.com/ghodsizadeh/jalali-pandas/compare/v0.2.2...v1.0.0a1
[0.2.2]: https://github.com/ghodsizadeh/jalali-pandas/releases/tag/v0.2.2
