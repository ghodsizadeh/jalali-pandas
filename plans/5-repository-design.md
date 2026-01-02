# Repository Design & Architecture

## Target Package Structure

```
jalali-pandas/
├── .github/
│   ├── workflows/
│   │   ├── ci.yml              # Main CI pipeline
│   │   ├── release.yml         # PyPI release workflow
│   │   └── docs.yml            # Documentation deployment
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── dependabot.yml
│
├── docs/                        # Documentation (Zensical/MkDocs)
│   ├── mkdocs.yml              # MkDocs configuration
│   ├── docs/
│   │   ├── index.md            # Home page
│   │   ├── getting-started/
│   │   │   ├── installation.md
│   │   │   ├── quickstart.md
│   │   ├── user-guide/
│   │   │   ├── timestamps.md
│   │   │   ├── date-ranges.md
│   │   │   ├── indexing.md
│   │   │   ├── resampling.md
│   │   │   ├── groupby.md
│   │   │   ├── timezones.md
│   │   │   └── offsets.md
│   │   ├── api-reference/      # Auto-generated from docstrings
│   │   │   ├── timestamp.md
│   │   │   ├── array.md
│   │   │   ├── index.md
│   │   │   ├── offsets.md
│   │   │   ├── accessors.md
│   │   │   └── functions.md
│   │   ├── examples/
│   │   │   ├── financial-data.md
│   │   │   ├── time-series-analysis.md
│   │   │   └── data-cleaning.md
│   │   └── contributing.md
│   └── overrides/              # Custom theme overrides
│
├── examples/
│   ├── basic_usage.ipynb       # Existing notebook (updated)
│   ├── financial_analysis.ipynb
│   ├── time_series_resampling.ipynb
│
├── jalali_pandas/
│   ├── __init__.py             # Public API exports
│   ├── py.typed                # PEP 561 marker
│   ├── _version.py             # Version info
│   │
│   ├── _typing.py              # Type aliases and protocols
│   ├── _libs/                  # Cython/compiled extensions (future)
│   │   ├── __init__.py
│   │   └── tslib.pyx           # Fast timestamp operations
│   │
│   ├── core/                   # Core implementations
│   │   ├── __init__.py
│   │   ├── timestamp.py        # JalaliTimestamp scalar
│   │   ├── arrays.py           # JalaliDatetimeArray
│   │   ├── dtypes.py           # JalaliDatetimeDtype
│   │   ├── indexes.py          # JalaliDatetimeIndex
│   │   ├── conversion.py       # Jalali <-> Gregorian conversion
│   │   └── calendar.py         # Jalali calendar rules
│   │
│   ├── offsets/                # Frequency offsets
│   │   ├── __init__.py
│   │   ├── base.py             # JalaliOffset base class
│   │   ├── month.py            # JalaliMonthEnd, JalaliMonthBegin
│   │   ├── quarter.py          # JalaliQuarterEnd, JalaliQuarterBegin
│   │   ├── year.py             # JalaliYearEnd, JalaliYearBegin
│   │   └── week.py             # JalaliWeek
│   │
│   ├── accessors/              # Pandas accessors
│   │   ├── __init__.py
│   │   ├── series.py           # JalaliSeriesAccessor
│   │   └── dataframe.py        # JalaliDataFrameAccessor
│   │
│   ├── api/                    # Public API functions
│   │   ├── __init__.py
│   │   ├── date_range.py       # jalali_date_range
│   │   ├── period_range.py     # jalali_period_range
│   │   ├── conversion.py       # to_jalali_datetime, to_gregorian_datetime
│   │   └── grouper.py          # JalaliGrouper
│   │
│   └── testing/                # Testing utilities
│       ├── __init__.py
│       └── assertions.py       # assert_jalali_equal, etc.
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # Pytest fixtures
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── test_timestamp.py
│   │   ├── test_arrays.py
│   │   ├── test_dtypes.py
│   │   ├── test_indexes.py
│   │   ├── test_conversion.py
│   │   └── test_calendar.py
│   │
│   ├── offsets/
│   │   ├── __init__.py
│   │   ├── test_month.py
│   │   ├── test_quarter.py
│   │   ├── test_year.py
│   │   └── test_week.py
│   │
│   ├── accessors/
│   │   ├── __init__.py
│   │   ├── test_series.py
│   │   └── test_dataframe.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── test_date_range.py
│   │   ├── test_period_range.py
│   │   ├── test_conversion.py
│   │   └── test_grouper.py
│   │
│   ├── integration/
│   │   ├── __init__.py
│   │   ├── test_resample.py
│   │   ├── test_rolling.py
│   │   ├── test_groupby.py
│   │   └── test_io.py
│   │
│   └── performance/
│       ├── __init__.py
│       └── benchmarks.py       # ASV benchmarks
│
├── benchmarks/                  # ASV benchmark suite
│   ├── asv.conf.json
│   └── benchmarks/
│       ├── __init__.py
│       ├── timestamp.py
│       ├── arrays.py
│       └── conversion.py
│
├── plans/                       # Project planning docs
│   ├── 1-jalali-pandas-north-star-plan.md
│   ├── 2-current-state-analysis.md
│   ├── 3-api-design.md
│   ├── 4-type-system.md
│   ├── 5-repository-design.md
│   ├── 6-testing-plan.md
│   └── 7-documentation-plan.md
│
├── .coveragerc
├── .gitignore
├── .pre-commit-config.yaml
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── pyproject.toml
└── uv.lock
```

