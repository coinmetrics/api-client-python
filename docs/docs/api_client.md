<a name="coinmetrics.api_client"></a>
# coinmetrics.api\_client

<a name="coinmetrics.api_client.CoinMetricsClient"></a>
## CoinMetricsClient Objects

```python
class CoinMetricsClient()
```

<a name="coinmetrics.api_client.CoinMetricsClient.catalog_assets"></a>
#### catalog\_assets

```python
 | catalog_assets(assets: Optional[Union[List[str], str]] = None) -> List[Dict[str, Any]]
```

Returns meta information about assets.

**Arguments**:

- `assets` (`list(str), str`): A single asset or a list of assets to return info for. If no assets provided, all available assets are returned.

**Returns**:

`list(dict(str, any))`: Information that is available for requested assets, like: Full name, metrics and available frequencies, markets, exchanges, etc.

<a name="coinmetrics.api_client.CoinMetricsClient.catalog_exchanges"></a>
#### catalog\_exchanges

```python
 | catalog_exchanges(exchanges: Optional[Union[List[str], str]] = None) -> List[Dict[str, Any]]
```

Returns meta information about exchanges.

**Arguments**:

- `exchanges` (`list(str), str`): A single exchange name or a list of exchanges to return info for. If no exchanges provided, all available exchanges are returned.

**Returns**:

`list(dict(str, any))`: Information that is available for requested exchanges, like: markets, min and max time available.

<a name="coinmetrics.api_client.CoinMetricsClient.catalog_indexes"></a>
#### catalog\_indexes

```python
 | catalog_indexes(indexes: Optional[Union[List[str], str]] = None) -> List[Dict[str, Any]]
```

Returns meta information about indexes.

**Arguments**:

- `indexes` (`list(str), str`): A single index name or a list of indexes to return info for. If no indexes provided, all available indexes are returned.

**Returns**:

`list(dict(str, any))`: Information that is available for requested indexes, like: Full name, and available frequencies.

<a name="coinmetrics.api_client.CoinMetricsClient.catalog_markets"></a>
#### catalog\_markets

```python
 | catalog_markets(exchange: Optional[str] = None, base: Optional[str] = None, quote: Optional[str] = None, asset: Optional[str] = None, symbol: Optional[str] = None) -> List[Dict[str, Any]]
```

Returns list of markets that correspond to a filter. If no filter is set, returns all available assets.

**Arguments**:

- `exchange` (`str`): name of the exchange
- `base` (`str`): name of base asset
- `quote` (`str`): name of quote asset
- `asset` (`str`): name of either base or quote asset
- `symbol` (`str`): name of a symbol. Usually used for futures contracts.

**Returns**:

`list(dict(str, any))`: Information about markets that correspond to a filter along with meta information like: type of market and min and max available time frames.

<a name="coinmetrics.api_client.CoinMetricsClient.catalog_metrics"></a>
#### catalog\_metrics

```python
 | catalog_metrics(metrics: Optional[Union[List[str], str]] = None, reviewable: Optional[bool] = None) -> List[Dict[str, Any]]
```

Returns list of available metrics along with information for them like
description, category, precision and assets for which a metric is available.

**Arguments**:

- `metrics` (`list(str), str`): A single metric name or a list of metrics to return info for. If no metrics provided, all available metrics are returned.
- `reviewable` (`bool`): Show only reviewable or non-reviewable by human metrics. By default all metrics are shown.

**Returns**:

`list(dict(str, any))`: Information about metrics that correspond to a filter along with meta information like: description, category, precision and assets for which a metric is available.

<a name="coinmetrics.api_client.CoinMetricsClient.get_index_levels"></a>
#### get\_index\_levels

```python
 | get_index_levels(indexes: Union[List[str], str], frequency: Optional[str] = None, page_size: Optional[int] = None, paging_from: Optional[Union[PagingFrom, str]] = None, start_time: Optional[Union[datetime, date, str]] = None, end_time: Optional[Union[datetime, date, str]] = None, start_inclusive: Optional[bool] = None, end_inclusive: Optional[bool] = None, timezone: Optional[str] = None) -> DataCollection
```

Returns index levels for specified indexes and date range.

**Arguments**:

