# Best Practices

## Use catalog_v2 to prefilter your asset/market/etc selection

Most common use cases can be achieved following the pattern shown below.

![Illustration](/docs/docs/assets/images/api_flow.png)

For example, let's follow the flow indicated in light blue.

First, we shall obtain all possible markets with a certain criterion, e.g. type='spot' or base='btc'. 

Then, we shall query the catalog for the data set we desire, e.g. market candles, to deliver more metadata
for the markets we identified in step 1. This step will allow us to remove, using appropriate python code, to remove obsolete markets. 

[Video Demo](https://youtu.be/YSC_pwd1B5k?si=DAEQaSthsE4uumkK&t=71)

```python
cat = client.catalog_market_candles_v2(
    markets=list(trump.market),
).to_dataframe()
cat = cat.loc[
    (cat.frequency == '1m') &
    (cat.max_time > '2025-01-15')
].reset_index(drop=True)

```

The code above, for example, whittles down all possible market candles to only the ones with 1m frequency and 
data available until at least 2025-01-15. This means it eliminates obsolete markets. 

In the final step, we can obtain the actual timeseries data, and we can be certain that all markets exist and are
relevant to our use case.

A similar logic can be applied when downloading asset metrics. Rather than going straight to the `get_asset_metrics` 
endpoint, we recommend using the reference data and catalog endpoints to craft the list of assets and metrics. 
Of course, a user may want to start with the catalog of available metrics and only later join the asset reference 
data -- the API is flexible and stateless. 

## Parallel Execution
There are times when it may be useful to pull in large amounts of data at once. The most effective way to do this 
when calling the CoinMetrics API is to split your request into many different queries. This functionality is now 
built into the API Client directly to allow for faster data export:

```python
import os
from coinmetrics.api_client import CoinMetricsClient


if __name__ == '__main__':
    client = CoinMetricsClient(os.environ['CM_API_KEY'])
    coinbase_eth_markets = [market['market'] for market in client.catalog_market_candles(exchange="coinbase", base="eth")]
    start_time = "2024-03-01"
    end_time = "2024-05-01"
    client.get_market_candles(
      markets=coinbase_eth_markets,
      start_time=start_time,
      end_time=end_time,
      page_size=1000
    ).parallel().export_to_json_files()
```

This feature splits the request into multiple threads and either store them in separate files (in the case of `.parallel().export_to_csv_files()` and `.parallel().export_to_json_files`)
or combine them all into one file or data structure (in the case of `.parallel().to_list()`, `.parallel().to_dataframe()`,
`.parallel().export_to_json()`). It's important to know that in order to send more requests per second to the CoinMetrics
this uses the [parallel tasks features in Python's concurrent.futures](https://docs.python.org/3/library/concurrent.futures.html)
package. This means when using this feature, the API Client will use significantly more resources and may approach
the [Coin Metrics rate limits](https://docs.python.org/3/library/concurrent.futures.html). 

In terms of resource usage and speed, these usages are in order from most performant to least:
* `.export_to_json_files()`
* `.export_to_csv_files()`
* `.to_list()`
* `.export_to_json()`
* `.to_dataframe()`

### Splitting Parameter Queries
There is a feature `time_increment` that can be used to split a single query into many based on time range, and then 
combine them later. Consider this example where we speed up getting a 2 months worth of BTC ReferenceRateUSD data into
many parallel threads to create a dataframe faster: 
```python
import datetime
import os
from coinmetrics.api_client import CoinMetricsClient
from dateutil.relativedelta import relativedelta
client = CoinMetricsClient(os.environ.get("CM_API_KEY"))
start_time = datetime.datetime.now()
assets = ["btc", "eth", "sol"]
if __name__ == '__main__':
    client.get_asset_metrics(
        assets=assets,
        metrics="ReferenceRateUSD",
        frequency="1m",
        start_time="2024-01-01",
        end_time="2025-01-01",
        page_size=1000,
        end_inclusive=False).parallel(
        time_increment=relativedelta(months=1)).export_to_csv("btcRRs.csv")
    print(f"Time taken parallel: {datetime.datetime.now() - start_time}")
    start_time = datetime.datetime.now()
    client.get_asset_metrics(
        assets=assets,
        metrics="ReferenceRateUSD",
        frequency="1m",
        start_time="2022-03-01",
        end_time="2023-03-01",
        page_size=1000,
        end_inclusive=False).export_to_csv("btcRRsNormal.csv")
```
Notice we pass in the `time_increment=relativedelta(months=1)` so that means we will split the threads up by month, in
addition to by asset. So this will run a total 36 separate threads, 12 threads for each month x 3 threads for each asset.
The difference it takes in time is dramatic:
```commandline
Exporting to dataframe type: 100%|██████████| 36/36 [00:00<00:00, 54.62it/s]
Time taken parallel: 0:00:36.654147
Time taken normal: 0:05:20.073826
```

Please note that for short time periods you can pass in a `time_increment` with `datetime.timedelta` to specify up to 
several weeks, for larger time frames you can use `dateutil.relativedelta.relativedelta` in order to split requests
up by increments of months or years.


## General Parallelization Guidelines
* If you are using a small `page_size` and trying to export a large number amount of, this will be your biggest bottleneck.
Generally the fastest `page_size` is `1000` to `10000`
* If you are unsure why an action is taking a long time, running the CoinMetricsClient using `verbose=True` or `debug=True`
can give better insight into what is happening under the hood
* The parallel feature is best used when you are exporting a large amount of data, that can be split by query params into 
many smaller requests. A good example of this is market candles over a long time frame - if you are querying hundreds
of markets and are sure there will be data, using `.parallel().export_to_csv_files("...")` can have a huge performance 
increase, if you are just querying a single market you will not see a difference
* The parallel feature is highly configurable, there is several configuration options that may be suitable for advanced
users like tweaking the `max_workers` parameter, or changing the default `ProcessPoolExecutor` to a `ThreadPoolExectuor`
* Using multithreaded code is inherently more complex, it will be harder to debug issues with long running queries 
when running parallel exports compared to normal single threaded code
* For that reason, this tool is best suited for exporting historical data rather than supporting a real time production
system.
* The methods that create separate files for each thread will be the safest and most performant to use - `.export_to_csv_files()`
and `.export_to_json_files()`. Using the methods that return a single output - `.export_to_csv()`, `export_to_list()`, and
`.export_to_dataframe()` need to join the data from many threads before it can be returned, this may use a lot of memory
if you are accessing data types like market orderbooks or market trades and could fail altogether
* If using `export_to_csv/json_files()` functions, note that by default they will be saved in the directory format `/{endpoint}/{parallelize_on}`.
For example, in `export_to_json_files()`, 
`client.get_market_trades("coinbase-eth-btc-spot,coinbase-eth-usdc-spot").parallel("markets")` will create a file each like ./market-trades/coinbase-eth-btc-spot.json, ./market-trades/coinbase-eth-usdc-spot.json
`client.get_asset_metrics('btc,eth', 'ReferenceRateUSD', start_time='2024-01-01', limit_per_asset=1).parallel("assets,metrics", time_increment=timedelta(days=1))`
will create a file each like ./asset-metrics/btc/ReferenceRateUSD/start_time=2024-01-01T00-00-00Z.json, ./asset-metrics/eth/ReferenceRateUSD/start_time=2024-01-01T00-00-00Z.json
* If you get the error `BrokenProcessPool` it [might be because you're missing a main() function](https://stackoverflow.com/questions/15900366/all-example-concurrent-futures-code-is-failing-with-brokenprocesspool)