"""Handle Jalali dates in pandas DataFrames."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

import jdatetime
import pandas as pd
from pandas.core.groupby.generic import DataFrameGroupBy as DataFrameGroupByRuntime
from typing_extensions import TypeAlias

if TYPE_CHECKING:
    from pandas.core.groupby.generic import DataFrameGroupBy

    DataFrameGroupByT: TypeAlias = DataFrameGroupBy[pd.DataFrame, Any]
else:
    DataFrameGroupByT = DataFrameGroupByRuntime


class JalaliDataframeAccessor:
    """Accessor methods on pandas DataFrames to handle Jalali dates."""

    TEMP_COLUMNS = ["__year", "__month", "__quarter", "__weekday", "__day"]

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
            if isinstance(self._obj[col].iloc[0], jdatetime.date):
                self.jdate = str(col)
                return
        raise ValueError("No jdatetime column found in the dataframe.")

    @property
    def _df(self) -> pd.DataFrame:
        """Generate temp DataFrame for groupby.

        Returns:
            pd.DataFrame: DataFrame with year, month, day, quarter, weekday columns.
        """
        df = self._obj.copy()
        df["__year"] = df[self.jdate].jalali.year
        df["__month"] = df[self.jdate].jalali.month
        df["__day"] = df[self.jdate].jalali.day
        df["__quarter"] = df[self.jdate].jalali.quarter
        df["__weekday"] = df[self.jdate].jalali.weekday
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
            grouper: Grouping key. Options: year, month, day, week, dayofweek,
                dayofmonth, ym, yq, ymd, md. Defaults to 'md'.

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

        Returns:
            DataFrame with aggregated values grouped by the specified period.

        Examples:
            >>> df.jalali.resample('month')
            >>> df.jalali.resample('quarter')
        """
        valid_types = ["month", "quarter", "year"]
        if resample_type not in valid_types:
            raise ValueError(
                f"{resample_type} is not a valid resample type. "
                f"Choose from {valid_types}"
            )

        # Map resample type to groupby key
        type_to_groupby: dict[str, str] = {
            "month": "ym",
            "quarter": "yq",
            "year": "year",
        }

        groupby_key = type_to_groupby[resample_type]
        return self.groupby(groupby_key).sum(numeric_only=True).reset_index(drop=True)
