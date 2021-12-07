[![HitCount](http://hits.dwyl.com/ghodsizadeh/jalali-pandas.svg)](http://hits.dwyl.com/ghodsizadeh/jalali-pandas)
![PyPI - Downloads](https://img.shields.io/pypi/dw/tehran_stocks.svg?color=blue)
[![PyPI version](https://badge.fury.io/py/jalali-pandas.svg)](https://badge.fury.io/py/jalali-pandas)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)
[![codecov](https://codecov.io/gh/ghodsizadeh/jalali-pandas/branch/main/graph/badge.svg?token=LWQ85TN0NU)](https://codecov.io/gh/ghodsizadeh/jalali-pandas)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ghodsizadeh/jalali-pandas/blob/main/examples/basic_usage.ipynb)
![GitHub Repo stars](https://img.shields.io/github/stars/ghodsizadeh/jalali-pandas?logoColor=blue&style=social)

# Jalali Pandas Extentsion

> A pandas extension that solves all problems of Jalai/Iraninan/Shamsi dates

![Jalali Pandas python package](/assets/github-jalali-pandas.png)

## Features

#### Series Extenstion

- Convert _string_ to _Jalali_ date `1388/03/25` --> `jdatetime(1388,3,25,0,0)`
- Convert _gregorian_ date to _Jalali_ date `datetime(2019,11,17,0,0)` --> `jdatetime(1398,8,26,0,0)`
- Convert _Jalali_ date to _gregorian_ date `jdatetime(1398,10,18,0,0)` --> `datetim(2020,1,8,6,19)`

#### DataFrame extenstion

- Support grouping by _Jalali_ date
- Group by year, month, days, ...
- Shortcuts for groups: `ymd` for `['year','month','day']` and more
- Resampling: Convenience method for frequency conversion and resampling of time series but in _Jalali_ dateformat. (comming soon)

## Installation

    pip install -U jalali-pandas

## Usage

Just import jalali-pandas and use pandas just use `.jalali` as a method for series and dataframes. Nothin outside pandas.

> `jalali-pandas` is an extentsion for pandas, that add a mehtod for series/columns and dataframes.

### Series

```python
import pandas as pd
import jalali_pandas

# create dataframe
df = pd.DataFrame({"date": pd.date_range("2019-01-01", periods=10, freq="D")})

# convert to jalali
df["jdate"] = df["date"].jalali.to_jalali()

# convert to gregorian
df["gdate"] = df["jdate"].jalali.to_gregorian()

# parse string to jalali
df1 = pd.DataFrame({"date": ["1399/08/02", "1399/08/03", "1399/08/04"]})
df1["jdate"] = df1["date"].jalali.parse_jalali("%Y/%m/%d")


# get access to jalali year,quarter ,month, day and weekday
df['year'] = df["jdate"].jalali.year
df['month'] = df["jdate"].jalali.month
df['quarter'] = df["jdate"].jalali.quarter
df['day'] = df["jdate"].jalali.day
df['weekday'] = df["jdate"].jalali.weekday

```

### DataFrame

```python

import pandas as pd
import jalali_pandas

df = pd.DataFrame(
    {
    "date": pd.date_range("2019-01-01", periods=10, freq="M"),
    "value": range(10),
    }
)
# make sure to create a column with jalali datetime format. (you can use any name)
df["jdate"] = df["date"].jalali.to_jalali()


# group by jalali year
gp = df.jalali.groupby("year")
gp.sum()

#group by month
mean = df.jalali.groupby('mean')

#groupby year and month and day
mean = df.jalali.groupby('ymd')
# or
mean = df.jalali.groupby(['year','month','day'])


#groupby year and quarter
mean = df.jalali.groupby('yq')
# or
mean = df.jalali.groupby(['year','quarter'])
```

## ToDos:

- [x] add gregorian to Jalali Conversion
- [x] add Jalali to gregorian Conversion
- [ ] add support for sampling
- [x] add date parser from other columns
- [x] add date parser from string
