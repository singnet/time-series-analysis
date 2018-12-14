[issue-template]: ../../issues/new?template=BUG_REPORT.md
[feature-template]: ../../issues/new?template=FEATURE_REQUEST.md

![singnetlogo](docs/assets/singnet-logo.jpg 'SingularityNET')

[![CircleCI](https://circleci.com/gh/singnet/time-series-analysis.svg?style=svg)](https://circleci.com/gh/singnet/time-series-analysis)

# Time Series Analysis Services

A collection of services for time series analysis.

[HTML User's Guide Hub](https://singnet.github.io/time-series-analysis/)

## Getting Started

For more details on how to publish and test a service, select it from the list below:

### Generic:
- [cntk-lstm-forecast](generic/cntk-lstm-forecast) ([User's Guide](docs/users_guide/generic/cntk-lstm-forecast.md)) - 
This service uses a CNTK LSTM model and [Python SAX](https://github.com/seninp/saxpy) to extrapolate a given time series.
[[Reference](https://cntk.ai/pythondocs/CNTK_106B_LSTM_Timeseries_with_IOT_Data.html)]

### Finance:
- [cntk-next-day-trend](finance/cntk-next-day-trend) ([User's Guide](docs/users_guide/finance/cntk-next-day-trend.md)) - 
This service uses a CNTK MLP to predict whether or not, for an input date, market will be above or below the previous day.
[[Reference](https://cntk.ai/pythondocs/CNTK_104_Finance_Timeseries_Basic_with_Pandas_Numpy.html)]

## Contributing and Reporting Issues

Please read our [guidelines](https://github.com/singnet/wiki/blob/master/guidelines/CONTRIBUTING.md#submitting-an-issue) 
before submitting an issue. If your issue is a bug, please use the bug template pre-populated [here][issue-template]. 
For feature requests and queries you can use [this template][feature-template].

## Authors

* **Artur Gontijo** - *Maintainer* - [SingularityNET](https://www.singularitynet.io)

## Licenses

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Each service is licensed as followed:

- cntk-lstm-forecast - [MIT License](https://github.com/Microsoft/CNTK/blob/master/LICENSE.md)
- cntk-next-day-trend - [MIT License](https://github.com/Microsoft/CNTK/blob/master/LICENSE.md)