# Documentation Plan

## Documentation Goals

1. **FastAPI-Style Documentation**: Clean, modern, interactive docs like FastAPI
2. **Zensical Theme**: Use MkDocs Material with customizations
3. **Auto-Generated API Reference**: Generate from docstrings
4. **Rich Examples**: Interactive code examples with outputs
5. **Bilingual Support**: English primary, Persian (فارسی) secondary

---

## Documentation Stack

### Tools

| Tool | Purpose |
|------|---------|
| **MkDocs** | Static site generator |
| **MkDocs Material** | Modern theme (FastAPI-style) |
| **mkdocstrings** | Auto-generate API docs from docstrings |
| **mkdocs-gen-files** | Generate API reference pages |
| **mkdocs-literate-nav** | Literate navigation |
| **mkdocs-jupyter** | Render Jupyter notebooks |

### Installation

```bash
uv add --group docs mkdocs mkdocs-material mkdocstrings[python] mkdocs-gen-files mkdocs-literate-nav mkdocs-jupyter
```

---

## Documentation Structure

```
docs/
├── mkdocs.yml                    # MkDocs configuration
├── docs/
│   ├── index.md                  # Home page
│   ├── getting-started/
│   │   ├── index.md              # Getting started overview
│   │   ├── installation.md       # Installation guide
│   │   ├── quickstart.md         # 5-minute quickstart
│   │
│   ├── user-guide/
│   │   ├── index.md              # User guide overview
│   │   ├── timestamps.md         # Working with JalaliTimestamp
│   │   ├── date-ranges.md        # Generating date ranges
│   │   ├── indexing.md           # Indexing and slicing
│   │   ├── resampling.md         # Time series resampling
│   │   ├── groupby.md            # Grouping by Jalali components
│   │   ├── timezones.md          # Timezone handling
│   │   ├── offsets.md            # Frequency offsets
│   │   └── performance.md        # Performance tips
│   │
│   ├── api-reference/            # Auto-generated
│   │   ├── index.md              # API overview
│   │   ├── timestamp.md          # JalaliTimestamp
│   │   ├── array.md              # JalaliDatetimeArray
│   │   ├── index.md              # JalaliDatetimeIndex
│   │   ├── dtype.md              # JalaliDatetimeDtype
│   │   ├── offsets.md            # All offset classes
│   │   ├── accessors.md          # Series/DataFrame accessors
│   │   └── functions.md          # Top-level functions
│   │
│   ├── examples/
│   │   ├── index.md              # Examples overview
│   │   ├── financial-data.md     # Financial time series
│   │   ├── sales-analysis.md     # Sales data analysis
│   │   └── data-cleaning.md      # Data cleaning patterns
│   │
│   ├── fa/                       # Persian documentation
│   │   ├── index.md              # صفحه اصلی
│   │   ├── getting-started.md    # شروع کار
│   │   └── quickstart.md         # شروع سریع
│   │
│   ├── contributing.md           # Contribution guide
│   ├── changelog.md              # Changelog
│   └── license.md                # License
│
├── overrides/                    # Theme customizations
│   ├── main.html                 # Custom main template
│   └── partials/
│       └── header.html           # Custom header
│
└── stylesheets/
    └── extra.css                 # Custom CSS
```

---

## MkDocs Configuration