---

## Module Responsibilities

### `jalali_pandas/core/`

The heart of the library containing core data structures.

| Module | Responsibility |
|--------|----------------|
| `timestamp.py` | `JalaliTimestamp` scalar class with all datetime operations |
| `arrays.py` | `JalaliDatetimeArray` ExtensionArray for vectorized operations |
| `dtypes.py` | `JalaliDatetimeDtype` ExtensionDtype for pandas integration |
| `indexes.py` | `JalaliDatetimeIndex` for time series indexing |
| `conversion.py` | Jalali ↔ Gregorian conversion algorithms (vectorized) |
| `calendar.py` | Jalali calendar rules (leap years, month lengths, week definitions) |

### `jalali_pandas/offsets/`

Jalali-aware frequency offsets for time series operations.

| Module | Classes |
|--------|---------|
| `base.py` | `JalaliOffset` base class |
| `month.py` | `JalaliMonthEnd`, `JalaliMonthBegin` |
| `quarter.py` | `JalaliQuarterEnd`, `JalaliQuarterBegin` |
| `year.py` | `JalaliYearEnd`, `JalaliYearBegin` |
| `week.py` | `JalaliWeek` |

### `jalali_pandas/accessors/`

Pandas accessor implementations.

| Module | Classes |
|--------|---------|
| `series.py` | `JalaliSeriesAccessor` - `.jalali` accessor for Series |
| `dataframe.py` | `JalaliDataFrameAccessor` - `.jalali` accessor for DataFrame |

### `jalali_pandas/api/`

Public API functions.

| Module | Functions |
|--------|-----------|
| `date_range.py` | `jalali_date_range()` |
| `period_range.py` | `jalali_period_range()` |
| `conversion.py` | `to_jalali_datetime()`, `to_gregorian_datetime()` |
| `grouper.py` | `JalaliGrouper` class |

## Public API (`__init__.py`)

