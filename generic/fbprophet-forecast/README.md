[issue-template]: ../../../../../issues/new?template=BUG_REPORT.md
[feature-template]: ../../../../../issues/new?template=FEATURE_REQUEST.md

![singnetlogo](../../docs/assets/singnet-logo.jpg?raw=true 'SingularityNET')

# Facebook Prophet Forecast

This service uses [Prophet](https://github.com/facebook/prophet) 
and [Statsmodel](https://github.com/statsmodels/statsmodels) to extrapolate a given time series.

It is part of our [Time Series Analysis Services](https://github.com/singnet/time-series-analysis).

## Getting Started

### Requirements

- [Python 3.6.5](https://www.python.org/downloads/release/python-365/)
- [Node 8+ w/npm](https://nodejs.org/en/download/)

### Development

Clone this repository:

```
$ git clone https://github.com/singnet/time-series-analysis.git
$ cd generic/fbprophet-forecast
```

### Running the service:

To get the `ORGANIZATION_ID` and `SERVICE_ID` you must have already published a service (check this [link](https://dev.singularitynet.io/tutorials/publish/)).

Create the `SNET Daemon`'s config JSON file (`snetd.config.json`).

```
{
   "DAEMON_END_POINT": "DAEMON_HOST:DAEMON_PORT",
   "IPFS_END_POINT": "http://ipfs.singularitynet.io:80",
   "BLOCKCHAIN_NETWORK_SELECTED": "BLOCKCHAIN_NETWORK",
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
   "DAEMON_END_POINT": "0.0.0.0:7042",
   "IPFS_END_POINT": "http://ipfs.singularitynet.io:80",
   "BLOCKCHAIN_NETWORK_SELECTED": "ropsten",
   "PASSTHROUGH_ENDPOINT": "http://localhost:7003",
   "ORGANIZATION_ID": "snet",
   "SERVICE_ID": "fbprophet-forecast",
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
$ python3 run_service.py
```

### Calling the service:

Inputs:
  - `url`: A CSV file URL (with `ds` and `y` headers).
  - `ds`: the date series if no `url` (`max: 3000`).
  - `y`: the data series if no `url`(`max: 3000`).
  - `period`: the Season-Trend period (`optional`).
  - `points`: Number of points to forecast (`max: 500`).

Note: The length of `ds` and `y` must be the same and greater then 100.

Local (testing purpose):

```
$ python3 test_service.py
Endpoint (localhost:7003): 
Method (forecast): 
CSV (URL): http://bh.singularitynet.io:7000/Resources/example_wp_log_peyton_manning.csv
Period (10): 
Points (100): 365

response:
len(response.observed): 2905
len(response.seasonal): 2905
len(response.forecast): 365
```

for further instructions about the output of this service, check the [User's Guide](../../docs/users_guide/generic/fbprophet-forecast.md).

Through SingularityNET (follow this [link](https://dev.singularitynet.io/tutorials/publish/) 
to learn how to publish a service and open a payment channel to be able to call it):

Assuming that you have an open channel (`id: 0`) to this service:

```
$ snet client call fbprophet-forecast forecast '{"url": "http://bh.singularitynet.io:7000/Resources/example_wp_log_peyton_manning.csv"}'

observed: [ ... ]
trend: [ ... ]
seasonal: [ ... ]
forecast: [ ... ]
forecast_ds: [ ... ]
forecast_lower: [ ... ]
forecast_upper: [ ... ]
```

## Contributing and Reporting Issues

Please read our [guidelines](https://dev.singularitynet.io/docs/contribute/contribution-guidelines/#submitting-an-issue) before submitting an issue. 
If your issue is a bug, please use the bug template pre-populated [here][issue-template]. 
For feature requests and queries you can use [this template][feature-template].

## Authors

* **Artur Gontijo** - *Maintainer* - [SingularityNET](https://www.singularitynet.io)