"""Test Series class
"""
import jdatetime
import pandas as pd
from jalali_pandas import JalaliSerieAccessor  # pylint: disable=W0611


class TestJalaliSerie:
    """Test Cases for JalaliSerieAccessor"""

    @property
    def df(self) -> pd.DataFrame:
        """get test dataframe

        Returns:
            pd.DataFrame: test dataframe
        """
        df = pd.DataFrame({"date": pd.date_range("2019-01-01", periods=10, freq="D")})
        df["jdate"] = df["date"].jalali.to_jalali()
        return df

    def test_jalali_convertor(self):
        """Test jalali convertor from georgian to jalali"""
        df = self.df
        assert df["jdate"].iloc[0] == jdatetime.datetime(year=1397, month=10, day=11)
        assert df["date"].iloc[0] == pd.Timestamp("2019-01-01")

    def test_jalali_property(self):
        """Test jalali property like year, month, weeknumber"""
        df = self.df
        assert df["jdate"].jalali.year[0] == 1397, "year is not 1397"
        assert df["jdate"].jalali.month[0] == 10, "month is not 10"
        assert df["jdate"].jalali.day[0] == 11, "day is not 11"
        assert df["jdate"].jalali.hour[0] == 0, "hour is not 0"
        assert df["jdate"].jalali.minute[0] == 0, "minute is not 0"
        assert df["jdate"].jalali.second[0] == 0, "second is not 0"
        assert df["jdate"].jalali.weekday[0] == 3, "weekday is not 4"
        assert df["jdate"].jalali.weeknumber[0] == 42, "weeknumber is not 42"
        assert df["jdate"].jalali.quarter[0] == 4, "quarter is not 4"
