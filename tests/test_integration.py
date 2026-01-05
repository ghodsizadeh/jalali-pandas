"""Integration tests across accessors and API helpers."""

from __future__ import annotations

import numpy as np
import pandas as pd

import jalali_pandas  # noqa: F401
from jalali_pandas import jalali_date_range
from jalali_pandas.api.grouper import resample_jalali


def test_dataframe_conversion_and_groupby() -> None:
    """Convert Gregorian series to Jalali and group by month."""
    df = pd.DataFrame(
        {
            "date": pd.date_range("2023-03-21", periods=10, freq="D"),
            "value": range(10),
        }
    )
    df["jdate"] = df["date"].jalali.to_jalali()

    grouped = df.jalali.groupby("month").sum()
    assert grouped["value"].sum() == df["value"].sum()


def test_resample_roundtrip() -> None:
    """Resample using Jalali boundaries on Gregorian-indexed data."""
    idx = jalali_date_range("1402-01-01", periods=45, freq="D")
    series = pd.Series(np.ones(len(idx)), index=idx.to_gregorian())

    result = resample_jalali(series, "JME").sum()
    assert result.sum() == len(series)
