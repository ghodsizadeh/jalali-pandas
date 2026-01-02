"""Benchmarks for conversion utilities."""

from __future__ import annotations

import numpy as np
import pandas as pd

from jalali_pandas.core.conversion import (
    datetime64_to_jalali,
    gregorian_to_jalali_vectorized,
    jalali_to_datetime64,
    jalali_to_gregorian_vectorized,
)


class TimeVectorizedConversions:
    """Benchmark vectorized conversion paths."""

    params = [1000, 100000]
    param_names = ["size"]

    def setup(self, size: int) -> None:
        self.j_years = np.full(size, 1402, dtype=np.int64)
        self.j_months = (np.arange(size, dtype=np.int64) % 12) + 1
        self.j_days = (np.arange(size, dtype=np.int64) % 28) + 1

        gregorian = pd.date_range("2023-01-01", periods=size, freq="D").to_numpy()
        self.gregorian = gregorian
        dti = pd.DatetimeIndex(gregorian)
        self.g_years = dti.year.to_numpy().astype(np.int64)
        self.g_months = dti.month.to_numpy().astype(np.int64)
        self.g_days = dti.day.to_numpy().astype(np.int64)

    def time_jalali_to_gregorian_vectorized(self, _size: int) -> None:
        jalali_to_gregorian_vectorized(self.j_years, self.j_months, self.j_days)

    def time_gregorian_to_jalali_vectorized(self, _size: int) -> None:
        gregorian_to_jalali_vectorized(self.g_years, self.g_months, self.g_days)

    def time_datetime64_to_jalali(self, _size: int) -> None:
        datetime64_to_jalali(self.gregorian)

    def time_jalali_to_datetime64(self, _size: int) -> None:
        jalali_to_datetime64(self.j_years, self.j_months, self.j_days)