**`docs/mkdocs.yml`**
```yaml
site_name: Jalali Pandas
site_description: Full Jalali calendar support for pandas time series
site_url: https://ghodsizadeh.github.io/jalali-pandas/
repo_url: https://github.com/ghodsizadeh/jalali-pandas
repo_name: ghodsizadeh/jalali-pandas
edit_uri: edit/main/docs/docs/

theme:
  name: material
  custom_dir: overrides
  language: en
  features:
    - navigation.instant
    - navigation.instant.prefetch
    - navigation.tracking
    - navigation.tabs
    - navigation.tabs.sticky
    - navigation.sections
    - navigation.expand
    - navigation.path
    - navigation.indexes
    - navigation.top
    - navigation.footer
    - toc.follow
    - search.suggest
    - search.highlight
    - search.share
    - content.tabs.link
    - content.code.copy
    - content.code.annotate
    - content.action.edit
    - content.action.view
  palette:
    - media: "(prefers-color-scheme: light)"
      scheme: default
      primary: teal
      accent: amber
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      primary: teal
      accent: amber
      toggle:
        icon: material/brightness-4
        name: Switch to light mode
  font:
    text: Roboto
    code: Roboto Mono
  icon:
    repo: fontawesome/brands/github
    logo: material/calendar-clock
  favicon: assets/favicon.png

plugins:
  - search:
      lang:
        - en
        - fa
  - gen-files:
      scripts:
        - scripts/gen_ref_pages.py
  - literate-nav:
      nav_file: SUMMARY.md
  - mkdocstrings:
      default_handler: python
      handlers:
        python:
          paths: [..]
          options:
            show_source: true
            show_root_heading: true
            show_root_full_path: false
            show_symbol_type_heading: true
            show_symbol_type_toc: true
            docstring_style: google
            docstring_section_style: spacy
            merge_init_into_class: true
            show_signature_annotations: true
            separate_signature: true
            signature_crossrefs: true
            members_order: source
            filters:
              - "!^_"
              - "^__init__$"
  - mkdocs-jupyter:
      include_source: true
      execute: false

markdown_extensions:
  - abbr
  - admonition
  - attr_list
  - def_list
  - footnotes
  - md_in_html
  - tables
  - toc:
      permalink: true
      toc_depth: 3
  - pymdownx.arithmatex:
      generic: true
  - pymdownx.betterem:
      smart_enable: all
  - pymdownx.caret
  - pymdownx.details
  - pymdownx.emoji:
      emoji_index: !!python/name:material.extensions.emoji.twemoji
      emoji_generator: !!python/name:material.extensions.emoji.to_svg
  - pymdownx.highlight:
      anchor_linenums: true
      line_spans: __span
      pygments_lang_class: true
  - pymdownx.inlinehilite
  - pymdownx.keys
  - pymdownx.magiclink:
      repo_url_shorthand: true
      user: ghodsizadeh
      repo: jalali-pandas
  - pymdownx.mark
  - pymdownx.smartsymbols
  - pymdownx.snippets:
      auto_append:
        - includes/abbreviations.md
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
  - pymdownx.tabbed:
      alternate_style: true
  - pymdownx.tasklist:
      custom_checkbox: true
  - pymdownx.tilde

extra:
  social:
    - icon: fontawesome/brands/github
      link: https://github.com/ghodsizadeh/jalali-pandas
    - icon: fontawesome/brands/python
      link: https://pypi.org/project/jalali-pandas/
  analytics:
    provider: google
    property: G-XXXXXXXXXX
  version:
    provider: mike
  alternate:
    - name: English
      link: /
      lang: en
    - name: فارسی
      link: /fa/
      lang: fa

extra_css:
  - stylesheets/extra.css

nav:
  - Home: index.md
  - Getting Started:
    - getting-started/index.md
    - Installation: getting-started/installation.md
    - Quickstart: getting-started/quickstart.md
    - Migration Guide: getting-started/migration.md
  - User Guide:
    - user-guide/index.md
    - Timestamps: user-guide/timestamps.md
    - Date Ranges: user-guide/date-ranges.md
    - Indexing: user-guide/indexing.md
    - Resampling: user-guide/resampling.md
    - GroupBy: user-guide/groupby.md
    - Timezones: user-guide/timezones.md
    - Offsets: user-guide/offsets.md
    - Performance: user-guide/performance.md
  - API Reference: api-reference/
  - Examples:
    - examples/index.md
    - Financial Data: examples/financial-data.md
    - Sales Analysis: examples/sales-analysis.md
    - Data Cleaning: examples/data-cleaning.md
  - فارسی:
    - fa/index.md
    - شروع کار: fa/getting-started.md
    - شروع سریع: fa/quickstart.md
  - Contributing: contributing.md
  - Changelog: changelog.md
```

---

## Page Templates

### Home Page (`docs/docs/index.md`)

