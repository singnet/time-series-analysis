[issue-template]: ../../../issues/new?template=BUG_REPORT.md
[feature-template]: ../../../issues/new?template=FEATURE_REQUEST.md

![singnetlogo](../../assets/singnet-logo.jpg?raw=true 'SingularityNET')

# CNTK Finance Next Day Trend

This service uses [CNTK Finance Timeseries](https://github.com/Microsoft/CNTK/blob/master/Tutorials/CNTK_104_Finance_Timeseries_Basic_with_Pandas_Numpy.ipynb) 
to perform a time series analysis to indicate a trend in an asset market.

It is part of our [Time Series Analysis Services](https://github.com/singnet/time-series-analysis).

### Welcome

The service receives as input the symbol of an asset contract (and the source to
get its market data), a date interval to train the model and a target date to
analyze. After training a model in the given period, the service outputs a
market trend ("UP" or "DOWN") for the target date.

### What’s the point?

A MultiLayer Perceptron (MLP) is trained on the closing data of the given time
series in a given period of time. The assumption here is that such period is
somehow similar (regarding the overall behavior of the target asset) to the
time period just before the target date.

If this premise is correct, the trained model can make a sensible estimate for
the asset UP/DOWN trending in the target date.

The service uses a limited set of sources for market data, as detailed below.
No intraday data is used. Actually, the model is trained only with "close"
prices so its outputs should be interpreted as the trend of the target asset
close price in the target date be greater/lower than the previous close.

### How does it work?

The user must provide the following inputs:

  - `source`: source to get market data (ie. "yahoo", "google", etc.)
  - `contract`: asset's market symbol (e.g. "SPY", "AMZN", etc).
  - `start`: start date of training dataset (format "YYYY-MM-DD").
  - `end`: end date of training dataset (format "YYYY-MM-DD"). **Important:** the training period must be greater than 100 days.
  - `target_date`: date that will be analised (format "YYYY-MM-DD").

The following tags are available for `source`: "yahoo", "google", "iex", "iex-tops",
"iex-last", "iex-last", "bankofcanada", "stooq", "iex-book", "enigma", "fred",
"famafrench", "oecd", "eurostat", "nasdaq", "quandl", "moex", "morningstar",
'robinhood', "tiingo", "yahoo-actions", "yahoo-dividends", "av-forex",
"av-daily", "av-daily-adjusted", "av-weekly", "av-weekly-adjusted",
"av-monthly", "av-monthly-adjusted".
See [here](https://pandas-datareader.readthedocs.io/en/latest/remote_data.html#remote-data-wb) 
for a reference of which data source each tag is related to.

`contract` is supposed to be a valid symbol in the given `source`.

You can use this service from [SingularityNET DApp](http://alpha.singularitynet.io/).

You can also call the service from SingularityNET CLI (`snet`).

Assuming that you have an open channel (`id: 0`) to this service:

```
$ snet client call 0 0.00000001 54.203.198.53:7070 trend '{"source": "yahoo", "contract": "SPY", "start": "2017-01-01", "end": "2017-10-31", "target_date": "2018-11-28"}'
...
response: "{'DOWN': 0.51}"
```

The output format is `{signal: confidence}`, where:

  - `signal`: is either `UP` or `DOWN`
  - `confidence`: is a number in `[0.5, 1]`. It's a measure of how reliable is
    the signaled trend. **Important:** `confidence` is not a model's estimate of
    how much the target asset's price will raise or fall. `confidence` values 
    near 0.5 indicates that the model could not detect neither UP or DOWN trends.

### What to expect from this service?

Input:

  - `source`: yahoo
  - `contract`: VALE
  - `start`: 2010-01-01
  - `end`: 2018-08-16
  - `target_date`: 2018-09-17

Response:

```
response: "{'DOWN': 0.5}"
```

Input:

  - `source`: yahoo
  - `contract`: VALE
  - `start`: 2010-01-01
  - `end`: 2018-08-16
  - `target_date`: 2018-10-02

Response:

```
response: "{'UP': 0.51}"
```