```python
"""
Jalali Pandas - Full Jalali calendar support for pandas.
"""

from jalali_pandas._version import __version__

# Core types
from jalali_pandas.core.timestamp import JalaliTimestamp
from jalali_pandas.core.arrays import JalaliDatetimeArray
from jalali_pandas.core.dtypes import JalaliDatetimeDtype
from jalali_pandas.core.indexes import JalaliDatetimeIndex

# Offsets
from jalali_pandas.offsets import (
    JalaliOffset,
    JalaliMonthEnd,
    JalaliMonthBegin,
    JalaliQuarterEnd,
    JalaliQuarterBegin,
    JalaliYearEnd,
    JalaliYearBegin,
    JalaliWeek,
)

# API functions
from jalali_pandas.api.date_range import jalali_date_range
from jalali_pandas.api.period_range import jalali_period_range
from jalali_pandas.api.conversion import to_jalali_datetime, to_gregorian_datetime
from jalali_pandas.api.grouper import JalaliGrouper

# Accessors (registered on import)
from jalali_pandas.accessors.series import JalaliSeriesAccessor
from jalali_pandas.accessors.dataframe import JalaliDataFrameAccessor

# Testing utilities
from jalali_pandas.testing import assert_jalali_equal

__all__ = [
    # Version
    "__version__",
    # Core types
    "JalaliTimestamp",
    "JalaliDatetimeArray",
    "JalaliDatetimeDtype",
    "JalaliDatetimeIndex",
    # Offsets
    "JalaliOffset",
    "JalaliMonthEnd",
    "JalaliMonthBegin",
    "JalaliQuarterEnd",
    "JalaliQuarterBegin",
    "JalaliYearEnd",
    "JalaliYearBegin",
    "JalaliWeek",
    # Functions
    "jalali_date_range",
    "jalali_period_range",
    "to_jalali_datetime",
    "to_gregorian_datetime",
    "JalaliGrouper",
    # Accessors
    "JalaliSeriesAccessor",
    "JalaliDataFrameAccessor",
    # Testing
    "assert_jalali_equal",
]
```

---

## Dependencies

### pyproject.toml

```toml
[project]
name = "jalali-pandas"
version = "1.0.0"
description = "Full Jalali calendar support for pandas time series"
authors = [{ name = "Mehdi Ghodsizadeh", email = "mehdi.ghodsizadeh@gmail.com" }]
requires-python = ">=3.9"
readme = "README.md"
license = { file = "LICENSE" }
keywords = ["jalali", "pandas", "persian", "shamsi", "calendar", "datetime", "timeseries"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Topic :: Scientific/Engineering",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Typing :: Typed",
]

dependencies = [
    "pandas>=2.0.0",
    "numpy>=1.23.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "pytest-xdist>=3.0.0",
    "mypy>=1.0.0",
    "pyright>=1.1.0",
    "ruff>=0.1.0",
    "pre-commit>=3.0.0",
    "hypothesis>=6.0.0",
]
docs = [
    "mkdocs>=1.5.0",
    "mkdocs-material>=9.0.0",
    "mkdocstrings[python]>=0.24.0",
    "mkdocs-gen-files>=0.5.0",
    "mkdocs-literate-nav>=0.6.0",
]
benchmark = [
    "asv>=0.6.0",
]
all = [
    "jalali-pandas[dev,docs,benchmark]",
]

[project.urls]
Documentation = "https://ghodsizadeh.github.io/jalali-pandas/"
Homepage = "https://ghodsizadeh.github.io/jalali-pandas/"
Repository = "https://github.com/ghodsizadeh/jalali-pandas"
Changelog = "https://github.com/ghodsizadeh/jalali-pandas/blob/main/CHANGELOG.md"
"Bug Tracker" = "https://github.com/ghodsizadeh/jalali-pandas/issues"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["jalali_pandas"]

[tool.hatch.build.targets.sdist]
include = [
    "/jalali_pandas",
    "/tests",
    "/README.md",
    "/LICENSE",
    "/CHANGELOG.md",
]

# Ruff configuration
[tool.ruff]
target-version = "py39"
line-length = 88
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
    "ARG", # flake8-unused-arguments
    "SIM", # flake8-simplify
]
ignore = [
    "E501",  # line too long (handled by formatter)
    "B008",  # do not perform function calls in argument defaults
]

[tool.ruff.isort]
known-first-party = ["jalali_pandas"]

# Pytest configuration
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = [
    "-ra",
    "-q",
    "--strict-markers",
    "--strict-config",
]
markers = [
    "slow: marks tests as slow",
    "integration: marks tests as integration tests",
]

# Coverage configuration
[tool.coverage.run]
source = ["jalali_pandas"]
branch = true
parallel = true

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise NotImplementedError",
    "if TYPE_CHECKING:",
    "if __name__ == .__main__.:",
    "@overload",
]

# MyPy configuration
[tool.mypy]
python_version = "3.9"
strict = true
warn_return_any = true
warn_unused_configs = true
plugins = ["numpy.typing.mypy_plugin"]

[[tool.mypy.overrides]]
module = ["jdatetime.*"]
ignore_missing_imports = true

# Pyright configuration
[tool.pyright]
pythonVersion = "3.9"
typeCheckingMode = "strict"
reportMissingImports = true
reportMissingTypeStubs = false
```

