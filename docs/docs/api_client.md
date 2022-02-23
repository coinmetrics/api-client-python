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
 | catalog_assets(assets: Optional[Union[List[str], str]] = None) -> CatalogAssetsData
```

Returns meta information about _available_ assets.

**Arguments**:

- `assets` (`list(str), str`): A single asset or a list of assets to return info for. If no assets provided, all available assets are returned.

**Returns**:

`list(dict(str, any))`: Information that is available for requested assets, like: Full name, metrics and available frequencies, markets, exchanges, etc.

<a name="coinmetrics.api_client.CoinMetricsClient.catalog_asset_alerts"></a>
#### catalog\_asset\_alerts

```python
 | catalog_asset_alerts(assets: Optional[Union[List[str], str]] = None, alerts: Optional[Union[List[str], str]] = None) -> CatalogAssetAlertsData
```

Returns meta information about _available_ assets.

**Arguments**:

- `assets` (`list(str), str`): A single asset or a list of assets to return info for. If no assets provided, all available assets are returned.
- `alerts` (`list(str), str`): A single alert or alert name to return info for. If no alerts provided, all available alerts are returned.

**Returns**:

`list(dict(str, any))`: Information that is available for requested assets alerts.

<a name="coinmetrics.api_client.CoinMetricsClient.catalog_asset_pairs"></a>
#### catalog\_asset\_pairs

```python
 | catalog_asset_pairs(asset_pairs: Optional[Union[List[str], str]] = None) -> CatalogAssetPairsData
```

Returns meta information about _available_ asset-asset pairs

**Arguments**:

- `asset_pairs` (`list(str), str`): A single asset-asset pair (e.g. "btc-eth") or a list of asset-asset pairs to return info for. If none are provided, all available pairs are returned.
- `as_dataframe` (`bool`): Boolean flag for returning dataframe. By default, a List(Dict) is returned.

**Returns**:

`list(dict(str, any))`: Information that is available for requested asset-asset pair like metrics and their respective frequencies and time ranges

<a name="coinmetrics.api_client.CoinMetricsClient.catalog_exchanges"></a>
#### catalog\_exchanges

```python
 | catalog_exchanges(exchanges: Optional[Union[List[str], str]] = None) -> CatalogExchangesData
```

Returns meta information about exchanges.

**Arguments**:

- `exchanges` (`list(str), str`): A single exchange name or a list of exchanges to return info for. If no exchanges provided, all available exchanges are returned.

**Returns**:

`list(dict(str, any))`: Information that is available for requested exchanges, like: markets, min and max time available.

<a name="coinmetrics.api_client.CoinMetricsClient.catalog_exchange_assets"></a>
#### catalog\_exchange\_assets

```python
 | catalog_exchange_assets(exchange_assets: Optional[Union[List[str], str]] = None) -> CatalogExchangeAssetsData
```

Returns meta information about _available_ exchange-asset pairs

**Arguments**:

- `exchange_assets` (`list(str), str`): A single exchange-asset pair (e.g. "binance-btc") or a list of exchange-asset pairs to return info for. If none are provided, all available pairs are returned.

**Returns**:

`list(dict(str, any))`: Information that is available for requested exchange-asset pair like metrics and their respective frequencies and time ranges

<a name="coinmetrics.api_client.CoinMetricsClient.catalog_indexes"></a>
#### catalog\_indexes

```python
 | catalog_indexes(indexes: Optional[Union[List[str], str]] = None) -> CatalogIndexesData
```

Returns meta information about _available_ indexes.

**Arguments**:

- `indexes` (`list(str), str`): A single index name or a list of indexes to return info for. If no indexes provided, all available indexes are returned.

**Returns**:

`list(dict(str, any))`: Information that is available for requested indexes, like: Full name, and available frequencies.

<a name="coinmetrics.api_client.CoinMetricsClient.catalog_institutions"></a>
#### catalog\_institutions

```python
 | catalog_institutions(institutions: Optional[Union[List[str], str]] = None) -> CatalogInstitutionsData
```

Returns meta information about _available_ institutions

**Arguments**:

- `institutions` (`list(str), str`): A single institution (e.g. "grayscale") or a list of institutions to return info for. If none are provided, all available pairs are returned.

**Returns**:

`list(dict(str, any))`: Information that is available for requested institution like metrics and their respective frequencies and time ranges.

<a name="coinmetrics.api_client.CoinMetricsClient.catalog_markets"></a>
#### catalog\_markets

```python
 | catalog_markets(markets: Optional[Union[List[str], str]] = None, market_type: Optional[str] = None, exchange: Optional[str] = None, base: Optional[str] = None, quote: Optional[str] = None, asset: Optional[str] = None, symbol: Optional[str] = None) -> CatalogMarketsData
```

Returns list of _available_ markets that correspond to a filter. If no filter is set, returns all available assets.

**Arguments**:

- `markets` (`list(str), str`): list of market names, e.g. 'coinbase-btc-usd-spot'
- `market_type` (`str`): Type of market: "spot", "future", "option"
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
 | catalog_metrics(metrics: Optional[Union[List[str], str]] = None, reviewable: Optional[bool] = None) -> CatalogMetricsData
```

Returns list of _available_ metrics along with information for them like
description, category, precision and assets for which a metric is available.

**Arguments**:

- `metrics` (`list(str), str`): A single metric name or a list of metrics to return info for. If no metrics provided, all available metrics are returned.
- `reviewable` (`bool`): Show only reviewable or non-reviewable by human metrics. By default all metrics are shown.
- `as_dataframe` (`bool`): Boolean flag for returning dataframe. By default, a List(Dict) is returned.

**Returns**:

`list(dict(str, any))`: Information about metrics that correspond to a filter along with meta information like: description, category, precision and assets for which a metric is available.

<a name="coinmetrics.api_client.CoinMetricsClient.catalog_full_assets"></a>
#### catalog\_full\_assets

```python
 | catalog_full_assets(assets: Optional[Union[List[str], str]] = None) -> CatalogAssetsData
```

Returns meta information about _supported_ assets.

**Arguments**:

- `assets` (`list(str), str`): A single asset or a list of assets to return info for. If no assets provided, all supported assets are returned.

**Returns**:

`list(dict(str, any))`: Information that is supported for requested assets, like: Full name, metrics and supported frequencies, markets, exchanges, etc.

<a name="coinmetrics.api_client.CoinMetricsClient.catalog_full_asset_alerts"></a>
#### catalog\_full\_asset\_alerts

```python
 | catalog_full_asset_alerts(assets: Optional[Union[List[str], str]] = None, alerts: Optional[Union[List[str], str]] = None) -> CatalogAssetAlertsData
```

Returns meta information about _supported_ assets.

**Arguments**:

- `assets` (`list(str), str`): A single asset or a list of assets to return info for. If no assets provided, all available assets are returned.
- `alerts` (`list(str), str`): A single alert or alert name to return info for. If no alerts provided, all available alerts are returned.

