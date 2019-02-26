[issue-template]: ../../../../../issues/new?template=BUG_REPORT.md
[feature-template]: ../../../../../issues/new?template=FEATURE_REQUEST.md

![singnetlogo](../../docs/assets/singnet-logo.jpg?raw=true 'SingularityNET')

# CNTK Time Series Forecast

This service uses [CNTK Time Series Prediction with LSTM](https://cntk.ai/pythondocs/CNTK_106B_LSTM_Timeseries_with_IOT_Data.html) 
and [Python SAX](https://github.com/seninp/saxpy) to extrapolate a given time series.

It is part of our [Time Series Analysis Services](https://github.com/singnet/time-series-analysis).

## Getting Started

### Requirements

- [Python 3.6.5](https://www.python.org/downloads/release/python-365/)
- [Node 8+ w/npm](https://nodejs.org/en/download/)

### Development

Clone this repository:

```
$ git clone https://github.com/singnet/time-series-analysis.git
$ cd generic/cntk-lstm-forecast
```

### Running the service:

To get the `ORGANIZATION_ID` and `SERVICE_ID` you must have already published a service (check this [link](https://dev.singularitynet.io/tutorials/publish/)).

Create the `SNET Daemon`'s config JSON file (`snetd.config.json`).

```
{
   "DAEMON_END_POINT": "DAEMON_HOST:DAEMON_PORT",
   "ETHEREUM_JSON_RPC_ENDPOINT": "JSON_RPC_ENDPOINT",
   "IPFS_END_POINT": "http://ipfs.singularitynet.io:80",
   "REGISTRY_ADDRESS_KEY": "REGISTRY_ADDRESS",
   "PASSTHROUGH_ENABLED": true,
   "PASSTHROUGH_ENDPOINT": "http://SERVICE_GRPC_HOST:SERVICE_GRPC_PORT",  
   "ORGANIZATION_ID": "ORGANIZATION_ID",
   "SERVICE_ID": "SERVICE_ID",
   "LOG": {
       "LEVEL": "debug",
       "OUTPUT": {
            "TYPE": "stdout"
           }
   }
}
```

For example (using the Ropsten testnet):

```
$ cat snetd.config.json
{
   "DAEMON_END_POINT": "0.0.0.0:7059",
   "ETHEREUM_JSON_RPC_ENDPOINT": "https://ropsten.infura.io",
   "IPFS_END_POINT": "http://ipfs.singularitynet.io:80",
   "REGISTRY_ADDRESS_KEY": "0x5156fde2ca71da4398f8c76763c41bc9633875e4",
   "PASSTHROUGH_ENABLED": true,
   "PASSTHROUGH_ENDPOINT": "http://localhost:7003",
   "ORGANIZATION_ID": "snet",
   "SERVICE_ID": "cntk-lstm-forecast",
   "LOG": {
       "LEVEL": "debug",
       "OUTPUT": {
           "TYPE": "stdout"
           }
   }
}
```

Note that we set `DAEMON_HOST = 0.0.0.0` because this service will run inside a Docker container.

Install all dependencies:
```
$ pip3 install -r requirements.txt
```
Generate the gRPC codes:
```
$ sh buildproto.sh
```
Start the service and `SNET Daemon`:
```
$ python3 run_time_series_forecast_service.py
```

### Calling the service:

Inputs:
  - `window_len`: the SAX window length.
  - `word_len`: the SAX word length.
  - `alphabet_size`: the SAX alphabet size.
  - `source_type`: from CSV file ("csv") or financial data ("financial").
    - For "csv":
        - The CSV file must have a column with name "input".
        - The data length that service supports is (CSV rows) * `window_len` <= 200k`.
  - `source`:
    - If `source_type: "csv"`, a URL to CSV file.
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

Note: The date delta must be >= `window_len`.

Local (testing purpose):

```
$ python3 test_time_series_forecast_service.py
Endpoint (localhost:7003): 
Method (forecast): 
Window length (24): 
Word length (8): 
Alphabet length (5): 
Source Type (financial): 
Source (yahoo): 
Contract (SPY): 
Start date (2012-01-01): 
End date (2018-12-10):

response:
last_sax_word           : "deccabeb"
forecast_sax_letter     : "c"
position_in_sax_interval: 0.14
```

  - `last_sax_word`: The last SAX's word of the series.
  - `forecast_sax_letter`: a SAX's letter that model has forecast.
  - `position_in_sax_interval`: is a number in `[0, 1]`.
    It's a measure of how much the prediction is inside a SAX's letter interval.
    - `"c"` and `position_in_sax_interval` tending to `0.00` (`0.14`) means that the prediction is at the beginning of SAX letter's interval.

for further instructions about the output of this service, check the [User's Guide](../../docs/users_guide/generic/cntk-lstm-forecast.md).

Through SingularityNET (follow this [link](https://dev.singularitynet.io/tutorials/publish/) 
to learn how to publish a service and open a payment channel to be able to call it):

Assuming that you have an open channel (`id: 0`) to this service:

```
$ snet client call cntk-lstm-forecast forecast '{"window_len": 36, "word_len": 18, "alphabet_size": 5, "source_type": "financial", "source": "yahoo", "contract": "AAPL", "start_date": "2017-01-01", "end_date": "2018-12-10"}'
unspent_amount_in_cogs before call (None means that we cannot get it now):1
last_sax_word: "eeeeeedddcbbaaaaaa"
forecast_sax_letter: "c"
position_in_sax_interval: 0.2819729149341583
```

## Contributing and Reporting Issues

Please read our [guidelines](https://dev.singularitynet.io/docs/contribute/contribution-guidelines/#submitting-an-issue) before submitting an issue. 
If your issue is a bug, please use the bug template pre-populated [here][issue-template]. 
For feature requests and queries you can use [this template][feature-template].

## Authors

* **Artur Gontijo** - *Maintainer* - [SingularityNET](https://www.singularitynet.io)