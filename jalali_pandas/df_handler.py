"""
handle jalaali dates in pandas dataframes
"""
from typing import List, Union
import pandas as pd
import jdatetime

# pylint: disable=unused-import
# from .serie_handler import JalaliSerieAccessor
LSTR = List[str]


@pd.api.extensions.register_dataframe_accessor("jalali")
class JalaliDataframeAccessor:
    """
    Accessor methods on pandas series to handle jalali dates

    """

    TEMP_COLUMNS = ["__year", "__month", "__quarter", "__weekday", "__day"]

    def __init__(self, pandas_obj: pd.DataFrame):
        """[summary]

        Args:
            pandas_obj (pd.Dataframe): [description]
        """
        self._obj = pandas_obj  # type: pd.DataFrame
        self.columns = self._obj.columns  # type: pd.Index
        self.jdate = "jdate"
        self.__validate()

    def __validate(self):
        """
        check if the pandas object is a dataframe with a jdatetime on it

        Args:
            pandas_obj (pd.DataFrame): [description]
        """
        for col in self.columns:
            if isinstance(self._obj[col].iloc[0], jdatetime.date):
                print(f'Column "{col}" will be the refrence.')
                self.jdate = col
                return
        raise ValueError("No jdatetime column found in the dataframe.")

    @property
    def __df(self) -> pd.DataFrame:
        """Genreate temp data frame for the groupby

        Returns:
            pd.DataFrame: a dataframe with year, month, day, week, dayofweek, dayofmonth
        """
        df = self._obj.copy()
        df["__year"] = df[self.jdate].jalali.year
        df["__month"] = df[self.jdate].jalali.month
        df["__day"] = df[self.jdate].jalali.day
        df["__quarter"] = df[self.jdate].jalali.quarter
        df["__weekday"] = df[self.jdate].jalali.weekday

        return df

    #  a function that get str or list of str

    def __clean_groupby(self, group: pd.Grouper) -> pd.Grouper:
        """
        clean the groupby object

        Args:
            group (pd.Grouper): [description]

        Returns:
            pd.Grouper: [description]
        """
        remaining_columns = list(set(self.columns).difference(self.TEMP_COLUMNS))
        # breakpoint
        return group[remaining_columns]

    def groupby(self, grouper: Union[str, LSTR] = "md") -> pd.Grouper:
        """
        groupby jalali date

        Args:
            kind (str, optional): [description]. Defaults to 'md'.

        Returns:
            pd.Grouper: [description]
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
        df = self.__df
        if grouper not in possible_keys:
            raise ValueError(
                f"{grouper} is not a valid groupby type. Choose from {possible_keys}"
            )

        keys = {
            "md": ["month", "day"],
            "ym": ["year", "month"],
            "yq": ["year", "quarter"],
            "ymd": ["year", "month", "day"],
        }
        if grouper in keys:
            grouper = keys[grouper]
            grouper = [f"__{g}" for g in grouper]
        else:
            grouper = [f"__{grouper}"]

        group = df.groupby(grouper)
        group = self.__clean_groupby(group)
        return group

    def resample(self, resample_type: str) -> pd.DataFrame:
        """[summary]

        Raises:
            NotImplementedError: [description]
        """
        raise NotImplementedError