---

## Internal Representation

### Storage Strategy

Store Jalali datetimes internally as **int64 nanoseconds since Jalali epoch** (or Gregorian epoch with metadata).

**Option A: Jalali Epoch (Recommended)**
- Epoch: 1 Farvardin 1 (Jalali year 1) = March 22, 622 CE
- Store as int64 nanoseconds from epoch
- Pros: Direct Jalali arithmetic, no conversion overhead for Jalali ops
- Cons: Need conversion for timezone operations

**Option B: Gregorian Epoch with Jalali Metadata**
- Store as int64 nanoseconds from Unix epoch (like pandas)
- Cache Jalali components or compute on demand
- Pros: Easy timezone handling via pandas
- Cons: Conversion overhead for every Jalali property access

### Recommended Approach

Use **Option A** for core storage with lazy Gregorian conversion:

```python
class JalaliDatetimeArray(ExtensionArray):
    _data: np.ndarray  # int64 nanoseconds from Jalali epoch
    _dtype: JalaliDatetimeDtype
    _gregorian_cache: np.ndarray | None = None  # Lazy cache

    @property
    def _gregorian(self) -> np.ndarray:
        if self._gregorian_cache is None:
            self._gregorian_cache = self._convert_to_gregorian(self._data)
        return self._gregorian_cache
```

---

## Versioning Strategy

Follow [Semantic Versioning](https://semver.org/):

- **1.0.0**: First stable release with full API
- **1.x.y**: Additions and fixes
- **2.0.0**: Breaking changes (if needed)

### Version Compatibility

| jalali-pandas | Python | pandas | numpy |
|---------------|--------|--------|-------|
| 1.0.x | 3.9-3.13 | 2.0-2.2 | 1.23+ |
| 1.1.x | 3.10-3.13 | 2.1-2.3 | 1.24+ |

---

## CI/CD Pipeline

### GitHub Actions Workflow (`.github/workflows/ci.yml`)

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python-version: ["3.9", "3.10", "3.11", "3.12", "3.13"]
        pandas-version: ["2.0", "2.1", "2.2"]

    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4
      - name: Install dependencies
        run: uv sync --all-extras
      - name: Install specific pandas version
        run: uv pip install pandas==${{ matrix.pandas-version }}.*
      - name: Run tests
        run: uv run pytest --cov=jalali_pandas --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v4

  type-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4
      - name: Install dependencies
        run: uv sync --all-extras
      - name: Run mypy
        run: uv run mypy jalali_pandas
      - name: Run pyright
        run: uv run pyright jalali_pandas

  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4
      - name: Install dependencies
        run: uv sync --all-extras
      - name: Run ruff
        run: uv run ruff check jalali_pandas tests
      - name: Run ruff format check
        run: uv run ruff format --check jalali_pandas tests

  docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4
      - name: Install dependencies
        run: uv sync --extra docs
      - name: Build docs
        run: uv run mkdocs build --strict
```

---

## Pre-commit Configuration

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.13.0
    hooks:
      - id: mypy
        additional_dependencies:
          - pandas-stubs
          - numpy

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict
```
