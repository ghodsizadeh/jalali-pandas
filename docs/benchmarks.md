# Benchmarks

## Overview
This project uses Airspeed Velocity (ASV) to track performance across key Jalali
operations. The benchmark suite focuses on timestamp construction, conversion
utilities, array operations, and Jalali-aware resampling.

## Setup
Install benchmark dependencies with uv:

```bash
uv sync --extra benchmark
```

## Running Benchmarks
Run a quick smoke benchmark against your current checkout:

```bash
uv run asv run --quick
```

Run the full suite for the current checkout:

```bash
uv run asv run
```

Run the development loop (useful while iterating on benchmarks):

```bash
uv run asv dev
```

Generate HTML results after a run:

```bash
uv run asv publish
```

Results are stored in:
- `.asv/results` for raw data
- `.asv/html` for rendered reports

## Benchmark Layout
Benchmarks live in `benchmarks/` and follow ASV naming conventions:
- `benchmarks/benchmark_timestamp.py` for JalaliTimestamp construction
- `benchmarks/benchmark_conversion.py` for vectorized conversions
- `benchmarks/benchmark_arrays.py` for JalaliDatetimeArray operations
- `benchmarks/benchmark_resample.py` for resampling

## Adding New Benchmarks
1. Create a new file under `benchmarks/` or extend an existing benchmark file.
2. Use `time_` methods for timing and `params` for size scaling.
3. Keep setup deterministic and avoid random inputs unless required.

## Profiling Support
For deeper profiling of conversion hot paths, use:

```bash
python scripts/profile_conversion.py --size 100000 --cprofile
```

This script reports wall-clock timing and optional cProfile statistics for the
core conversion functions.
