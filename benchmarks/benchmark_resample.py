"""Benchmarks for Jalali resampling."""

from __future__ import annotations

import numpy as np
import pandas as pd

from jalali_pandas import jalali_date_range
from jalali_pandas.api.grouper import resample_jalali


class TimeResample:
    """Benchmark resampling operations."""

    params = [365, 3650]
    param_names = ["size"]

    def setup(self, size: int) -> None:
        idx = jalali_date_range("1402-01-01", periods=size, freq="D")
        self.series = pd.Series(np.arange(size), index=idx.to_gregorian())

    def time_resample_month_end(self, _size: int) -> None:
        resample_jalali(self.series, "JME").sum()
