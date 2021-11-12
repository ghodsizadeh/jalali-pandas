"""
handle jalaali dates in pandas series
"""
import pandas as pd
import jdatetime


@pd.api.extensions.register_series_accessor("jalali")
class JalaliSerieAccessor:
    """
    Accessor methods on pandas series to handle jalali dates

    """

    def __init__(self, pandas_obj: pd.Series):
        """[summary]

        Args:
            pandas_obj (pd.Series): [description]
        """
        # self._validate(pandas_obj)
        self._obj = pandas_obj

    def to_jalali(self) -> pd.Series:
        """convert python datetime to jalali datetime.

        Returns:
            pd.Series:  pd.Series of jalali datetime.
        """
        return self._obj.apply(lambda x: jdatetime.datetime.fromgregorian(date=x))

    def to_georgian(self) -> pd.Series:
        """convert jalali datetime to python default datetime.

        Returns:
            pd.Series: pd.Series of python datetime.
        """

        return self._obj.apply(jdatetime.datetime.togregorian)

    #  pylint: disable=redefined-builtin
    def parse_jalali(self, format: str = "%Y-%m-%d") -> pd.Series:
        """[summary]

        Args:
            format (str, optional): like georgian datetime format. Defaults to "%Y-%m-%d".

        Returns:
            pd.Series: pd.Series of jalali datetime.
        """
        return self._obj.apply(lambda x: jdatetime.datetime.strptime(x, format))


if __name__ == "__main__":
    df = pd.DataFrame({"date": pd.date_range("2019-01-01", "2019-01-31")})
    df["jdate"] = df.date.jalali.to_jalali()
    print(all(df["date"] == df.jdate.jalali.to_georgian()))
    print(jdatetime.datetime.strptime("1396-01-01", "%Y-%m-%d"))
