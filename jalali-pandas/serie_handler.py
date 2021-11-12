import pandas as pd
import jdatetime



@pd.api.extensions.register_dataframe_accessor("jalali")
@pd.api.extensions.register_series_accessor("jalali")
class JalaliSerieAccessor:
    def __init__(self, pandas_obj: pd.Series):
        # self._validate(pandas_obj)
        self._obj = pandas_obj

    def to_jalali(self):
        return self._obj.apply(lambda x: jdatetime.datetime.fromgregorian(date=x))
    
    def to_georgian(self):
        return self._obj.apply(lambda x: jdatetime.datetime.togregorian(x))

    def parse_jalali(self, format='%Y-%m-%d'):
        strptime= lambda date: jdatetime.datetime.strptime(date,)
        return self._obj.apply(lambda x: strptime(x, format))
    
    def groupby(self, day=False, month=False, year=False):
        print(type(self._obj))



if __name__ == "__main__":
    df = pd.DataFrame({"date": pd.date_range("2019-01-01", "2019-01-31")})
    df['jdate'] = df.date.jalali.to_jalali()
    print(all(df['date']==df.jdate.jalali.to_georgian()))
    print(jdatetime.datetime.strptime('1396-01-01','%Y-%m-%d'))
    print(df.jalali.groupby())
    print(df.date.jalali.groupby())




