"""Benchmarks for JalaliTimestamp construction."""

from __future__ import annotations

import numpy as np
import pandas as pd

from jalali_pandas import JalaliTimestamp


class TimeTimestampConstruction:
    """Benchmark timestamp creation paths."""

    params = [1000, 10000]
    param_names = ["size"]

    def setup(self, size: int) -> None:
        self.years = np.full(size, 1402, dtype=np.int64)
        self.months = (np.arange(size, dtype=np.int64) % 12) + 1
        self.days = (np.arange(size, dtype=np.int64) % 28) + 1
        self.gregorian = pd.date_range("2023-01-01", periods=size, freq="D")

    def time_init(self, _size: int) -> None:
        for year, month, day in zip(self.years, self.months, self.days):
            JalaliTimestamp(int(year), int(month), int(day))

    def time_from_gregorian(self, _size: int) -> None:
        for ts in self.gregorian:
            JalaliTimestamp.from_gregorian(ts)
