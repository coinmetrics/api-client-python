This section walks through basic usage of the API Client. If this is your first time using the client, we recommend walking through the tutorial in our [<ins>product documentation</ins>](https://docs.coinmetrics.io/tutorials-and-examples/tutorials/walkthrough_community). The full list of methods can be found in the [API Client Spec](../reference/api_client.md).


## Initialization

To initialize the client you should use your API key, and the CoinMetricsClient class like the following.
```python
from coinmetrics.api_client import CoinMetricsClient
import os

# we recommend storing your Coin Metrics API key in an environment variable
api_key = os.environ.get("CM_API_KEY")
client = CoinMetricsClient(api_key)

# or to use community API:
client = CoinMetricsClient()
```

If you are curious to see how the API calls are being made and with what parameters, instantiating the client with the `verbose` argument like 
`CoinMetricsClient(api_key=<YOUR_API_KEY>, verbose=True)` will print the API calls as well as information on performance to console. 

## DataCollection

When calling a method from the `CoinMetricsClient` object, note that it returns some form of a `DataCollection` object. The `DataCollection` object is an abstraction for the requests made to the API, containing attributes such as the endpoint, URL, parameters passed, and so on. Importantly, it does **not** return the contents of the response until it is iterated over (using `next(DataCollection)`) or until a transformation method is called (e.g. `DataCollection.to_list()`, `DataCollection.export_to_csv()`). `DataCollection`s can be thought of as Python generator objects. 

For example, if you want to get a bunch of market data trades for coinbase btc-usd pair you can run something similar to the following:

```python
for trade in client.get_market_trades(
    markets='coinbase-btc-usd-spot', 
    start_time='2020-01-01', 
    end_time='2020-01-03',
    limit_per_market=10
):
    print(trade)
```
This example uses the `DataCollection` as a Python iterator: with each iteration of the Python for loop it will
call the Coin Metrics API and return data. The default `page_size` for calls to the API is 100, so each call will return
100 trades until it reaches the end of the query. To get more trades in each API call, you can add the parameter
`page_size` to the `.get_market_trades()` method call, up to a maximum of 10000. 

A similar query can be made when querying daily metrics.

```python
for metric_data in client.get_asset_metrics(
    assets='btc', 
    metrics=['ReferenceRateUSD', 'BlkHgt', 'AdrActCnt', 'AdrActRecCnt', 'FlowOutBFXUSD'], 
    frequency='1d',
    limit_per_asset=10
):
    print(metric_data)
```

### Example: Exploring Available Data

We can get the list of markets which have the `trades` data type using the `catalog_market_trades_v2` method, which is equivalent to querying `catalog-v2/market-trades`:

```python
print(client.catalog_market_trades_v2(markets='coinbase-btc-usd-spot').to_list())
```

Or by iterating over each page of data:

```python
for data in client.catalog_market_trades_v2(markets='coinbase-btc-usd-spot'):
    print(data)
```

You can also use filters for the catalog endpoints like this:

```python
print(client.catalog_market_trades_v2(exchange='coinbase', base='btc', quote='usd').to_list())
```

All the catalog V2 endpoints are meant to help access the historical data served by other endpoints. For example, you can
get all the BTC market trades for a certain day from Coinbase like this:

```python
btc_coinbase_markets = [market['market'] for market in client.catalog_market_trades_v2(exchange="coinbase", asset="btc").to_list()]
start_time = "2023-01-01T00:00:00"
end_time = "2023-01-01T01:00:00"
coinbase_market_trades = client.get_market_trades(
  markets=btc_coinbase_markets,
  start_time=start_time,
  end_time=end_time,
).export_to_csv("coinbase_trades.csv")
```

## DataFrames

The Coin Metrics API Client allows you to leverage `pandas` DataFrames as a convenient data structure. These can be accessed using the `DataCollection.to_dataframe()` method.

```python
print(client.catalog_market_metrics_v2(exchange="coinbase", base='btc', quote='usd').to_dataframe())
```

Output:
```
|market                |metric                                      |frequency|min_time                 |max_time                 |
|----------------------|--------------------------------------------|---------|-------------------------|-------------------------|
|coinbase-btc-usdc-spot|liquidity_depth_0_1_percent_ask_volume_units|1h       |2021-08-20 13:00:00+00:00|2022-07-13 19:00:00+00:00|
|coinbase-btc-usdc-spot|liquidity_depth_0_1_percent_ask_volume_usd  |1h       |2021-08-20 13:00:00+00:00|2022-07-13 19:00:00+00:00|
|coinbase-btc-usdc-spot|liquidity_depth_0_1_percent_bid_volume_units|1h       |2021-08-20 13:00:00+00:00|2022-07-13 19:00:00+00:00|
|coinbase-btc-usdc-spot|liquidity_depth_0_1_percent_bid_volume_usd  |1h       |2021-08-20 13:00:00+00:00|2022-07-13 19:00:00+00:00|
|coinbase-btc-usdc-spot|liquidity_depth_10_percent_ask_volume_units |1h       |2021-08-20 13:00:00+00:00|2022-07-13 19:00:00+00:00|
|coinbase-btc-usdc-spot|liquidity_depth_10_percent_ask_volume_usd   |1h       |2021-08-20 13:00:00+00:00|2022-07-13 19:00:00+00:00|

```

You can use the pandas Dataframe functionality to do useful transformations, such as filtering out the assets 
without metrics available, then saving that data to a csv file:
```python
import pandas as pd
import os
from coinmetrics.api_client import CoinMetricsClient
from datetime import timedelta
client = CoinMetricsClient(os.environ['CM_API_KEY'])
coinbase_markets = client.catalog_market_trades_v2(exchange="coinbase", base="btc", quote="usd", page_size=1000).to_dataframe()
coinbase_markets['max_time'] = pd.to_datetime(coinbase_markets['max_time'], utc=True)
current_utc_time = pd.Timestamp.now(tz='UTC')
one_day_ago = current_utc_time - timedelta(days=1)
filtered_coinbase_markets = coinbase_markets[coinbase_markets['max_time'] > one_day_ago]
```

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

- This only works with requests that return the type `DataCollection`. 
- API restrictions apply. Some requests may return empty results due to limited access to the API from you API key.

### Type Conversion 
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

Alternatively, you can manually enter your own type conversion by passing in a dictionary for `dtype_mapper`. This can be done in conjunction with pandas' built in type inference.
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

pandas type inference can also be turned off in favor of a user-specified dtype map.

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

## File Exports

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

## Paging
You can make the datapoints to iterate from start (default) or from end.

for that you should use a paging_from argument like the following:
```python
from coinmetrics.api_client import CoinMetricsClient
from coinmetrics.constants import PagingFrom

client = CoinMetricsClient()

for metric_data in client.get_asset_metrics(assets='btc', metrics=['ReferenceRateUSD'],
                                            paging_from=PagingFrom.START):
    print(metric_data)
```

PagingFrom.END: is available but by default it will page from the start.