```markdown
---
hide:
  - navigation
  - toc
---

# Jalali Pandas

<p align="center">
  <img src="assets/logo.png" alt="Jalali Pandas" width="300">
</p>

<p align="center">
  <em>Full Jalali calendar support for pandas time series</em>
</p>

<p align="center">
  <a href="https://pypi.org/project/jalali-pandas/">
    <img src="https://img.shields.io/pypi/v/jalali-pandas" alt="PyPI">
  </a>
  <a href="https://github.com/ghodsizadeh/jalali-pandas/actions">
    <img src="https://github.com/ghodsizadeh/jalali-pandas/workflows/CI/badge.svg" alt="CI">
  </a>
  <a href="https://codecov.io/gh/ghodsizadeh/jalali-pandas">
    <img src="https://codecov.io/gh/ghodsizadeh/jalali-pandas/branch/main/graph/badge.svg" alt="Coverage">
  </a>
  <a href="https://github.com/ghodsizadeh/jalali-pandas/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/ghodsizadeh/jalali-pandas" alt="License">
  </a>
</p>

---

**Jalali Pandas** provides first-class Jalali (Persian/Shamsi) calendar support for pandas, enabling full time series functionality with Jalali dates.

## Features

<div class="grid cards" markdown>

- :material-calendar-clock:{ .lg .middle } **Native Jalali Types**

    ---

    `JalaliTimestamp`, `JalaliDatetimeIndex`, and `JalaliDatetimeArray`
    integrate seamlessly with pandas.

    [:octicons-arrow-right-24: Learn more](user-guide/timestamps.md)

- :material-chart-timeline:{ .lg .middle } **Full Time Series Support**

    ---

    Resampling, groupby, rolling windows, and shifting with
    Jalali calendar boundaries.

    [:octicons-arrow-right-24: Resampling guide](user-guide/resampling.md)

- :material-swap-horizontal:{ .lg .middle } **Easy Conversion**

    ---

    Convert between Jalali and Gregorian dates with a single
    function call.

    [:octicons-arrow-right-24: Conversion guide](user-guide/timestamps.md#conversion)

- :material-clock-fast:{ .lg .middle } **High Performance**

    ---

    Vectorized operations for fast processing of large datasets.

    [:octicons-arrow-right-24: Performance tips](user-guide/performance.md)

</div>

## Quick Example

```python
import pandas as pd
import jalali_pandas as jp

# Create a Jalali date range
idx = jp.jalali_date_range("1402-01-01", periods=365, freq="D")

# Create a time series
ts = pd.Series(range(365), index=idx)

# Resample by Jalali month
monthly = ts.resample("JME").mean()

# Group by Jalali quarter
quarterly = ts.groupby(jp.JalaliGrouper(freq="JQE")).sum()

# Access Jalali properties
print(idx.year)      # [1402, 1402, ...]
print(idx.month)     # [1, 1, 1, ..., 12, 12]
print(idx.quarter)   # [1, 1, 1, ..., 4, 4]
```

## Installation

=== "pip"

    ```bash
    pip install jalali-pandas
    ```

=== "uv"

    ```bash
    uv add jalali-pandas
    ```

=== "conda"

    ```bash
    conda install -c conda-forge jalali-pandas
    ```

## Requirements

- Python 3.9+
- pandas 2.0+
- numpy 1.23+

---

<p align="center">
  <a href="getting-started/quickstart/">Get Started</a> •
  <a href="user-guide/">User Guide</a> •
  <a href="api-reference/">API Reference</a> •
  <a href="https://github.com/ghodsizadeh/jalali-pandas">GitHub</a>
</p>
```

### Quickstart Page (`docs/docs/getting-started/quickstart.md`)

```markdown
# Quickstart

This guide will get you up and running with Jalali Pandas in 5 minutes.

## Installation

```bash
pip install jalali-pandas
```

## Basic Usage

### Import the Library

```python
import pandas as pd
import jalali_pandas as jp
```

### Create Jalali Timestamps

```python
# From components
ts = jp.JalaliTimestamp(1402, 6, 15)
print(ts)  # JalaliTimestamp('1402-06-15 00:00:00')

# From string
ts = jp.JalaliTimestamp("1402-06-15")

# Current time
now = jp.JalaliTimestamp.now()
today = jp.JalaliTimestamp.today()
```

### Generate Date Ranges

```python
# Daily range
daily = jp.jalali_date_range("1402-01-01", periods=30, freq="D")

# Monthly range (month end)
monthly = jp.jalali_date_range("1402-01-01", periods=12, freq="JME")