- `indexes` (`list(str), str`): list of index names, e.g. 'CMBI10'
- `frequency` (`str`): frequency of the returned timeseries, e.g 15s, 1d, etc.
- `page_size` (`int`): number of items returned per page when calling the API. If the request times out, try using a smaller number.
- `paging_from` (`PagingFrom, str`): Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
- `start_time` (`datetime, date, str`): Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `end_time` (`datetime, date, str`): End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `start_inclusive` (`bool`): Flag to define if start timestamp must be included in the timeseries if present. True by default.
- `end_inclusive` (`bool`): Flag to define if end timestamp must be included in the timeseries if present. True by default.
- `timezone` (`str`): timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.

**Returns**:

`DataCollection`: Index Levels timeseries.

<a name="coinmetrics.api_client.CoinMetricsClient.get_market_candles"></a>
#### get\_market\_candles

```python
 | get_market_candles(markets: Union[List[str], str], frequency: Optional[str] = None, page_size: Optional[int] = None, paging_from: Optional[Union[PagingFrom, str]] = None, start_time: Optional[Union[datetime, date, str]] = None, end_time: Optional[Union[datetime, date, str]] = None, start_inclusive: Optional[bool] = None, end_inclusive: Optional[bool] = None, timezone: Optional[str] = None) -> DataCollection
```

Returns market candles for specified markets, frequency and date range.

**Arguments**:

- `markets` (`list(str), str`): list of market names, e.g. 'coinbase-btc-usd-spot'
- `frequency` (`str`): frequency of the returned timeseries, e.g 15s, 1d, etc.
- `page_size` (`int`): number of items returned per page when calling the API. If the request times out, try using a smaller number.
- `paging_from` (`PagingFrom, str`): Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
- `start_time` (`datetime, date, str`): Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `end_time` (`datetime, date, str`): End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `start_inclusive` (`bool`): Flag to define if start timestamp must be included in the timeseries if present. True by default.
- `end_inclusive` (`bool`): Flag to define if end timestamp must be included in the timeseries if present. True by default.
- `timezone` (`str`): timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.

**Returns**:

`DataCollection`: Market Candles timeseries.

<a name="coinmetrics.api_client.CoinMetricsClient.get_market_trades"></a>
#### get\_market\_trades

```python
 | get_market_trades(markets: Union[List[str], str], page_size: Optional[int] = None, paging_from: Optional[Union[PagingFrom, str]] = None, start_time: Optional[Union[datetime, date, str]] = None, end_time: Optional[Union[datetime, date, str]] = None, start_inclusive: Optional[bool] = None, end_inclusive: Optional[bool] = None, timezone: Optional[str] = None) -> DataCollection
```

Returns market trades for specified markets and date range.

**Arguments**:

- `markets` (`list(str), str`): list of market names, e.g. 'coinbase-btc-usd-spot'
- `page_size` (`int`): number of items returned per page when calling the API. If the request times out, try using a smaller number.
- `paging_from` (`PagingFrom, str`): Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
- `start_time` (`datetime, date, str`): Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `end_time` (`datetime, date, str`): End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `start_inclusive` (`bool`): Flag to define if start timestamp must be included in the timeseries if present. True by default.
- `end_inclusive` (`bool`): Flag to define if end timestamp must be included in the timeseries if present. True by default.
- `timezone` (`str`): timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.

**Returns**:

`DataCollection`: Market Trades timeseries.

<a name="coinmetrics.api_client.CoinMetricsClient.get_market_quotes"></a>
#### get\_market\_quotes

```python
 | get_market_quotes(markets: Union[List[str], str], page_size: Optional[int] = None, paging_from: Optional[Union[PagingFrom, str]] = None, start_time: Optional[Union[datetime, date, str]] = None, end_time: Optional[Union[datetime, date, str]] = None, start_inclusive: Optional[bool] = None, end_inclusive: Optional[bool] = None, timezone: Optional[str] = None) -> DataCollection
```

Returns market quotes for specified markets and date range.

**Arguments**:

- `markets` (`list(str), str`): list of market names, e.g. 'coinbase-btc-usd-spot'
- `page_size` (`int`): number of items returned per page when calling the API. If the request times out, try using a smaller number.
- `paging_from` (`PagingFrom, str`): Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
- `start_time` (`datetime, date, str`): Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `end_time` (`datetime, date, str`): End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `start_inclusive` (`bool`): Flag to define if start timestamp must be included in the timeseries if present. True by default.
- `end_inclusive` (`bool`): Flag to define if end timestamp must be included in the timeseries if present. True by default.
- `timezone` (`str`): timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.

**Returns**:

`DataCollection`: Market Quotes timeseries.

<a name="coinmetrics.api_client.CoinMetricsClient.get_market_orderbooks"></a>
#### get\_market\_orderbooks

