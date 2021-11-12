"""
handle jalaali dates in pandas dataframes
"""
import pandas as pd
import jdatetime

# pylint: disable=unused-import
from .serie_handler import JalaliSerieAccessor


@pd.api.extensions.register_dataframe_accessor("jalali")
class JalaliDataframeAccessor:
    """
    Accessor methods on pandas series to handle jalali dates

    """

    def __init__(self, pandas_obj: pd.DataFrame):
        """[summary]

        Args:
            pandas_obj (pd.Dataframe): [description]
        """
        self._obj = pandas_obj  # type: pd.DataFrame
        self.columns = self._obj.columns  # type: pd.Index
        self.jdate = "jdate"
        self._validate()
        self.prepare()

    def _validate(self):
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

    def prepare(self) -> pd.DataFrame:
        """Genreate temp data frame for the groupby

        Returns:
            pd.DataFrame: a dataframe with year, month, day, week, dayofweek, dayofmonth
        """

        df["year"] = df[self.jdate].jalali.year
        df["month"] = df[self.jdate].jalali.month
        df["day"] = df[self.jdate].jalali.year

    def groupby(self, kind="md") -> pd.Grouper:
        """
        groupby jalali date

        Args:
            kind (str, optional): [description]. Defaults to 'md'.

        Returns:
            pd.Grouper: [description]
        """
        group = self._obj

        if kind == "md":
            group = self._obj.groupby(self._obj[self.jdate].jalali.month)
        elif kind == "wd":
            group = self._obj.groupby(self._obj[self.jdate].jalali.dayofweek)
        elif kind == "wd":
            group = self._obj.groupby(self._obj[self.jdate].jalali.dayofweek)
        else:
            raise ValueError("kind must be one of 'md','wd','d'")

        return group

    def resample(self):
        """[summary]

        Raises:
            NotImplementedError: [description]
        """
        raise NotImplementedError


if __name__ == "__main__":
    df = pd.DataFrame(
        {
            "date": pd.date_range("2019-01-01", periods=10, freq="D"),
            "temperature": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        }
    )

    df["hdate"] = df.date.jalali.to_jalali()
    res = df.jalali.groupby("md")
    print(res)
    print(df.head(1))
