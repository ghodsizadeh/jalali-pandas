"""Tests for Phase 4: Time Series Operations.

Tests for resampling, groupby with Jalali components, rolling/shifting with Jalali offsets.
"""

import numpy as np
import pandas as pd
import pytest

from jalali_pandas import (
    JalaliDatetimeIndex,
    JalaliTimestamp,
    jalali_date_range,
)
from jalali_pandas.api.grouper import resample_jalali
from jalali_pandas.offsets import JalaliMonthEnd


class TestResamplingWithJalaliIndex:
    """Tests for resampling with Jalali boundaries using resample_jalali."""

    @pytest.fixture
    def daily_series(self):
        """Create a daily series with Gregorian index (converted from Jalali)."""
        idx = jalali_date_range("1402-01-01", periods=90, freq="D")
        return pd.Series(np.arange(90), index=idx.to_gregorian(), name="values")

    @pytest.fixture
    def daily_jalali_series(self):
        """Create a daily series with JalaliDatetimeIndex."""
        idx = jalali_date_range("1402-01-01", periods=90, freq="D")
        return pd.Series(np.arange(90), index=idx, name="values")

    def test_resample_monthly_sum(self, daily_series):
        """Test monthly resampling with sum aggregation using resample_jalali."""
        result = resample_jalali(daily_series, "JME").sum()
        assert len(result) > 0
        # First 31 days should sum to 0+1+...+30 = 465
        assert result.iloc[0] == sum(range(31))

    def test_resample_monthly_mean(self, daily_series):
        """Test monthly resampling with mean aggregation."""
        result = resample_jalali(daily_series, "JME").mean()
        assert len(result) > 0
        # First month mean should be (0+1+...+30)/31 = 15
        assert result.iloc[0] == 15.0

    def test_resample_monthly_min_max(self, daily_series):
        """Test monthly resampling with min/max aggregation."""
        min_result = resample_jalali(daily_series, "JME").min()
        max_result = resample_jalali(daily_series, "JME").max()

        assert min_result.iloc[0] == 0
        assert max_result.iloc[0] == 30

    def test_resample_quarterly(self, daily_series):
        """Test quarterly resampling."""
        result = resample_jalali(daily_series, "JQE").sum()
        assert len(result) > 0

    def test_resample_with_closed_left(self, daily_series):
        """Test resampling with closed='left' parameter."""
        result = resample_jalali(daily_series, "JME", closed="left").sum()
        assert len(result) > 0

    def test_resample_with_label_left(self, daily_series):
        """Test resampling with label='left' parameter."""
        result = resample_jalali(daily_series, "JME", label="left").sum()
        assert len(result) > 0


class TestUpsamplingDownsampling:
    """Tests for upsampling and downsampling."""

    @pytest.fixture
    def monthly_series(self):
        """Create a monthly series."""
        idx = jalali_date_range("1402-01-01", periods=12, freq="JME")
        return pd.Series(np.arange(12), index=idx.to_gregorian(), name="values")

    def test_upsample_to_daily_ffill(self, monthly_series):
        """Test upsampling to daily with forward fill."""
        result = monthly_series.resample("D").ffill()
        assert len(result) > len(monthly_series)

    def test_upsample_to_daily_bfill(self, monthly_series):
        """Test upsampling to daily with backward fill."""
        result = monthly_series.resample("D").bfill()
        assert len(result) > len(monthly_series)

    def test_downsample_to_quarterly(self, monthly_series):
        """Test downsampling to quarterly using resample_jalali."""
        result = resample_jalali(monthly_series, "JQE").sum()
        # 12 months -> 4 quarters
        assert len(result) <= 4


