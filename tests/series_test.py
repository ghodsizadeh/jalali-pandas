"""Test Series class"""

import jdatetime
import pandas as pd
import pytest

import jalali_pandas  # noqa: F401


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
        """Test jalali convertor from gregorian to jalali"""
        df = self.df
        assert df["jdate"].iloc[0] == jdatetime.datetime(year=1397, month=10, day=11)
        assert df["date"].iloc[0] == pd.Timestamp("2019-01-01")

    def test_gregorian_convertor(self):
        """Test jalali convertor from jalali to gregorian"""

        df = self.df
        df["gdate"] = df["jdate"].jalali.to_gregorian()
        date = df["gdate"].iloc[0]
        assert date.year == 2019, "year is not 2019"
        assert date.month == 1, "month is not 1"
        assert date.day == 1, "day is not 1"

    def test_on_not_jdatetime(self):
        """Test jalali raise error on wrong columns"""
        df = self.df
        with pytest.raises(TypeError):
            _ = df["date"].jalali.year

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


def test_jalali_strptime():
    """Test jalali convertor from str to jalali"""
    df = pd.DataFrame({"date": ["1399/08/02", "1399/08/03", "1399/08/04"]})
    df["jdate"] = df["date"].jalali.parse_jalali("%Y/%m/%d")
    date = df["jdate"].iloc[0]
    assert date.year == 1399, "year is not 1399"
    assert date.month == 8, "month is not 8"
    assert date.day == 2, "day is not 2"
