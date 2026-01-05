"""Comprehensive tests for enhanced Series and DataFrame accessors."""

from datetime import time

import jdatetime
import pandas as pd
import pytest

import jalali_pandas  # noqa: F401


class TestJalaliSeriesAccessor:
    """Test cases for JalaliSeriesAccessor."""

    @pytest.fixture
    def jalali_series(self) -> pd.Series:
        """Create a test series with jdatetime objects."""
        dates = [
            jdatetime.datetime(1402, 1, 1, 10, 30, 45),  # Nowruz
            jdatetime.datetime(1402, 3, 31, 12, 0, 0),  # End of Q1
            jdatetime.datetime(1402, 6, 31, 0, 0, 0),  # End of Q2
            jdatetime.datetime(1402, 9, 30, 23, 59, 59),  # End of Q3
            jdatetime.datetime(1402, 12, 29, 0, 0, 0),  # End of year (non-leap)
        ]
        return pd.Series(dates)

    @pytest.fixture
    def gregorian_series(self) -> pd.Series:
        """Create a test series with Gregorian dates."""
        return pd.Series(pd.date_range("2023-03-21", periods=5, freq="D"))

    # -------------------------------------------------------------------------
    # Conversion Tests
    # -------------------------------------------------------------------------

    def test_to_jalali(self, gregorian_series: pd.Series) -> None:
        """Test conversion from Gregorian to Jalali."""
        result = gregorian_series.jalali.to_jalali()
        assert len(result) == 5
        assert result.iloc[0].year == 1402
        assert result.iloc[0].month == 1
        assert result.iloc[0].day == 1

    def test_to_gregorian(self, jalali_series: pd.Series) -> None:
        """Test conversion from Jalali to Gregorian."""
        result = jalali_series.jalali.to_gregorian()
        assert len(result) == 5
        # 1402/1/1 = 2023/3/21
        assert result.iloc[0].year == 2023
        assert result.iloc[0].month == 3
        assert result.iloc[0].day == 21

    def test_parse_jalali(self) -> None:
        """Test parsing string dates to jdatetime."""
        s = pd.Series(["1402-01-01", "1402-06-15", "1402-12-29"])
        result = s.jalali.parse_jalali("%Y-%m-%d")
        assert result.iloc[0].year == 1402
        assert result.iloc[1].month == 6
        assert result.iloc[2].day == 29

    # -------------------------------------------------------------------------
    # Basic Property Tests
    # -------------------------------------------------------------------------

    def test_year_property(self, jalali_series: pd.Series) -> None:
        """Test year property."""
        result = jalali_series.jalali.year
        assert (result == 1402).all()

    def test_month_property(self, jalali_series: pd.Series) -> None:
        """Test month property."""
        result = jalali_series.jalali.month
        assert list(result) == [1, 3, 6, 9, 12]

    def test_day_property(self, jalali_series: pd.Series) -> None:
        """Test day property."""
        result = jalali_series.jalali.day
        assert list(result) == [1, 31, 31, 30, 29]

    def test_hour_property(self, jalali_series: pd.Series) -> None:
        """Test hour property."""
        result = jalali_series.jalali.hour
        assert list(result) == [10, 12, 0, 23, 0]

    def test_minute_property(self, jalali_series: pd.Series) -> None:
        """Test minute property."""
        result = jalali_series.jalali.minute
        assert list(result) == [30, 0, 0, 59, 0]

    def test_second_property(self, jalali_series: pd.Series) -> None:
        """Test second property."""
        result = jalali_series.jalali.second
        assert list(result) == [45, 0, 0, 59, 0]

    def test_quarter_property(self, jalali_series: pd.Series) -> None:
        """Test quarter property."""
        result = jalali_series.jalali.quarter
        assert list(result) == [1, 1, 2, 3, 4]

    def test_weekday_property(self, jalali_series: pd.Series) -> None:
        """Test weekday property."""
        result = jalali_series.jalali.weekday
        assert len(result) == 5
        # All values should be 0-6
        assert all(0 <= x <= 6 for x in result)

    def test_dayofweek_alias(self, jalali_series: pd.Series) -> None:
        """Test dayofweek is alias for weekday."""
        weekday = jalali_series.jalali.weekday
        dayofweek = jalali_series.jalali.dayofweek
        assert (weekday == dayofweek).all()

    def test_dayofyear_property(self, jalali_series: pd.Series) -> None:
        """Test dayofyear property."""
        result = jalali_series.jalali.dayofyear
        # 1402/1/1 = day 1
        assert result.iloc[0] == 1
        # 1402/3/31 = 31 + 31 + 31 = 93
        assert result.iloc[1] == 93

    def test_daysinmonth_property(self, jalali_series: pd.Series) -> None:
        """Test daysinmonth property."""
        result = jalali_series.jalali.daysinmonth
        # Month 1 has 31 days, month 12 has 29 (non-leap)
        assert result.iloc[0] == 31
        assert result.iloc[4] == 29

    def test_days_in_month_alias(self, jalali_series: pd.Series) -> None:
        """Test days_in_month is alias for daysinmonth."""
        daysinmonth = jalali_series.jalali.daysinmonth
        days_in_month = jalali_series.jalali.days_in_month
        assert (daysinmonth == days_in_month).all()

    def test_week_property(self, jalali_series: pd.Series) -> None:
        """Test week property."""
        result = jalali_series.jalali.week
        assert len(result) == 5
        # All values should be 1-53
        assert all(1 <= x <= 53 for x in result)

    def test_weekofyear_alias(self, jalali_series: pd.Series) -> None:
        """Test weekofyear is alias for week."""
        week = jalali_series.jalali.week
        weekofyear = jalali_series.jalali.weekofyear
        assert (week == weekofyear).all()

    # -------------------------------------------------------------------------
    # Boolean Property Tests
    # -------------------------------------------------------------------------

    def test_is_leap_year(self) -> None:
        """Test is_leap_year property."""
        dates = [
            jdatetime.datetime(1403, 1, 1),  # Leap year
            jdatetime.datetime(1402, 1, 1),  # Non-leap year
        ]
        s = pd.Series(dates)
        result = s.jalali.is_leap_year
        assert result.iloc[0]
        assert not result.iloc[1]

    def test_is_month_start(self, jalali_series: pd.Series) -> None:
        """Test is_month_start property."""
        result = jalali_series.jalali.is_month_start
        # Only first date (1402/1/1) is month start
        assert result.iloc[0]
        assert not result.iloc[1]

    def test_is_month_end(self, jalali_series: pd.Series) -> None:
        """Test is_month_end property."""
        result = jalali_series.jalali.is_month_end
        # Dates 2, 3, 4, 5 are month ends
        assert not result.iloc[0]
        assert result.iloc[1]  # 3/31
        assert result.iloc[2]  # 6/31
        assert result.iloc[3]  # 9/30
        assert result.iloc[4]  # 12/29

    def test_is_quarter_start(self) -> None:
        """Test is_quarter_start property."""
        dates = [
            jdatetime.datetime(1402, 1, 1),  # Q1 start
            jdatetime.datetime(1402, 4, 1),  # Q2 start
            jdatetime.datetime(1402, 7, 1),  # Q3 start
            jdatetime.datetime(1402, 10, 1),  # Q4 start
            jdatetime.datetime(1402, 2, 1),  # Not quarter start
        ]
        s = pd.Series(dates)
        result = s.jalali.is_quarter_start
        assert list(result) == [True, True, True, True, False]

    def test_is_quarter_end(self, jalali_series: pd.Series) -> None:
        """Test is_quarter_end property."""
        result = jalali_series.jalali.is_quarter_end
        # 3/31, 6/31, 9/30, 12/29 are quarter ends
        assert not result.iloc[0]  # 1/1
        assert result.iloc[1]  # 3/31
        assert result.iloc[2]  # 6/31
        assert result.iloc[3]  # 9/30
        assert result.iloc[4]  # 12/29

    def test_is_year_start(self, jalali_series: pd.Series) -> None:
        """Test is_year_start property."""
        result = jalali_series.jalali.is_year_start
        # Only 1/1 is year start
        assert result.iloc[0]
        assert not result.iloc[1]

    def test_is_year_end(self, jalali_series: pd.Series) -> None:
        """Test is_year_end property."""
        result = jalali_series.jalali.is_year_end
        # Only 12/29 (non-leap) is year end
        assert not result.iloc[0]
        assert result.iloc[4]

    # -------------------------------------------------------------------------
    # Date/Time Property Tests
    # -------------------------------------------------------------------------

    def test_date_property(self, jalali_series: pd.Series) -> None:
        """Test date property returns dates at midnight."""
        result = jalali_series.jalali.date
        # All should have time = 0
        assert result.iloc[0].hour == 0
        assert result.iloc[0].minute == 0
        assert result.iloc[0].second == 0

    def test_time_property(self, jalali_series: pd.Series) -> None:
        """Test time property returns Python time objects."""
        result = jalali_series.jalali.time
        assert isinstance(result.iloc[0], time)
        assert result.iloc[0].hour == 10
        assert result.iloc[0].minute == 30
        assert result.iloc[0].second == 45

    # -------------------------------------------------------------------------
    # String Method Tests
    # -------------------------------------------------------------------------

    def test_strftime(self, jalali_series: pd.Series) -> None:
        """Test strftime method."""
        result = jalali_series.jalali.strftime("%Y/%m/%d")
        assert result.iloc[0] == "1402/01/01"
        assert result.iloc[1] == "1402/03/31"

    def test_month_name_english(self, jalali_series: pd.Series) -> None:
        """Test month_name with English locale."""
        result = jalali_series.jalali.month_name(locale="en")
        assert result.iloc[0] == "Farvardin"
        assert result.iloc[1] == "Khordad"
        assert result.iloc[4] == "Esfand"

    def test_month_name_persian(self, jalali_series: pd.Series) -> None:
        """Test month_name with Persian locale."""
        result = jalali_series.jalali.month_name(locale="fa")
        assert result.iloc[0] == "فروردین"
        assert result.iloc[4] == "اسفند"

    def test_day_name_english(self, jalali_series: pd.Series) -> None:
        """Test day_name with English locale."""
        result = jalali_series.jalali.day_name(locale="en")
        # All should be valid day names
        valid_names = [
            "Shanbeh",
            "Yekshanbeh",
            "Doshanbeh",
            "Seshanbeh",
            "Chaharshanbeh",
            "Panjshanbeh",
            "Jomeh",
        ]
        assert all(name in valid_names for name in result)

    def test_day_name_persian(self, jalali_series: pd.Series) -> None:
        """Test day_name with Persian locale."""
        result = jalali_series.jalali.day_name(locale="fa")
        valid_names = [
            "شنبه",
            "یکشنبه",
            "دوشنبه",
            "سه‌شنبه",
            "چهارشنبه",
            "پنجشنبه",
            "جمعه",
        ]
        assert all(name in valid_names for name in result)

    # -------------------------------------------------------------------------
    # Normalization Method Tests
    # -------------------------------------------------------------------------

    def test_normalize(self, jalali_series: pd.Series) -> None:
        """Test normalize method sets time to midnight."""
        result = jalali_series.jalali.normalize()
        for dt in result:
            assert dt.hour == 0
            assert dt.minute == 0
            assert dt.second == 0

    def test_floor_day(self, jalali_series: pd.Series) -> None:
        """Test floor to day."""
        result = jalali_series.jalali.floor("D")
        for dt in result:
            assert dt.hour == 0
            assert dt.minute == 0
            assert dt.second == 0

    def test_floor_hour(self, jalali_series: pd.Series) -> None:
        """Test floor to hour."""
        result = jalali_series.jalali.floor("h")
        assert result.iloc[0].hour == 10
        assert result.iloc[0].minute == 0
        assert result.iloc[0].second == 0

    def test_ceil_day(self) -> None:
        """Test ceil to day."""
        dates = [jdatetime.datetime(1402, 1, 1, 10, 30, 0)]
        s = pd.Series(dates)
        result = s.jalali.ceil("D")
        # Should round up to next day
        assert result.iloc[0].day == 2
        assert result.iloc[0].hour == 0

    def test_ceil_hour(self) -> None:
        """Test ceil to hour."""
        dates = [jdatetime.datetime(1402, 1, 1, 10, 30, 0)]
        s = pd.Series(dates)
        result = s.jalali.ceil("h")
        assert result.iloc[0].hour == 11
        assert result.iloc[0].minute == 0

    def test_round_day(self) -> None:
        """Test round to day."""
        dates = [
            jdatetime.datetime(1402, 1, 1, 10, 0, 0),  # Before noon
            jdatetime.datetime(1402, 1, 1, 14, 0, 0),  # After noon
        ]
        s = pd.Series(dates)
        result = s.jalali.round("D")
        assert result.iloc[0].day == 1  # Rounds down
        assert result.iloc[1].day == 2  # Rounds up

    def test_round_hour(self) -> None:
        """Test round to hour."""
        dates = [
            jdatetime.datetime(1402, 1, 1, 10, 20, 0),  # Before 30 min
            jdatetime.datetime(1402, 1, 1, 10, 40, 0),  # After 30 min
        ]
        s = pd.Series(dates)
        result = s.jalali.round("h")
        assert result.iloc[0].hour == 10  # Rounds down
        assert result.iloc[1].hour == 11  # Rounds up

    def test_floor_invalid_freq(self, jalali_series: pd.Series) -> None:
        """Test floor with invalid frequency raises error."""
        with pytest.raises(ValueError):
            jalali_series.jalali.floor("invalid")

    # -------------------------------------------------------------------------
    # NaT Handling Tests
    # -------------------------------------------------------------------------

    def test_properties_with_nat(self) -> None:
        """Test properties handle NaT correctly."""
        dates = [jdatetime.datetime(1402, 1, 1), pd.NaT]
        s = pd.Series(dates)

        year = s.jalali.year
        assert year.iloc[0] == 1402
        assert pd.isna(year.iloc[1])

    def test_strftime_with_nat(self) -> None:
        """Test strftime handles NaT correctly."""
        dates = [jdatetime.datetime(1402, 1, 1), pd.NaT]
        s = pd.Series(dates)
        result = s.jalali.strftime("%Y-%m-%d")
        assert result.iloc[0] == "1402-01-01"
        assert result.iloc[1] is None

    def test_empty_series_property(self) -> None:
        """Test empty series property access returns empty series."""
        s = pd.Series([], dtype=object)
        result = s.jalali.year
        assert result.empty

    def test_microsecond_and_nanosecond(self) -> None:
        """Test microsecond and nanosecond properties."""
        dates = [jdatetime.datetime(1402, 1, 1, 0, 0, 0, 123456), pd.NaT]
        s = pd.Series(dates)
        result_micro = s.jalali.microsecond
        result_nano = s.jalali.nanosecond

        assert result_micro.iloc[0] == 123456
        assert result_nano.iloc[0] == 0
        assert pd.isna(result_nano.iloc[1])

    def test_week_dayofyear_daysinmonth_with_nat(self) -> None:
        """Test week/dayofyear/daysinmonth handle NaT correctly."""
        dates = [jdatetime.datetime(1402, 1, 1), pd.NaT]
        s = pd.Series(dates)

        assert s.jalali.week.iloc[0] >= 1
        assert pd.isna(s.jalali.week.iloc[1])
        assert s.jalali.dayofyear.iloc[0] == 1
        assert pd.isna(s.jalali.dayofyear.iloc[1])
        assert s.jalali.daysinmonth.iloc[0] == 31
        assert pd.isna(s.jalali.daysinmonth.iloc[1])

    def test_date_and_time_with_date_objects(self) -> None:
        """Test date/time properties with jdatetime.date inputs."""
        dates = [jdatetime.date(1402, 1, 1), pd.NaT]
        s = pd.Series(dates)

        result_date = s.jalali.date
        result_time = s.jalali.time

        assert isinstance(result_date.iloc[0], jdatetime.date)
        assert result_time.iloc[0] == time(0, 0, 0)
        assert result_time.iloc[1] is None

    def test_month_day_name_with_nat(self, jalali_series: pd.Series) -> None:
        """Test month/day name returns None for NaT values."""
        s = pd.concat([jalali_series, pd.Series([pd.NaT])], ignore_index=True)
        month_names = s.jalali.month_name(locale="en")
        day_names = s.jalali.day_name(locale="en")

        assert month_names.iloc[-1] is None
        assert day_names.iloc[-1] is None

    def test_floor_minute_second(self) -> None:
        """Test floor for minute and second frequencies."""
        dates = [jdatetime.datetime(1402, 1, 1, 10, 5, 45, 123456)]
        s = pd.Series(dates)

        floored_min = s.jalali.floor("min")
        floored_sec = s.jalali.floor("s")

        assert floored_min.iloc[0].minute == 5
        assert floored_min.iloc[0].second == 0
        assert floored_sec.iloc[0].second == 45
        assert floored_sec.iloc[0].microsecond == 0

    def test_floor_date_passthrough(self) -> None:
        """Test floor returns non-datetime values unchanged."""
        dates = [jdatetime.date(1402, 1, 1)]
        s = pd.Series(dates)

        result = s.jalali.floor("D")
        assert isinstance(result.iloc[0], jdatetime.date)

    def test_ceil_minute_second(self) -> None:
        """Test ceil for minute and second frequencies."""
        dates = [jdatetime.datetime(1402, 1, 1, 10, 5, 30, 1)]
        s = pd.Series(dates)

        ceiled_min = s.jalali.ceil("min")
        ceiled_sec = s.jalali.ceil("s")

        assert ceiled_min.iloc[0].minute == 6
        assert ceiled_min.iloc[0].second == 0
        assert ceiled_sec.iloc[0].second == 31

    def test_round_minute_second(self) -> None:
        """Test round for minute and second frequencies."""
        dates = [jdatetime.datetime(1402, 1, 1, 10, 5, 40, 600000)]
        s = pd.Series(dates)

        rounded_min = s.jalali.round("min")
        rounded_sec = s.jalali.round("s")

        assert rounded_min.iloc[0].minute == 6
        assert rounded_sec.iloc[0].second == 41

    def test_ceil_and_round_invalid_freq(self, jalali_series: pd.Series) -> None:
        """Test ceil and round with invalid frequency raises error."""
        with pytest.raises(ValueError):
            jalali_series.jalali.ceil("invalid")
        with pytest.raises(ValueError):
            jalali_series.jalali.round("invalid")

    def test_timezone_localize_and_convert(self) -> None:
        """Test tz_localize and tz_convert methods."""
        from datetime import timedelta, timezone

        naive_dates = [jdatetime.datetime(1402, 1, 1, 12, 0, 0)]
        s = pd.Series(naive_dates)
        localized = s.jalali.tz_localize("UTC")
        assert localized.iloc[0].tzinfo is not None

        offset_tz = timezone(timedelta(hours=3, minutes=30))
        aware_dates = [jdatetime.datetime(1402, 1, 1, 12, 0, 0, tzinfo=timezone.utc)]
        aware_series = pd.Series(aware_dates)
        converted = aware_series.jalali.tz_convert(offset_tz)
        assert converted.iloc[0].tzinfo is not None


