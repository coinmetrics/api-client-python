# Coin Metrics Python API v4 client library

This is an official Python API client for Coin Metrics API v4.

## Installation
To install the client you can run the following command:
```
pip install coinmetrics-api-client
```


## Introduction
You can use this client for querying all kinds of data with your API.

To initialize the client you should use your API key, and the CoinMetricsClient class like the following.
```
from coinmetrics.api_client import CoinMetricsClient

client = CoinMetricsClient(environ.get("CM_API_KEY"))

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

## Getting timeseries data

For getting timeseries data you want to use methods of the client class that start with `get_`.

For example if you want to get a bunch of market data trades for coinbase btc-usd pair you can run something similar to the following:

```
for trade in client.get_market_trades(markets='coinbase-btc-usd-spot', 
                                      start_time='2020-01-01', end_time='2020-01-03'):
    print(trade)
```

Or if you want to see daily btc asset metrics you can use something like this:

```
for metric_data in client.get_asset_metrics(assets='btc', 
                                            metrics=['ReferenceRateUSD', 'BlkHgt', 'AdrActCnt',  
                                                     'AdrActRecCnt', 'FlowOutBFXUSD'], 
                                            frequency='1d'):
    print(metric_data)
```
This will print you the requested metrics for all the days where we have any of the metrics present. 

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

## Extended documentation
For more information about the available methods in the client please reference [API Client Spec](https://coinmetrics.github.io/api-client-python/site/api_client.html)