```python
 | get_market_orderbooks(markets: Union[List[str], str], page_size: Optional[int] = None, paging_from: Optional[Union[PagingFrom, str]] = None, start_time: Optional[Union[datetime, date, str]] = None, end_time: Optional[Union[datetime, date, str]] = None, start_inclusive: Optional[bool] = None, end_inclusive: Optional[bool] = None, timezone: Optional[str] = None) -> DataCollection
```

Returns market order books for specified markets and date range.

**Arguments**:

- `markets` (`list(str), str`): list of market names, e.g. 'coinbase-btc-usd-spot'
- `page_size` (`int`): number of items returned per page when calling the API. If the request times out, try using a smaller number.
- `paging_from` (`PagingFrom, str`): Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
- `start_time` (`datetime, date, str`): Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `end_time` (`datetime, date, str`): End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `start_inclusive` (`bool`): Flag to define if start timestamp must be included in the timeseries if present. True by default.
- `end_inclusive` (`bool`): Flag to define if end timestamp must be included in the timeseries if present. True by default.
- `timezone` (`str`): timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.

**Returns**:

`DataCollection`: Market Order Books timeseries.

<a name="coinmetrics.api_client.CoinMetricsClient.get_asset_metrics"></a>
#### get\_asset\_metrics

```python
 | get_asset_metrics(assets: Union[List[str], str], metrics: Union[List[str], str], frequency: Optional[str] = None, page_size: Optional[int] = None, paging_from: Optional[Union[PagingFrom, str]] = None, start_time: Optional[Union[datetime, date, str]] = None, end_time: Optional[Union[datetime, date, str]] = None, start_height: Optional[int] = None, end_height: Optional[int] = None, start_inclusive: Optional[bool] = None, end_inclusive: Optional[bool] = None, timezone: Optional[str] = None) -> DataCollection
```

Returns asset metrics books for specified assets, metrics, date range and frequency.

**Arguments**:

- `assets` (`list(str), str`): list of asset names, e.g. 'btc'
- `metrics` (`list(str), str`): list of metric names, e.g. 'PriceUSD'
- `frequency` (`str`): frequency of the returned timeseries, e.g 15s, 1d, etc.
- `page_size` (`int`): number of items returned per page when calling the API. If the request times out, try using a smaller number.
- `paging_from` (`PagingFrom, str`): Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
- `start_time` (`datetime, date, str`): Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `end_time` (`datetime, date, str`): End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `start_height` (`int`): Start block of the timeseries (only applicable when querying with frequency 1b).
- `end_height` (`int`): End block of the timeseries (only applicable when querying with frequency 1b).
- `start_inclusive` (`bool`): Flag to define if start timestamp must be included in the timeseries if present. True by default.
- `end_inclusive` (`bool`): Flag to define if end timestamp must be included in the timeseries if present. True by default.
- `timezone` (`str`): timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.

**Returns**:

`DataCollection`: Asset Metrics timeseries.

<a name="coinmetrics.api_client.CoinMetricsClient.get_mining_pool_tips_summary"></a>
#### get\_mining\_pool\_tips\_summary

```python
 | get_mining_pool_tips_summary(assets: Union[List[str], str], page_size: Optional[int] = None, paging_from: Optional[Union[PagingFrom, str]] = None, start_time: Optional[Union[datetime, date, str]] = None, end_time: Optional[Union[datetime, date, str]] = None, start_inclusive: Optional[bool] = None, end_inclusive: Optional[bool] = None, timezone: Optional[str] = None) -> DataCollection
```

Returns asset metrics books for specified assets, metrics, date range and frequency.

**Arguments**:

- `assets` (`list(str), str`): list of asset names, e.g. 'btc'
- `page_size` (`int`): number of items returned per page when calling the API. If the request times out, try using a smaller number.
- `paging_from` (`PagingFrom, str`): Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
- `start_time` (`datetime, date, str`): Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `end_time` (`datetime, date, str`): End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `start_height` (`int`): Start block of the timeseries (only applicable when querying with frequency 1b).
- `end_height` (`int`): End block of the timeseries (only applicable when querying with frequency 1b).
- `start_inclusive` (`bool`): Flag to define if start timestamp must be included in the timeseries if present. True by default.
- `end_inclusive` (`bool`): Flag to define if end timestamp must be included in the timeseries if present. True by default.
- `timezone` (`str`): timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.

**Returns**:

`DataCollection`: Asset Metrics timeseries.