class TestJalaliDataFrameAccessor:
    """Test cases for JalaliDataFrameAccessor."""

    @pytest.fixture
    def jalali_df(self) -> pd.DataFrame:
        """Create a test DataFrame with jdatetime column."""
        dates = [
            jdatetime.datetime(1402, 1, 1),
            jdatetime.datetime(1402, 1, 15),
            jdatetime.datetime(1402, 2, 1),
            jdatetime.datetime(1402, 4, 1),
            jdatetime.datetime(1402, 7, 1),
        ]
        return pd.DataFrame({"jdate": dates, "value": [10, 20, 30, 40, 50]})

    # -------------------------------------------------------------------------
    # Validation Tests
    # -------------------------------------------------------------------------

    def test_validation_no_jdate_column(self) -> None:
        """Test validation fails without jdatetime column."""
        df = pd.DataFrame(
            {"date": pd.date_range("2023-01-01", periods=5), "value": range(5)}
        )
        with pytest.raises(ValueError, match="No jdatetime column found"):
            _ = df.jalali

    def test_set_date_column(self, jalali_df: pd.DataFrame) -> None:
        """Test set_date_column method."""
        accessor = jalali_df.jalali.set_date_column("jdate")
        assert accessor.jdate == "jdate"

    def test_set_date_column_invalid(self, jalali_df: pd.DataFrame) -> None:
        """Test set_date_column with invalid column raises error."""
        with pytest.raises(ValueError, match="not found"):
            jalali_df.jalali.set_date_column("nonexistent")

    def test_set_date_column_wrong_type(self) -> None:
        """Test set_date_column with non-jdatetime column raises error."""
        df = pd.DataFrame(
            {
                "jdate": [
                    jdatetime.datetime(1402, 1, 1),
                    jdatetime.datetime(1402, 1, 2),
                ],
                "date": pd.date_range("2023-01-01", periods=2),
                "value": [1, 2],
            }
        )
        with pytest.raises(ValueError, match="does not contain jdatetime"):
            df.jalali.set_date_column("date")

    # -------------------------------------------------------------------------
    # Groupby Tests
    # -------------------------------------------------------------------------

    def test_groupby_year(self, jalali_df: pd.DataFrame) -> None:
        """Test groupby by year."""
        result = jalali_df.jalali.groupby("year").sum()
        assert len(result) == 1  # All same year

    def test_groupby_month(self, jalali_df: pd.DataFrame) -> None:
        """Test groupby by month."""
        result = jalali_df.jalali.groupby("month").sum()
        assert len(result) == 4  # 4 unique months

    def test_groupby_quarter(self, jalali_df: pd.DataFrame) -> None:
        """Test groupby by quarter."""
        result = jalali_df.jalali.groupby("quarter").sum()
        assert len(result) == 3  # Q1, Q2, Q3

    def test_groupby_ym(self, jalali_df: pd.DataFrame) -> None:
        """Test groupby by year-month."""
        result = jalali_df.jalali.groupby("ym").sum()
        assert "__year" in result.index.names
        assert "__month" in result.index.names

    def test_groupby_yq(self, jalali_df: pd.DataFrame) -> None:
        """Test groupby by year-quarter."""
        result = jalali_df.jalali.groupby("yq").sum()
        assert "__year" in result.index.names
        assert "__quarter" in result.index.names

    def test_groupby_invalid(self, jalali_df: pd.DataFrame) -> None:
        """Test groupby with invalid key raises error."""
        with pytest.raises(ValueError):
            jalali_df.jalali.groupby("invalid")

    def test_groupby_dayofmonth(self, jalali_df: pd.DataFrame) -> None:
        """Test groupby by dayofmonth alias."""
        result = jalali_df.jalali.groupby("dayofmonth").sum()
        assert "__day" in result.index.names

    # -------------------------------------------------------------------------
    # Resample Tests
    # -------------------------------------------------------------------------

    def test_resample_month(self, jalali_df: pd.DataFrame) -> None:
        """Test resample by month."""
        result = jalali_df.jalali.resample("month")
        assert isinstance(result, pd.DataFrame)
        assert len(result) > 0

    def test_resample_quarter(self, jalali_df: pd.DataFrame) -> None:
        """Test resample by quarter."""
        result = jalali_df.jalali.resample("quarter")
        assert isinstance(result, pd.DataFrame)

    def test_resample_year(self, jalali_df: pd.DataFrame) -> None:
        """Test resample by year."""
        result = jalali_df.jalali.resample("year")
        assert isinstance(result, pd.DataFrame)

    def test_resample_week(self, jalali_df: pd.DataFrame) -> None:
        """Test resample by week."""
        result = jalali_df.jalali.resample("week")
        assert isinstance(result, pd.DataFrame)

    def test_resample_invalid(self, jalali_df: pd.DataFrame) -> None:
        """Test resample with invalid type raises error."""
        with pytest.raises(ValueError):
            jalali_df.jalali.resample("invalid")

    # -------------------------------------------------------------------------
    # Convert Columns Tests
    # -------------------------------------------------------------------------

    def test_convert_columns_to_jalali(self, jalali_df: pd.DataFrame) -> None:
        """Test convert_columns to Jalali."""
        # Add a Gregorian column to convert
        jalali_df["gdate"] = pd.date_range("2023-03-21", periods=5)
        result = jalali_df.jalali.convert_columns("gdate", to_jalali=True)
        assert result["gdate"].iloc[0].year == 1402

    def test_convert_columns_to_gregorian(self, jalali_df: pd.DataFrame) -> None:
        """Test convert_columns to Gregorian."""
        result = jalali_df.jalali.convert_columns("jdate", to_jalali=False)
        assert result["jdate"].iloc[0].year == 2023

    def test_convert_columns_multiple(self, jalali_df: pd.DataFrame) -> None:
        """Test convert_columns with multiple columns."""
        # Add Gregorian columns to convert
        jalali_df["gdate1"] = pd.date_range("2023-03-21", periods=5)
        jalali_df["gdate2"] = pd.date_range("2023-06-21", periods=5)
        result = jalali_df.jalali.convert_columns(["gdate1", "gdate2"], to_jalali=True)
        assert result["gdate1"].iloc[0].year == 1402
        assert result["gdate2"].iloc[0].year == 1402

    def test_convert_columns_invalid(self, jalali_df: pd.DataFrame) -> None:
        """Test convert_columns with invalid column raises error."""
        with pytest.raises(ValueError, match="not found"):
            jalali_df.jalali.convert_columns("nonexistent")

    def test_convert_columns_parse_strings(self) -> None:
        """Test convert_columns parses Jalali strings before Gregorian conversion."""
        df = pd.DataFrame(
            {
                "jdate": [
                    jdatetime.datetime(1402, 1, 1),
                    jdatetime.datetime(1402, 1, 2),
                ],
                "jdate_str": ["1402-01-01", "1402-01-02"],
                "value": [1, 2],
            }
        )
        result = df.jalali.convert_columns("jdate_str", to_jalali=False)
        assert isinstance(result["jdate_str"].iloc[0], pd.Timestamp)

    # -------------------------------------------------------------------------
    # To Period Tests
    # -------------------------------------------------------------------------

    def test_to_period_year(self, jalali_df: pd.DataFrame) -> None:
        """Test to_period with year frequency."""
        result = jalali_df.jalali.to_period("Y")
        assert "jdate_period" in result.columns
        assert result["jdate_period"].iloc[0] == "1402"

    def test_to_period_quarter(self, jalali_df: pd.DataFrame) -> None:
        """Test to_period with quarter frequency."""
        result = jalali_df.jalali.to_period("Q")
        assert result["jdate_period"].iloc[0] == "1402Q1"

    def test_to_period_month(self, jalali_df: pd.DataFrame) -> None:
        """Test to_period with month frequency."""
        result = jalali_df.jalali.to_period("M")
        assert result["jdate_period"].iloc[0] == "1402-01"

    def test_to_period_week(self, jalali_df: pd.DataFrame) -> None:
        """Test to_period with week frequency."""
        result = jalali_df.jalali.to_period("W")
        assert "jdate_period" in result.columns
        assert result["jdate_period"].iloc[0].startswith("1402W")

    def test_to_period_day(self, jalali_df: pd.DataFrame) -> None:
        """Test to_period with day frequency."""
        result = jalali_df.jalali.to_period("D")
        assert result["jdate_period"].iloc[0] == "1402-01-01"

    def test_to_period_with_nat(self) -> None:
        """Test to_period handles NaT values."""
        df = pd.DataFrame(
            {"jdate": [jdatetime.datetime(1402, 1, 1), pd.NaT], "value": [1, 2]}
        )
        result = df.jalali.to_period("M")
        assert result["jdate_period"].iloc[1] is None

    def test_to_period_invalid_freq(self, jalali_df: pd.DataFrame) -> None:
        """Test to_period with invalid frequency raises error."""
        with pytest.raises(ValueError, match="Unsupported frequency"):
            jalali_df.jalali.to_period("INVALID")

    # -------------------------------------------------------------------------
    # Filter Tests
    # -------------------------------------------------------------------------

    def test_filter_by_year(self, jalali_df: pd.DataFrame) -> None:
        """Test filter_by_year method."""
        result = jalali_df.jalali.filter_by_year(1402)
        assert len(result) == 5

    def test_filter_by_year_list(self) -> None:
        """Test filter_by_year with list of years."""
        dates = [
            jdatetime.datetime(1401, 1, 1),
            jdatetime.datetime(1402, 1, 1),
            jdatetime.datetime(1403, 1, 1),
        ]
        df = pd.DataFrame({"jdate": dates, "value": [1, 2, 3]})
        result = df.jalali.filter_by_year([1401, 1402])
        assert len(result) == 2

    def test_filter_by_month(self, jalali_df: pd.DataFrame) -> None:
        """Test filter_by_month method."""
        result = jalali_df.jalali.filter_by_month(1)
        assert len(result) == 2  # Two dates in month 1

    def test_filter_by_month_list(self, jalali_df: pd.DataFrame) -> None:
        """Test filter_by_month with list of months."""
        result = jalali_df.jalali.filter_by_month([1, 2])
        assert len(result) == 3

    def test_filter_by_quarter(self, jalali_df: pd.DataFrame) -> None:
        """Test filter_by_quarter method."""
        result = jalali_df.jalali.filter_by_quarter(1)
        assert len(result) == 3  # Q1 = months 1, 2, 3

    def test_filter_by_date_range(self, jalali_df: pd.DataFrame) -> None:
        """Test filter_by_date_range method."""
        result = jalali_df.jalali.filter_by_date_range(
            start="1402-01-01", end="1402-02-01"
        )
        assert len(result) == 3

    def test_filter_by_date_range_start_only(self, jalali_df: pd.DataFrame) -> None:
        """Test filter_by_date_range with start only."""
        result = jalali_df.jalali.filter_by_date_range(start="1402-04-01")
        assert len(result) == 2

    def test_filter_by_date_range_end_only(self, jalali_df: pd.DataFrame) -> None:
        """Test filter_by_date_range with end only."""
        result = jalali_df.jalali.filter_by_date_range(end="1402-02-01")
        assert len(result) == 3


class TestAccessorEdgeCases:
    """Test edge cases for accessors."""

    def test_empty_series(self) -> None:
        """Test accessor with empty series."""
        s = pd.Series([], dtype=object)
        # Should not raise during validation
        result = s.jalali.to_jalali()
        assert len(result) == 0

    def test_empty_dataframe(self) -> None:
        """Test accessor with empty DataFrame."""
        df = pd.DataFrame({"jdate": [], "value": []})
        # Empty DataFrame should raise since no jdatetime found
        with pytest.raises(ValueError):
            _ = df.jalali

    def test_series_with_all_nat(self) -> None:
        """Test series with all NaT values."""
        s = pd.Series([pd.NaT, pd.NaT, pd.NaT])
        result = s.jalali.to_jalali()
        assert all(pd.isna(x) for x in result)

    def test_leap_year_end(self) -> None:
        """Test leap year end date."""
        # 1403 is a leap year
        dates = [jdatetime.datetime(1403, 12, 30)]
        s = pd.Series(dates)
        assert s.jalali.is_year_end.iloc[0]
        assert s.jalali.daysinmonth.iloc[0] == 30
