"""Benchmarks for JalaliDatetimeArray operations."""

from __future__ import annotations

import numpy as np

from jalali_pandas import JalaliTimestamp
from jalali_pandas.core.arrays import JalaliDatetimeArray


class TimeArrayOperations:
    """Benchmark array construction and formatting."""

    params = [1000, 100000]
    param_names = ["size"]

    def setup(self, size: int) -> None:
        years = np.full(size, 1402, dtype=np.int64)
        months = (np.arange(size, dtype=np.int64) % 12) + 1
        days = (np.arange(size, dtype=np.int64) % 28) + 1
        self.values = [
            JalaliTimestamp(int(year), int(month), int(day))
            for year, month, day in zip(years, months, days)
        ]
        self.array = JalaliDatetimeArray._from_sequence(self.values)

    def time_from_sequence(self, _size: int) -> None:
        JalaliDatetimeArray._from_sequence(self.values)

    def time_to_gregorian(self, _size: int) -> None:
        self.array.to_gregorian()

    def time_strftime(self, _size: int) -> None:
        self.array.strftime("%Y-%m-%d")
