[issue-template]: ../../../issues/new?template=BUG_REPORT.md
[feature-template]: ../../../issues/new?template=FEATURE_REQUEST.md

![singnetlogo](../../assets/singnet-logo.jpg?raw=true 'SingularityNET')

# CNTK Time Series LSTM Forecast

This service uses [CNTK Time Series Prediction with LSTM](https://cntk.ai/pythondocs/CNTK_106B_LSTM_Timeseries_with_IOT_Data.html) 
and [Python SAX](https://github.com/seninp/saxpy) to extrapolate a given time series.

It is part of our [Time Series Analysis Services](https://github.com/singnet/time-series-analysis).

### Welcome

The service receives as input a time series from a CSV file or from an online source of financial data.
The given time series is discretized using SAX ([Reference](https://jmotif.github.io/sax-vsm_site/morea/algorithm/SAX.html)) 
which transforms the input series in a sequence of words of fixed length.
With this new data the service trains a LSTM model to extrapolate the discretized series.

### What’s the point?

The idea is simplifying the forecasting problem by discretizing its values and training a model to forecast a class rather than an actual value. 
This approach allows the training of models for generic time series at the cost of loss of precision in the forecast (the parameters of 
SAX discretization can be used to tune precision of forecast, for example, using greater values for the alphabet size may increase precision).

If you are using this service with financial data:

- The service uses a limited set of sources for market data, as detailed below.
- No intraday data is used. Actually, the model is trained only with "close"
prices so its outputs should be interpreted as the trend of the target asset
close price in the target date be greater/lower than the previous close.

### How does it work?

The user must provide the following inputs:

  - `window_len`: the SAX's window length.
  - `word_len`: the SAX's  word length.
  - `alphabet_size`: the SAX's alphabet size.
  - `source_type`: from CSV file ("csv") or financial data ("financial").
  - `source`:
    - If `source_type: "csv"`, a URL to CSV file.
        - The CSV file most have a column with name "input".
        - The data length that service supports is (CSV rows) * `window_len` <= 200k.
    - If `source_type: "financial"`, the source to get market data (ie. yahoo, check this [link](https://github.com/pydata/pandas-datareader/blob/master/pandas_datareader/data.py#L306)).
  - `contract`:
    - If `source_type: "csv"`, empty.
    - If `source_type: "financial"`, label of asset (like "SPY", check this [link](https://finance.yahoo.com/most-active)).
  - `start_date`: 
    - If `source_type: "csv"`, empty.
    - If `source_type: "financial"`, start date of training dataset (format "YYYY-MM-DD").
  - `end_date`:
    - If `source_type: "csv"`, empty.
    - If `source_type: "financial"`, end date of training dataset (format "YYYY-MM-DD").
  - The date delta must be >= `window_len`.

The following tags are available for `source`: "yahoo", "google", "iex", "iex-tops",
"iex-last", "iex-last", "bankofcanada", "stooq", "iex-book", "enigma", "fred",
"famafrench", "oecd", "eurostat", "nasdaq", "quandl", "moex", "morningstar",
'robinhood', "tiingo", "yahoo-actions", "yahoo-dividends", "av-forex",
"av-daily", "av-daily-adjusted", "av-weekly", "av-weekly-adjusted",
"av-monthly", "av-monthly-adjusted".
See [here](https://pandas-datareader.readthedocs.io/en/latest/remote_data.html#remote-data-wb) 
for a reference of which data source each tag is related to.

`contract` is supposed to be a valid symbol in the given `source`.

You can use this service from [SingularityNET DApp](http://beta.singularitynet.io/).

You can also call the service from SingularityNET CLI (`snet`).

Assuming that you have an open channel (`id: 0`) to this service:

```
$ snet client call 0 0.00000001 54.203.198.53:7071 forecast '{"window_len": 20, "word_len": 5, "alphabet_size": 5, "source_type": "financial", "source": "yahoo", "contract": "AMZN", "start_date": "2012-01-01", "end_date": "2018-12-10"}'
...
Read call params from cmdline...

Calling service...

    response:
        last_sax_word: "dbadd"
        forecast_sax_letter: "c"
        position_in_sax_interval: 0.762189507484436
```

The output format is:

```
last_sax_word           : LAST_SAX_WORD
forecast_sax_letter     : FORECAST_LETTER_LETTER
position_in_sax_interval: POSITION_IN_SAX_INTERVAL
```

  - `LAST_SAX_WORD`: the last SAX's word of the series.
  - `FORECAST_LETTER_LETTER`: a SAX's letter that model has forecast.
  - `POSITION_IN_SAX_INTERVAL`: is a number in `[0, 1]`.
    It's a measure of how much the prediction is inside a SAX's letter interval.
    Example:
    - `"c"` and `position_in_sax_interval` tending to `1.00` (e.g. `0.80`) means that the prediction is at the end of the SAX letter's interval.
    - `"c"` and `position_in_sax_interval` tending to `0.00` (e.g. `0.20`) means that the prediction is at the beginning of the SAX letter's interval.

### What to expect from this service?

Input:

  - `window_len`: 14.
  - `word_len`: 7.
  - `alphabet_size`: 5.
  - `source_type`: "csv".
  - `source`: "http://54.203.198.53:7000/TimeSeriesAnalysis/cntk-lstm-forecast/cntk_iot_solar.csv".
  - `contract`: "".
  - `start_date`: "".
  - `end_date`: "".

Response:

```
last_sax_word           : "baabcee"
forecast_sax_letter     : "e"
position_in_sax_interval: 0.964960515499115
```

Input:

  - `window_len`: 36.
  - `word_len`: 18.
  - `alphabet_size`: 5.
  - `source_type`: "financial".
  - `source`: "yahoo".
  - `contract`: "AAPL".
  - `start_date`: "2017-01-01".
  - `end_date`: "2018-12-10".

Response:

```
last_sax_word           : "eeeeeedddcbbaaaaaa"
forecast_sax_letter     : "c"
position_in_sax_interval: 0.2819729149341583
```