**Returns**:

`list(dict(str, any))`: Information that is available for requested assets alerts.

<a name="coinmetrics.api_client.CoinMetricsClient.catalog_full_asset_pairs"></a>
#### catalog\_full\_asset\_pairs

```python
 | catalog_full_asset_pairs(asset_pairs: Optional[Union[List[str], str]] = None) -> CatalogAssetPairsData
```

Returns meta information about _supported_ asset-asset pairs

**Arguments**:

- `asset_pairs` (`list(str), str`): A single asset-asset pair (e.g. "btc-eth") or a list of asset-asset pairs to return info for. If none are provided, all supported pairs are returned.

**Returns**:

`list(dict(str, any))`: Information that is supported for requested asset-asset pair like metrics and their respective frequencies and time ranges

<a name="coinmetrics.api_client.CoinMetricsClient.catalog_full_exchanges"></a>
#### catalog\_full\_exchanges

```python
 | catalog_full_exchanges(exchanges: Optional[Union[List[str], str]] = None) -> CatalogExchangesData
```

Returns meta information about exchanges.

**Arguments**:

- `exchanges` (`list(str), str`): A single exchange name or a list of exchanges to return info for. If no exchanges provided, all supported exchanges are returned.

**Returns**:

`list(dict(str, any))`: Information that is supported for requested exchanges, like: markets, min and max time supported.

<a name="coinmetrics.api_client.CoinMetricsClient.catalog_full_exchange_assets"></a>
#### catalog\_full\_exchange\_assets

```python
 | catalog_full_exchange_assets(exchange_assets: Optional[Union[List[str], str]] = None) -> CatalogExchangeAssetsData
```

Returns meta information about _supported_ exchange-asset pairs

**Arguments**:

- `exchange_assets` (`list(str), str`): A single exchange-asset pair (e.g. "binance-btc") or a list of exchange-asset pairs to return info for. If none are provided, all supported pairs are returned.

**Returns**:

`list(dict(str, any))`: Information that is supported for requested exchange-asset pair like metrics and their respective frequencies and time ranges

<a name="coinmetrics.api_client.CoinMetricsClient.catalog_full_indexes"></a>
#### catalog\_full\_indexes

```python
 | catalog_full_indexes(indexes: Optional[Union[List[str], str]] = None) -> CatalogIndexesData
```

Returns meta information about _supported_ indexes.

**Arguments**:

- `indexes` (`list(str), str`): A single index name or a list of indexes to return info for. If no indexes provided, all supported indexes are returned.

**Returns**:

`list(dict(str, any))`: Information that is supported for requested indexes, like: Full name, and supported frequencies.

<a name="coinmetrics.api_client.CoinMetricsClient.catalog_full_institutions"></a>
#### catalog\_full\_institutions

```python
 | catalog_full_institutions(institutions: Optional[Union[List[str], str]] = None) -> CatalogInstitutionsData
```

Returns meta information about _supported_ institutions

**Arguments**:

- `institutions` (`list(str), str`): A single institution (e.g. "grayscale") or a list of institutions to return info for. If none are provided, all supported pairs are returned.

**Returns**:

`list(dict(str, any))`: Information that is supported for requested institution like metrics and their respective frequencies and time ranges.

<a name="coinmetrics.api_client.CoinMetricsClient.catalog_full_markets"></a>
#### catalog\_full\_markets

```python
 | catalog_full_markets(markets: Optional[Union[List[str], str]] = None, market_type: Optional[str] = None, exchange: Optional[str] = None, base: Optional[str] = None, quote: Optional[str] = None, asset: Optional[str] = None, symbol: Optional[str] = None) -> CatalogMarketsData
```

Returns list of _supported_ markets that correspond to a filter. If no filter is set, returns all supported assets.

**Arguments**:

- `markets` (`list(str), str`): list of market names, e.g. 'coinbase-btc-usd-spot'
- `market_type` (`str`): Type of market: "spot", "future", "option"
- `exchange` (`str`): name of the exchange
- `base` (`str`): name of base asset
- `quote` (`str`): name of quote asset
- `asset` (`str`): name of either base or quote asset
- `symbol` (`str`): name of a symbol. Usually used for futures contracts.

**Returns**:

`list(dict(str, any))`: Information about markets that correspond to a filter along with meta information like: type of market and min and max supported time frames.

<a name="coinmetrics.api_client.CoinMetricsClient.catalog_full_metrics"></a>
#### catalog\_full\_metrics

```python
 | catalog_full_metrics(metrics: Optional[Union[List[str], str]] = None, reviewable: Optional[bool] = None) -> CatalogMetricsData
```

Returns list of _supported_ metrics along with information for them like
description, category, precision and assets for which a metric is supported.

**Arguments**:

- `metrics` (`list(str), str`): A single metric name or a list of metrics to return info for. If no metrics provided, all supported metrics are returned.
- `reviewable` (`bool`): Show only reviewable or non-reviewable by human metrics. By default all metrics are shown.

**Returns**:

`list(dict(str, any))`: Information about metrics that correspond to a filter along with meta information like: description, category, precision and assets for which a metric is supported.

<a name="coinmetrics.api_client.CoinMetricsClient.get_asset_alerts"></a>
#### get\_asset\_alerts

```python
 | get_asset_alerts(assets: Union[List[str], str], alerts: Union[List[str], str], page_size: Optional[int] = None, paging_from: Optional[Union[PagingFrom, str]] = None, start_time: Optional[Union[datetime, date, str]] = None, end_time: Optional[Union[datetime, date, str]] = None, start_inclusive: Optional[bool] = None, end_inclusive: Optional[bool] = None, timezone: Optional[str] = None) -> DataCollection
```

Returns asset alerts for the specified assets.

**Arguments**:

- `assets` (`list(str), str`): list of asset names, e.g. 'btc'
- `alerts` (`list(str), str`): list of asset alert names
- `page_size` (`int`): number of items returned per page when calling the API. If the request times out, try using a smaller number.
- `paging_from` (`PagingFrom, str`): Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
- `start_time` (`datetime, date, str`): Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `end_time` (`datetime, date, str`): End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `start_inclusive` (`bool`): Flag to define if start timestamp must be included in the timeseries if present. True by default.
- `end_inclusive` (`bool`): Flag to define if end timestamp must be included in the timeseries if present. True by default.
- `timezone` (`str`): timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.

**Returns**:

`DataCollection`: Asset alerts timeseries.

<a name="coinmetrics.api_client.CoinMetricsClient.get_asset_chains"></a>
#### get\_asset\_chains

```python
 | get_asset_chains(assets: Union[List[str], str], page_size: Optional[int] = None, paging_from: Optional[Union[PagingFrom, str]] = None, start_time: Optional[Union[datetime, date, str]] = None, end_time: Optional[Union[datetime, date, str]] = None, start_inclusive: Optional[bool] = None, end_inclusive: Optional[bool] = None, timezone: Optional[str] = None) -> DataCollection
```

