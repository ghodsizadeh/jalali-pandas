"""Enhanced DataFrame accessor for Jalali datetime operations."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

import jdatetime
import pandas as pd
from pandas.core.groupby.generic import DataFrameGroupBy as DataFrameGroupByRuntime

if TYPE_CHECKING:
    from pandas.core.groupby.generic import DataFrameGroupBy

    DataFrameGroupByT = DataFrameGroupBy[pd.DataFrame, Any]
else:
    DataFrameGroupByT = DataFrameGroupByRuntime


@pd.api.extensions.register_dataframe_accessor("jalali")
class JalaliDataFrameAccessor:
    """Enhanced accessor for Jalali datetime operations on pandas DataFrames.

    Provides methods for working with Jalali (Persian/Shamsi) dates in
    pandas DataFrames, including groupby, resample, and column conversion.

    Attributes:
        jdate: Name of the detected Jalali date column.
        columns: DataFrame columns.

    Examples:
        >>> import pandas as pd
        >>> import jalali_pandas
        >>> df = pd.DataFrame({
        ...     'date': pd.date_range('2023-03-21', periods=5),
        ...     'value': [1, 2, 3, 4, 5]
        ... })
        >>> df['jdate'] = df['date'].jalali.to_jalali()
        >>> df.jalali.groupby('month').sum()
    """

    TEMP_COLUMNS: list[str] = [
        "__year",
        "__month",
        "__quarter",
        "__weekday",
        "__day",
        "__week",
        "__dayofyear",
    ]

    def __init__(self, pandas_obj: pd.DataFrame) -> None:
        """Initialize the accessor.

        Args:
            pandas_obj: A pandas DataFrame containing Jalali datetime data.
        """
        self._obj: pd.DataFrame = pandas_obj
        self.columns: pd.Index[Any] = self._obj.columns
        self.jdate: str = "jdate"
        self._validate()

    def _validate(self) -> None:
        """Check if the DataFrame has a jdatetime column.

        Raises:
            ValueError: If no jdatetime column is found.
        """
        for col in self.columns:
            if len(self._obj) > 0:
                first_val = self._obj[col].iloc[0]
                if isinstance(first_val, (jdatetime.date, jdatetime.datetime)):
                    self.jdate = str(col)
                    return
        raise ValueError("No jdatetime column found in the dataframe.")

    def set_date_column(self, column: str) -> JalaliDataFrameAccessor:
        """Set the Jalali date column to use for operations.

        Args:
            column: Name of the column containing Jalali dates.

        Returns:
            Self for method chaining.

        Raises:
            ValueError: If column doesn't exist or doesn't contain jdatetime.
        """
        if column not in self.columns:
            raise ValueError(f"Column '{column}' not found in DataFrame.")

        if len(self._obj) > 0:
            first_val = self._obj[column].iloc[0]
            if not isinstance(first_val, (jdatetime.date, jdatetime.datetime)):
                raise ValueError(
                    f"Column '{column}' does not contain jdatetime objects."
                )

        self.jdate = column
        return self

    @property
    def _df(self) -> pd.DataFrame:
        """Generate temp DataFrame with extracted date components.

        Returns:
            DataFrame with year, month, day, quarter, weekday columns.
        """
        df = self._obj.copy()
        df["__year"] = df[self.jdate].jalali.year
        df["__month"] = df[self.jdate].jalali.month
        df["__day"] = df[self.jdate].jalali.day
        df["__quarter"] = df[self.jdate].jalali.quarter
        df["__weekday"] = df[self.jdate].jalali.weekday
        df["__week"] = df[self.jdate].jalali.week
        df["__dayofyear"] = df[self.jdate].jalali.dayofyear
        return df

    def _clean_groupby(self, group: DataFrameGroupByT) -> DataFrameGroupByT:
        """Clean the groupby object by removing temp columns.

        Args:
            group: The groupby object to clean.

        Returns:
            Cleaned groupby object with only original columns.
        """
        numeric_columns: pd.Index[Any] = cast(
            pd.DataFrame, self._obj.select_dtypes(include="number")
        ).columns
        remaining_columns = [
            col
            for col in numeric_columns
            if col in set(self.columns).difference(self.TEMP_COLUMNS)
        ]
        if not remaining_columns:
            return group
        return cast(DataFrameGroupByT, group[remaining_columns])

    def groupby(self, grouper: str = "md") -> DataFrameGroupByT:
        """Group by Jalali date components.

        Args:
            grouper: Grouping key. Options:
                - 'year': Group by year
                - 'month': Group by month
                - 'day': Group by day
                - 'week': Group by week number
                - 'dayofweek': Group by day of week
                - 'dayofmonth': Group by day of month (alias for 'day')
                - 'quarter': Group by quarter
                - 'dayofyear': Group by day of year
                - 'ym': Group by year and month
                - 'yq': Group by year and quarter
                - 'ymd': Group by year, month, and day
                - 'md': Group by month and day (default)

        Returns:
            DataFrameGroupBy object.

        Raises:
            ValueError: If grouper is not a valid option.
        """
        possible_keys = [
            "year",
            "month",
            "day",
            "week",
            "dayofweek",
            "dayofmonth",
            "quarter",
            "dayofyear",
            "ym",
            "yq",
            "ymd",
            "md",
        ]
        df = self._df
        if grouper not in possible_keys:
            raise ValueError(
                f"{grouper} is not a valid groupby type. Choose from {possible_keys}"
            )

        keys: dict[str, list[str]] = {
            "md": ["month", "day"],
            "ym": ["year", "month"],
            "yq": ["year", "quarter"],
            "ymd": ["year", "month", "day"],
        }
        grouper_cols: list[str]
        if grouper in keys:
            grouper_cols = [f"__{g}" for g in keys[grouper]]
        elif grouper == "dayofmonth":
            grouper_cols = ["__day"]
        else:
            grouper_cols = [f"__{grouper}"]

        group = cast(DataFrameGroupByT, df.groupby(grouper_cols))
        return self._clean_groupby(group)

    def resample(self, resample_type: str) -> pd.DataFrame:
        """Resample by Jalali frequency.

        Groups the DataFrame by Jalali calendar periods and aggregates.

        Args:
            resample_type: The resample frequency. Options:
                - 'month': Group by Jalali month
                - 'quarter': Group by Jalali quarter
                - 'year': Group by Jalali year
                - 'week': Group by Jalali week

        Returns:
            DataFrame with aggregated values grouped by the specified period.

        Raises:
            ValueError: If resample_type is not valid.

        Examples:
            >>> df.jalali.resample('month')
            >>> df.jalali.resample('quarter')
        """
        valid_types = ["month", "quarter", "year", "week"]
        if resample_type not in valid_types:
            raise ValueError(
                f"{resample_type} is not a valid resample type. "
                f"Choose from {valid_types}"
            )

        type_to_groupby: dict[str, str] = {
            "month": "ym",
            "quarter": "yq",
            "year": "year",
            "week": "week",
        }

        groupby_key = type_to_groupby[resample_type]
        return self.groupby(groupby_key).sum(numeric_only=True).reset_index(drop=True)

    def convert_columns(
        self,
        columns: list[str] | str,
        to_jalali: bool = True,
        format: str = "%Y-%m-%d",
    ) -> pd.DataFrame:
        """Convert date columns between Jalali and Gregorian.

        Args:
            columns: Column name(s) to convert.
            to_jalali: If True, convert Gregorian to Jalali.
                If False, convert Jalali to Gregorian. Defaults to True.
            format: Format string for parsing string dates. Defaults to "%Y-%m-%d".

        Returns:
            DataFrame with converted columns.

        Examples:
            >>> df.jalali.convert_columns('date', to_jalali=True)
            >>> df.jalali.convert_columns(['date1', 'date2'], to_jalali=False)
        """
        df = self._obj.copy()

        if isinstance(columns, str):
            columns = [columns]

        for col in columns:
            if col not in df.columns:
                raise ValueError(f"Column '{col}' not found in DataFrame.")

            if to_jalali:
                df[col] = df[col].jalali.to_jalali()
            else:
                if df[col].dtype == object:
                    first_val = (
                        df[col].dropna().iloc[0] if len(df[col].dropna()) > 0 else None
                    )
                    if isinstance(first_val, str):
                        df[col] = df[col].jalali.parse_jalali(format)
                df[col] = df[col].jalali.to_gregorian()

        return df

    def to_period(self, freq: str = "M") -> pd.DataFrame:
        """Convert Jalali dates to period representation.

        Args:
            freq: Frequency for period. Options:
                - 'Y': Year
                - 'Q': Quarter
                - 'M': Month (default)
                - 'W': Week
                - 'D': Day

        Returns:
            DataFrame with period column added.
        """
        df = self._obj.copy()

        def get_period(x: Any) -> str | None:
            if pd.isna(x):
                return None
            if freq == "Y":
                return f"{x.year}"
            elif freq == "Q":
                q = (x.month - 1) // 3 + 1
                return f"{x.year}Q{q}"
            elif freq == "M":
                return f"{x.year}-{x.month:02d}"
            elif freq == "W":
                from jalali_pandas.core.calendar import week_of_year

                w = week_of_year(x.year, x.month, x.day)
                return f"{x.year}W{w:02d}"
            elif freq == "D":
                return f"{x.year}-{x.month:02d}-{x.day:02d}"
            else:
                raise ValueError(f"Unsupported frequency: {freq}")

        df[f"{self.jdate}_period"] = df[self.jdate].apply(get_period)
        return df

    def filter_by_year(self, year: int | list[int]) -> pd.DataFrame:
        """Filter DataFrame by Jalali year(s).

        Args:
            year: Year or list of years to filter by.

        Returns:
            Filtered DataFrame.
        """
        years = [year] if isinstance(year, int) else year
        mask = self._obj[self.jdate].jalali.year.isin(years)
        return cast(pd.DataFrame, self._obj[mask].copy())

    def filter_by_month(self, month: int | list[int]) -> pd.DataFrame:
        """Filter DataFrame by Jalali month(s).

        Args:
            month: Month or list of months to filter by (1-12).

        Returns:
            Filtered DataFrame.
        """
        months = [month] if isinstance(month, int) else month
        mask = self._obj[self.jdate].jalali.month.isin(months)
        return cast(pd.DataFrame, self._obj[mask].copy())

    def filter_by_quarter(self, quarter: int | list[int]) -> pd.DataFrame:
        """Filter DataFrame by Jalali quarter(s).

        Args:
            quarter: Quarter or list of quarters to filter by (1-4).

        Returns:
            Filtered DataFrame.
        """
        quarters = [quarter] if isinstance(quarter, int) else quarter
        mask = self._obj[self.jdate].jalali.quarter.isin(quarters)
        return cast(pd.DataFrame, self._obj[mask].copy())

    def filter_by_date_range(
        self,
        start: str | jdatetime.date | None = None,
        end: str | jdatetime.date | None = None,
    ) -> pd.DataFrame:
        """Filter DataFrame by Jalali date range.

        Args:
            start: Start date (inclusive). Can be string 'YYYY-MM-DD' or jdatetime.
            end: End date (inclusive). Can be string 'YYYY-MM-DD' or jdatetime.

        Returns:
            Filtered DataFrame.
        """
        df = self._obj.copy()
        mask = pd.Series([True] * len(df), index=df.index)

        if start is not None:
            if isinstance(start, str):
                start = jdatetime.datetime.strptime(start, "%Y-%m-%d")
            mask = mask & (df[self.jdate] >= start)

        if end is not None:
            if isinstance(end, str):
                end = jdatetime.datetime.strptime(end, "%Y-%m-%d")
            mask = mask & (df[self.jdate] <= end)

        return cast(pd.DataFrame, df[mask].copy())


__all__ = ["JalaliDataFrameAccessor"]
