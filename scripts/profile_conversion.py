"""Profile Jalali conversion hot paths."""

from __future__ import annotations

import argparse
import cProfile
import pstats
import time
from typing import Callable, cast

import numpy as np
import pandas as pd
from numpy.typing import NDArray

from jalali_pandas.core import conversion


def _build_gregorian_datetimes(size: int) -> NDArray[np.datetime64]:
    """Create a datetime64 array for profiling."""
    return cast(
        NDArray[np.datetime64],
        pd.date_range("2023-01-01", periods=size, freq="D").to_numpy(),
    )


def _build_jalali_components(
    size: int,
) -> tuple[NDArray[np.int64], NDArray[np.int64], NDArray[np.int64]]:
    """Create Jalali component arrays with valid day ranges."""
    years = np.full(size, 1402, dtype=np.int64)
    months = (np.arange(size, dtype=np.int64) % 12) + 1
    days = (np.arange(size, dtype=np.int64) % 28) + 1
    return years, months, days


def _time_call(label: str, func: Callable[[], object]) -> None:
    """Time a callable and report wall-clock duration."""
    start = time.perf_counter()
    func()
    duration = time.perf_counter() - start
    print(f"{label}: {duration:.4f}s")


def run_profile(size: int, use_cprofile: bool) -> None:
    """Run timing and optional cProfile for conversion operations."""
    gregorian = _build_gregorian_datetimes(size)
    years, months, days = _build_jalali_components(size)

    def to_jalali() -> None:
        conversion.datetime64_to_jalali(gregorian)

    def to_gregorian() -> None:
        conversion.jalali_to_datetime64(years, months, days)

    _time_call("datetime64_to_jalali", to_jalali)
    _time_call("jalali_to_datetime64", to_gregorian)

    if not use_cprofile:
        return

    profiler = cProfile.Profile()
    profiler.enable()
    to_jalali()
    to_gregorian()
    profiler.disable()

    stats = pstats.Stats(profiler).sort_stats("cumulative")
    stats.print_stats(15)


def main() -> None:
    parser = argparse.ArgumentParser(description="Profile Jalali conversion hot paths.")
    parser.add_argument("--size", type=int, default=100_000)
    parser.add_argument("--cprofile", action="store_true")
    args = parser.parse_args()

    run_profile(args.size, args.cprofile)


if __name__ == "__main__":
    main()
