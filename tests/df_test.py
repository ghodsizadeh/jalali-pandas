"""Test Series class"""

import pandas as pd
import pytest

import jalali_pandas  # noqa: F401


class TestJalaliDataFrame:
    """Test Cases for JalaliSerieAccessor"""

    @property
    def df(self) -> pd.DataFrame:
        """get test dataframe

        Returns:
            pd.DataFrame: test dataframe
        """
        df = pd.DataFrame(
            {
                "date": pd.date_range("2019-01-01", periods=10, freq="M"),
                "value": range(10),
            }
        )
        df["jdate"] = df["date"].jalali.to_jalali()
        return df

    def test_jalali_groupby(self):
        """Test jalali property like year, month, weeknumber"""
        df = self.df
        mean = df.jalali.groupby("year").mean()
        assert (mean.index == [1397, 1398]).all(), "Year grouping is wrong"
        mean = df.jalali.groupby("month").mean()
        assert not set(mean.index).difference(
            {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}
        ), "computaion is wrong"

    def test_jalali_groupby_shorts(self):
        """Test jalali property like ymd, ym, yq, md"""
        df = self.df
        mean = df.jalali.groupby("ymd").mean()
        assert mean.index.names == [
            "__year",
            "__month",
            "__day",
        ], "ymd grouping is wrong"
        mean = df.jalali.groupby("ym").mean()
        assert mean.index.names == ["__year", "__month"], "ym grouping is wrong"
        mean = df.jalali.groupby("yq").mean()
        assert mean.index.names == ["__year", "__quarter"], "yq grouping is wrong"
        mean = df.jalali.groupby("md").mean()
        assert mean.index.names == ["__month", "__day"], "md grouping is wrong"

    def test_check_wrong_groupby(self):
        """Test check_df"""
        df = self.df
        # check it raise Value Error
        with pytest.raises(ValueError):
            df.jalali.groupby("wrong")

    def test_resample_invalid_type(self):
        """Test resample with invalid type raises ValueError."""
        df = self.df
        with pytest.raises(ValueError):
            df.jalali.resample("invalid_type")

    def test_resample_monthly(self):
        """Test resample by month works."""
        df = self.df
        result = df.jalali.resample("month")
        assert result is not None
        assert len(result) > 0

    def test_validation(self):
        """Test validation"""
        df = self.df.copy()
        del df["jdate"]
        with pytest.raises(ValueError):
            _ = df.jalali
