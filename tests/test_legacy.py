"""Tests for legacy accessors to keep backward compatibility stable."""

from __future__ import annotations

import jdatetime
import pandas as pd
import pytest

from jalali_pandas.df_handler import JalaliDataframeAccessor
from jalali_pandas.serie_handler import JalaliSerieAccessor


class TestLegacySeriesAccessor:
    """Tests for the legacy Series accessor."""

    def test_to_jalali_and_to_gregorian(self) -> None:
        series = pd.Series([pd.Timestamp("2023-03-21"), pd.Timestamp("2023-03-22")])
        accessor = JalaliSerieAccessor(series)
        jalali = accessor.to_jalali()

        assert isinstance(jalali.iloc[0], jdatetime.datetime)

        gregorian = JalaliSerieAccessor(jalali).to_gregorian()
        assert gregorian.iloc[0] == pd.Timestamp("2023-03-21")

    def test_parse_jalali(self) -> None:
        series = pd.Series(["1402-01-01", "1402-01-02"])
        parsed = JalaliSerieAccessor(series).parse_jalali("%Y-%m-%d")

        assert parsed.iloc[0].year == 1402
        assert parsed.iloc[0].month == 1
        assert parsed.iloc[0].day == 1

    def test_properties(self) -> None:
        series = pd.Series([jdatetime.datetime(1402, 7, 1, 10, 15, 20)])
        accessor = JalaliSerieAccessor(series)

        assert accessor.year.iloc[0] == 1402
        assert accessor.month.iloc[0] == 7
        assert accessor.day.iloc[0] == 1
        assert accessor.hour.iloc[0] == 10
        assert accessor.minute.iloc[0] == 15
        assert accessor.second.iloc[0] == 20
        assert accessor.weekday.iloc[0] == series.iloc[0].weekday()
        assert accessor.weeknumber.iloc[0] == series.iloc[0].weeknumber()
        assert accessor.quarter.iloc[0] == 3

    def test_validate_raises_on_invalid_type(self) -> None:
        series = pd.Series([1, 2, 3])
        accessor = JalaliSerieAccessor(series)

        with pytest.raises(TypeError):
            _ = accessor.year


class TestLegacyDataFrameAccessor:
    """Tests for the legacy DataFrame accessor."""

    def test_detects_jalali_column(self) -> None:
        df = pd.DataFrame(
            {
                "jalali": [jdatetime.datetime(1402, 1, 1)],
                "value": [10],
            }
        )
        accessor = JalaliDataframeAccessor(df)

        assert accessor.jdate == "jalali"
        temp = accessor._df
        assert "__year" in temp.columns
        assert "__month" in temp.columns

    def test_missing_jalali_column_raises(self) -> None:
        df = pd.DataFrame({"date": pd.date_range("2023-01-01", periods=2)})
        with pytest.raises(ValueError, match="No jdatetime column"):
            _ = JalaliDataframeAccessor(df)

    def test_groupby_with_numeric_columns(self) -> None:
        dates = [jdatetime.datetime(1402, 1, 1), jdatetime.datetime(1402, 1, 2)]
        df = pd.DataFrame({"jdate": dates, "value": [1, 2]})
        accessor = JalaliDataframeAccessor(df)

        result = accessor.groupby("year").sum()
        assert result["value"].iloc[0] == 3

    def test_groupby_without_numeric_columns(self) -> None:
        dates = [jdatetime.datetime(1402, 1, 1), jdatetime.datetime(1402, 1, 2)]
        df = pd.DataFrame({"jdate": dates, "label": ["a", "b"]})
        accessor = JalaliDataframeAccessor(df)

        grouped = accessor.groupby("year")
        assert grouped.size().iloc[0] == 2

    def test_groupby_invalid_key(self) -> None:
        df = pd.DataFrame({"jdate": [jdatetime.datetime(1402, 1, 1)], "value": [10]})
        accessor = JalaliDataframeAccessor(df)

        with pytest.raises(ValueError, match="not a valid groupby"):
            accessor.groupby("invalid")

    def test_resample_valid_and_invalid(self) -> None:
        dates = [
            jdatetime.datetime(1402, 1, 1),
            jdatetime.datetime(1402, 1, 15),
            jdatetime.datetime(1402, 2, 1),
        ]
        df = pd.DataFrame({"jdate": dates, "value": [1, 2, 3]})
        accessor = JalaliDataframeAccessor(df)

        result = accessor.resample("month")
        assert not result.empty

        with pytest.raises(ValueError, match="not a valid resample"):
            accessor.resample("daily")
