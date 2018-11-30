[issue-template]: ../../../issues/new?template=BUG_REPORT.md
[feature-template]: ../../../issues/new?template=FEATURE_REQUEST.md

![singnetlogo](../../assets/singnet-logo.jpg?raw=true 'SingularityNET')

# CNTK Finance Next Day Trend

This service uses [CNTK Finance Timeseries](https://github.com/Microsoft/CNTK/blob/master/Tutorials/CNTK_104_Finance_Timeseries_Basic_with_Pandas_Numpy.ipynb) 
to perform a time series analysis to indicate a trend in an asset market.

It is part of our [Time Series Analysis Services](https://github.com/singnet/time-series-analysis).

### Welcome

The service receives as input the name of an asset contract (from financial market), a date interval to train the model and a 
target date to analyze. After the training it uses the model to output a market trend ("UP" or "DOWN")
 and its confidence for the next date.

### What’s the point?

The service receives a time series (market data) that is used to train a MultiLayer Perceptron (MLP) to analyze a trend.

The service outputs a market trend and its confidence.

### How does it work?

The user must provide the following inputs in order to start the service and get a response:

Inputs:
  - `source`: Source to get market data (ie. yahoo, check this [link](https://github.com/pydata/pandas-datareader/blob/master/pandas_datareader/data.py#L306)).
  - `contract`: Label of asset (like "SPY").
  - `start`: Start date of training dataset.
  - `end`: End date of training dataset.
  - `target_date`: Date that will be analysed.
  - The date delta must be >= 100 days.

You can use this service from [SingularityNET DApp](http://alpha.singularitynet.io/), clicking on `SNET/ImageRecon`.

You can also call the service from SingularityNET CLI (`snet`).

Assuming that you have an open channel (`id: 0`) to this service:

```
$ snet client call 0 0.00000001 54.203.198.53:7009 trend '{"source": "yahoo", "contract": "SPY", "start": "2017-01-01", "end": "2017-10-31", "target_date": "2018-11-28"}'
...
Read call params from cmdline...

Calling service...

    response:
        {'DOWN': 0.54}
```

### What to expect from this service?

Input:

  - `source`: yahoo
  - `contract`: VALE
  - `start`: 2010-01-01
  - `end`: 2018-08-16
  - `target_date`: 2018-09-17

Response:

```
{'UP': 0.53}
```

![chart_vale_1](../../assets/users_guide/chart_1.png 'Chart_VALE')

Input :

  - `source`: yahoo
  - `contract`: VALE
  - `start`: 2010-01-01
  - `end`: 2018-08-16
  - `target_date`: 2018-10-02

Response:

```
{'UP': 0.55}
```

![chart_vale_2](../../assets/users_guide/chart_2.png 'Chart_VALE_2')