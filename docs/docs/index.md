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

After that you can use the client object for getting information such as available markets:
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
in this case you would get all the information for btc only. 

You can use this client to connect to our API v4 and get catalog or timeseries data from python environment. It natively supports paging over the data so you can use it to iterate over timeseries entries seamlessly.

The client can be used to query both pro and community data.

The full list of methods can be found in the [API Client Spec](https://coinmetrics.github.io/api-client-python/site/api_client.html).


If you'd like a more wholistic view of what is offered from an API endpoint you can use the `to_dataframe()` function 
associated with our catalog endpoints. The code snippet below shows getting a dataframe of information on all the 
assets that data is provided for:
```python
print(client.catalog_assets().to_dataframe())
```

Output:
```commandline
      asset          full_name          exchanges  ... metrics atlas  experimental
0      100x           100xCoin          [gate.io]  ...     NaN  <NA>          <NA>
1     10set             Tenset   [gate.io, lbank]  ...     NaN  <NA>          <NA>
2       18c           Block 18            [huobi]  ...     NaN  <NA>          <NA>
3      1art          ArtWallet          [gate.io]  ...     NaN  <NA>          <NA>
4      1box               1BOX           [zb.com]  ...     NaN  <NA>          <NA>
```

Now you can use the pandas Dataframe functionality to do useful transformations, such as filtering out the assets 
without metrics available, then saving that data to a csv file:
```python
catalog_assets_df = client.catalog_assets().to_dataframe()
only_assets_with_metrics = catalog_assets_df.dropna(subset=['metrics'])
only_assets_with_metrics.to_csv("cm_assets_with_metrics.csv")
```

You may notice that in that data saved, the "metrics" column for example is a list of json data describing the metrics 
offered and the frequency at which they are available. To help parse this information there is a keyword for all catalog
endpoint data `secondary_level`:
```python
catalog_assets_df = client.catalog_assets().to_dataframe(secondary_level="metrics")
only_assets_with_metrics = catalog_assets_df.dropna(subset=['metric'])
eth_metrics = only_assets_with_metrics[only_assets_with_metrics['asset'] == "eth"]
eth_metrics.to_csv("eth_metrics_granular.csv")
```

The above example queries for eth metrics at the level of metrics and frequency, where it will have one row for each 
metric and frequency related to Ethereum. This allows users to quickly get high level information about exactly what
is offered from the Coin Metrics API and to make custom queries against the API from there. This example only covers 
`catalog_assets()`, but the pattern can be used across all of our catalog endpoints. 


## Examples
The API Client allows you to chain together workflows for importing, transforming, then exporting Coin Metrics data.
Below are examples of common use-cases that can be altered to tailor your specific needs. In addition to the examples 
listed below, there's examples covering all the API methods, found in the [examples directory](https://github.com/coinmetrics/api-client-python/tree/master/examples).

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

For getting timeseries data you want to use methods of the client class that start with `get_`. It's important to note
that the timeseries endpoints return data of a parent class type `DataCollection`. The `DataCollection` class is meant
to support a variety of different data export and data manipulation use cases, so just calling one of the client
methods such as `data = client.get_market_trades(markets="coinbase-btc-usd-spot")` will not actually retrieve the data related
to this API call. You must then call a function on this `DataCollection` such as `data.export_to_csv("coinbase_btc_usd_spot_trades.csv)`
or `data.to_dataframe()` in order to access the data. There is more explicit examples below.If you are curious to see
how the API calls are being made and with what parameters, instantiating the client with the `verbose` argument like 
`CoinMetricsClient(api_key=<YOUR_API_KEY>, verbose=True)` will print the API calls as well as information on performance to console. 

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
This example uses the `DataCollection` as a Python iterator, so with each iteration of the Python for loop it will
call the Coin Metrics API and return data. The default `page_size` for calls to the API is 100, so each call will return
100 trades until it reaches the end of the query. To get more trades in each API call, you can add the parameter
`page_size` to the `.get_market_trades()` method call, up to a maximum of 10000. 

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

This can be turned off by setting `optimize_pandas_types=False`

Alternatively, you can manually enter your own type conversion by passing in a dictionary for `dtype_mapper`. This can be done in conjunction with pandas' built in type optimizations.
```python
mapper = {
  'SplyFF': 'Float64',
  'AdrBalUSD1Cnt': 'Int64',
}
df_mapped = client.get_asset_metrics(
  assets=asset_list, metrics=metrics_list, start_time=start_time, limit_per_asset=3
).to_dataframe(dtype_mapper=mapper, optimize_pandas_types=True)
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

Or as strictly the only types in the dataframe

```python
dtype_mapper = {
    'ReferenceRateUSD': np.float64,
    'time': np.datetime64
}
df = client.get_asset_metrics(
  assets='btc', metrics='ReferenceRateUSD', start_time='2022-06-15', limit_per_asset=1
).to_dataframe(dtype_mapper=dtype_mapper, optimize_pandas_types=False)
df.info()
```
```
RangeIndex: 1 entries, 0 to 0
Data columns (total 3 columns):
 #   Column            Non-Null Count  Dtype         
---  ------            --------------  -----         
 0   asset             1 non-null      object        
 1   time              1 non-null      datetime64[ns]
 2   ReferenceRateUSD  1 non-null      float64       
dtypes: datetime64[ns](1), float64(1), object(1)
memory usage: 152.0+ bytes
```

Note that in order to pass a custom datetime object, setting a dtype_mapper is mandatory.

Pandas type conversion tends to be more performant. But if there are custom operations that must be done using numpy datatypes, this option will let you perform them.

### Exporting to csv and json files:
You can also easily export timeseries data to csv and json files with builtin functions on the `DataCollection` type. 
For example this script will export Coinbase btc and eth trades for a date to csv and json files respectively:
```python
    start_date = datetime.date(year=2022, month=1, day=1)
    end_date = datetime.datetime(year=2022, month=1, day=1)
    market_trades_btc = client.get_market_trades(page_size=1000, markets="coinbase-btc-usd-spot", start_time=start_date, end_time=end_date)
    market_trades_btc.export_to_csv("jan_1_2022_coinbase_btc_trades.csv")
    market_trades_eth = client.get_market_trades(page_size=1000, markets="coinbase-eth-usd-spot", start_time=start_date, end_time=end_date)
    market_trades_eth.export_to_json("jan_1_2022_coinbase_eth.json")
```

### Paging
You can make the datapoints to iterate from start (default) or from end.

for that you should use a paging_from argument like the following:
```
from coinmetrics.api_client import CoinMetricsClient
from coinmetrics.constants import PagingFrom

client = CoinMetricsClient()

for metric_data in client.get_asset_metrics(assets='btc', metrics=['ReferenceRateUSD'],
                                            paging_from=PagingFrom.START):
    print(metric_data)
```

PagingFrom.END: is available but by default it will page from the start.


### Debugging the API Client
There are two additional options for the API Client - `debug_mode` and `verbose`. These two options log network calls 
to the console, and in the case of `debug_mode` it will generate a log file of all the network requests and the time
it takes to call them. These tools can be used to diagnose issues in your code and also to get a better understanding 
of request times so that users can write more performant code. For example, running the below code:
```python
import os

from coinmetrics.api_client import CoinMetricsClient

api_key = os.environ['CM_API_KEY']

if __name__ == '__main__':
    client = CoinMetricsClient(api_key=api_key, debug_mode=True)
    reference_rates_example = client.get_asset_metrics(assets=['btc', 'algo', 'eth'], metrics=['ReferenceRateUSD'])
    for data in reference_rates_example:
        continue
```

The console output will look like:
```commandline
[DEBUG] 2023-01-09 11:01:02,044 - Starting API Client debugging session. logging to stdout and cm_api_client_debug_2023_01_09_11_01_02.txt
[DEBUG] 2023-01-09 11:01:02,044 - Using coinmetrics version 2022.11.14.16
[DEBUG] 2023-01-09 11:01:02,044 - Current state of API Client, excluding API KEY: {'_verify_ssl_certs': True, '_api_base_url': 'https://api.coinmetrics.io/v4', '_ws_api_base_url': 'wss://api.coinmetrics.io/v4', '_http_header': {'Api-Client-Version': '2022.11.14.16'}, '_proxies': {'http': None, 'https': None}, 'debug_mode': True, 'verbose': False}
[DEBUG] 2023-01-09 11:01:02,044 - Attempting to call url: timeseries/asset-metrics with params: {'assets': ['btc', 'algo', 'eth'], 'metrics': ['ReferenceRateUSD'], 'frequency': None, 'page_size': None, 'paging_from': 'start', 'start_time': None, 'end_time': None, 'start_height': None, 'end_height': None, 'start_inclusive': None, 'end_inclusive': None, 'timezone': None, 'sort': None, 'limit_per_asset': None}
[DEBUG] 2023-01-09 11:01:02,387 - Response status code: 200 for url: https://api.coinmetrics.io/v4/timeseries/asset-metrics?api_key=[REDACTED]&assets=btc%2Calgo%2Ceth&metrics=ReferenceRateUSD&paging_from=start took: 0:00:00.342874 response body size (bytes): 9832
[DEBUG] 2023-01-09 11:01:02,388 - Attempting to call url: timeseries/asset-metrics with params: {'assets': ['btc', 'algo', 'eth'], 'metrics': ['ReferenceRateUSD'], 'frequency': None, 'page_size': None, 'paging_from': 'start', 'start_time': None, 'end_time': None, 'start_height': None, 'end_height': None, 'start_inclusive': None, 'end_inclusive': None, 'timezone': None, 'sort': None, 'limit_per_asset': None, 'next_page_token': '0.MjAxOS0wOS0zMFQwMDowMDowMFo'}
[DEBUG] 2023-01-09 11:01:02,559 - Response status code: 200 for url: https://api.coinmetrics.io/v4/timeseries/asset-metrics?api_key=[REDACTED]&assets=btc%2Calgo%2Ceth&metrics=ReferenceRateUSD&paging_from=start&next_page_token=0.MjAxOS0wOS0zMFQwMDowMDowMFo took: 0:00:00.171487 response body size (bytes): 9857
```
Then it can be easier to understand what network calls the API Client is making, and where any issues may exist. If you
wish to dig even deeper, you may consider modifying the `_send_request()` method of the API Client to log additional 
data about the state of your environment, or anything else that would help diagnose issues. You will notice a log file
generated in the format `cm_api_client_debug_2023_01_09_11_01_02.txt`. This log file might be helpful for your own use
or to give more context if you are working with Coin Metrics customer success. 

### SSL Certs verification

Sometimes your organization network have special rules on SSL certs verification and in this case you might face the
following error when running the script:
```text
SSLError: HTTPSConnectionPool(host='api.coinmetrics.io', port=443): Max retries exceeded with url: <some_url_path> (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self signed certificate in certificate chain (_ssl.c:1123)')))
```

In this case, you can pass an option during client initialization to disable ssl verification for requests like this:

```python

client = CoinMetricsClient(verify_ssl_certs=False)
```

We don't recommend setting it to False by default and you should make sure you understand the security risks of disabling SSL certs verification.

Additionally, you may choose to specify the path to the SSL certificates on your machine. This may cause errors where 
Python is unable to locate the certificates on your machine, particularly when using Python virtual environments. 

```python
from coinmetrics.api_client import CoinMetricsClient
SSL_CERT_LOCATION = '/Users/<USER_NAME>/Library/Python/3.8/lib/python/site-packages/certifi/cacert.pem'
client = CoinMetricsClient(verify_ssl_certs=SSL_CERT_LOCATION)
```

A quick way to find the certs on your machine is:  
`python3 -c "import requests; print(requests.certs.where())"`  
And note that this will change based on whether or not you are using a [Python virtual environment or not](https://realpython.com/python-virtual-environments-a-primer/)

### Installing and running coinmetrics package and other python packages behind a secure python network
Related to SSL Certs verification, you may have trouble installing and updating PyPi packages to your local environment.
So you may need to choose the best solution for your company and environment - either using package managers or
installing offline.

#### Installing using package managers
Full instructions for setting up your environment to use conda, pip, yarn, npm, etc. can be [found here](https://medium.com/@iffi33/dealing-with-ssl-authentication-on-a-secure-corporate-network-pip-conda-git-npm-yarn-bower-73e5b93fd4b2).
Additionally, a workaround to disable SSL verification when installing a trusted Python package is this:  
```commandline
pip install --trusted-host pypi.python.org <packagename>
```  
Although it is important to make sure you understand the risks associated with disabling SSL verification and ensure 
compliance with company policies.



#### Installing Python packages locally/ offline
It may be easier to download and install the package locally. Steps:  
1. Download the files for the [Coin Metrics API Client from PyPi](https://pypi.org/project/coinmetrics-api-client/#files)
2. [Install it locally](https://packaging.python.org/en/latest/tutorials/installing-packages/#installing-from-local-archives)

### Requests Proxy
Sometimes your organization has special rules on making requests to third parties and you have to use proxies in order to comply with the rules.

For proxies that don't require auth you can specify them similar to this example:
```python

client = CoinMetricsClient(proxy_url=f'http://<hostname>:<port>')
```

For proxies that require auth, you should be able to specify username and password similar to this example:
```python

client = CoinMetricsClient(proxy_url=f'http://<username>:<password>@<hostname>:<port>')
```

## Extended documentation
For more information about the available methods in the client please reference [API Client Spec](https://coinmetrics.github.io/api-client-python/site/api_client.html)

