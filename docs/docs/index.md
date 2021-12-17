# Coin Metrics Python API v4 client library

This is an official Python API client for Coin Metrics API v4.

## Installation and Updates
To install the client you can run the following command:
```
pip install coinmetrics-api-client
```

Note that the client is updated regularly to reflect the changes made in [API v4](https://docs.coinmetrics.io/api/v4). Ensure that your latest version matches with what's in [pyPI](https://pypi.org/project/coinmetrics-api-client/) 

To update your version, run the following command:
```
pip install coinmetrics-api-client -U
```

## Introduction
You can use this client for querying all kinds of data with your API.

To initialize the client you should use your API key, and the CoinMetricsClient class like the following.
```
from coinmetrics.api_client import CoinMetricsClient

client = CoinMetricsClient("<cm_api_key>")

# or to use community API:
client = CoinMetricsClient()
```

After that you can use the client object for getting stuff like available markets:
```
print(client.catalog_markets())
```

or to query all available assets along with what is available for those assets, like metrics, markets:

```
print(client.catalog_assets())
```


you can also use filters for the catalog endpoints like this:

```
print(client.catalog_assets(assets=['btc']))
```
in this case you would get all the information for btc only

You can use this client to connect to our API v4 and get catalog or timeseries data from python environment. It natively supports paging over the data so you can use it to iterate over timeseries entries seamlessly.

The client can be used to query both pro and community data.

The full list of methods can be found in the [API Client Spec](https://coinmetrics.github.io/api-client-python/site/api_client.html).

## Examples
The API Client allows you to chain together workflows for importing, transforming, then exporting Coin Metrics data. Below are examples of common use-cases that can be altered to tailor your specific needs.

**[Example Notebooks](https://github.com/coinmetrics/api-client-python/tree/master/examples/notebooks)**

* `walkthrough_community.ipynb`: Walks through the basic functionality available using the community client.

**[Asset Metrics](https://github.com/coinmetrics/api-client-python/tree/master/examples/asset_metrics)**

* `bbb_metrics_csv_exporter_using_plain_requests.py`: Queries block-by-block metrics using the `requests` library and exports the output into a CSV file.
* `bbb_metrics_json_exporter.py`: Queries block-by-block metrics and exports the output into a JSON file.
* `eod_metrics_csv_exporter.py`: Exports a set of user-defined metrics and assets published at end-of-day and exports the output into a CSV file.
* `reference_rates_json_exporter.py`: Queries Coin Metrics Reference Rates at a user-defined frequency for a set of assets, then exports the output into a JSON file.

**[Market Data](https://github.com/coinmetrics/api-client-python/tree/master/examples/market_data)** 

* `books_json_exporter.py`: Queries market orderbook data then exports the output into a JSON file.
* `candles_json_exporter.py`: Queries market candles data then exports the output into a JSON file.
* `funding_rates_json_exporter.py`: Queries market funding rates data then exports the output into a JSON file.
* `trades_csv_exporter.py`: Queries market trades data then exports the output into a CSV file.
* `trades_json_exporter.py`: Queries market trades data then exports the output into a JSON file.

## Getting timeseries data

For getting timeseries data you want to use methods of the client class that start with `get_`.

For example if you want to get a bunch of market data trades for coinbase btc-usd pair you can run something similar to the following:

```
for trade in client.get_market_trades(
    markets='coinbase-btc-usd-spot', 
    start_time='2020-01-01', 
    end_time='2020-01-03',
    limit_per_market=10
):
    print(trade)
```

Or if you want to see daily btc asset metrics you can use something like this:

```
for metric_data in client.get_asset_metrics(assets='btc', 
                                            metrics=['ReferenceRateUSD', 'BlkHgt', 'AdrActCnt',  
                                                     'AdrActRecCnt', 'FlowOutBFXUSD'], 
                                            frequency='1d',
                                            limit_per_asset=10):
    print(metric_data)
```
This will print you the requested metrics for all the days where we have any of the metrics present.


### DataFrames
_(New in >=`2021.9.30.14.30`)_

Timeseries data can be transformed into a pandas dataframe by using the `to_dataframe()` method. The code snippet below shows how:
```
import pandas as pd
from coinmetrics.api_client import CoinMetricsClient
from os import environ

client = CoinMetricsClient()
trades = client.get_market_trades(
    markets='coinbase-btc-usd-spot', 
    start_time='2021-09-19T00:00:00Z', 
    limit_per_market=10
)
trades_df = trades.to_dataframe()
print(trades_df.head())

```
If you want to use dataframes, then you will need to install pandas

**Notes**

- This only works with requests that return the type `DataCollection`. Thus, `catalog` requests, which return lists cannot be returned as dataframes.
  Please see the [API Client Spec](https://coinmetrics.github.io/api-client-python/site/api_client.html) for a full list
  of requests and their return types.
- API restrictions apply. Some requests may return empty results due to limited access to the API from you API key.

#### Type Conversion 
_(New in >=`2021.12.17.18.00`)_

As of version `2021.12.17.18.00` or later, outputs from the  `to_dataframe` function automatically convert the dtypes for a dataframe to the optimal pandas types.
```python
metrics_list = ['volume_trusted_spot_usd_1d', 'SplyFF', 'AdrBalUSD1Cnt']
asset_list = ['btc','xmr']
start_time='2021-12-01'
df_metrics = client.get_asset_metrics(
  assets=asset_list, metrics=metrics_list, start_time=start_time, limit_per_asset=3
).to_dataframe()
print(df_metrics.dtypes)
```
```
asset                          string
time                           datetime64[ns, tzutc()]
AdrBalUSD1Cnt                   Int64
SplyFF                        Float64
volume_trusted_spot_usd_1d    Float64
dtype: object
```

Alternatively, you can manually enter your own type conversion by passing in a dictionary for `dtype_mapper`.
```python
mapper = {
  'SplyFF': 'Float64',
  'AdrBalUSD1Cnt': 'Int64',
}
df_mapped = client.get_asset_metrics(
  assets=asset_list, metrics=metrics_list, start_time=start_time, limit_per_asset=3
).to_dataframe(dtype_mapper=mapper)
print(df_mapped.dtypes)
```

```
asset                                          object
time                          datetime64[ns, tzutc()]
AdrBalUSD1Cnt                                   Int64
SplyFF                                        Float64
volume_trusted_spot_usd_1d                    float64
dtype: object
```

However, pandas will throw an error if you manually map a datetime type using the above method, e.g. `{'time': 'datetime64'}`.

```python
TypeError: the dtype datetime64 is not supported for parsing, pass this column using parse_dates instead
```

We generally recommend sticking to automatically converted dtypes especially for datetimes.

### Paging
You can make the datapoints to iterate from start or from end (default).

for that you should use a paging_from argument like the following:
```
from coinmetrics.api_client import CoinMetricsClient
from coinmetrics.constants import PagingFrom

client = CoinMetricsClient()

for metric_data in client.get_asset_metrics(assets='btc', metrics=['ReferenceRateUSD'],
                                            paging_from=PagingFrom.START):
    print(metric_data)
```

PagingFrom.END: is available but it is also a default value also, so you might not want to set it.

### SSL Certs verification

Sometimes your organization network have special rules on SSL certs verification and in this case you might face the following error when running the script:
```text
SSLError: HTTPSConnectionPool(host='api.coinmetrics.io', port=443): Max retries exceeded with url: <some_url_path> (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self signed certificate in certificate chain (_ssl.c:1123)')))
```

In this case, you can pass an option during client initialization to disable ssl verification for requests like this:

```python

client = CoinMetricsClient(verify_ssl_certs=False)
```

We don't recommend setting it to False by default and you should make sure you understand the security risks of disabling SSL certs verification.

## Extended documentation
For more information about the available methods in the client please reference [API Client Spec](https://coinmetrics.github.io/api-client-python/site/api_client.html)
