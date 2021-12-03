"""
handle jalaali dates in pandas series
"""
import jdatetime
import pandas as pd


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

    def __validate(self):
        """validate pandas series is datetime or not.

        Raises:
            TypeError: [description]
        """

        if not all(isinstance(x, (str, jdatetime.date)) for x in self._obj):
            raise TypeError("pandas series must be jdatetime or string of jdate")

    def to_jalali(self) -> pd.Series:
        """convert python datetime to jalali datetime.

        Returns:
            pd.Series:  pd.Series of jalali datetime.
        """
        return self._obj.apply(lambda x: jdatetime.datetime.fromgregorian(date=x))

    def to_gregorian(self) -> pd.Series:
        """convert jalali datetime to python default datetime.

        Returns:
            pd.Series: pd.Series of python datetime.
        """

        return self._obj.apply(jdatetime.datetime.togregorian)

    #  pylint: disable=redefined-builtin
    def parse_jalali(self, format: str = "%Y-%m-%d") -> pd.Series:
        """[summary]

        Args:
            format (str, optional): like gregorian datetime format. Defaults to "%Y-%m-%d".

        Returns:
            pd.Series: pd.Series of jalali datetime.
        """
        return self._obj.apply(lambda x: jdatetime.datetime.strptime(x, format))

    @property
    def year(self) -> pd.Series:
        """get Jalali year

        Returns:
            pd.Series: Jalali year
        """
        self.__validate()
        return self._obj.apply(lambda x: x.year)

    @property
    def month(self) -> pd.Series:
        """get Jalali


        Returns:
            pd.Series: Jalali month
        """
        self.__validate()
        return self._obj.apply(lambda x: x.month)

    @property
    def day(self) -> pd.Series:
        """get Jalali day

        Returns:
            pd.Series: Jalali day
        """
        self.__validate()
        return self._obj.apply(lambda x: x.day)

    @property
    def hour(self) -> pd.Series:
        """get Jalali hour

        Returns:
            pd.Series: Jalali hour
        """
        self.__validate()
        return self._obj.apply(lambda x: x.hour)

    @property
    def minute(self) -> pd.Series:
        """get Jalali minute

        Returns:
            pd.Series: Jalali minute
        """
        self.__validate()
        return self._obj.apply(lambda x: x.minute)

    @property
    def second(self) -> pd.Series:
        """get Jalali second

        Returns:
            pd.Series: Jalali second
        """
        self.__validate()
        return self._obj.apply(lambda x: x.second)

    @property
    def weekday(self) -> pd.Series:
        """get Jalali weekday

        Returns:
            pd.Series: Jalali weekday
        """
        self.__validate()
        return self._obj.apply(lambda x: x.weekday())

    @property
    def weeknumber(self) -> pd.Series:
        """get Jalali day of year

        Returns:
            pd.Series: Jalali day of year
        """
        self.__validate()
        return self._obj.apply(lambda x: x.weeknumber())

    @property
    def quarter(self):
        """get Jalali quarter

        Returns:
            pd.Series: Jalali quarter
        """
        self.__validate()
        month = self.month
        return month.apply(lambda x: (x - 1) // 3 + 1)
