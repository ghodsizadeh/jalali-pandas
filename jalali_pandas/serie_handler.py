"""Handle Jalali dates in pandas series."""

from __future__ import annotations

from typing import Any, cast

import jdatetime
import pandas as pd


class JalaliSerieAccessor:
    """Accessor methods on pandas series to handle Jalali dates."""

    def __init__(self, pandas_obj: pd.Series[Any]) -> None:
        """Initialize the accessor.

        Args:
            pandas_obj: A pandas Series containing datetime data.
        """
        self._obj = pandas_obj

    def _validate(self) -> None:
        """Validate pandas series contains jdatetime objects.

        Raises:
            TypeError: If series doesn't contain jdatetime or string dates.
        """
        if not all(isinstance(x, (str, jdatetime.date)) for x in self._obj):
            raise TypeError("pandas series must be jdatetime or string of jdate")

    def to_jalali(self) -> pd.Series[Any]:
        """convert python datetime to jalali datetime.

        Returns:
            pd.Series:  pd.Series of jalali datetime.
        """
        return cast(
            pd.Series,
            self._obj.apply(lambda x: jdatetime.datetime.fromgregorian(date=x)),
        )

    def to_gregorian(self) -> pd.Series[Any]:
        """convert jalali datetime to python default datetime.

        Returns:
            pd.Series: pd.Series of python datetime.
        """

        return cast(pd.Series, self._obj.apply(jdatetime.datetime.togregorian))

    #  pylint: disable=redefined-builtin
    def parse_jalali(self, format: str = "%Y-%m-%d") -> pd.Series[Any]:
        """[summary]

        Args:
            format (str, optional): like gregorian datetime format. Defaults to "%Y-%m-%d".

        Returns:
            pd.Series: pd.Series of jalali datetime.
        """
        return cast(
            pd.Series, self._obj.apply(lambda x: jdatetime.datetime.strptime(x, format))
        )

    @property
    def year(self) -> pd.Series[Any]:
        """get Jalali year

        Returns:
            pd.Series: Jalali year
        """
        self._validate()
        return cast(pd.Series, self._obj.apply(lambda x: x.year))

    @property
    def month(self) -> pd.Series[Any]:
        """get Jalali


        Returns:
            pd.Series: Jalali month
        """
        self._validate()
        return cast(pd.Series, self._obj.apply(lambda x: x.month))

    @property
    def day(self) -> pd.Series[Any]:
        """get Jalali day

        Returns:
            pd.Series: Jalali day
        """
        self._validate()
        return cast(pd.Series, self._obj.apply(lambda x: x.day))

    @property
    def hour(self) -> pd.Series[Any]:
        """get Jalali hour

        Returns:
            pd.Series: Jalali hour
        """
        self._validate()
        return cast(pd.Series, self._obj.apply(lambda x: x.hour))

    @property
    def minute(self) -> pd.Series[Any]:
        """get Jalali minute

        Returns:
            pd.Series: Jalali minute
        """
        self._validate()
        return cast(pd.Series, self._obj.apply(lambda x: x.minute))

    @property
    def second(self) -> pd.Series[Any]:
        """get Jalali second

        Returns:
            pd.Series: Jalali second
        """
        self._validate()
        return cast(pd.Series, self._obj.apply(lambda x: x.second))

    @property
    def weekday(self) -> pd.Series[Any]:
        """get Jalali weekday

        Returns:
            pd.Series: Jalali weekday
        """
        self._validate()
        return cast(pd.Series, self._obj.apply(lambda x: x.weekday()))

    @property
    def weeknumber(self) -> pd.Series[Any]:
        """get Jalali day of year

        Returns:
            pd.Series: Jalali day of year
        """
        self._validate()
        return cast(pd.Series, self._obj.apply(lambda x: x.weeknumber()))

    @property
    def quarter(self) -> pd.Series[Any]:
        """Get Jalali quarter.

        Returns:
            pd.Series: Jalali quarter (1-4).
        """
        self._validate()
        month = self.month
        return cast(pd.Series, month.apply(lambda x: (x - 1) // 3 + 1))
