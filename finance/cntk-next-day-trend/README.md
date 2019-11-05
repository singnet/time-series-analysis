[issue-template]: ../../../../../issues/new?template=BUG_REPORT.md
[feature-template]: ../../../../../issues/new?template=FEATURE_REQUEST.md

![singnetlogo](../../docs/assets/singnet-logo.jpg?raw=true 'SingularityNET')

# CNTK Finance Time Series Analysis

This service uses [CNTK Finance Timeseries](https://cntk.ai/pythondocs/CNTK_104_Finance_Timeseries_Basic_with_Pandas_Numpy.html) 
to predict whether or not, for an input date, market will be above or below the previous day.

It is part of our [Time Series Analysis Services](https://github.com/singnet/time-series-analysis).

## Getting Started

### Requirements

- [Python 3.6.5](https://www.python.org/downloads/release/python-365/)
- [Node 8+ w/npm](https://nodejs.org/en/download/)

### Development

Clone this repository:

```
$ git clone https://github.com/singnet/time-series-analysis.git
$ cd finance/cntk-next-day-trend
```

### Running the service:

To get the `ORGANIZATION_ID` and `SERVICE_ID` you must have already published a service (check this [link](https://dev.singularitynet.io/tutorials/publish/)).

Create the `SNET Daemon`'s config JSON file (`snetd.config.json`).

```
{
   "DAEMON_END_POINT": "DAEMON_HOST:DAEMON_PORT",
   "IPFS_END_POINT": "http://ipfs.singularitynet.io:80",
   "BLOCKCHAIN_NETWORK_SELECTED": "BLOCKCHAIN_NETWORK",
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
   "DAEMON_END_POINT": "0.0.0.0:7051",
   "IPFS_END_POINT": "http://ipfs.singularitynet.io:80",
   "BLOCKCHAIN_NETWORK_SELECTED": "ropsten",
   "PASSTHROUGH_ENABLED": true,
   "PASSTHROUGH_ENDPOINT": "http://localhost:7003",
   "ORGANIZATION_ID": "snet",
   "SERVICE_ID": "cntk-next-day-trend",
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
$ python3 run_next_day_trend_service.py
```

### Calling the service:

Inputs:
  - `source`: source to get market data (ie. yahoo, check this [link](https://github.com/pydata/pandas-datareader/blob/master/pandas_datareader/data.py#L306)).
  - `contract`: label of asset (like "SPY", check this [link](https://finance.yahoo.com/most-active)).
  - `start`: start date of training dataset (format "YYYY-MM-DD").
  - `end`: end date of training dataset (format "YYYY-MM-DD").
  - `target_date`: date that will be analysed (format "YYYY-MM-DD").
  
Note: The date delta must be >= 100 days.

Local (testing purpose):

```
$ python3 test_next_day_trend_service.py 
Endpoint (localhost:7003): 
Method (trend): 
Source(yahoo): 
Contract(SPY): AMZN
Start Date(2000-01-01): 2017-01-01
End Date(2009-01-01): 2017-11-28
Target Date(2018-11-12): 2018-11-28
{'DOWN': 0.5}
```

Through SingularityNET (follow this [link](https://dev.singularitynet.io/tutorials/publish/) 
to learn how to publish a service and open a payment channel to be able to call it):

Assuming that you have an open channel (`id: 0`) to this service:

```
$ snet client call snet cntk-next-day-trend trend '{"source": "yahoo", "contract": "AAPL", "start": "2018-01-01", "end": "2018-10-31", "target_date": "2018-11-28"}'
...
response: "{'DOWN': 0.51}"
```

## Contributing and Reporting Issues

Please read our [guidelines](https://dev.singularitynet.io/docs/contribute/contribution-guidelines/#submitting-an-issue) before submitting an issue. 
If your issue is a bug, please use the bug template pre-populated [here][issue-template]. 
For feature requests and queries you can use [this template][feature-template].

## Authors

* **Artur Gontijo** - *Maintainer* - [SingularityNET](https://www.singularitynet.io)