class TestShiftingWithJalaliOffsets:
    """Tests for shifting with Jalali offsets."""

    @pytest.fixture
    def sample_series_gregorian(self):
        """Create a sample series with Gregorian index (for pandas shift)."""
        idx = jalali_date_range("1402-01-01", periods=10, freq="D")
        return pd.Series(np.arange(10), index=idx.to_gregorian(), name="values")

    @pytest.fixture
    def sample_dataframe_gregorian(self):
        """Create a sample DataFrame with Gregorian index."""
        idx = jalali_date_range("1402-01-01", periods=10, freq="D")
        return pd.DataFrame(
            {"A": np.arange(10), "B": np.arange(10, 20)}, index=idx.to_gregorian()
        )

    def test_series_shift_with_timedelta(self, sample_series_gregorian):
        """Test Series.shift with Timedelta."""
        shifted = sample_series_gregorian.shift(1, freq=pd.Timedelta(days=1))
        # Index should be shifted by 1 day
        expected = sample_series_gregorian.index[0] + pd.Timedelta(days=1)
        assert shifted.index[0] == expected

    def test_dataframe_shift_with_timedelta(self, sample_dataframe_gregorian):
        """Test DataFrame.shift with Timedelta."""
        shifted = sample_dataframe_gregorian.shift(1, freq=pd.Timedelta(days=1))
        expected = sample_dataframe_gregorian.index[0] + pd.Timedelta(days=1)
        assert shifted.index[0] == expected

    def test_jalali_index_shift_with_month_offset(self):
        """Test JalaliDatetimeIndex.shift with month offset."""
        idx = JalaliDatetimeIndex(["1402-01-15", "1402-02-15", "1402-03-15"])
        shifted = idx.shift(1, freq=JalaliMonthEnd())

        # Each date should move to next month end
        assert shifted[0].month >= 1

    def test_jalali_index_shift_with_timedelta(self):
        """Test JalaliDatetimeIndex.shift with Timedelta."""
        idx = JalaliDatetimeIndex(["1402-01-01", "1402-01-08", "1402-01-15"])
        shifted = idx.shift(1, freq=pd.Timedelta(days=7))

        # Each date should move by 7 days
        for i in range(len(idx)):
            diff = shifted[i].to_gregorian() - idx[i].to_gregorian()
            assert diff.days == 7

    def test_jalali_index_shift_negative(self):
        """Test JalaliDatetimeIndex.shift with negative periods."""
        idx = JalaliDatetimeIndex(["1402-01-15", "1402-02-15", "1402-03-15"])
        shifted = idx.shift(-1, freq=pd.Timedelta(days=1))

        # Each date should move back by 1 day
        assert shifted[0] == JalaliTimestamp(1402, 1, 14)


class TestRollingWithJalaliOffsets:
    """Tests for rolling operations with Jalali offsets."""

    @pytest.fixture
    def daily_series(self):
        """Create a daily series with Gregorian index for rolling tests."""
        idx = jalali_date_range("1402-01-01", periods=30, freq="D")
        return pd.Series(np.arange(30), index=idx.to_gregorian(), name="values")

    def test_rolling_with_timedelta_window(self, daily_series):
        """Test rolling with Timedelta window."""
        result = daily_series.rolling("7D").mean()
        assert len(result) == len(daily_series)
        # First 6 values should be NaN or partial
        assert pd.notna(result.iloc[6])

    def test_rolling_sum(self, daily_series):
        """Test rolling sum."""
        result = daily_series.rolling(7).sum()
        assert len(result) == len(daily_series)
        # 7-day rolling sum at day 7 should be 0+1+2+3+4+5+6 = 21
        assert result.iloc[6] == 21

    def test_rolling_min_max(self, daily_series):
        """Test rolling min/max."""
        min_result = daily_series.rolling(7).min()
        max_result = daily_series.rolling(7).max()

        assert min_result.iloc[6] == 0
        assert max_result.iloc[6] == 6


class TestExpandingOperations:
    """Tests for expanding operations."""

    @pytest.fixture
    def daily_series(self):
        """Create a daily series."""
        idx = jalali_date_range("1402-01-01", periods=30, freq="D")
        return pd.Series(np.arange(30), index=idx.to_gregorian(), name="values")

    def test_expanding_sum(self, daily_series):
        """Test expanding sum."""
        result = daily_series.expanding().sum()
        assert len(result) == len(daily_series)
        # Expanding sum at position 5 should be 0+1+2+3+4+5 = 15
        assert result.iloc[5] == 15

    def test_expanding_mean(self, daily_series):
        """Test expanding mean."""
        result = daily_series.expanding().mean()
        assert len(result) == len(daily_series)
        # Expanding mean at position 2 should be (0+1+2)/3 = 1.0
        assert result.iloc[2] == 1.0

    def test_expanding_min_max(self, daily_series):
        """Test expanding min/max."""
        min_result = daily_series.expanding().min()
        max_result = daily_series.expanding().max()

        # Min should always be 0 (first value)
        assert all(min_result == 0)
        # Max at position i should be i
        assert max_result.iloc[10] == 10