Returns the chains of blocks for the specified assets.

**Arguments**:

- `assets` (`list(str), str`): list of asset names, e.g. 'btc'
- `page_size` (`int`): number of items returned per page when calling the API. If the request times out, try using a smaller number.
- `paging_from` (`PagingFrom, str`): Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
- `start_time` (`datetime, date, str`): Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `end_time` (`datetime, date, str`): End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `start_inclusive` (`bool`): Flag to define if start timestamp must be included in the timeseries if present. True by default.
- `end_inclusive` (`bool`): Flag to define if end timestamp must be included in the timeseries if present. True by default.
- `timezone` (`str`): timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.

**Returns**:

`DataCollection`: Asset chains timeseries.

<a name="coinmetrics.api_client.CoinMetricsClient.get_asset_metrics"></a>
#### get\_asset\_metrics

```python
 | get_asset_metrics(assets: Union[List[str], str], metrics: Union[List[str], str], frequency: Optional[str] = None, page_size: Optional[int] = None, paging_from: Optional[Union[PagingFrom, str]] = None, start_time: Optional[Union[datetime, date, str]] = None, end_time: Optional[Union[datetime, date, str]] = None, start_height: Optional[int] = None, end_height: Optional[int] = None, start_inclusive: Optional[bool] = None, end_inclusive: Optional[bool] = None, timezone: Optional[str] = None, sort: Optional[str] = None, limit_per_asset: Optional[int] = None) -> DataCollection
```

Returns requested metrics for specified assets.

**Arguments**:

- `assets` (`list(str), str`): list of asset names, e.g. 'btc'
- `metrics` (`list(str), str`): list of _asset-specific_ metric names, e.g. 'PriceUSD'
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
- `sort` (`str`): How results will be sorted, e.g. "asset", "height", or "time". Default is "asset". Metrics with 1b frequency are sorted by (asset, height, block_hash) tuples by default. Metrics with other frequencies are sorted by (asset, time) by default. If you want to sort 1d metrics by (time, asset) you should choose time as value for the sort parameter. Sorting by time is useful if you request metrics for a set of assets.
- `limit_per_asset` (`int`): How many entries _per asset_ the result should contain.

**Returns**:

`DataCollection`: Asset Metrics timeseries.

<a name="coinmetrics.api_client.CoinMetricsClient.get_exchange_metrics"></a>
#### get\_exchange\_metrics

```python
 | get_exchange_metrics(exchanges: Union[List[str], str], metrics: Union[List[str], str], frequency: Optional[str] = None, page_size: Optional[int] = None, paging_from: Optional[Union[PagingFrom, str]] = None, start_time: Optional[Union[datetime, date, str]] = None, end_time: Optional[Union[datetime, date, str]] = None, start_height: Optional[int] = None, end_height: Optional[int] = None, start_inclusive: Optional[bool] = None, end_inclusive: Optional[bool] = None, timezone: Optional[str] = None, sort: Optional[str] = None, limit_per_exchange: Optional[int] = None) -> DataCollection
```

Returns metrics for specified exchanges.

**Arguments**:

- `exchanges` (`list(str), str`): A single exchange name or a list of exchanges to return info for.
- `metrics` (`list(str), str`): list of _exchange-specific_ metric names, e.g. 'open_interest_reported_future_usd'. To find a list of available metrics for a given exchange, call `client.catalog_exchanges()`
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
- `sort` (`str`): How results will be sorted, e.g. 'exchange', 'time'. Metrics are sorted by 'exchange' by default.
- `limit_per_exchange` (`int`): How many entries _per exchange_ the result should contain.

**Returns**:

`DataCollection`: Asset Metrics timeseries.

<a name="coinmetrics.api_client.CoinMetricsClient.get_exchange_asset_metrics"></a>
#### get\_exchange\_asset\_metrics

```python
 | get_exchange_asset_metrics(exchange_assets: Union[List[str], str], metrics: Union[List[str], str], frequency: Optional[str] = None, page_size: Optional[int] = None, paging_from: Optional[Union[PagingFrom, str]] = None, start_time: Optional[Union[datetime, date, str]] = None, end_time: Optional[Union[datetime, date, str]] = None, start_height: Optional[int] = None, end_height: Optional[int] = None, start_inclusive: Optional[bool] = None, end_inclusive: Optional[bool] = None, timezone: Optional[str] = None, sort: Optional[str] = None, limit_per_exchange_asset: Optional[int] = None) -> DataCollection
```

Returns metrics for specified exchange-asset.

**Arguments**:

- `exchange_assets` (`list(str), str`): A single exchange-asset pairs (e.g. "binance-btc" or a list of exchange-asset-pair to return info for.
- `metrics` (`list(str), str`): list of _exchange-specific_ metric names, e.g. 'open_interest_reported_future_usd'. To find a list of available metrics for a given exchange, call `client.catalog_exchanges()`
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
- `sort` (`str`): How results will be sorted, e.g. "exchange_asset", "time". Default is "exchange_asset".
- `limit_per_exchange_asset` (`int`): How many entries _per exchange-asset_ the result should contain.

**Returns**:

`DataCollection`: Exchange-Asset Metrics timeseries.

<a name="coinmetrics.api_client.CoinMetricsClient.get_pair_metrics"></a>
#### get\_pair\_metrics

```python
 | get_pair_metrics(pairs: Union[List[str], str], metrics: Union[List[str], str], frequency: Optional[str] = None, page_size: Optional[int] = None, paging_from: Optional[Union[PagingFrom, str]] = None, start_time: Optional[Union[datetime, date, str]] = None, end_time: Optional[Union[datetime, date, str]] = None, start_height: Optional[int] = None, end_height: Optional[int] = None, start_inclusive: Optional[bool] = None, end_inclusive: Optional[bool] = None, timezone: Optional[str] = None, sort: Optional[str] = None, limit_per_pair: Optional[int] = None) -> DataCollection
```

Returns metrics books for specified asset-asset pairs.

**Arguments**:

- `pairs` (`list(str), str`): A single asset-asset pairs (e.g. "btc-usd") or a list of asset-asset-pairs to return info for.
- `metrics` (`list(str), str`): list of _exchange-specific_ metric names, e.g. 'open_interest_reported_future_usd'. To find a list of available metrics for a given exchange, call `client.catalog_exchanges()`
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
- `sort` (`str`): How results will be sorted, e.g."pair", "time". "pair" by default
- `limit_per_pair` (`int`): How many entries _per asset pair_ the result should contain.

**Returns**:

`DataCollection`: Exchange-Asset Metrics timeseries.

<a name="coinmetrics.api_client.CoinMetricsClient.get_institution_metrics"></a>
#### get\_institution\_metrics

```python
 | get_institution_metrics(institutions: Union[List[str], str], metrics: Union[List[str], str], frequency: Optional[str] = None, page_size: Optional[int] = None, paging_from: Optional[Union[PagingFrom, str]] = None, start_time: Optional[Union[datetime, date, str]] = None, end_time: Optional[Union[datetime, date, str]] = None, start_height: Optional[int] = None, end_height: Optional[int] = None, start_inclusive: Optional[bool] = None, end_inclusive: Optional[bool] = None, timezone: Optional[str] = None, sort: Optional[str] = None, limit_per_institution: Optional[int] = None) -> DataCollection
```

Returns metrics for specified institutions.

**Arguments**:

- `institutions` (`list(str), str`): A single institution name or a list of institutions to return info for.
- `metrics` (`list(str), str`): list of _institution-specific_ metric names, e.g. 'gbtc_total_assets'
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
- `sort` (`str`): How results will be sorted, e.g. "institution", or "time". Default is "institution".
- `limit_per_institution` (`int`): How many entries _per institution_ the result should contain.

**Returns**:

`DataCollection`: Asset Metrics timeseries.

<a name="coinmetrics.api_client.CoinMetricsClient.get_index_levels"></a>
#### get\_index\_levels

```python
 | get_index_levels(indexes: Union[List[str], str], frequency: Optional[str] = None, page_size: Optional[int] = None, paging_from: Optional[Union[PagingFrom, str]] = None, start_time: Optional[Union[datetime, date, str]] = None, end_time: Optional[Union[datetime, date, str]] = None, start_inclusive: Optional[bool] = None, end_inclusive: Optional[bool] = None, timezone: Optional[str] = None, limit_per_index: Optional[int] = None) -> DataCollection
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
- `limit_per_index` (`int`): How many entries _per index_ the result should contain.

**Returns**:

`DataCollection`: Index Levels timeseries.

<a name="coinmetrics.api_client.CoinMetricsClient.get_index_constituents"></a>
#### get\_index\_constituents

```python
 | get_index_constituents(indexes: Union[List[str], str], frequency: Optional[str] = None, page_size: Optional[int] = None, paging_from: Optional[Union[PagingFrom, str]] = None, start_time: Optional[Union[datetime, date, str]] = None, end_time: Optional[Union[datetime, date, str]] = None, start_inclusive: Optional[bool] = None, end_inclusive: Optional[bool] = None, timezone: Optional[str] = None) -> DataCollection
```

Returns index constituents for specified indexes and date range.

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

`DataCollection`: Index Constituents timeseries.

<a name="coinmetrics.api_client.CoinMetricsClient.get_market_candles"></a>
#### get\_market\_candles

```python
 | get_market_candles(markets: Union[List[str], str], frequency: Optional[str] = None, page_size: Optional[int] = None, paging_from: Optional[Union[PagingFrom, str]] = None, start_time: Optional[Union[datetime, date, str]] = None, end_time: Optional[Union[datetime, date, str]] = None, start_inclusive: Optional[bool] = None, end_inclusive: Optional[bool] = None, timezone: Optional[str] = None, limit_per_market: Optional[int] = None) -> DataCollection
```

Returns market candles for specified markets, frequency and date range.
For more information on market candles, see: https://docs.coinmetrics.io/info/markets/candles

**Arguments**:

- `markets` (`list(str), str`): list of market ids. Market ids use the following naming convention: `exchangeName-baseAsset-quoteAsset-spot` for spot markets, `exchangeName-futuresSymbol-future` for futures markets, and `exchangeName-optionsSymbol-option` for options markets. e.g., `'coinbase-btc-usd-spot'`, `'bitmex-XBTUSD-future'`
- `frequency` (`str`): frequency of the returned timeseries, e.g 15s, 1d, etc.
- `page_size` (`int`): number of items returned per page when calling the API. If the request times out, try using a smaller number.
- `paging_from` (`PagingFrom, str`): Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
- `start_time` (`datetime, date, str`): Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `end_time` (`datetime, date, str`): End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `start_inclusive` (`bool`): Flag to define if start timestamp must be included in the timeseries if present. True by default.
- `end_inclusive` (`bool`): Flag to define if end timestamp must be included in the timeseries if present. True by default.
- `timezone` (`str`): timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.
- `limit_per_market` (`int`): How many entries _per market_ the result should contain.

**Returns**:

`DataCollection`: Market Candles timeseries.

<a name="coinmetrics.api_client.CoinMetricsClient.get_market_trades"></a>
#### get\_market\_trades

```python
 | get_market_trades(markets: Union[List[str], str], page_size: Optional[int] = None, paging_from: Optional[Union[PagingFrom, str]] = None, start_time: Optional[Union[datetime, date, str]] = None, end_time: Optional[Union[datetime, date, str]] = None, start_inclusive: Optional[bool] = None, end_inclusive: Optional[bool] = None, timezone: Optional[str] = None, limit_per_market: Optional[int] = None) -> DataCollection
```

Returns market trades for specified markets and date range.
For more information on market trades, see: https://docs.coinmetrics.io/info/markets/trades

**Arguments**:

- `markets` (`list(str), str`): list of market ids. Market ids use the following naming convention: `exchangeName-baseAsset-quoteAsset-spot` for spot markets, `exchangeName-futuresSymbol-future` for futures markets, and `exchangeName-optionsSymbol-option` for options markets. e.g., `'coinbase-btc-usd-spot'`, `'bitmex-XBTUSD-future'`
- `page_size` (`int`): number of items returned per page when calling the API. If the request times out, try using a smaller number.
- `paging_from` (`PagingFrom, str`): Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
- `start_time` (`datetime, date, str`): Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `end_time` (`datetime, date, str`): End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `start_inclusive` (`bool`): Flag to define if start timestamp must be included in the timeseries if present. True by default.
- `end_inclusive` (`bool`): Flag to define if end timestamp must be included in the timeseries if present. True by default.
- `timezone` (`str`): timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.
- `limit_per_market` (`int`): How many entries _per market_ the result should contain.

**Returns**:

`DataCollection`: Market Trades timeseries.

<a name="coinmetrics.api_client.CoinMetricsClient.get_market_open_interest"></a>
#### get\_market\_open\_interest

```python
 | get_market_open_interest(markets: Union[List[str], str], page_size: Optional[int] = None, paging_from: Optional[Union[PagingFrom, str]] = None, start_time: Optional[Union[datetime, date, str]] = None, end_time: Optional[Union[datetime, date, str]] = None, start_inclusive: Optional[bool] = None, end_inclusive: Optional[bool] = None, timezone: Optional[str] = None, limit_per_market: Optional[int] = None) -> DataCollection
```

Returns market open interest for specified markets and date range.
For more information on open interest, see: https://docs.coinmetrics.io/info/markets/openinterest

**Arguments**:

- `markets` (`list(str), str`): list of market ids. Market ids use the following naming convention: `exchangeName-baseAsset-quoteAsset-spot` for spot markets, `exchangeName-futuresSymbol-future` for futures markets, and `exchangeName-optionsSymbol-option` for options markets. e.g., `'coinbase-btc-usd-spot'`, `'bitmex-XBTUSD-future'`
- `page_size` (`int`): number of items returned per page when calling the API. If the request times out, try using a smaller number.
- `paging_from` (`PagingFrom, str`): Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
- `start_time` (`datetime, date, str`): Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `end_time` (`datetime, date, str`): End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `start_inclusive` (`bool`): Flag to define if start timestamp must be included in the timeseries if present. True by default.
- `end_inclusive` (`bool`): Flag to define if end timestamp must be included in the timeseries if present. True by default.
- `timezone` (`str`): timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.
- `limit_per_market` (`int`): How many entries _per market_ the result should contain.

**Returns**:

`DataCollection`: Market Open Interest timeseries.

<a name="coinmetrics.api_client.CoinMetricsClient.get_market_liquidations"></a>
#### get\_market\_liquidations

```python
 | get_market_liquidations(markets: Union[List[str], str], page_size: Optional[int] = None, paging_from: Optional[Union[PagingFrom, str]] = None, start_time: Optional[Union[datetime, date, str]] = None, end_time: Optional[Union[datetime, date, str]] = None, start_inclusive: Optional[bool] = None, end_inclusive: Optional[bool] = None, timezone: Optional[str] = None, limit_per_market: Optional[int] = None) -> DataCollection
```

Returns market liquidations for specified markets and date range.
For more information on liquidations, see: https://docs.coinmetrics.io/info/markets/liquidations

**Arguments**:

- `markets` (`list(str), str`): list of market ids. Market ids use the following naming convention: `exchangeName-baseAsset-quoteAsset-spot` for spot markets, `exchangeName-futuresSymbol-future` for futures markets, and `exchangeName-optionsSymbol-option` for options markets. e.g., `'coinbase-btc-usd-spot'`, `'bitmex-XBTUSD-future'`
- `page_size` (`int`): number of items returned per page when calling the API. If the request times out, try using a smaller number.
- `paging_from` (`PagingFrom, str`): Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
- `start_time` (`datetime, date, str`): Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `end_time` (`datetime, date, str`): End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `start_inclusive` (`bool`): Flag to define if start timestamp must be included in the timeseries if present. True by default.
- `end_inclusive` (`bool`): Flag to define if end timestamp must be included in the timeseries if present. True by default.
- `timezone` (`str`): timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.
- `limit_per_market` (`int`): How many entries _per market_ the result should contain.

**Returns**:

`DataCollection`: Market Liquidations timeseries.

<a name="coinmetrics.api_client.CoinMetricsClient.get_market_funding_rates"></a>
#### get\_market\_funding\_rates

```python
 | get_market_funding_rates(markets: Union[List[str], str], page_size: Optional[int] = None, paging_from: Optional[Union[PagingFrom, str]] = None, start_time: Optional[Union[datetime, date, str]] = None, end_time: Optional[Union[datetime, date, str]] = None, start_inclusive: Optional[bool] = None, end_inclusive: Optional[bool] = None, timezone: Optional[str] = None, limit_per_market: Optional[int] = None) -> DataCollection
```

Returns market funding rates for specified markets and date range.
For more information on funding rates, see: https://docs.coinmetrics.io/info/markets/fundingrates

**Arguments**:

- `markets` (`list(str), str`): list of market ids. Market ids use the following naming convention: `exchangeName-baseAsset-quoteAsset-spot` for spot markets, `exchangeName-futuresSymbol-future` for futures markets, and `exchangeName-optionsSymbol-option` for options markets. e.g., `'coinbase-btc-usd-spot'`, `'bitmex-XBTUSD-future'`
- `page_size` (`int`): number of items returned per page when calling the API. If the request times out, try using a smaller number.
- `paging_from` (`PagingFrom, str`): Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
- `start_time` (`datetime, date, str`): Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `end_time` (`datetime, date, str`): End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `start_inclusive` (`bool`): Flag to define if start timestamp must be included in the timeseries if present. True by default.
- `end_inclusive` (`bool`): Flag to define if end timestamp must be included in the timeseries if present. True by default.
- `timezone` (`str`): timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.
- `limit_per_market` (`int`): How many entries _per market_ the result should contain.

**Returns**:

`DataCollection`: Market Funding Rates timeseries.

<a name="coinmetrics.api_client.CoinMetricsClient.get_market_orderbooks"></a>
#### get\_market\_orderbooks

```python
 | get_market_orderbooks(markets: Union[List[str], str], page_size: Optional[int] = None, paging_from: Optional[Union[PagingFrom, str]] = None, start_time: Optional[Union[datetime, date, str]] = None, end_time: Optional[Union[datetime, date, str]] = None, start_inclusive: Optional[bool] = None, end_inclusive: Optional[bool] = None, depth_limit: Optional[str] = "100", timezone: Optional[str] = None, limit_per_market: Optional[int] = None) -> DataCollection
```

Returns market order books for specified markets and date range.
For more information on order books, see: https://docs.coinmetrics.io/info/markets/orderbook

**Arguments**:

- `markets` (`list(str), str`): list of market ids. Market ids use the following naming convention: `exchangeName-baseAsset-quoteAsset-spot` for spot markets, `exchangeName-futuresSymbol-future` for futures markets, and `exchangeName-optionsSymbol-option` for options markets. e.g., `'coinbase-btc-usd-spot'`, `'bitmex-XBTUSD-future'`
- `page_size` (`int`): number of items returned per page when calling the API. If the request times out, try using a smaller number.
- `paging_from` (`PagingFrom, str`): Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
- `start_time` (`datetime, date, str`): Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `end_time` (`datetime, date, str`): End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `start_inclusive` (`bool`): Flag to define if start timestamp must be included in the timeseries if present. True by default.
- `end_inclusive` (`bool`): Flag to define if end timestamp must be included in the timeseries if present. True by default.
- `depth_limit` (`str`): book depth limit, 100 levels max or full book that is not limited and provided as is from the exchange. Full book snapshots are collected once per hour
- `timezone` (`str`): timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.
- `limit_per_market` (`int`): How many entries _per market_ the result should contain.

**Returns**:

`DataCollection`: Market Order Books timeseries.

<a name="coinmetrics.api_client.CoinMetricsClient.get_market_quotes"></a>
#### get\_market\_quotes

```python
 | get_market_quotes(markets: Union[List[str], str], page_size: Optional[int] = None, paging_from: Optional[Union[PagingFrom, str]] = None, start_time: Optional[Union[datetime, date, str]] = None, end_time: Optional[Union[datetime, date, str]] = None, start_inclusive: Optional[bool] = None, end_inclusive: Optional[bool] = None, timezone: Optional[str] = None, limit_per_market: Optional[int] = None) -> DataCollection
```

Returns market quotes for specified markets and date range.
For more information on quotes, see: https://docs.coinmetrics.io/info/markets/quotes

**Arguments**:

- `markets` (`list(str), str`): list of market ids. Market ids use the following naming convention: `exchangeName-baseAsset-quoteAsset-spot` for spot markets, `exchangeName-futuresSymbol-future` for futures markets, and `exchangeName-optionsSymbol-option` for options markets. e.g., `'coinbase-btc-usd-spot'`, `'bitmex-XBTUSD-future'`
- `page_size` (`int`): number of items returned per page when calling the API. If the request times out, try using a smaller number.
- `paging_from` (`PagingFrom, str`): Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
- `start_time` (`datetime, date, str`): Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `end_time` (`datetime, date, str`): End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `start_inclusive` (`bool`): Flag to define if start timestamp must be included in the timeseries if present. True by default.
- `end_inclusive` (`bool`): Flag to define if end timestamp must be included in the timeseries if present. True by default.
- `timezone` (`str`): timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.
- `limit_per_market` (`int`): How many entries _per market_ the result should contain.

**Returns**:

`DataCollection`: Market Quotes timeseries.

<a name="coinmetrics.api_client.CoinMetricsClient.get_market_contract_prices"></a>
#### get\_market\_contract\_prices

```python
 | get_market_contract_prices(markets: Union[List[str], str], page_size: Optional[int] = None, paging_from: Optional[Union[PagingFrom, str]] = None, start_time: Optional[Union[datetime, date, str]] = None, end_time: Optional[Union[datetime, date, str]] = None, start_inclusive: Optional[bool] = None, end_inclusive: Optional[bool] = None, timezone: Optional[str] = None, limit_per_market: Optional[int] = None) -> DataCollection
```

Returns contract prices for specified markets. This includes index price and mark price that are used by the exchange for settlement and risk management purposes.

**Arguments**:

- `markets` (`list(str), str`): list of market ids. Market ids use the following naming convention: `exchangeName-baseAsset-quoteAsset-spot` for spot markets, `exchangeName-futuresSymbol-future` for futures markets, and `exchangeName-optionsSymbol-option` for options markets. e.g., `'coinbase-btc-usd-spot'`, `'bitmex-XBTUSD-future', 'deribit-ETH-25MAR22-1200-P-option'`
- `page_size` (`int`): number of items returned per page when calling the API. If the request times out, try using a smaller number.
- `paging_from` (`PagingFrom, str`): Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
- `start_time` (`datetime, date, str`): Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `end_time` (`datetime, date, str`): End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `start_inclusive` (`bool`): Flag to define if start timestamp must be included in the timeseries if present. True by default.
- `end_inclusive` (`bool`): Flag to define if end timestamp must be included in the timeseries if present. True by default.
- `timezone` (`str`): timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.
- `limit_per_market` (`int`): How many entries _per market_ the result should contain.

**Returns**:

`DataCollection`: Market Contract Prices timeseries.

<a name="coinmetrics.api_client.CoinMetricsClient.get_market_implied_volatility"></a>
#### get\_market\_implied\_volatility

```python
 | get_market_implied_volatility(markets: Union[List[str], str], page_size: Optional[int] = None, paging_from: Optional[Union[PagingFrom, str]] = None, start_time: Optional[Union[datetime, date, str]] = None, end_time: Optional[Union[datetime, date, str]] = None, start_inclusive: Optional[bool] = None, end_inclusive: Optional[bool] = None, timezone: Optional[str] = None, limit_per_market: Optional[int] = None) -> DataCollection
```

Returns implied volatility for specified markets.

**Arguments**:

- `markets` (`list(str), str`): list of market ids. Market ids use the following naming convention: `exchangeName-baseAsset-quoteAsset-spot` for spot markets, `exchangeName-futuresSymbol-future` for futures markets, and `exchangeName-optionsSymbol-option` for options markets. e.g., `'coinbase-btc-usd-spot'`, `'bitmex-XBTUSD-future', 'deribit-ETH-25MAR22-1200-P-option'`
- `page_size` (`int`): number of items returned per page when calling the API. If the request times out, try using a smaller number.
- `paging_from` (`PagingFrom, str`): Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
- `start_time` (`datetime, date, str`): Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `end_time` (`datetime, date, str`): End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `start_inclusive` (`bool`): Flag to define if start timestamp must be included in the timeseries if present. True by default.
- `end_inclusive` (`bool`): Flag to define if end timestamp must be included in the timeseries if present. True by default.
- `timezone` (`str`): timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.
- `limit_per_market` (`int`): How many entries _per market_ the result should contain.

**Returns**:

`DataCollection`: Market Volatility timeseries.

<a name="coinmetrics.api_client.CoinMetricsClient.get_market_greeks"></a>
#### get\_market\_greeks

```python
 | get_market_greeks(markets: Union[List[str], str], page_size: Optional[int] = None, paging_from: Optional[Union[PagingFrom, str]] = None, start_time: Optional[Union[datetime, date, str]] = None, end_time: Optional[Union[datetime, date, str]] = None, start_inclusive: Optional[bool] = None, end_inclusive: Optional[bool] = None, timezone: Optional[str] = None, limit_per_market: Optional[int] = None) -> DataCollection
```

Returns greeks for option markets.

**Arguments**:

- `markets` (`list(str), str`): list of market ids. Market ids use the following naming convention: `exchangeName-baseAsset-quoteAsset-spot` for spot markets, `exchangeName-futuresSymbol-future` for futures markets, and `exchangeName-optionsSymbol-option` for options markets. e.g., `'coinbase-btc-usd-spot'`, `'bitmex-XBTUSD-future', 'deribit-ETH-25MAR22-1200-P-option'`
- `page_size` (`int`): number of items returned per page when calling the API. If the request times out, try using a smaller number.
- `paging_from` (`PagingFrom, str`): Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
- `start_time` (`datetime, date, str`): Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `end_time` (`datetime, date, str`): End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `start_inclusive` (`bool`): Flag to define if start timestamp must be included in the timeseries if present. True by default.
- `end_inclusive` (`bool`): Flag to define if end timestamp must be included in the timeseries if present. True by default.
- `timezone` (`str`): timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.
- `limit_per_market` (`int`): How many entries _per market_ the result should contain.

**Returns**:

`DataCollection`: Market Volatility timeseries.

<a name="coinmetrics.api_client.CoinMetricsClient.get_mining_pool_tips_summary"></a>
#### get\_mining\_pool\_tips\_summary

```python
 | get_mining_pool_tips_summary(assets: Union[List[str], str], page_size: Optional[int] = None, paging_from: Optional[Union[PagingFrom, str]] = None, start_time: Optional[Union[datetime, date, str]] = None, end_time: Optional[Union[datetime, date, str]] = None, start_inclusive: Optional[bool] = None, end_inclusive: Optional[bool] = None, timezone: Optional[str] = None) -> DataCollection
```

Returns mining pool tips summaries for specified assets.

**Arguments**:

- `assets` (`list(str), str`): list of asset names, e.g. 'btc'
- `page_size` (`int`): number of items returned per page when calling the API. If the request times out, try using a smaller number.
- `paging_from` (`PagingFrom, str`): Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
- `start_time` (`datetime, date, str`): Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `end_time` (`datetime, date, str`): End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `start_inclusive` (`bool`): Flag to define if start timestamp must be included in the timeseries if present. True by default.
- `end_inclusive` (`bool`): Flag to define if end timestamp must be included in the timeseries if present. True by default.
- `timezone` (`str`): timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.

**Returns**:

`DataCollection`: Mining Pool Tips timeseries.

<a name="coinmetrics.api_client.CoinMetricsClient.get_mempool_feerates"></a>
#### get\_mempool\_feerates

```python
 | get_mempool_feerates(assets: Union[List[str], str], page_size: Optional[int] = 200, paging_from: Optional[Union[PagingFrom, str]] = None, start_time: Optional[Union[datetime, date, str]] = None, end_time: Optional[Union[datetime, date, str]] = None, start_inclusive: Optional[bool] = None, end_inclusive: Optional[bool] = None, timezone: Optional[str] = None) -> DataCollection
```

Returns mempool feerates for the specified assets. Note: for this method, page_size must be <= 200.

**Arguments**:

- `assets` (`list(str), str`): list of asset names, e.g. 'btc'
- `page_size` (`int`): number of items returned per page when calling the API. If the request times out, try using a smaller number.
- `paging_from` (`PagingFrom, str`): Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
- `start_time` (`datetime, date, str`): Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `end_time` (`datetime, date, str`): End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `start_inclusive` (`bool`): Flag to define if start timestamp must be included in the timeseries if present. True by default.
- `end_inclusive` (`bool`): Flag to define if end timestamp must be included in the timeseries if present. True by default.
- `timezone` (`str`): timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.

**Returns**:

`DataCollection`: Mempool Fee Rates timeseries.

<a name="coinmetrics.api_client.CoinMetricsClient.get_stream_asset_metrics"></a>
#### get\_stream\_asset\_metrics

```python
 | get_stream_asset_metrics(assets: Union[List[str], str], metrics: Union[List[str], str], frequency: Optional[str] = None, backfill: Union[Backfill, str] = Backfill.LATEST) -> CmStream
```

Returns timeseries stream of metrics for specified assets.

**Arguments**:

- `assets` (`list(str), str`): list of asset names, e.g. 'btc'
- `metrics` (`list(str), str`): list of _asset-specific_ metric names, e.g. 'PriceUSD'
- `frequency` (`str`): frequency of the returned timeseries, e.g 15s, 1d, etc.
- `backfill` (`str`): What data should be sent upon a connection ("latest" or "none"). By default the latest values are sent just before real-time data.

**Returns**:

`CmStream`: Asset Metrics timeseries stream.

<a name="coinmetrics.api_client.CoinMetricsClient.get_stream_market_trades"></a>
#### get\_stream\_market\_trades

```python
 | get_stream_market_trades(markets: Union[List[str], str], backfill: Union[Backfill, str] = Backfill.LATEST) -> CmStream
```

Returns timeseries stream of market trades.

**Arguments**:

- `markets` (`list(str), str`): list of markets or market patterns like exchange-* or exchange-*-spot or *USDT-future.
- `backfill` (`str`): What data should be sent upon a connection ("latest" or "none"). By default the latest values are sent just before real-time data.

**Returns**:

`CmStream`: Market Trades timeseries stream.

<a name="coinmetrics.api_client.CoinMetricsClient.get_stream_market_orderbooks"></a>
#### get\_stream\_market\_orderbooks

```python
 | get_stream_market_orderbooks(markets: Union[List[str], str], backfill: Union[Backfill, str] = Backfill.LATEST) -> CmStream
```

Returns timeseries stream of market orderbooks.

**Arguments**:

- `markets` (`list(str), str`): list of markets or market patterns like exchange-* or exchange-*-spot or *USDT-future.
- `backfill` (`str`): What data should be sent upon a connection ("latest" or "none"). By default the latest values are sent just before real-time data.

**Returns**:

`CmStream`: Market Orderbooks timeseries stream.

<a name="coinmetrics.api_client.CoinMetricsClient.get_stream_market_quotes"></a>
#### get\_stream\_market\_quotes

```python
 | get_stream_market_quotes(markets: Union[List[str], str], backfill: Union[Backfill, str] = Backfill.LATEST) -> CmStream
```

Returns timeseries stream of market quotes.

**Arguments**:

- `markets` (`list(str), str`): list of markets or market patterns like exchange-* or exchange-*-spot or *USDT-future.
- `backfill` (`str`): What data should be sent upon a connection ("latest" or "none"). By default the latest values are sent just before real-time data.

**Returns**:

`CmStream`: Market Quotes timeseries stream.

<a name="coinmetrics.api_client.CoinMetricsClient.get_list_of_blocks"></a>
#### get\_list\_of\_blocks

```python
 | get_list_of_blocks(asset: str, block_hashes: Optional[Union[List[str], str]] = None, heights: Optional[Union[List[str], str]] = None, page_size: Optional[int] = None, paging_from: Optional[Union[PagingFrom, str]] = None, start_time: Optional[Union[datetime, date, str]] = None, end_time: Optional[Union[datetime, date, str]] = None, start_inclusive: Optional[bool] = None, end_inclusive: Optional[bool] = None, timezone: Optional[str] = None) -> DataCollection
```

Returns a list of blockchain blocks metadata.

**Arguments**:

- `asset` (`str`): Asset name
- `block_hashes` (`str, list(str)`): Optional comma separated list of block hashes to filter a response.
- `heights` (`str, list(str)`): Optional comma separated list of block heights to filter a response.
- `page_size` (`int`): number of items returned per page when calling the API. If the request times out, try using a smaller number.
- `paging_from` (`PagingFrom, str`): Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
- `start_time` (`datetime, date, str`): Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `end_time` (`datetime, date, str`): End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `start_inclusive` (`bool`): Flag to define if start timestamp must be included in the timeseries if present. True by default.
- `end_inclusive` (`bool`): Flag to define if end timestamp must be included in the timeseries if present. True by default.
- `timezone` (`str`): timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.

**Returns**:

`DataCollection`: list of blockchain blocks metadata

<a name="coinmetrics.api_client.CoinMetricsClient.get_list_of_accounts"></a>
#### get\_list\_of\_accounts

```python
 | get_list_of_accounts(asset: str, accounts: Optional[Union[List[str], str]] = None, page_size: Optional[int] = None, paging_from: Optional[Union[PagingFrom, str]] = None, start_time: Optional[Union[datetime, date, str]] = None, end_time: Optional[Union[datetime, date, str]] = None, start_inclusive: Optional[bool] = None, end_inclusive: Optional[bool] = None, timezone: Optional[str] = None) -> DataCollection
```

Returns a list of blockchain accounts with their balances.

**Arguments**:

- `asset` (`str`): Asset name
- `accounts` (`str, list(str)`): Optional comma separated list of accounts to filter a response.
- `page_size` (`int`): number of items returned per page when calling the API. If the request times out, try using a smaller number.
- `paging_from` (`PagingFrom, str`): Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
- `start_time` (`datetime, date, str`): Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `end_time` (`datetime, date, str`): End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `start_inclusive` (`bool`): Flag to define if start timestamp must be included in the timeseries if present. True by default.
- `end_inclusive` (`bool`): Flag to define if end timestamp must be included in the timeseries if present. True by default.
- `timezone` (`str`): timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.

**Returns**:

`DataCollection`: list of blockchain accounts metadata

<a name="coinmetrics.api_client.CoinMetricsClient.get_list_of_transactions"></a>
#### get\_list\_of\_transactions

```python
 | get_list_of_transactions(asset: str, transaction_hashes: Optional[Union[List[str], str]] = None, block_hashes: Optional[Union[List[str], str]] = None, page_size: Optional[int] = None, paging_from: Optional[Union[PagingFrom, str]] = None, start_time: Optional[Union[datetime, date, str]] = None, end_time: Optional[Union[datetime, date, str]] = None, start_inclusive: Optional[bool] = None, end_inclusive: Optional[bool] = None, timezone: Optional[str] = None) -> DataCollection
```

Returns a list of blockchain transactions metadata.

**Arguments**:

- `asset` (`str`): Asset name
- `transaction_hashes` (`str, list(str)`): Optional comma separated list of transaction hashes to filter a response.
- `block_hashes` (`str, list(str)`): Optional comma separated list of block hashes to filter a response.
- `page_size` (`int`): number of items returned per page when calling the API. If the request times out, try using a smaller number.
- `paging_from` (`PagingFrom, str`): Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
- `start_time` (`datetime, date, str`): Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `end_time` (`datetime, date, str`): End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `start_inclusive` (`bool`): Flag to define if start timestamp must be included in the timeseries if present. True by default.
- `end_inclusive` (`bool`): Flag to define if end timestamp must be included in the timeseries if present. True by default.
- `timezone` (`str`): timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.

**Returns**:

`DataCollection`: list of transaction metadata

<a name="coinmetrics.api_client.CoinMetricsClient.get_list_of_balance_updates"></a>
#### get\_list\_of\_balance\_updates

```python
 | get_list_of_balance_updates(asset: str, accounts: Optional[Union[List[str], str]] = None, transaction_hashes: Optional[Union[List[str], str]] = None, block_hashes: Optional[Union[List[str], str]] = None, page_size: Optional[int] = None, paging_from: Optional[Union[PagingFrom, str]] = None, start_time: Optional[Union[datetime, date, str]] = None, end_time: Optional[Union[datetime, date, str]] = None, start_inclusive: Optional[bool] = None, end_inclusive: Optional[bool] = None, timezone: Optional[str] = None) -> DataCollection
```

Returns a list of blockchain accounts balance updates.

**Arguments**:

- `asset` (`str`): Asset name
- `accounts` (`str, list(str)`): Optional comma separated list of accounts to filter a response.
- `transaction_hashes` (`str, list(str)`): Optional comma separated list of transaction hashes to filter a response.
- `block_hashes` (`str, list(str)`): Optional comma separated list of block hashes to filter a response.
- `page_size` (`int`): number of items returned per page when calling the API. If the request times out, try using a smaller number.
- `paging_from` (`PagingFrom, str`): Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
- `start_time` (`datetime, date, str`): Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `end_time` (`datetime, date, str`): End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `start_inclusive` (`bool`): Flag to define if start timestamp must be included in the timeseries if present. True by default.
- `end_inclusive` (`bool`): Flag to define if end timestamp must be included in the timeseries if present. True by default.
- `timezone` (`str`): timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.

**Returns**:

`DataCollection`: list of balance updates

<a name="coinmetrics.api_client.CoinMetricsClient.get_full_block"></a>
#### get\_full\_block

```python
 | get_full_block(asset: str, block_hash: str) -> List[Dict[str, Any]]
```

Returns a full blockchain block with all transactions and balance updates.

**Arguments**:

- `asset` (`str`): Asset name
- `block_hash` (`str`): block hash

**Returns**:

`list(dict(str), any)`: blockchain block data

<a name="coinmetrics.api_client.CoinMetricsClient.get_full_transaction"></a>
#### get\_full\_transaction

```python
 | get_full_transaction(asset: str, transaction_hash: str) -> List[Dict[str, Any]]
```

Returns a full blockchain transaction with all balance updates.

**Arguments**:

- `asset` (`str`): Asset name
- `transaction_hash` (`str`): transaction hash

**Returns**:

`list(dict(str), any)`: block transaction data

<a name="coinmetrics.api_client.CoinMetricsClient.get_full_transaction_for_block"></a>
#### get\_full\_transaction\_for\_block

```python
 | get_full_transaction_for_block(asset: str, block_hash: str, transaction_hash: str) -> List[Dict[str, Any]]
```

Returns a full blockchain transaction with all balance updates for a specific block.

**Arguments**:

- `asset` (`str`): Asset name
- `block_hash` (`str`): block hash
- `transaction_hash` (`str`): transaction hash

**Returns**:

`list(dict(str, Any))`: block transaction data with balance updates

<a name="coinmetrics.api_client.CoinMetricsClient.get_transaction_tracker"></a>
#### get\_transaction\_tracker

```python
 | get_transaction_tracker(asset: str, txids: Optional[Union[List[str], str]] = None, replacements_for_txids: Optional[Union[List[str], str]] = None, replacements_only: Optional[bool] = None, page_size: Optional[int] = None, paging_from: Optional[Union[PagingFrom, str]] = None, start_time: Optional[Union[datetime, date, str]] = None, end_time: Optional[Union[datetime, date, str]] = None, start_inclusive: Optional[bool] = None, end_inclusive: Optional[bool] = None, timezone: Optional[str] = None) -> DataCollection
```

Returns status updates for the specified or all transactions.

**Arguments**:

- `asset` (`str`): Asset name
- `txids` (`str, list(str)`): Optional comma separated list of transaction identifiers (txid) to track.
- `replacements_for_txids` (`str, list(str)`): Optional comma separated list of transaction identifiers (txid) to get the corresponding replacement transactions for. Mutually exclusive with txids.
- `replacements_only` (`bool`): Boolean indicating if the response should contain only the replacement transactions.
- `page_size` (`int`): number of items returned per page when calling the API. If the request times out, try using a smaller number.
- `paging_from` (`PagingFrom, str`): Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
- `start_time` (`datetime, date, str`): Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `end_time` (`datetime, date, str`): End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `start_inclusive` (`bool`): Flag to define if start timestamp must be included in the timeseries if present. True by default.
- `end_inclusive` (`bool`): Flag to define if end timestamp must be included in the timeseries if present. True by default.
- `timezone` (`str`): timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.

**Returns**:

`DataCollection`: status updates for the specified or all transactions.

