# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Release tooling for version bumps, changelog finalization, and builds
- GitHub Actions workflows for releases, docs versioning, and release drafts
- Versioned documentation publishing with Mike and MkDocs API generation

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

[Unreleased]: https://github.com/ghodsizadeh/jalali-pandas/compare/v1.0.0a1...HEAD
[1.0.0a1]: https://github.com/ghodsizadeh/jalali-pandas/compare/v0.2.2...v1.0.0a1
[0.2.2]: https://github.com/ghodsizadeh/jalali-pandas/releases/tag/v0.2.2