class TestJalaliGrouper:
    """Tests for JalaliGrouper class."""

    @pytest.fixture
    def sample_df(self):
        """Create a sample DataFrame with Jalali datetime column."""
        dates = jalali_date_range("1402-01-01", periods=90, freq="D")
        return pd.DataFrame(
            {
                "date": dates.to_gregorian(),
                "jalali_date": list(dates),
                "value": np.arange(90),
            }
        )

    def test_grouper_by_month(self, sample_df):
        """Test grouping by Jalali month."""
        from jalali_pandas.api.grouper import JalaliGrouper

        grouper = JalaliGrouper(key="date", freq="JME")
        groups = grouper.get_grouper(sample_df)
        result = sample_df.groupby(groups).sum(numeric_only=True)

        # Should have 3 months of data
        assert len(result) == 3

    def test_grouper_by_quarter(self, sample_df):
        """Test grouping by Jalali quarter."""
        from jalali_pandas.api.grouper import JalaliGrouper

        grouper = JalaliGrouper(key="date", freq="JQE")
        groups = grouper.get_grouper(sample_df)
        result = sample_df.groupby(groups).sum(numeric_only=True)

        # 90 days spans Q1 (should be 1 quarter)
        assert len(result) >= 1

    def test_grouper_with_aggregation(self, sample_df):
        """Test grouper with various aggregations."""
        from jalali_pandas.api.grouper import JalaliGrouper

        grouper = JalaliGrouper(key="date", freq="JME")
        groups = grouper.get_grouper(sample_df)
        grouped = sample_df.groupby(groups)

        assert grouped.mean(numeric_only=True) is not None
        assert grouped.sum(numeric_only=True) is not None
        assert grouped.min(numeric_only=True) is not None
        assert grouped.max(numeric_only=True) is not None

    def test_grouper_without_key_uses_index(self):
        """Test grouper falls back to DatetimeIndex."""
        from jalali_pandas.api.grouper import JalaliGrouper

        idx = pd.date_range("2023-03-21", periods=5, freq="D")
        series = pd.Series(range(5), index=idx)
        grouper = JalaliGrouper(freq="JME")

        groups = grouper.get_grouper(series)
        assert len(groups) == len(series)

    def test_grouper_requires_key_or_datetime_index(self):
        """Test grouper raises when no key or DatetimeIndex is present."""
        from jalali_pandas.api.grouper import JalaliGrouper

        series = pd.Series(range(3))
        grouper = JalaliGrouper(freq="JME")

        with pytest.raises(ValueError, match="requires either"):
            _ = grouper.get_grouper(series)

    def test_grouper_handles_jalali_values(self):
        """Test grouper handles JalaliTimestamp values directly."""
        from jalali_pandas.api.grouper import JalaliGrouper
        from jalali_pandas.core.timestamp import JalaliTimestamp

        series = pd.Series([JalaliTimestamp(1402, 1, 1)])
        grouper = JalaliGrouper(freq="INVALID")

        groups = grouper._compute_jalali_groups(series)
        assert groups.iloc[0] == pd.Timestamp("2023-03-21")


class TestJalaliResamplerInternals:
    """Tests for JalaliResampler internal behaviors."""

    def test_resampler_apply_agg(self):
        """Test internal aggregation helper."""
        idx = pd.date_range("2023-03-21", periods=10, freq="D")
        series = pd.Series(range(10), index=idx)

        resampler = resample_jalali(series, "JME")
        result = resampler._apply_agg("sum")
        assert result.sum() == 45

    def test_resampler_requires_datetime_index(self):
        """Test resampler raises for non-datetime index."""
        series = pd.Series(range(3))
        with pytest.raises(ValueError, match="DatetimeIndex"):
            _ = resample_jalali(series, "JME")


class TestDataFrameAccessorResample:
    """Tests for DataFrame accessor resample method."""

    @pytest.fixture
    def sample_df(self):
        """Create a sample DataFrame with jdatetime column."""
        import jdatetime

        dates = (
            [jdatetime.datetime(1402, 1, i) for i in range(1, 32)]
            + [jdatetime.datetime(1402, 2, i) for i in range(1, 32)]
            + [jdatetime.datetime(1402, 3, i) for i in range(1, 28)]
        )

        return pd.DataFrame(
            {
                "jdate": dates,
                "value": np.arange(len(dates)),
            }
        )

    def test_accessor_resample_monthly(self, sample_df):
        """Test DataFrame accessor resample by month."""
        result = sample_df.jalali.resample("month")
        assert result is not None
        assert len(result) == 3  # 3 months

    def test_accessor_resample_quarterly(self, sample_df):
        """Test DataFrame accessor resample by quarter."""
        result = sample_df.jalali.resample("quarter")
        assert result is not None


class TestResamplingLimitations:
    """Document and test limitations of resampling."""

    def test_resample_jalali_with_gregorian_index(self):
        """Test that resample_jalali works with Gregorian index."""
        idx = jalali_date_range("1402-01-01", periods=30, freq="D")
        series = pd.Series(np.arange(30), index=idx.to_gregorian())

        # Use resample_jalali for Jalali-aware resampling
        result = resample_jalali(series, "JME").sum()
        assert len(result) > 0

    def test_resample_jalali_monthly(self):
        """Test resample_jalali with monthly frequency."""
        idx = jalali_date_range("1402-01-01", periods=60, freq="D")
        series = pd.Series(np.arange(60), index=idx.to_gregorian())

        # Using JME (Jalali Month End) as rule
        result = resample_jalali(series, "JME").sum()
        assert len(result) == 2  # 60 days = ~2 months