# Yearly range
yearly = jp.jalali_date_range("1400-01-01", "1405-12-29", freq="JYE")
```

### Convert Between Calendars

```python
# Gregorian to Jalali
gregorian_dates = pd.date_range("2023-01-01", periods=10, freq="D")
jalali_dates = jp.to_jalali_datetime(gregorian_dates)

# Jalali to Gregorian
gregorian = jalali_dates.to_gregorian()
```

### Access Date Components

```python
idx = jp.jalali_date_range("1402-01-01", periods=100, freq="D")

# Properties
idx.year       # Jalali year
idx.month      # Jalali month (1-12)
idx.day        # Jalali day
idx.quarter    # Jalali quarter (1-4)
idx.dayofweek  # Day of week (Saturday=0)
idx.dayofyear  # Day of year (1-366)
```

### Resample Time Series

```python
# Create time series with Jalali index
ts = pd.Series(
    range(365),
    index=jp.jalali_date_range("1402-01-01", periods=365, freq="D")
)

# Resample by Jalali month
monthly = ts.resample("JME").mean()

# Resample by Jalali quarter
quarterly = ts.resample("JQE").sum()

# Resample by Jalali year
yearly = ts.resample("JYE").sum()
```

### Group by Jalali Components

```python
df = pd.DataFrame({
    "date": jp.jalali_date_range("1402-01-01", periods=365, freq="D"),
    "value": range(365),
})

# Using accessor
df["jdate"] = df["date"]
monthly_sum = df.jalali.groupby("month").sum()

# Using JalaliGrouper
from jalali_pandas import JalaliGrouper
grouped = df.groupby(JalaliGrouper(key="date", freq="JME")).mean()
```

## Next Steps

- [User Guide](../user-guide/index.md) - Detailed documentation
- [API Reference](../api-reference/index.md) - Complete API documentation
- [Examples](../examples/index.md) - Real-world examples
```

### API Reference Auto-Generation Script

**`docs/scripts/gen_ref_pages.py`**
```python
"""Generate API reference pages."""
from pathlib import Path
import mkdocs_gen_files

nav = mkdocs_gen_files.Nav()

src = Path(__file__).parent.parent.parent / "jalali_pandas"

for path in sorted(src.rglob("*.py")):
    module_path = path.relative_to(src.parent).with_suffix("")
    doc_path = path.relative_to(src).with_suffix(".md")
    full_doc_path = Path("api-reference", doc_path)

    parts = tuple(module_path.parts)

    if parts[-1] == "__init__":
        parts = parts[:-1]
        doc_path = doc_path.with_name("index.md")
        full_doc_path = full_doc_path.with_name("index.md")
    elif parts[-1].startswith("_"):
        continue

    nav[parts] = doc_path.as_posix()

    with mkdocs_gen_files.open(full_doc_path, "w") as fd:
        identifier = ".".join(parts)
        fd.write(f"::: {identifier}")

    mkdocs_gen_files.set_edit_path(full_doc_path, path)

with mkdocs_gen_files.open("api-reference/SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())
```

---

## Docstring Style Guide

Use Google-style docstrings for all public APIs:

```python
def jalali_date_range(
    start: str | JalaliTimestamp | None = None,
    end: str | JalaliTimestamp | None = None,
    periods: int | None = None,
    freq: str | JalaliOffset | None = None,
    tz: str | tzinfo | None = None,
    normalize: bool = False,
    name: Hashable = None,
    inclusive: Literal["both", "neither", "left", "right"] = "both",
) -> JalaliDatetimeIndex:
    """Generate a fixed frequency JalaliDatetimeIndex.

    Returns a JalaliDatetimeIndex with a fixed frequency, similar to
    pandas.date_range but using the Jalali calendar.

    Args:
        start: Left bound for generating dates. Can be a string like
            "1402-01-01" or a JalaliTimestamp.
        end: Right bound for generating dates.
        periods: Number of periods to generate.
        freq: Frequency string or offset. Use Jalali-specific frequencies
            like "JME" (Jalali Month End) or "JYE" (Jalali Year End).
        tz: Timezone name or tzinfo object.
        normalize: Normalize start/end dates to midnight.
        name: Name of the resulting index.
        inclusive: Include boundaries; "both", "neither", "left", "right".

    Returns:
        A JalaliDatetimeIndex with the specified frequency.

    Raises:
        ValueError: If the frequency is invalid or if an invalid
            combination of start, end, and periods is provided.

    Examples:
        Generate 10 days starting from 1 Farvardin 1402:

        >>> jp.jalali_date_range("1402-01-01", periods=10, freq="D")
        JalaliDatetimeIndex(['1402-01-01', '1402-01-02', ..., '1402-01-10'],
                           dtype='jalali_datetime64[ns]', freq='D')

        Generate month ends for a year:

        >>> jp.jalali_date_range("1402-01-01", periods=12, freq="JME")
        JalaliDatetimeIndex(['1402-01-31', '1402-02-31', ..., '1402-12-29'],
                           dtype='jalali_datetime64[ns]', freq='JME')

        Generate with timezone:

        >>> jp.jalali_date_range("1402-01-01", periods=5, freq="D", tz="Asia/Tehran")
        JalaliDatetimeIndex(['1402-01-01 00:00:00+03:30', ...],
                           dtype='jalali_datetime64[ns, Asia/Tehran]', freq='D')

    See Also:
        - :func:`jalali_period_range`: Generate a PeriodIndex.
        - :class:`JalaliDatetimeIndex`: The returned index type.
        - :class:`JalaliMonthEnd`: Month end offset.

    Note:
        Exactly two of start, end, and periods must be specified.
    """
```

---

## Custom CSS

**`docs/stylesheets/extra.css`**
```css
/* FastAPI-style customizations */

:root {
  --md-primary-fg-color: #009688;
  --md-primary-fg-color--light: #4db6ac;
  --md-primary-fg-color--dark: #00796b;
  --md-accent-fg-color: #ffc107;
}

/* Hero section styling */
.md-typeset h1 {
  font-weight: 700;
}

/* Code block styling */
.md-typeset code {
  background-color: var(--md-code-bg-color);
  border-radius: 0.2rem;
  padding: 0 0.3rem;
}

/* Card grid styling */
.grid.cards > ul > li {
  border: 1px solid var(--md-default-fg-color--lightest);
  border-radius: 0.5rem;
  padding: 1rem;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.grid.cards > ul > li:hover {
  border-color: var(--md-accent-fg-color);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* RTL support for Persian */
[dir="rtl"] .md-typeset {
  font-family: "Vazirmatn", "Roboto", sans-serif;
}

/* API reference styling */
.doc-heading {
  border-bottom: 2px solid var(--md-primary-fg-color);
  padding-bottom: 0.5rem;
}

/* Admonition customization */
.md-typeset .admonition.tip {
  border-color: var(--md-accent-fg-color);
}

/* Version badge */
.version-badge {
  background-color: var(--md-primary-fg-color);
  color: white;
  padding: 0.2rem 0.5rem;
  border-radius: 0.3rem;
  font-size: 0.8rem;
}
```

---

## Deployment

### GitHub Actions Workflow

**`.github/workflows/docs.yml`**
```yaml
name: Documentation

on:
  push:
    branches: [main]
    paths:
      - "docs/**"
      - "jalali_pandas/**"
      - ".github/workflows/docs.yml"
  pull_request:
    branches: [main]
    paths:
      - "docs/**"

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: astral-sh/setup-uv@v4

      - name: Install dependencies
        run: uv sync --extra docs

      - name: Build documentation
        run: uv run mkdocs build --strict

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: site/

  deploy:
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    needs: build
    runs-on: ubuntu-latest
    permissions:
      pages: write
      id-token: write
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

### Local Development

```bash
# Install docs dependencies
uv sync --extra docs

# Serve locally with hot reload
uv run mkdocs serve

# Build static site
uv run mkdocs build

# Deploy to GitHub Pages (manual)
uv run mkdocs gh-deploy
```

---

## Documentation Checklist

### Before v1.0 Release

- [ ] Home page with feature overview
- [ ] Installation guide
- [ ] Quickstart tutorial
- [ ] Complete API reference (auto-generated)
- [ ] User guide for all major features
- [ ] At least 3 real-world examples
- [ ] Contributing guide
- [ ] Changelog

### Post-Release

- [ ] Persian translation of key pages
- [ ] Video tutorials
- [ ] Interactive examples (Jupyter notebooks)
- [ ] FAQ section
- [ ] Troubleshooting guide
- [ ] Performance benchmarks page
