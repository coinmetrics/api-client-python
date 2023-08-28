<a id="coinmetrics.api_client"></a>

# coinmetrics.api\_client

<a id="coinmetrics.api_client.CoinMetricsClient"></a>

## CoinMetricsClient Objects

```python
class CoinMetricsClient()
```

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_assets"></a>

#### catalog\_assets

```python
def catalog_assets(
        assets: Optional[Union[List[str], str]] = None,
        include: Optional[Union[List[str], str]] = None,
        exclude: Optional[Union[List[str], str]] = None) -> CatalogAssetsData
```

Returns meta information about _available_ assets.

**Arguments**:

- `assets` (`list(str), str`): A single asset or a list of assets to return info for. If no assets provided, all available assets are returned.
- `include` (`list(str), str`): list of fields to include in response. Supported values are metrics, markets, exchanges. Included by default if omitted.
- `exclude` (`list(str), str`): list of fields to include in response. Supported values are metrics, markets, exchanges. Included by default if omitted.

**Returns**:

`list(dict(str, any))`: Information that is available for requested assets, like: Full name, metrics and available frequencies, markets, exchanges, etc.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_asset_alerts"></a>

#### catalog\_asset\_alerts

```python
def catalog_asset_alerts(
        assets: Optional[Union[str, List[str]]] = None,
        alerts: Optional[Union[str,
                               List[str]]] = None) -> CatalogAssetAlertsData
```

**Arguments**:

- `assets` (`Union[str, List[str]]`): Comma separated list of assets. By default all assets are returned.
- `alerts` (`Union[str, List[str]]`): Comma separated list of asset alert names. By default all asset alerts are returned.

**Returns**:

`CatalogAssetAlertsData`: List of asset alerts.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_asset_chains"></a>

#### catalog\_asset\_chains

```python
def catalog_asset_chains(
        assets: Optional[Union[str,
                               List[str]]] = None) -> CatalogAssetChainsData
```

**Arguments**:

- `assets` (`Optional[Union[str, List[str]]]`): Comma separated list of assets. By default all assets are returned.

**Returns**:

`CatalogAssetChainsData`: List of asset chains assets

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_mempool_feerates"></a>

#### catalog\_mempool\_feerates

```python
def catalog_mempool_feerates(
    assets: Optional[Union[str,
                           List[str]]] = None) -> CatalogMempoolFeeratesData
```

**Arguments**:

- `assets` (`Optional[Union[str, List[str]]]`): Comma separated list of assets. By default all assets are returned.

**Returns**:

`CatalogMempoolFeeratesData`: List of mempool feerates assets

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_mining_pool_tips_summaries"></a>

#### catalog\_mining\_pool\_tips\_summaries

```python
def catalog_mining_pool_tips_summaries(
    assets: Optional[Union[str,
                           List[str]]] = None) -> CatalogMiningPoolTipsData
```

**Arguments**:

- `assets` (`Optional[Union[str, List[str]]]`): Comma separated list of assets. By default all assets are returned.

**Returns**:

`CatalogMiningPoolTipsData`: List of mining pool tips assets

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_transaction_tracker_assets"></a>

#### catalog\_transaction\_tracker\_assets

```python
def catalog_transaction_tracker_assets(
    assets: Optional[Union[str, List[str]]] = None
) -> CatalogTransactionTrackerData
```

**Arguments**:

- `assets` (`Optional[Union[str, List[str]]]`): Comma separated list of assets. By default all assets are returned.

**Returns**:

`CatalogTransactionTrackerData`: List of transaction tracker assets

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_asset_pairs"></a>

#### catalog\_asset\_pairs

```python
def catalog_asset_pairs(
    asset_pairs: Optional[Union[List[str],
                                str]] = None) -> CatalogAssetPairsData
```

Returns meta information about _available_ asset-asset pairs

**Arguments**:

- `asset_pairs` (`list(str), str`): A single asset-asset pair (e.g. "btc-eth") or a list of asset-asset pairs to return info for. If none are provided, all available pairs are returned.

**Returns**:

`list(dict(str, any))`: Information that is available for requested asset-asset pair like metrics and their respective frequencies and time ranges

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_asset_metrics"></a>

#### catalog\_asset\_metrics

```python
def catalog_asset_metrics(
        metrics: Optional[Union[List[str], str]] = None,
        reviewable: Optional[bool] = None) -> CatalogMetricsData
```

Returns list of _available_ asset metrics along with information for them like

description, category, precision and assets for which a metric is available.

**Arguments**:

- `metrics` (`list(str), str`): A single asset metric name or a list of metrics to return info for. If no metrics provided, all available metrics are returned.
- `reviewable` (`bool`): Show only reviewable or non-reviewable by human metrics. By default all metrics are shown.

**Returns**:

`list(dict(str, any))`: Information about asset metrics that correspond to a filter along with meta information like: description, category, precision and assets for which a metric is available.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_exchange_metrics"></a>

#### catalog\_exchange\_metrics

```python
def catalog_exchange_metrics(
        metrics: Optional[Union[List[str], str]] = None,
        reviewable: Optional[bool] = None) -> CatalogMetricsData
```

Returns list of _available_ exchange metrics along with information for them like

description, category, precision and assets for which a metric is available.

**Arguments**:

- `metrics` (`list(str), str`): A single exchange metric name or a list of metrics to return info for. If no metrics provided, all available metrics are returned.
- `reviewable` (`bool`): Show only reviewable or non-reviewable by human metrics. By default all metrics are shown.

**Returns**:

`list(dict(str, any))`: Information about exchange metrics that correspond to a filter along with meta information like: description, category, precision and assets for which a metric is available.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_exchange_asset_metrics"></a>

#### catalog\_exchange\_asset\_metrics

```python
def catalog_exchange_asset_metrics(
        metrics: Optional[Union[List[str], str]] = None,
        reviewable: Optional[bool] = None) -> CatalogExchangeAssetMetricsData
```

Returns list of _available_ exchange metrics along with information for them like

description, category, precision and assets for which a metric is available.

**Arguments**:

- `metrics` (`list(str), str`): A single exchange metric name or a list of metrics to return info for. If no metrics provided, all available metrics are returned.
- `reviewable` (`bool`): Show only reviewable or non-reviewable by human metrics. By default all metrics are shown.

**Returns**:

`list(dict(str, any))`: Information about exchange metrics that correspond to a filter along with meta information like: description, category, precision and assets for which a metric is available.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_pair_metrics"></a>

#### catalog\_pair\_metrics

```python
def catalog_pair_metrics(
        metrics: Optional[Union[List[str], str]] = None,
        reviewable: Optional[bool] = None) -> CatalogPairMetricsData
```

Returns list of _available_ pair metrics along with information for them like

description, category, precision and assets for which a metric is available.

**Arguments**:

- `metrics` (`list(str), str`): A single pair metric name or a list of metrics to return info for. If no metrics provided, all available metrics are returned.
- `reviewable` (`bool`): Show only reviewable or non-reviewable by human metrics. By default all metrics are shown.

**Returns**:

`list(dict(str, any))`: Information about pair metrics that correspond to a filter along with meta information like: description, category, precision and assets for which a metric is available.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_institution_metrics"></a>

#### catalog\_institution\_metrics

```python
def catalog_institution_metrics(
        metrics: Optional[Union[List[str], str]] = None,
        reviewable: Optional[bool] = None) -> CatalogInstitutionMetricsData
```

Returns list of _available_ institution metrics along with information for them like

description, category, precision and assets for which a metric is available.

**Arguments**:

- `metrics` (`list(str), str`): A single institution metric name or a list of metrics to return info for. If no metrics provided, all available metrics are returned.
- `reviewable` (`bool`): Show only reviewable or non-reviewable by human metrics. By default all metrics are shown.

**Returns**:

`list(dict(str, any))`: Information about institution metrics that correspond to a filter along with meta information like: description, category, precision and assets for which a metric is available.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_asset_pair_candles"></a>

#### catalog\_asset\_pair\_candles

```python
def catalog_asset_pair_candles(
    asset_pairs: Optional[Union[List[str], str]] = None
) -> CatalogAssetPairCandlesData
```

Returns meta information about _available_ asset-asset pairs

**Arguments**:

- `asset_pairs` (`list(str), str`): A single asset-asset pair (e.g. "btc-eth") or a list of asset-asset pairs to return info for. If none are provided, all available pairs are returned.

**Returns**:

`list(dict(str, any))`: Returns a list of available asset pair candles along with the time ranges of available data per candle duration.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_exchanges"></a>

#### catalog\_exchanges

```python
def catalog_exchanges(
        exchanges: Optional[Union[List[str],
                                  str]] = None) -> CatalogExchangesData
```

Returns meta information about exchanges.

**Arguments**:

- `exchanges` (`list(str), str`): A single exchange name or a list of exchanges to return info for. If no exchanges provided, all available exchanges are returned.

**Returns**:

`list(dict(str, any))`: Information that is available for requested exchanges, like: markets, min and max time available.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_exchange_assets"></a>

#### catalog\_exchange\_assets

```python
def catalog_exchange_assets(
    exchange_assets: Optional[Union[List[str], str]] = None
) -> CatalogExchangeAssetsData
```

Returns meta information about _available_ exchange-asset pairs

**Arguments**:

- `exchange_assets` (`list(str), str`): A single exchange-asset pair (e.g. "binance-btc") or a list of exchange-asset pairs to return info for. If none are provided, all available pairs are returned.

**Returns**:

`list(dict(str, any))`: Information that is available for requested exchange-asset pair like metrics and their respective frequencies and time ranges

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_indexes"></a>

#### catalog\_indexes

```python
def catalog_indexes(
        indexes: Optional[Union[List[str], str]] = None) -> CatalogIndexesData
```

Returns meta information about _available_ indexes.

**Arguments**:

- `indexes` (`list(str), str`): A single index name or a list of indexes to return info for. If no indexes provided, all available indexes are returned.

**Returns**:

`list(dict(str, any))`: Information that is available for requested indexes, like: Full name, and available frequencies.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_index_candles"></a>

#### catalog\_index\_candles

```python
def catalog_index_candles(
    indexes: Optional[Union[List[str],
                            str]] = None) -> CatalogMarketCandlesData
```

Returns meta information about _available_ index candles.

**Arguments**:

- `indexes` (`list(str), str`): A single index name or a list of indexes to return info for. If no indexes provided, all available index candles are returned.

**Returns**:

`list(dict(str, any))`: Information that is available for requested index candles, like: Full name, and available frequencies.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_institutions"></a>

#### catalog\_institutions

```python
def catalog_institutions(
    institutions: Optional[Union[List[str], str]] = None
) -> CatalogInstitutionsData
```

Returns meta information about _available_ institutions

**Arguments**:

- `institutions` (`list(str), str`): A single institution (e.g. "grayscale") or a list of institutions to return info for. If none are provided, all available pairs are returned.

**Returns**:

`list(dict(str, any))`: Information that is available for requested institution like metrics and their respective frequencies and time ranges.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_markets"></a>

#### catalog\_markets

```python
def catalog_markets(
        markets: Optional[Union[List[str], str]] = None,
        market_type: Optional[str] = None,
        exchange: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None,
        include: Optional[Union[List[str], str]] = None,
        exclude: Optional[Union[List[str], str]] = None) -> CatalogMarketsData
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
- `include` (`list(str), str`): list of fields to include in response. Supported values are trades, orderbooks,
quotes, funding_rates, openinterest, liquidations. Included by default if omitted.
- `exclude` (`list(str), str`): list of fields to exclude from response. Supported values are trades, orderbooks,
quotes, funding_rates, openinterest, liquidations. Included by default if omitted.

**Returns**:

`list(dict(str, any))`: Information about markets that correspond to a filter along with meta information like: type of market and min and max available time frames.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_market_trades"></a>

#### catalog\_market\_trades

```python
def catalog_market_trades(
        markets: Optional[Union[List[str], str]] = None,
        market_type: Optional[str] = None,
        exchange: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None) -> CatalogMarketTradesData
```

Returns a list of markets with trades support along with the time ranges of available data.

**Arguments**:

- `markets` (`list(str), str`): list of market names, e.g. 'coinbase-btc-usd-spot'
- `market_type` (`str`): Type of market: "spot", "future", "option"
- `exchange` (`str`): name of the exchange
- `base` (`str`): name of base asset
- `quote` (`str`): name of quote asset
- `asset` (`str`): name of either base or quote asset
- `symbol` (`str`): name of a symbol. Usually used for futures contracts.

**Returns**:

`list(dict(str, any))`: Information about market trades that are available for the provided filter, as well as the time frames they are available

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_metrics"></a>

#### catalog\_metrics

```python
def catalog_metrics(metrics: Optional[Union[List[str], str]] = None,
                    reviewable: Optional[bool] = None) -> CatalogMetricsData
```

Returns list of _available_ metrics along with information for them like

description, category, precision and assets for which a metric is available.

**Arguments**:

- `metrics` (`list(str), str`): A single metric name or a list of metrics to return info for. If no metrics provided, all available metrics are returned.
- `reviewable` (`bool`): Show only reviewable or non-reviewable by human metrics. By default all metrics are shown.

**Returns**:

`list(dict(str, any))`: Information about metrics that correspond to a filter along with meta information like: description, category, precision and assets for which a metric is available.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_market_metrics"></a>

#### catalog\_market\_metrics

```python
def catalog_market_metrics(
        markets: Optional[Union[List[str], str]] = None,
        market_type: Optional[str] = None,
        exchange: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None) -> CatalogMarketMetricsData
```

Returns list of _available_ markets with metrics support along woth time ranges of available data per metric.

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

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_market_candles"></a>

#### catalog\_market\_candles

```python
def catalog_market_candles(
        markets: Optional[Union[List[str], str]] = None,
        market_type: Optional[str] = None,
        exchange: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None) -> CatalogMarketCandlesData
```

Returns list of _available_ markets with candles support along woth time ranges of available data per metric.

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

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_market_orderbooks"></a>

#### catalog\_market\_orderbooks

```python
def catalog_market_orderbooks(
        markets: Optional[Union[List[str], str]] = None,
        market_type: Optional[str] = None,
        exchange: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None) -> CatalogMarketOrderbooksData
```

Returns a list of markets with orderbooks support along with the time ranges of available data.

**Arguments**:

- `markets` (`list(str), str`): list of market names, e.g. 'coinbase-btc-usd-spot'
- `market_type` (`str`): Type of market: "spot", "future", "option"
- `exchange` (`str`): name of the exchange
- `base` (`str`): name of base asset
- `quote` (`str`): name of quote asset
- `asset` (`str`): name of either base or quote asset
- `symbol` (`str`): name of a symbol. Usually used for futures contracts.

**Returns**:

`list(dict(str, any))`: Information about markets orderbooks that correspond to a filter

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_market_quotes"></a>

#### catalog\_market\_quotes

```python
def catalog_market_quotes(
        markets: Optional[Union[List[str], str]] = None,
        market_type: Optional[str] = None,
        exchange: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None) -> CatalogMarketTradesData
```

Returns a list of markets with quotes support along with the time ranges of available data.

**Arguments**:

- `markets` (`list(str), str`): list of market names, e.g. 'coinbase-btc-usd-spot'
- `market_type` (`str`): Type of market: "spot", "future", "option"
- `exchange` (`str`): name of the exchange
- `base` (`str`): name of base asset
- `quote` (`str`): name of quote asset
- `asset` (`str`): name of either base or quote asset
- `symbol` (`str`): name of a symbol. Usually used for futures contracts.

**Returns**:

`list(dict(str, any))`: Information about markets quotes that correspond to a filter

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_market_funding_rates"></a>

#### catalog\_market\_funding\_rates

```python
def catalog_market_funding_rates(
        markets: Optional[Union[List[str], str]] = None,
        market_type: Optional[str] = None,
        exchange: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None) -> CatalogMarketTradesData
```

Returns a list of markets with funding rates support along with the time ranges of available data.

**Arguments**:

- `markets` (`list(str), str`): list of market names, e.g. 'coinbase-btc-usd-spot'
- `market_type` (`str`): Type of market: "spot", "future", "option"
- `exchange` (`str`): name of the exchange
- `base` (`str`): name of base asset
- `quote` (`str`): name of quote asset
- `asset` (`str`): name of either base or quote asset
- `symbol` (`str`): name of a symbol. Usually used for futures contracts.

**Returns**:

`list(dict(str, any))`: Information about funding rates that correspond to a filter

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_market_contract_prices"></a>

#### catalog\_market\_contract\_prices

```python
def catalog_market_contract_prices(
        markets: Optional[Union[str, List[str]]] = None,
        exchange: Optional[str] = None,
        type: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None,
        format: Optional[str] = None,
        limit: Optional[str] = None) -> CatalogMarketContractPrices
```

**Arguments**:

- `markets` (`Optional[Union[str, List[str]]]`): Comma separated list of markets. By default all markets are returned.
- `exchange` (`Optional[str]`): Unique name of an exchange.
- `type` (`Optional[str]`): Type of markets.
- `base` (`Optional[str]`): Base asset of markets.
- `quote` (`Optional[str]`): Quote asset of markets.
- `asset` (`Optional[str]`): Any asset of markets.
- `symbol` (`Optional[str]`): Symbol of derivative markets, full instrument name.
- `format` (`Optional[str]`): Format of the response. Supported values are `json`, `json_stream`.
- `limit` (`Optional[str]`): Limit of response items. `none` means no limit.

**Returns**:

`CatalogMarketContractPrices`: List of contract prices statistics.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_market_implied_volatility"></a>

#### catalog\_market\_implied\_volatility

```python
def catalog_market_implied_volatility(
        markets: Optional[Union[str, List[str]]] = None,
        exchange: Optional[str] = None,
        type: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None,
        format: Optional[str] = None,
        limit: Optional[str] = None) -> CatalogMarketImpliedVolatility
```

**Arguments**:

- `markets` (`Optional[Union[str, List[str]]]`): Comma separated list of markets. By default all markets are returned.
- `exchange` (`Optional[str]`): Unique name of an exchange.
- `type` (`Optional[str]`): Type of markets.
- `base` (`Optional[str]`): Base asset of markets.
- `quote` (`Optional[str]`): Quote asset of markets.
- `asset` (`Optional[str]`): Any asset of markets.
- `symbol` (`Optional[str]`): Symbol of derivative markets, full instrument name.
- `format` (`Optional[str]`): Format of the response. Supported values are `json`, `json_stream`.
- `limit` (`Optional[str]`): Limit of response items. `none` means no limit.

**Returns**:

`CatalogMarketImpliedVolatility`: List of implied volatility statistics.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_market_greeks"></a>

#### catalog\_market\_greeks

```python
def catalog_market_greeks(
        markets: Optional[Union[List[str], str]] = None,
        market_type: Optional[str] = None,
        exchange: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None) -> CatalogMarketTradesData
```

Returns a list of markets with greeks support along with the time ranges of available data.

**Arguments**:

- `markets` (`list(str), str`): list of market names, e.g. 'coinbase-btc-usd-spot'
- `market_type` (`str`): Type of market: "spot", "future", "option"
- `exchange` (`str`): name of the exchange
- `base` (`str`): name of base asset
- `quote` (`str`): name of quote asset
- `asset` (`str`): name of either base or quote asset
- `symbol` (`str`): name of a symbol. Usually used for futures contracts.

**Returns**:

`list(dict(str, any))`: Information about market greeks that correspond to the filter

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_market_open_interest"></a>

#### catalog\_market\_open\_interest

```python
def catalog_market_open_interest(
        markets: Optional[Union[List[str], str]] = None,
        market_type: Optional[str] = None,
        exchange: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None) -> CatalogMarketTradesData
```

Returns a list of markets with open interest support along with the time ranges of available data.

**Arguments**:

- `markets` (`list(str), str`): list of market names, e.g. 'coinbase-btc-usd-spot'
- `market_type` (`str`): Type of market: "spot", "future", "option"
- `exchange` (`str`): name of the exchange
- `base` (`str`): name of base asset
- `quote` (`str`): name of quote asset
- `asset` (`str`): name of either base or quote asset
- `symbol` (`str`): name of a symbol. Usually used for futures contracts.

**Returns**:

`list(dict(str, any))`: Information about market open interest that correspond to a filter

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_market_liquidations"></a>

#### catalog\_market\_liquidations

```python
def catalog_market_liquidations(
        markets: Optional[Union[List[str], str]] = None,
        market_type: Optional[str] = None,
        exchange: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None) -> CatalogMarketTradesData
```

Returns a list of markets with liquidations support along with the time ranges of available data.

**Arguments**:

- `markets` (`list(str), str`): list of market names, e.g. 'coinbase-btc-usd-spot'
- `market_type` (`str`): Type of market: "spot", "future", "option"
- `exchange` (`str`): name of the exchange
- `base` (`str`): name of base asset
- `quote` (`str`): name of quote asset
- `asset` (`str`): name of either base or quote asset
- `symbol` (`str`): name of a symbol. Usually used for futures contracts.

**Returns**:

`list(dict(str, any))`: Information about market liquidations that correspond to a filter

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_full_assets"></a>

#### catalog\_full\_assets

```python
def catalog_full_assets(
        assets: Optional[Union[List[str], str]] = None,
        include: Optional[Union[List[str], str]] = None,
        exclude: Optional[Union[List[str], str]] = None) -> CatalogAssetsData
```

Returns meta information about _supported_ assets.

**Arguments**:

- `assets` (`list(str), str`): A single asset or a list of assets to return info for. If no assets provided, all supported assets are returned.
- `include` (`list(str), str`): list of fields to include in response. Supported values are metrics, markets,
exchanges. Included by default if omitted.
- `exclude` (`list(str), str`): list of fields to exclude from response. Supported values are metrics, markets,
exchanges. Included by default if omitted.

**Returns**:

`list(dict(str, any))`: Information that is supported for requested assets, like: Full name, metrics and supported frequencies, markets, exchanges, etc.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_full_asset_metrics"></a>

#### catalog\_full\_asset\_metrics

```python
def catalog_full_asset_metrics(
        metrics: Optional[Union[List[str], str]] = None,
        reviewable: Optional[bool] = None) -> CatalogMetricsData
```

Returns list of all _available_ asset metrics along with information for them like

description, category, precision and assets for which a metric is available.

**Arguments**:

- `metrics` (`list(str), str`): A single asset metric name or a list of metrics to return info for. If no metrics provided, all available metrics are returned.
- `reviewable` (`bool`): Show only reviewable or non-reviewable by human metrics. By default all metrics are shown.

**Returns**:

`list(dict(str, any))`: Information about asset metrics that correspond to a filter along with meta information like: description, category, precision and assets for which a metric is available.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_full_asset_alerts"></a>

#### catalog\_full\_asset\_alerts

```python
def catalog_full_asset_alerts(
        assets: Optional[Union[str, List[str]]] = None,
        alerts: Optional[Union[str,
                               List[str]]] = None) -> CatalogAssetAlertsData
```

**Arguments**:

- `assets` (`Union[str, List[str]]`): Comma separated list of assets. By default all assets are returned.
- `alerts` (`Union[str, List[str]]`): Comma separated list of asset alert names. By default all asset alerts are returned.

**Returns**:

`CatalogAssetAlertsData`: List of asset alerts.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_full_asset_chains"></a>

#### catalog\_full\_asset\_chains

```python
def catalog_full_asset_chains(
        assets: Optional[Union[str,
                               List[str]]] = None) -> CatalogAssetChainsData
```

**Arguments**:

- `assets` (`Optional[Union[str, List[str]]]`): Comma separated list of assets. By default all assets are returned.

**Returns**:

`CatalogAssetChainsData`: List of asset chains assets

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_full_mempool_feerates"></a>

#### catalog\_full\_mempool\_feerates

```python
def catalog_full_mempool_feerates(
    assets: Optional[Union[str,
                           List[str]]] = None) -> CatalogMempoolFeeratesData
```

**Arguments**:

- `assets` (`Optional[Union[str, List[str]]]`): Comma separated list of assets. By default all assets are returned.

**Returns**:

`CatalogMempoolFeeratesData`: List of mempool feerates assets

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_full_mining_pool_tips_summaries"></a>

#### catalog\_full\_mining\_pool\_tips\_summaries

```python
def catalog_full_mining_pool_tips_summaries(
    assets: Optional[Union[str,
                           List[str]]] = None) -> CatalogMiningPoolTipsData
```

**Arguments**:

- `assets` (`Optional[Union[str, List[str]]]`): Comma separated list of assets. By default all assets are returned.

**Returns**:

`CatalogMiningPoolTipsData`: List of mining pool tips assets

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_full_transaction_tracker_assets"></a>

#### catalog\_full\_transaction\_tracker\_assets

```python
def catalog_full_transaction_tracker_assets(
    assets: Optional[Union[str, List[str]]] = None
) -> CatalogTransactionTrackerData
```

**Arguments**:

- `assets` (`Optional[Union[str, List[str]]]`): Comma separated list of assets. By default all assets are returned.

**Returns**:

`CatalogTransactionTrackerData`: List of transaction tracker assets

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_full_asset_pairs"></a>

#### catalog\_full\_asset\_pairs

```python
def catalog_full_asset_pairs(
    asset_pairs: Optional[Union[List[str],
                                str]] = None) -> CatalogAssetPairsData
```

Returns meta information about _supported_ asset-asset pairs

**Arguments**:

- `asset_pairs` (`list(str), str`): A single asset-asset pair (e.g. "btc-eth") or a list of asset-asset pairs to return info for. If none are provided, all supported pairs are returned.

**Returns**:

`list(dict(str, any))`: Information that is supported for requested asset-asset pair like metrics and their respective frequencies and time ranges

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_full_pair_metrics"></a>

#### catalog\_full\_pair\_metrics

```python
def catalog_full_pair_metrics(
        metrics: Optional[Union[List[str], str]] = None,
        reviewable: Optional[bool] = None) -> CatalogPairMetricsData
```

Returns list of all _available_ pair metrics along with information for them like

description, category, precision and assets for which a metric is available.

**Arguments**:

- `metrics` (`list(str), str`): A single pair metric name or a list of metrics to return info for. If no metrics provided, all available metrics are returned.
- `reviewable` (`bool`): Show only reviewable or non-reviewable by human metrics. By default all metrics are shown.

**Returns**:

`list(dict(str, any))`: Information about pair metrics that correspond to a filter along with meta information like: description, category, precision and assets for which a metric is available.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_full_institution_metrics"></a>

#### catalog\_full\_institution\_metrics

```python
def catalog_full_institution_metrics(
        metrics: Optional[Union[List[str], str]] = None,
        reviewable: Optional[bool] = None) -> CatalogInstitutionMetricsData
```

Returns list of _available_ institution metrics along with information for them like

description, category, precision and assets for which a metric is available.

**Arguments**:

- `metrics` (`list(str), str`): A single institution metric name or a list of metrics to return info for. If no metrics provided, all available metrics are returned.
- `reviewable` (`bool`): Show only reviewable or non-reviewable by human metrics. By default all metrics are shown.

**Returns**:

`list(dict(str, any))`: Information about institution metrics that correspond to a filter along with meta information like: description, category, precision and assets for which a metric is available.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_full_asset_pair_candles"></a>

#### catalog\_full\_asset\_pair\_candles

```python
def catalog_full_asset_pair_candles(
    asset_pairs: Optional[Union[List[str], str]] = None
) -> CatalogAssetPairCandlesData
```

Returns meta information about _available_ asset-asset pairs

**Arguments**:

- `asset_pairs` (`list(str), str`): A single asset-asset pair (e.g. "btc-eth") or a list of asset-asset pairs to return info for. If none are provided, all available pairs are returned.

**Returns**:

`list(dict(str, any))`: Returns a list of available asset pair candles along with the time ranges of available data per candle duration.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_full_exchanges"></a>

#### catalog\_full\_exchanges

```python
def catalog_full_exchanges(
        exchanges: Optional[Union[List[str],
                                  str]] = None) -> CatalogExchangesData
```

Returns meta information about exchanges.

**Arguments**:

- `exchanges` (`list(str), str`): A single exchange name or a list of exchanges to return info for. If no exchanges provided,
all supported exchanges are returned.

**Returns**:

`list(dict(str, any))`: Information that is supported for requested exchanges, like: markets, min and max time supported.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_full_exchange_assets"></a>

#### catalog\_full\_exchange\_assets

```python
def catalog_full_exchange_assets(
    exchange_assets: Optional[Union[List[str], str]] = None
) -> CatalogExchangeAssetsData
```

Returns meta information about _supported_ exchange-asset pairs

**Arguments**:

- `exchange_assets` (`list(str), str`): A single exchange-asset pair (e.g. "binance-btc") or a list of exchange-asset pairs to return info for. If none are provided, all supported pairs are returned.

**Returns**:

`list(dict(str, any))`: Information that is supported for requested exchange-asset pair like metrics and their respective frequencies and time ranges

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_full_exchange_metrics"></a>

#### catalog\_full\_exchange\_metrics

```python
def catalog_full_exchange_metrics(
        metrics: Optional[Union[List[str], str]] = None,
        reviewable: Optional[bool] = None) -> CatalogMetricsData
```

Returns list of all _available_ exchange metrics along with information for them like

description, category, precision and assets for which a metric is available.

**Arguments**:

- `metrics` (`list(str), str`): A single exchange metric name or a list of metrics to return info for. If no metrics provided, all available metrics are returned.
- `reviewable` (`bool`): Show only reviewable or non-reviewable by human metrics. By default all metrics are shown.

**Returns**:

`list(dict(str, any))`: Information about exchange metrics that correspond to a filter along with meta information like: description, category, precision and assets for which a metric is available.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_full_exchange_asset_metrics"></a>

#### catalog\_full\_exchange\_asset\_metrics

```python
def catalog_full_exchange_asset_metrics(
        metrics: Optional[Union[List[str], str]] = None,
        reviewable: Optional[bool] = None) -> CatalogExchangeAssetMetricsData
```

Returns list of _available_ exchange metrics along with information for them like

description, category, precision and assets for which a metric is available.

**Arguments**:

- `metrics` (`list(str), str`): A single exchange metric name or a list of metrics to return info for. If no metrics provided, all available metrics are returned.
- `reviewable` (`bool`): Show only reviewable or non-reviewable by human metrics. By default all metrics are shown.

**Returns**:

`list(dict(str, any))`: Information about exchange metrics that correspond to a filter along with meta information like: description, category, precision and assets for which a metric is available.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_full_indexes"></a>

#### catalog\_full\_indexes

```python
def catalog_full_indexes(
        indexes: Optional[Union[List[str], str]] = None) -> CatalogIndexesData
```

Returns meta information about _supported_ indexes.

**Arguments**:

- `indexes` (`list(str), str`): A single index name or a list of indexes to return info for. If no indexes provided, all supported indexes are returned.

**Returns**:

`list(dict(str, any))`: Information that is supported for requested indexes, like: Full name, and supported frequencies.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_full_index_candles"></a>

#### catalog\_full\_index\_candles

```python
def catalog_full_index_candles(
    indexes: Optional[Union[List[str],
                            str]] = None) -> CatalogMarketCandlesData
```

Returns meta information about _supported_ index candles.

**Arguments**:

- `indexes` (`list(str), str`): A single index name or a list of indexes to return info for. If no indexes provided, all supported indexes are returned.

**Returns**:

`list(dict(str, any))`: Information that is supported for requested index candles, like: Full name, and supported frequencies.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_full_institutions"></a>

#### catalog\_full\_institutions

```python
def catalog_full_institutions(
    institutions: Optional[Union[List[str], str]] = None
) -> CatalogInstitutionsData
```

Returns meta information about _supported_ institutions

**Arguments**:

- `institutions` (`list(str), str`): A single institution (e.g. "grayscale") or a list of institutions to return info for. If none are provided, all supported pairs are returned.

**Returns**:

`list(dict(str, any))`: Information that is supported for requested institution like metrics and their respective frequencies and time ranges.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_full_markets"></a>

#### catalog\_full\_markets

```python
def catalog_full_markets(markets: Optional[Union[List[str], str]] = None,
                         market_type: Optional[str] = None,
                         exchange: Optional[str] = None,
                         base: Optional[str] = None,
                         quote: Optional[str] = None,
                         asset: Optional[str] = None,
                         symbol: Optional[str] = None,
                         include: Optional[str] = None,
                         exclude: Optional[str] = None) -> CatalogMarketsData
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
- `include` (`list(str), str`): ist of fields to include in response. Supported values are trades, orderbooks, quotes,
funding_rates, openinterest, liquidations. Included by default if omitted.
- `exclude` (`list(str), str`): list of fields to exclude from response. Supported values are trades, orderbooks, quotes,
funding_rates, openinterest, liquidations. Included by default if omitted.

**Returns**:

`list(dict(str, any))`: Information about markets that correspond to a filter along with meta information like: type of market and min and max supported time frames.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_full_market_trades"></a>

#### catalog\_full\_market\_trades

```python
def catalog_full_market_trades(
        markets: Optional[Union[List[str], str]] = None,
        market_type: Optional[str] = None,
        exchange: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None) -> CatalogMarketTradesData
```

Returns a list of all markets with trades support along with the time ranges of available data.

**Arguments**:

- `markets` (`list(str), str`): list of market names, e.g. 'coinbase-btc-usd-spot'
- `market_type` (`str`): Type of market: "spot", "future", "option"
- `exchange` (`str`): name of the exchange
- `base` (`str`): name of base asset
- `quote` (`str`): name of quote asset
- `asset` (`str`): name of either base or quote asset
- `symbol` (`str`): name of a symbol. Usually used for futures contracts.

**Returns**:

`list(dict(str, any))`: Information about market trades that are available for the provided filter, as well as the time frames they are available

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_full_metrics"></a>

#### catalog\_full\_metrics

```python
def catalog_full_metrics(
        metrics: Optional[Union[List[str], str]] = None,
        reviewable: Optional[bool] = None) -> CatalogMetricsData
```

Returns list of _supported_ metrics along with information for them like

description, category, precision and assets for which a metric is supported.

**Arguments**:

- `metrics` (`list(str), str`): A single metric name or a list of metrics to return info for. If no metrics provided, all supported metrics are returned.
- `reviewable` (`bool`): Show only reviewable or non-reviewable by human metrics. By default all metrics are shown.

**Returns**:

`list(dict(str, any))`: Information about metrics that correspond to a filter along with meta information like: description, category, precision and assets for which a metric is supported.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_full_market_metrics"></a>

#### catalog\_full\_market\_metrics

```python
def catalog_full_market_metrics(
        markets: Optional[Union[List[str], str]] = None,
        market_type: Optional[str] = None,
        exchange: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None) -> CatalogMarketMetricsData
```

Returns list of _supported_ markets with metrics support along woth time ranges of available data per metric.

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

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_full_market_candles"></a>

#### catalog\_full\_market\_candles

```python
def catalog_full_market_candles(
        markets: Optional[Union[List[str], str]] = None,
        market_type: Optional[str] = None,
        exchange: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None) -> CatalogMarketCandlesData
```

Returns list of _available_ markets with candles support along woth time ranges of available data per metric.

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

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_full_market_orderbooks"></a>

#### catalog\_full\_market\_orderbooks

```python
def catalog_full_market_orderbooks(
        markets: Optional[Union[List[str], str]] = None,
        market_type: Optional[str] = None,
        exchange: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None) -> CatalogMarketTradesData
```

Returns a list of markets with orderbooks support along with the time ranges of available data.

**Arguments**:

- `markets` (`list(str), str`): list of market names, e.g. 'coinbase-btc-usd-spot'
- `market_type` (`str`): Type of market: "spot", "future", "option"
- `exchange` (`str`): name of the exchange
- `base` (`str`): name of base asset
- `quote` (`str`): name of quote asset
- `asset` (`str`): name of either base or quote asset
- `symbol` (`str`): name of a symbol. Usually used for futures contracts.

**Returns**:

`list(dict(str, any))`: Information about markets orderbooks that correspond to a filter

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_full_market_quotes"></a>

#### catalog\_full\_market\_quotes

```python
def catalog_full_market_quotes(
        markets: Optional[Union[List[str], str]] = None,
        market_type: Optional[str] = None,
        exchange: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None) -> CatalogMarketTradesData
```

Returns a list of markets with quotes support along with the time ranges of available data.

**Arguments**:

- `markets` (`list(str), str`): list of market names, e.g. 'coinbase-btc-usd-spot'
- `market_type` (`str`): Type of market: "spot", "future", "option"
- `exchange` (`str`): name of the exchange
- `base` (`str`): name of base asset
- `quote` (`str`): name of quote asset
- `asset` (`str`): name of either base or quote asset
- `symbol` (`str`): name of a symbol. Usually used for futures contracts.

**Returns**:

`list(dict(str, any))`: Information about markets quotes that correspond to a filter

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_full_market_funding_rates"></a>

#### catalog\_full\_market\_funding\_rates

```python
def catalog_full_market_funding_rates(
        markets: Optional[Union[List[str], str]] = None,
        market_type: Optional[str] = None,
        exchange: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None) -> CatalogMarketTradesData
```

Returns a list of all markets with funding rates support along with the time ranges of available data.

**Arguments**:

- `markets` (`list(str), str`): list of market names, e.g. 'coinbase-btc-usd-spot'
- `market_type` (`str`): Type of market: "spot", "future", "option"
- `exchange` (`str`): name of the exchange
- `base` (`str`): name of base asset
- `quote` (`str`): name of quote asset
- `asset` (`str`): name of either base or quote asset
- `symbol` (`str`): name of a symbol. Usually used for futures contracts.

**Returns**:

`list(dict(str, any))`: Information about funding rates that correspond to a filter

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_full_market_contract_prices"></a>

#### catalog\_full\_market\_contract\_prices

```python
def catalog_full_market_contract_prices(
        markets: Optional[Union[str, List[str]]] = None,
        exchange: Optional[str] = None,
        type: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None,
        format: Optional[str] = None,
        limit: Optional[str] = None) -> CatalogMarketContractPrices
```

**Arguments**:

- `markets` (`Optional[Union[str, List[str]]]`): Comma separated list of markets. By default all markets are returned.
- `exchange` (`Optional[str]`): Unique name of an exchange.
- `type` (`Optional[str]`): Type of markets.
- `base` (`Optional[str]`): Base asset of markets.
- `quote` (`Optional[str]`): Quote asset of markets.
- `asset` (`Optional[str]`): Any asset of markets.
- `symbol` (`Optional[str]`): Symbol of derivative markets, full instrument name.
- `format` (`Optional[str]`): Format of the response. Supported values are `json`, `json_stream`.
- `limit` (`Optional[str]`): Limit of response items. `none` means no limit.

**Returns**:

`CatalogMarketContractPrices`: List of contract prices statistics.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_full_contract_prices_v2"></a>

#### catalog\_full\_contract\_prices\_v2

```python
def catalog_full_contract_prices_v2(
        markets: Optional[Union[str, List[str]]] = None,
        exchange: Optional[str] = None,
        market_type: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None,
        format: Optional[str] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[str] = None,
        next_page_token: Optional[str] = None) -> CatalogV2DataCollection
```

**Arguments**:

- `markets` (`Optional[Union[str, List[str]]]`): Comma separated list of markets. By default all markets are returned.
- `exchange` (`Optional[str]`): Unique name of an exchange.
- `market_type` (`Optional[str]`): Type of markets.
- `base` (`Optional[str]`): Base asset of markets.
- `quote` (`Optional[str]`): Quote asset of markets.
- `asset` (`Optional[str]`): Any asset of markets.
- `symbol` (`Optional[str]`): Symbol of derivative markets, full instrument name.
- `format` (`Optional[str]`): Format of the response. Supported values are `json`, `json_stream`.
- `page_size` (`Optional[int]`): Number of items per single page of results.
- `paging_from` (`Optional[str]`): Where does the first page start, at the start of the interval or at the end.
- `next_page_token` (`Optional[str]`): Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.

**Returns**:

`CatalogV2DataCollection`: List of contract prices statistics.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_full_market_implied_volatility"></a>

#### catalog\_full\_market\_implied\_volatility

```python
def catalog_full_market_implied_volatility(
        markets: Optional[Union[str, List[str]]] = None,
        exchange: Optional[str] = None,
        type: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None,
        format: Optional[str] = None,
        limit: Optional[str] = None) -> CatalogMarketImpliedVolatility
```

**Arguments**:

- `markets` (`Optional[Union[str, List[str]]]`): Comma separated list of markets. By default all markets are returned.
- `exchange` (`Optional[str]`): Unique name of an exchange.
- `type` (`Optional[str]`): Type of markets.
- `base` (`Optional[str]`): Base asset of markets.
- `quote` (`Optional[str]`): Quote asset of markets.
- `asset` (`Optional[str]`): Any asset of markets.
- `symbol` (`Optional[str]`): Symbol of derivative markets, full instrument name.
- `format` (`Optional[str]`): Format of the response. Supported values are `json`, `json_stream`.
- `limit` (`Optional[str]`): Limit of response items. `none` means no limit.

**Returns**:

`CatalogMarketImpliedVolatility`: List of implied volatility statistics.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_full_market_greeks"></a>

#### catalog\_full\_market\_greeks

```python
def catalog_full_market_greeks(
        markets: Optional[Union[List[str], str]] = None,
        market_type: Optional[str] = None,
        exchange: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None) -> CatalogMarketTradesData
```

Returns a list of all markets with greeks support along with the time ranges of available data.

**Arguments**:

- `markets` (`list(str), str`): list of market names, e.g. 'coinbase-btc-usd-spot'
- `market_type` (`str`): Type of market: "spot", "future", "option"
- `exchange` (`str`): name of the exchange
- `base` (`str`): name of base asset
- `quote` (`str`): name of quote asset
- `asset` (`str`): name of either base or quote asset
- `symbol` (`str`): name of a symbol. Usually used for futures contracts.

**Returns**:

`list(dict(str, any))`: Information about market greeks that correspond to the filter

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_full_market_open_interest"></a>

#### catalog\_full\_market\_open\_interest

```python
def catalog_full_market_open_interest(
        markets: Optional[Union[List[str], str]] = None,
        market_type: Optional[str] = None,
        exchange: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None) -> CatalogMarketTradesData
```

Returns a list of markets with open interest support along with the time ranges of available data.

**Arguments**:

- `markets` (`list(str), str`): list of market names, e.g. 'coinbase-btc-usd-spot'
- `market_type` (`str`): Type of market: "spot", "future", "option"
- `exchange` (`str`): name of the exchange
- `base` (`str`): name of base asset
- `quote` (`str`): name of quote asset
- `asset` (`str`): name of either base or quote asset
- `symbol` (`str`): name of a symbol. Usually used for futures contracts.

**Returns**:

`list(dict(str, any))`: Information about market open interest that correspond to a filter

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_full_market_liquidations"></a>

#### catalog\_full\_market\_liquidations

```python
def catalog_full_market_liquidations(
        markets: Optional[Union[List[str], str]] = None,
        market_type: Optional[str] = None,
        exchange: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None) -> CatalogMarketTradesData
```

Returns a list of all markets with liquidations support along with the time ranges of available data.

**Arguments**:

- `markets` (`list(str), str`): list of market names, e.g. 'coinbase-btc-usd-spot'
- `market_type` (`str`): Type of market: "spot", "future", "option"
- `exchange` (`str`): name of the exchange
- `base` (`str`): name of base asset
- `quote` (`str`): name of quote asset
- `asset` (`str`): name of either base or quote asset
- `symbol` (`str`): name of a symbol. Usually used for futures contracts.

**Returns**:

`list(dict(str, any))`: Information about market liquidations that correspond to a filter

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_market_trades_v2"></a>

#### catalog\_market\_trades\_v2

```python
def catalog_market_trades_v2(
        markets: Optional[Union[str, List[str]]] = None,
        exchange: Optional[str] = None,
        market_type: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None,
        format: Optional[str] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[str] = None,
        next_page_token: Optional[str] = None) -> CatalogV2DataCollection
```

**Arguments**:

- `markets` (`Optional[Union[str, List[str]]]`): Comma separated list of markets. By default all markets are returned.
- `exchange` (`Optional[str]`): Unique name of an exchange.
- `market_type` (`Optional[str]`): Type of markets.
- `base` (`Optional[str]`): Base asset of markets.
- `quote` (`Optional[str]`): Quote asset of markets.
- `asset` (`Optional[str]`): Any asset of markets.
- `symbol` (`Optional[str]`): Symbol of derivative markets, full instrument name.
- `format` (`Optional[str]`): Format of the response. Supported values are `json`, `json_stream`.
- `page_size` (`Optional[int]`): Number of items per single page of results.
- `paging_from` (`Optional[str]`): Where does the first page start, at the start of the interval or at the end.
- `next_page_token` (`Optional[str]`): Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.

**Returns**:

`CatalogV2DataCollection`: List of market trades statistics.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_market_candles_v2"></a>

#### catalog\_market\_candles\_v2

```python
def catalog_market_candles_v2(
        markets: Optional[Union[str, List[str]]] = None,
        exchange: Optional[str] = None,
        market_type: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None,
        format: Optional[str] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[str] = None,
        next_page_token: Optional[str] = None) -> CatalogV2DataCollection
```

**Arguments**:

- `markets` (`Optional[Union[str, List[str]]]`): Comma separated list of markets. By default all markets are returned.
- `exchange` (`Optional[str]`): Unique name of an exchange.
- `market_type` (`Optional[str]`): Type of markets.
- `base` (`Optional[str]`): Base asset of markets.
- `quote` (`Optional[str]`): Quote asset of markets.
- `asset` (`Optional[str]`): Any asset of markets.
- `symbol` (`Optional[str]`): Symbol of derivative markets, full instrument name.
- `format` (`Optional[str]`): Format of the response. Supported values are `json`, `json_stream`.
- `page_size` (`Optional[int]`): Number of items per single page of results.
- `paging_from` (`Optional[str]`): Where does the first page start, at the start of the interval or at the end.
- `next_page_token` (`Optional[str]`): Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.

**Returns**:

`CatalogV2DataCollection`: List of market candles statistics.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_market_orderbooks_v2"></a>

#### catalog\_market\_orderbooks\_v2

```python
def catalog_market_orderbooks_v2(
        markets: Optional[Union[str, List[str]]] = None,
        exchange: Optional[str] = None,
        market_type: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None,
        format: Optional[str] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[str] = None,
        next_page_token: Optional[str] = None) -> CatalogV2DataCollection
```

**Arguments**:

- `markets` (`Optional[Union[str, List[str]]]`): Comma separated list of markets. By default all markets are returned.
- `exchange` (`Optional[str]`): Unique name of an exchange.
- `market_type` (`Optional[str]`): Type of markets.
- `base` (`Optional[str]`): Base asset of markets.
- `quote` (`Optional[str]`): Quote asset of markets.
- `asset` (`Optional[str]`): Any asset of markets.
- `symbol` (`Optional[str]`): Symbol of derivative markets, full instrument name.
- `format` (`Optional[str]`): Format of the response. Supported values are `json`, `json_stream`.
- `page_size` (`Optional[int]`): Number of items per single page of results.
- `paging_from` (`Optional[str]`): Where does the first page start, at the start of the interval or at the end.
- `next_page_token` (`Optional[str]`): Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.

**Returns**:

`CatalogV2DataCollection`: List of market orderbooks statistics.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_market_quotes_v2"></a>

#### catalog\_market\_quotes\_v2

```python
def catalog_market_quotes_v2(
        markets: Optional[Union[str, List[str]]] = None,
        exchange: Optional[str] = None,
        market_type: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None,
        format: Optional[str] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[str] = None,
        next_page_token: Optional[str] = None) -> CatalogV2DataCollection
```

**Arguments**:

- `markets` (`Optional[Union[str, List[str]]]`): Comma separated list of markets. By default all markets are returned.
- `exchange` (`Optional[str]`): Unique name of an exchange.
- `market_type` (`Optional[str]`): Type of markets.
- `base` (`Optional[str]`): Base asset of markets.
- `quote` (`Optional[str]`): Quote asset of markets.
- `asset` (`Optional[str]`): Any asset of markets.
- `symbol` (`Optional[str]`): Symbol of derivative markets, full instrument name.
- `format` (`Optional[str]`): Format of the response. Supported values are `json`, `json_stream`.
- `page_size` (`Optional[int]`): Number of items per single page of results.
- `paging_from` (`Optional[str]`): Where does the first page start, at the start of the interval or at the end.
- `next_page_token` (`Optional[str]`): Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.

**Returns**:

`CatalogV2DataCollection`: List of market quotes statistics.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_market_funding_rates_v2"></a>

#### catalog\_market\_funding\_rates\_v2

```python
def catalog_market_funding_rates_v2(
        markets: Optional[Union[str, List[str]]] = None,
        exchange: Optional[str] = None,
        market_type: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None,
        format: Optional[str] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[str] = None,
        next_page_token: Optional[str] = None) -> CatalogV2DataCollection
```

**Arguments**:

- `markets` (`Optional[Union[str, List[str]]]`): Comma separated list of markets. By default all markets are returned.
- `exchange` (`Optional[str]`): Unique name of an exchange.
- `market_type` (`Optional[str]`): Type of markets.
- `base` (`Optional[str]`): Base asset of markets.
- `quote` (`Optional[str]`): Quote asset of markets.
- `asset` (`Optional[str]`): Any asset of markets.
- `symbol` (`Optional[str]`): Symbol of derivative markets, full instrument name.
- `format` (`Optional[str]`): Format of the response. Supported values are `json`, `json_stream`.
- `page_size` (`Optional[int]`): Number of items per single page of results.
- `paging_from` (`Optional[str]`): Where does the first page start, at the start of the interval or at the end.
- `next_page_token` (`Optional[str]`): Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.

**Returns**:

`CatalogV2DataCollection`: List of market funding rates statistics.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_market_contract_prices_v2"></a>

#### catalog\_market\_contract\_prices\_v2

```python
def catalog_market_contract_prices_v2(
        markets: Optional[Union[str, List[str]]] = None,
        exchange: Optional[str] = None,
        market_type: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None,
        format: Optional[str] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[str] = None,
        next_page_token: Optional[str] = None) -> CatalogV2DataCollection
```

**Arguments**:

- `markets` (`Optional[Union[str, List[str]]]`): Comma separated list of markets. By default all markets are returned.
- `exchange` (`Optional[str]`): Unique name of an exchange.
- `market_type` (`Optional[str]`): Type of markets.
- `base` (`Optional[str]`): Base asset of markets.
- `quote` (`Optional[str]`): Quote asset of markets.
- `asset` (`Optional[str]`): Any asset of markets.
- `symbol` (`Optional[str]`): Symbol of derivative markets, full instrument name.
- `format` (`Optional[str]`): Format of the response. Supported values are `json`, `json_stream`.
- `page_size` (`Optional[int]`): Number of items per single page of results.
- `paging_from` (`Optional[str]`): Where does the first page start, at the start of the interval or at the end.
- `next_page_token` (`Optional[str]`): Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.

**Returns**:

`CatalogV2DataCollection`: List of contract prices statistics.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_market_implied_volatility_v2"></a>

#### catalog\_market\_implied\_volatility\_v2

```python
def catalog_market_implied_volatility_v2(
        markets: Optional[Union[str, List[str]]] = None,
        exchange: Optional[str] = None,
        market_type: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None,
        format: Optional[str] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[str] = None,
        next_page_token: Optional[str] = None) -> CatalogV2DataCollection
```

**Arguments**:

- `markets` (`Optional[Union[str, List[str]]]`): Comma separated list of markets. By default all markets are returned.
- `exchange` (`Optional[str]`): Unique name of an exchange.
- `market_type` (`Optional[str]`): Type of markets.
- `base` (`Optional[str]`): Base asset of markets.
- `quote` (`Optional[str]`): Quote asset of markets.
- `asset` (`Optional[str]`): Any asset of markets.
- `symbol` (`Optional[str]`): Symbol of derivative markets, full instrument name.
- `format` (`Optional[str]`): Format of the response. Supported values are `json`, `json_stream`.
- `page_size` (`Optional[int]`): Number of items per single page of results.
- `paging_from` (`Optional[str]`): Where does the first page start, at the start of the interval or at the end.
- `next_page_token` (`Optional[str]`): Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.

**Returns**:

`CatalogV2DataCollection`: List of implied volatility statistics.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_market_greeks_v2"></a>

#### catalog\_market\_greeks\_v2

```python
def catalog_market_greeks_v2(
        markets: Optional[Union[str, List[str]]] = None,
        exchange: Optional[str] = None,
        market_type: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None,
        format: Optional[str] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[str] = None,
        next_page_token: Optional[str] = None) -> CatalogV2DataCollection
```

**Arguments**:

- `markets` (`Optional[Union[str, List[str]]]`): Comma separated list of markets. By default all markets are returned.
- `exchange` (`Optional[str]`): Unique name of an exchange.
- `market_type` (`Optional[str]`): Type of markets.
- `base` (`Optional[str]`): Base asset of markets.
- `quote` (`Optional[str]`): Quote asset of markets.
- `asset` (`Optional[str]`): Any asset of markets.
- `symbol` (`Optional[str]`): Symbol of derivative markets, full instrument name.
- `format` (`Optional[str]`): Format of the response. Supported values are `json`, `json_stream`.
- `page_size` (`Optional[int]`): Number of items per single page of results.
- `paging_from` (`Optional[str]`): Where does the first page start, at the start of the interval or at the end.
- `next_page_token` (`Optional[str]`): Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.

**Returns**:

`CatalogV2DataCollection`: List of greeks statistics.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_market_open_interest_v2"></a>

#### catalog\_market\_open\_interest\_v2

```python
def catalog_market_open_interest_v2(
        markets: Optional[Union[str, List[str]]] = None,
        exchange: Optional[str] = None,
        market_type: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None,
        format: Optional[str] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[str] = None,
        next_page_token: Optional[str] = None) -> CatalogV2DataCollection
```

**Arguments**:

- `markets` (`Optional[Union[str, List[str]]]`): Comma separated list of markets. By default all markets are returned.
- `exchange` (`Optional[str]`): Unique name of an exchange.
- `market_type` (`Optional[str]`): Type of markets.
- `base` (`Optional[str]`): Base asset of markets.
- `quote` (`Optional[str]`): Quote asset of markets.
- `asset` (`Optional[str]`): Any asset of markets.
- `symbol` (`Optional[str]`): Symbol of derivative markets, full instrument name.
- `format` (`Optional[str]`): Format of the response. Supported values are `json`, `json_stream`.
- `page_size` (`Optional[int]`): Number of items per single page of results.
- `paging_from` (`Optional[str]`): Where does the first page start, at the start of the interval or at the end.
- `next_page_token` (`Optional[str]`): Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.

**Returns**:

`CatalogV2DataCollection`: List of market open interest statistics.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_market_liquidations_v2"></a>

#### catalog\_market\_liquidations\_v2

```python
def catalog_market_liquidations_v2(
        markets: Optional[Union[str, List[str]]] = None,
        exchange: Optional[str] = None,
        market_type: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None,
        format: Optional[str] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[str] = None,
        next_page_token: Optional[str] = None) -> CatalogV2DataCollection
```

**Arguments**:

- `markets` (`Optional[Union[str, List[str]]]`): Comma separated list of markets. By default all markets are returned.
- `exchange` (`Optional[str]`): Unique name of an exchange.
- `market_type` (`Optional[str]`): Type of markets.
- `base` (`Optional[str]`): Base asset of markets.
- `quote` (`Optional[str]`): Quote asset of markets.
- `asset` (`Optional[str]`): Any asset of markets.
- `symbol` (`Optional[str]`): Symbol of derivative markets, full instrument name.
- `format` (`Optional[str]`): Format of the response. Supported values are `json`, `json_stream`.
- `page_size` (`Optional[int]`): Number of items per single page of results.
- `paging_from` (`Optional[str]`): Where does the first page start, at the start of the interval or at the end.
- `next_page_token` (`Optional[str]`): Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.

**Returns**:

`CatalogV2DataCollection`: List of market liquidations statistics.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_market_metrics_v2"></a>

#### catalog\_market\_metrics\_v2

```python
def catalog_market_metrics_v2(
        markets: Optional[Union[str, List[str]]] = None,
        exchange: Optional[str] = None,
        market_type: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None,
        format: Optional[str] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[str] = None,
        next_page_token: Optional[str] = None) -> CatalogV2DataCollection
```

**Arguments**:

- `markets` (`Optional[Union[str, List[str]]]`): Comma separated list of markets. By default all markets are returned.
- `exchange` (`Optional[str]`): Unique name of an exchange.
- `market_type` (`Optional[str]`): Type of markets.
- `base` (`Optional[str]`): Base asset of markets.
- `quote` (`Optional[str]`): Quote asset of markets.
- `asset` (`Optional[str]`): Any asset of markets.
- `symbol` (`Optional[str]`): Symbol of derivative markets, full instrument name.
- `format` (`Optional[str]`): Format of the response. Supported values are `json`, `json_stream`.
- `page_size` (`Optional[int]`): Number of items per single page of results.
- `paging_from` (`Optional[str]`): Where does the first page start, at the start of the interval or at the end.
- `next_page_token` (`Optional[str]`): Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.

**Returns**:

`CatalogV2DataCollection`: List of market metrics statistics.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_full_market_trades_v2"></a>

#### catalog\_full\_market\_trades\_v2

```python
def catalog_full_market_trades_v2(
        markets: Optional[Union[str, List[str]]] = None,
        exchange: Optional[str] = None,
        market_type: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None,
        format: Optional[str] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[str] = None,
        next_page_token: Optional[str] = None) -> CatalogV2DataCollection
```

**Arguments**:

- `markets` (`Optional[Union[str, List[str]]]`): Comma separated list of markets. By default all markets are returned.
- `exchange` (`Optional[str]`): Unique name of an exchange.
- `market_type` (`Optional[str]`): Type of markets.
- `base` (`Optional[str]`): Base asset of markets.
- `quote` (`Optional[str]`): Quote asset of markets.
- `asset` (`Optional[str]`): Any asset of markets.
- `symbol` (`Optional[str]`): Symbol of derivative markets, full instrument name.
- `format` (`Optional[str]`): Format of the response. Supported values are `json`, `json_stream`.
- `page_size` (`Optional[int]`): Number of items per single page of results.
- `paging_from` (`Optional[str]`): Where does the first page start, at the start of the interval or at the end.
- `next_page_token` (`Optional[str]`): Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.

**Returns**:

`CatalogV2DataCollection`: List of market trades statistics.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_full_market_candles_v2"></a>

#### catalog\_full\_market\_candles\_v2

```python
def catalog_full_market_candles_v2(
        markets: Optional[Union[str, List[str]]] = None,
        exchange: Optional[str] = None,
        market_type: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None,
        format: Optional[str] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[str] = None,
        next_page_token: Optional[str] = None) -> CatalogV2DataCollection
```

**Arguments**:

- `markets` (`Optional[Union[str, List[str]]]`): Comma separated list of markets. By default all markets are returned.
- `exchange` (`Optional[str]`): Unique name of an exchange.
- `market_type` (`Optional[str]`): Type of markets.
- `base` (`Optional[str]`): Base asset of markets.
- `quote` (`Optional[str]`): Quote asset of markets.
- `asset` (`Optional[str]`): Any asset of markets.
- `symbol` (`Optional[str]`): Symbol of derivative markets, full instrument name.
- `format` (`Optional[str]`): Format of the response. Supported values are `json`, `json_stream`.
- `page_size` (`Optional[int]`): Number of items per single page of results.
- `paging_from` (`Optional[str]`): Where does the first page start, at the start of the interval or at the end.
- `next_page_token` (`Optional[str]`): Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.

**Returns**:

`CatalogV2DataCollection`: List of market candles statistics.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_full_market_orderbooks_v2"></a>

#### catalog\_full\_market\_orderbooks\_v2

```python
def catalog_full_market_orderbooks_v2(
        markets: Optional[Union[str, List[str]]] = None,
        exchange: Optional[str] = None,
        market_type: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None,
        format: Optional[str] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[str] = None,
        next_page_token: Optional[str] = None) -> CatalogV2DataCollection
```

**Arguments**:

- `markets` (`Optional[Union[str, List[str]]]`): Comma separated list of markets. By default all markets are returned.
- `exchange` (`Optional[str]`): Unique name of an exchange.
- `market_type` (`Optional[str]`): Type of markets.
- `base` (`Optional[str]`): Base asset of markets.
- `quote` (`Optional[str]`): Quote asset of markets.
- `asset` (`Optional[str]`): Any asset of markets.
- `symbol` (`Optional[str]`): Symbol of derivative markets, full instrument name.
- `format` (`Optional[str]`): Format of the response. Supported values are `json`, `json_stream`.
- `page_size` (`Optional[int]`): Number of items per single page of results.
- `paging_from` (`Optional[str]`): Where does the first page start, at the start of the interval or at the end.
- `next_page_token` (`Optional[str]`): Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.

**Returns**:

`CatalogV2DataCollection`: List of market orderbooks statistics.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_full_market_quotes_v2"></a>

#### catalog\_full\_market\_quotes\_v2

```python
def catalog_full_market_quotes_v2(
        markets: Optional[Union[str, List[str]]] = None,
        exchange: Optional[str] = None,
        market_type: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None,
        format: Optional[str] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[str] = None,
        next_page_token: Optional[str] = None) -> CatalogV2DataCollection
```

**Arguments**:

- `markets` (`Optional[Union[str, List[str]]]`): Comma separated list of markets. By default all markets are returned.
- `exchange` (`Optional[str]`): Unique name of an exchange.
- `market_type` (`Optional[str]`): Type of markets.
- `base` (`Optional[str]`): Base asset of markets.
- `quote` (`Optional[str]`): Quote asset of markets.
- `asset` (`Optional[str]`): Any asset of markets.
- `symbol` (`Optional[str]`): Symbol of derivative markets, full instrument name.
- `format` (`Optional[str]`): Format of the response. Supported values are `json`, `json_stream`.
- `page_size` (`Optional[int]`): Number of items per single page of results.
- `paging_from` (`Optional[str]`): Where does the first page start, at the start of the interval or at the end.
- `next_page_token` (`Optional[str]`): Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.

**Returns**:

`CatalogV2DataCollection`: List of market quotes statistics.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_full_market_funding_rates_v2"></a>

#### catalog\_full\_market\_funding\_rates\_v2

```python
def catalog_full_market_funding_rates_v2(
        markets: Optional[Union[str, List[str]]] = None,
        exchange: Optional[str] = None,
        market_type: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None,
        format: Optional[str] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[str] = None,
        next_page_token: Optional[str] = None) -> CatalogV2DataCollection
```

**Arguments**:

- `markets` (`Optional[Union[str, List[str]]]`): Comma separated list of markets. By default all markets are returned.
- `exchange` (`Optional[str]`): Unique name of an exchange.
- `market_type` (`Optional[str]`): Type of markets.
- `base` (`Optional[str]`): Base asset of markets.
- `quote` (`Optional[str]`): Quote asset of markets.
- `asset` (`Optional[str]`): Any asset of markets.
- `symbol` (`Optional[str]`): Symbol of derivative markets, full instrument name.
- `format` (`Optional[str]`): Format of the response. Supported values are `json`, `json_stream`.
- `page_size` (`Optional[int]`): Number of items per single page of results.
- `paging_from` (`Optional[str]`): Where does the first page start, at the start of the interval or at the end.
- `next_page_token` (`Optional[str]`): Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.

**Returns**:

`CatalogV2DataCollection`: List of market funding rates statistics.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_full_market_contract_prices_v2"></a>

#### catalog\_full\_market\_contract\_prices\_v2

```python
def catalog_full_market_contract_prices_v2(
        markets: Optional[Union[str, List[str]]] = None,
        exchange: Optional[str] = None,
        market_type: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None,
        format: Optional[str] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[str] = None,
        next_page_token: Optional[str] = None) -> CatalogV2DataCollection
```

**Arguments**:

- `markets` (`Optional[Union[str, List[str]]]`): Comma separated list of markets. By default all markets are returned.
- `exchange` (`Optional[str]`): Unique name of an exchange.
- `market_type` (`Optional[str]`): Type of markets.
- `base` (`Optional[str]`): Base asset of markets.
- `quote` (`Optional[str]`): Quote asset of markets.
- `asset` (`Optional[str]`): Any asset of markets.
- `symbol` (`Optional[str]`): Symbol of derivative markets, full instrument name.
- `format` (`Optional[str]`): Format of the response. Supported values are `json`, `json_stream`.
- `page_size` (`Optional[int]`): Number of items per single page of results.
- `paging_from` (`Optional[str]`): Where does the first page start, at the start of the interval or at the end.
- `next_page_token` (`Optional[str]`): Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.

**Returns**:

`CatalogV2DataCollection`: List of contract prices statistics.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_full_market_implied_volatility_v2"></a>

#### catalog\_full\_market\_implied\_volatility\_v2

```python
def catalog_full_market_implied_volatility_v2(
        markets: Optional[Union[str, List[str]]] = None,
        exchange: Optional[str] = None,
        market_type: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None,
        format: Optional[str] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[str] = None,
        next_page_token: Optional[str] = None) -> CatalogV2DataCollection
```

**Arguments**:

- `markets` (`Optional[Union[str, List[str]]]`): Comma separated list of markets. By default all markets are returned.
- `exchange` (`Optional[str]`): Unique name of an exchange.
- `market_type` (`Optional[str]`): Type of markets.
- `base` (`Optional[str]`): Base asset of markets.
- `quote` (`Optional[str]`): Quote asset of markets.
- `asset` (`Optional[str]`): Any asset of markets.
- `symbol` (`Optional[str]`): Symbol of derivative markets, full instrument name.
- `format` (`Optional[str]`): Format of the response. Supported values are `json`, `json_stream`.
- `page_size` (`Optional[int]`): Number of items per single page of results.
- `paging_from` (`Optional[str]`): Where does the first page start, at the start of the interval or at the end.
- `next_page_token` (`Optional[str]`): Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.

**Returns**:

`CatalogV2DataCollection`: List of implied volatility statistics.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_full_market_greeks_v2"></a>

#### catalog\_full\_market\_greeks\_v2

```python
def catalog_full_market_greeks_v2(
        markets: Optional[Union[str, List[str]]] = None,
        exchange: Optional[str] = None,
        market_type: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None,
        format: Optional[str] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[str] = None,
        next_page_token: Optional[str] = None) -> CatalogV2DataCollection
```

**Arguments**:

- `markets` (`Optional[Union[str, List[str]]]`): Comma separated list of markets. By default all markets are returned.
- `exchange` (`Optional[str]`): Unique name of an exchange.
- `market_type` (`Optional[str]`): Type of markets.
- `base` (`Optional[str]`): Base asset of markets.
- `quote` (`Optional[str]`): Quote asset of markets.
- `asset` (`Optional[str]`): Any asset of markets.
- `symbol` (`Optional[str]`): Symbol of derivative markets, full instrument name.
- `format` (`Optional[str]`): Format of the response. Supported values are `json`, `json_stream`.
- `page_size` (`Optional[int]`): Number of items per single page of results.
- `paging_from` (`Optional[str]`): Where does the first page start, at the start of the interval or at the end.
- `next_page_token` (`Optional[str]`): Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.

**Returns**:

`CatalogV2DataCollection`: List of greeks statistics.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_full_market_open_interest_v2"></a>

#### catalog\_full\_market\_open\_interest\_v2

```python
def catalog_full_market_open_interest_v2(
        markets: Optional[Union[str, List[str]]] = None,
        exchange: Optional[str] = None,
        market_type: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None,
        format: Optional[str] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[str] = None,
        next_page_token: Optional[str] = None) -> CatalogV2DataCollection
```

**Arguments**:

- `markets` (`Optional[Union[str, List[str]]]`): Comma separated list of markets. By default all markets are returned.
- `exchange` (`Optional[str]`): Unique name of an exchange.
- `market_type` (`Optional[str]`): Type of markets.
- `base` (`Optional[str]`): Base asset of markets.
- `quote` (`Optional[str]`): Quote asset of markets.
- `asset` (`Optional[str]`): Any asset of markets.
- `symbol` (`Optional[str]`): Symbol of derivative markets, full instrument name.
- `format` (`Optional[str]`): Format of the response. Supported values are `json`, `json_stream`.
- `page_size` (`Optional[int]`): Number of items per single page of results.
- `paging_from` (`Optional[str]`): Where does the first page start, at the start of the interval or at the end.
- `next_page_token` (`Optional[str]`): Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.

**Returns**:

`CatalogV2DataCollection`: List of market open interest statistics.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_full_market_liquidations_v2"></a>

#### catalog\_full\_market\_liquidations\_v2

```python
def catalog_full_market_liquidations_v2(
        markets: Optional[Union[str, List[str]]] = None,
        exchange: Optional[str] = None,
        market_type: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None,
        format: Optional[str] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[str] = None,
        next_page_token: Optional[str] = None) -> CatalogV2DataCollection
```

**Arguments**:

- `markets` (`Optional[Union[str, List[str]]]`): Comma separated list of markets. By default all markets are returned.
- `exchange` (`Optional[str]`): Unique name of an exchange.
- `market_type` (`Optional[str]`): Type of markets.
- `base` (`Optional[str]`): Base asset of markets.
- `quote` (`Optional[str]`): Quote asset of markets.
- `asset` (`Optional[str]`): Any asset of markets.
- `symbol` (`Optional[str]`): Symbol of derivative markets, full instrument name.
- `format` (`Optional[str]`): Format of the response. Supported values are `json`, `json_stream`.
- `page_size` (`Optional[int]`): Number of items per single page of results.
- `paging_from` (`Optional[str]`): Where does the first page start, at the start of the interval or at the end.
- `next_page_token` (`Optional[str]`): Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.

**Returns**:

`CatalogV2DataCollection`: List of market liquidations statistics.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_full_market_metrics_v2"></a>

#### catalog\_full\_market\_metrics\_v2

```python
def catalog_full_market_metrics_v2(
        markets: Optional[Union[str, List[str]]] = None,
        exchange: Optional[str] = None,
        market_type: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None,
        format: Optional[str] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[str] = None,
        next_page_token: Optional[str] = None) -> CatalogV2DataCollection
```

**Arguments**:

- `markets` (`Optional[Union[str, List[str]]]`): Comma separated list of markets. By default all markets are returned.
- `exchange` (`Optional[str]`): Unique name of an exchange.
- `market_type` (`Optional[str]`): Type of markets.
- `base` (`Optional[str]`): Base asset of markets.
- `quote` (`Optional[str]`): Quote asset of markets.
- `asset` (`Optional[str]`): Any asset of markets.
- `symbol` (`Optional[str]`): Symbol of derivative markets, full instrument name.
- `format` (`Optional[str]`): Format of the response. Supported values are `json`, `json_stream`.
- `page_size` (`Optional[int]`): Number of items per single page of results.
- `paging_from` (`Optional[str]`): Where does the first page start, at the start of the interval or at the end.
- `next_page_token` (`Optional[str]`): Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.

**Returns**:

`CatalogV2DataCollection`: List of market metrics statistics.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_asset_metrics_v2"></a>

#### catalog\_asset\_metrics\_v2

```python
def catalog_asset_metrics_v2(
        assets: Optional[Union[str, List[str]]] = None,
        metrics: Optional[Union[str, List[str]]] = None,
        reviewable: Optional[bool] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[str] = None,
        next_page_token: Optional[str] = None,
        format: Optional[str] = None) -> CatalogV2DataCollection
```

**Arguments**:

- `assets` (`Optional[Union[str, List[str]]]`): Comma separated list of assets. By default all assets are returned.
- `metrics` (`Optional[Union[str, List[str]]]`): Comma separated list of metrics. By default all metrics are returned.
- `reviewable` (`Optional[bool]`): Limit to human-reviewable metrics. By default all metrics are returned.
- `page_size` (`Optional[int]`): Number of items per single page of results.
- `paging_from` (`Optional[str]`): Where does the first page start, at the start of the interval or at the end.
- `next_page_token` (`Optional[str]`): Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
- `format` (`Optional[str]`): Format of the response. Supported values are `json`, `json_stream`.

**Returns**:

`CatalogV2DataCollection`: List of asset metrics.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_full_asset_metrics_v2"></a>

#### catalog\_full\_asset\_metrics\_v2

```python
def catalog_full_asset_metrics_v2(
        assets: Optional[Union[str, List[str]]] = None,
        metrics: Optional[Union[str, List[str]]] = None,
        reviewable: Optional[bool] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[str] = None,
        next_page_token: Optional[str] = None,
        format: Optional[str] = None) -> CatalogV2DataCollection
```

**Arguments**:

- `assets` (`Optional[Union[str, List[str]]]`): Comma separated list of assets. By default all assets are returned.
- `metrics` (`Optional[Union[str, List[str]]]`): Comma separated list of metrics. By default all metrics are returned.
- `reviewable` (`Optional[bool]`): Limit to human-reviewable metrics. By default all metrics are returned.
- `page_size` (`Optional[int]`): Number of items per single page of results.
- `paging_from` (`Optional[str]`): Where does the first page start, at the start of the interval or at the end.
- `next_page_token` (`Optional[str]`): Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
- `format` (`Optional[str]`): Format of the response. Supported values are `json`, `json_stream`.

**Returns**:

`CatalogV2DataCollection`: List of asset metrics.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_exchange_metrics_v2"></a>

#### catalog\_exchange\_metrics\_v2

```python
def catalog_exchange_metrics_v2(
        exchanges: Optional[Union[str, List[str]]] = None,
        metrics: Optional[Union[str, List[str]]] = None,
        reviewable: Optional[bool] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[str] = None,
        next_page_token: Optional[str] = None,
        format: Optional[str] = None) -> CatalogV2DataCollection
```

**Arguments**:

- `exchanges` (`Optional[Union[str, List[str]]]`): Comma separated list of exchanges. By default all exchanges are returned.
- `metrics` (`Optional[Union[str, List[str]]]`): Comma separated list of metrics. By default all metrics are returned.
- `reviewable` (`Optional[bool]`): Limit to human-reviewable metrics. By default all metrics are returned.
- `page_size` (`Optional[int]`): Number of items per single page of results.
- `paging_from` (`Optional[str]`): Where does the first page start, at the start of the interval or at the end.
- `next_page_token` (`Optional[str]`): Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
- `format` (`Optional[str]`): Format of the response. Supported values are `json`, `json_stream`.

**Returns**:

`CatalogV2DataCollection`: List of exchange metrics.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_full_exchange_metrics_v2"></a>

#### catalog\_full\_exchange\_metrics\_v2

```python
def catalog_full_exchange_metrics_v2(
        exchanges: Optional[Union[str, List[str]]] = None,
        metrics: Optional[Union[str, List[str]]] = None,
        reviewable: Optional[bool] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[str] = None,
        next_page_token: Optional[str] = None,
        format: Optional[str] = None) -> CatalogV2DataCollection
```

**Arguments**:

- `exchanges` (`Optional[Union[str, List[str]]]`): Comma separated list of exchanges. By default all exchanges are returned.
- `metrics` (`Optional[Union[str, List[str]]]`): Comma separated list of metrics. By default all metrics are returned.
- `reviewable` (`Optional[bool]`): Limit to human-reviewable metrics. By default all metrics are returned.
- `page_size` (`Optional[int]`): Number of items per single page of results.
- `paging_from` (`Optional[str]`): Where does the first page start, at the start of the interval or at the end.
- `next_page_token` (`Optional[str]`): Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
- `format` (`Optional[str]`): Format of the response. Supported values are `json`, `json_stream`.

**Returns**:

`CatalogV2DataCollection`: List of exchange metrics.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_exchange_asset_metrics_v2"></a>

#### catalog\_exchange\_asset\_metrics\_v2

```python
def catalog_exchange_asset_metrics_v2(
        exchange_assets: Optional[Union[str, List[str]]] = None,
        metrics: Optional[Union[str, List[str]]] = None,
        reviewable: Optional[bool] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[str] = None,
        next_page_token: Optional[str] = None,
        format: Optional[str] = None) -> CatalogV2DataCollection
```

**Arguments**:

- `exchange_assets` (`Optional[Union[str, List[str]]]`): Comma separated list of exchange-assets. By default, all exchange-assets pairs are returned.
- `metrics` (`Optional[Union[str, List[str]]]`): Comma separated list of metrics. By default all metrics are returned.
- `reviewable` (`Optional[bool]`): Limit to human-reviewable metrics. By default all metrics are returned.
- `page_size` (`Optional[int]`): Number of items per single page of results.
- `paging_from` (`Optional[str]`): Where does the first page start, at the start of the interval or at the end.
- `next_page_token` (`Optional[str]`): Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
- `format` (`Optional[str]`): Format of the response. Supported values are `json`, `json_stream`.

**Returns**:

`CatalogV2DataCollection`: List of exchange-asset metrics.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_full_exchange_asset_metrics_v2"></a>

#### catalog\_full\_exchange\_asset\_metrics\_v2

```python
def catalog_full_exchange_asset_metrics_v2(
        exchange_assets: Optional[Union[str, List[str]]] = None,
        metrics: Optional[Union[str, List[str]]] = None,
        reviewable: Optional[bool] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[str] = None,
        next_page_token: Optional[str] = None,
        format: Optional[str] = None) -> CatalogV2DataCollection
```

**Arguments**:

- `exchange_assets` (`Optional[Union[str, List[str]]]`): Comma separated list of exchange-assets. By default, all exchange-assets pairs are returned.
- `metrics` (`Optional[Union[str, List[str]]]`): Comma separated list of metrics. By default all metrics are returned.
- `reviewable` (`Optional[bool]`): Limit to human-reviewable metrics. By default all metrics are returned.
- `page_size` (`Optional[int]`): Number of items per single page of results.
- `paging_from` (`Optional[str]`): Where does the first page start, at the start of the interval or at the end.
- `next_page_token` (`Optional[str]`): Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
- `format` (`Optional[str]`): Format of the response. Supported values are `json`, `json_stream`.

**Returns**:

`CatalogV2DataCollection`: List of exchange-asset metrics.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_pair_metrics_v2"></a>

#### catalog\_pair\_metrics\_v2

```python
def catalog_pair_metrics_v2(
        pairs: Optional[Union[str, List[str]]] = None,
        metrics: Optional[Union[str, List[str]]] = None,
        reviewable: Optional[bool] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[str] = None,
        next_page_token: Optional[str] = None,
        format: Optional[str] = None) -> CatalogV2DataCollection
```

**Arguments**:

- `pairs` (`Optional[Union[str, List[str]]]`): Comma separated list of asset pairs. By default, all asset pairs are returned.
- `metrics` (`Optional[Union[str, List[str]]]`): Comma separated list of metrics. By default all metrics are returned.
- `reviewable` (`Optional[bool]`): Limit to human-reviewable metrics. By default all metrics are returned.
- `page_size` (`Optional[int]`): Number of items per single page of results.
- `paging_from` (`Optional[str]`): Where does the first page start, at the start of the interval or at the end.
- `next_page_token` (`Optional[str]`): Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
- `format` (`Optional[str]`): Format of the response. Supported values are `json`, `json_stream`.

**Returns**:

`CatalogV2DataCollection`: List of pair metrics.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_full_pair_metrics_v2"></a>

#### catalog\_full\_pair\_metrics\_v2

```python
def catalog_full_pair_metrics_v2(
        pairs: Optional[Union[str, List[str]]] = None,
        metrics: Optional[Union[str, List[str]]] = None,
        reviewable: Optional[bool] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[str] = None,
        next_page_token: Optional[str] = None,
        format: Optional[str] = None) -> CatalogV2DataCollection
```

**Arguments**:

- `pairs` (`Optional[Union[str, List[str]]]`): Comma separated list of asset pairs. By default, all asset pairs are returned.
- `metrics` (`Optional[Union[str, List[str]]]`): Comma separated list of metrics. By default all metrics are returned.
- `reviewable` (`Optional[bool]`): Limit to human-reviewable metrics. By default all metrics are returned.
- `page_size` (`Optional[int]`): Number of items per single page of results.
- `paging_from` (`Optional[str]`): Where does the first page start, at the start of the interval or at the end.
- `next_page_token` (`Optional[str]`): Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
- `format` (`Optional[str]`): Format of the response. Supported values are `json`, `json_stream`.

**Returns**:

`CatalogV2DataCollection`: List of pair metrics.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_institution_metrics_v2"></a>

#### catalog\_institution\_metrics\_v2

```python
def catalog_institution_metrics_v2(
        institutions: Optional[Union[str, List[str]]] = None,
        metrics: Optional[Union[str, List[str]]] = None,
        reviewable: Optional[bool] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[str] = None,
        next_page_token: Optional[str] = None,
        format: Optional[str] = None) -> CatalogV2DataCollection
```

**Arguments**:

- `institutions` (`Optional[Union[str, List[str]]]`): Comma separated list of institutions. By default, all institutions are returned.
- `metrics` (`Optional[Union[str, List[str]]]`): Comma separated list of metrics. By default all metrics are returned.
- `reviewable` (`Optional[bool]`): Limit to human-reviewable metrics. By default all metrics are returned.
- `page_size` (`Optional[int]`): Number of items per single page of results.
- `paging_from` (`Optional[str]`): Where does the first page start, at the start of the interval or at the end.
- `next_page_token` (`Optional[str]`): Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
- `format` (`Optional[str]`): Format of the response. Supported values are `json`, `json_stream`.

**Returns**:

`CatalogV2DataCollection`: List of institution metrics.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_full_institution_metrics_v2"></a>

#### catalog\_full\_institution\_metrics\_v2

```python
def catalog_full_institution_metrics_v2(
        institutions: Optional[Union[str, List[str]]] = None,
        metrics: Optional[Union[str, List[str]]] = None,
        reviewable: Optional[bool] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[str] = None,
        next_page_token: Optional[str] = None,
        format: Optional[str] = None) -> CatalogV2DataCollection
```

**Arguments**:

- `institutions` (`Optional[Union[str, List[str]]]`): Comma separated list of institutions. By default, all institutions are returned.
- `metrics` (`Optional[Union[str, List[str]]]`): Comma separated list of metrics. By default all metrics are returned.
- `reviewable` (`Optional[bool]`): Limit to human-reviewable metrics. By default all metrics are returned.
- `page_size` (`Optional[int]`): Number of items per single page of results.
- `paging_from` (`Optional[str]`): Where does the first page start, at the start of the interval or at the end.
- `next_page_token` (`Optional[str]`): Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
- `format` (`Optional[str]`): Format of the response. Supported values are `json`, `json_stream`.

**Returns**:

`CatalogV2DataCollection`: List of institution metrics.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_pair_candles_v2"></a>

#### catalog\_pair\_candles\_v2

```python
def catalog_pair_candles_v2(
        pairs: Optional[Union[str, List[str]]] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[str] = None,
        next_page_token: Optional[str] = None) -> CatalogV2DataCollection
```

**Arguments**:

- `pairs` (`Optional[Union[str, List[str]]]`): Comma separated list of asset pairs. By default, all asset pairs are returned.
- `page_size` (`Optional[int]`): Number of items per single page of results.
- `paging_from` (`Optional[str]`): Where does the first page start, at the start of the interval or at the end.
- `next_page_token` (`Optional[str]`): Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.

**Returns**:

`CatalogV2DataCollection`: List of asset pair candles statistics.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_index_candles_v2"></a>

#### catalog\_index\_candles\_v2

```python
def catalog_index_candles_v2(
        indexes: Optional[Union[str, List[str]]] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[str] = None,
        next_page_token: Optional[str] = None) -> CatalogV2DataCollection
```

**Arguments**:

- `indexes` (`Optional[Union[str, List[str]]]`): Comma separated list of indexes. By default all assets are returned.
- `page_size` (`Optional[int]`): Number of items per single page of results.
- `paging_from` (`Optional[str]`): Where does the first page start, at the start of the interval or at the end.
- `next_page_token` (`Optional[str]`): Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.

**Returns**:

`CatalogV2DataCollection`: List of index candles statistics.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_asset_chains_v2"></a>

#### catalog\_asset\_chains\_v2

```python
def catalog_asset_chains_v2(
        assets: Optional[Union[str, List[str]]] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[str] = None,
        next_page_token: Optional[str] = None) -> CatalogV2DataCollection
```

**Arguments**:

- `assets` (`Optional[Union[str, List[str]]]`): Comma separated list of assets. By default all assets are returned.
- `page_size` (`Optional[int]`): Number of items per single page of results.
- `paging_from` (`Optional[str]`): Where does the first page start, at the start of the interval or at the end.
- `next_page_token` (`Optional[str]`): Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.

**Returns**:

`CatalogV2DataCollection`: List of asset chains assets

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_mempool_feerates_v2"></a>

#### catalog\_mempool\_feerates\_v2

```python
def catalog_mempool_feerates_v2(
        assets: Optional[Union[str, List[str]]] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[str] = None,
        next_page_token: Optional[str] = None) -> CatalogV2DataCollection
```

**Arguments**:

- `assets` (`Optional[Union[str, List[str]]]`): Comma separated list of assets. By default all assets are returned.
- `page_size` (`Optional[int]`): Number of items per single page of results.
- `paging_from` (`Optional[str]`): Where does the first page start, at the start of the interval or at the end.
- `next_page_token` (`Optional[str]`): Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.

**Returns**:

`CatalogV2DataCollection`: List of mempool feerates assets

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_mining_pool_tips_summaries_v2"></a>

#### catalog\_mining\_pool\_tips\_summaries\_v2

```python
def catalog_mining_pool_tips_summaries_v2(
        assets: Optional[Union[str, List[str]]] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[str] = None,
        next_page_token: Optional[str] = None) -> CatalogV2DataCollection
```

**Arguments**:

- `assets` (`Optional[Union[str, List[str]]]`): Comma separated list of assets. By default all assets are returned.
- `page_size` (`Optional[int]`): Number of items per single page of results.
- `paging_from` (`Optional[str]`): Where does the first page start, at the start of the interval or at the end.
- `next_page_token` (`Optional[str]`): Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.

**Returns**:

`CatalogV2DataCollection`: List of mining pool tips assets

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_transaction_tracker_assets_v2"></a>

#### catalog\_transaction\_tracker\_assets\_v2

```python
def catalog_transaction_tracker_assets_v2(
        assets: Optional[Union[str, List[str]]] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[str] = None,
        next_page_token: Optional[str] = None) -> CatalogV2DataCollection
```

**Arguments**:

- `assets` (`Optional[Union[str, List[str]]]`): Comma separated list of assets. By default all assets are returned.
- `page_size` (`Optional[int]`): Number of items per single page of results.
- `paging_from` (`Optional[str]`): Where does the first page start, at the start of the interval or at the end.
- `next_page_token` (`Optional[str]`): Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.

**Returns**:

`CatalogV2DataCollection`: List of transaction tracker assets

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_full_pair_candles_v2"></a>

#### catalog\_full\_pair\_candles\_v2

```python
def catalog_full_pair_candles_v2(
        pairs: Optional[Union[str, List[str]]] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[str] = None,
        next_page_token: Optional[str] = None) -> CatalogV2DataCollection
```

**Arguments**:

- `pairs` (`Optional[Union[str, List[str]]]`): Comma separated list of asset pairs. By default, all asset pairs are returned.
- `page_size` (`Optional[int]`): Number of items per single page of results.
- `paging_from` (`Optional[str]`): Where does the first page start, at the start of the interval or at the end.
- `next_page_token` (`Optional[str]`): Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.

**Returns**:

`CatalogV2DataCollection`: List of asset pair candles statistics.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_full_index_candles_v2"></a>

#### catalog\_full\_index\_candles\_v2

```python
def catalog_full_index_candles_v2(
        indexes: Optional[Union[str, List[str]]] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[str] = None,
        next_page_token: Optional[str] = None) -> CatalogV2DataCollection
```

**Arguments**:

- `indexes` (`Optional[Union[str, List[str]]]`): Comma separated list of indexes. By default all assets are returned.
- `page_size` (`Optional[int]`): Number of items per single page of results.
- `paging_from` (`Optional[str]`): Where does the first page start, at the start of the interval or at the end.
- `next_page_token` (`Optional[str]`): Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.

**Returns**:

`CatalogV2DataCollection`: List of index candles statistics.

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_full_asset_chains_v2"></a>

#### catalog\_full\_asset\_chains\_v2

```python
def catalog_full_asset_chains_v2(
        assets: Optional[Union[str, List[str]]] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[str] = None,
        next_page_token: Optional[str] = None) -> CatalogV2DataCollection
```

**Arguments**:

- `assets` (`Optional[Union[str, List[str]]]`): Comma separated list of assets. By default all assets are returned.
- `page_size` (`Optional[int]`): Number of items per single page of results.
- `paging_from` (`Optional[str]`): Where does the first page start, at the start of the interval or at the end.
- `next_page_token` (`Optional[str]`): Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.

**Returns**:

`CatalogV2DataCollection`: List of asset chains assets

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_full_mempool_feerates_v2"></a>

#### catalog\_full\_mempool\_feerates\_v2

```python
def catalog_full_mempool_feerates_v2(
        assets: Optional[Union[str, List[str]]] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[str] = None,
        next_page_token: Optional[str] = None) -> CatalogV2DataCollection
```

**Arguments**:

- `assets` (`Optional[Union[str, List[str]]]`): Comma separated list of assets. By default all assets are returned.
- `page_size` (`Optional[int]`): Number of items per single page of results.
- `paging_from` (`Optional[str]`): Where does the first page start, at the start of the interval or at the end.
- `next_page_token` (`Optional[str]`): Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.

**Returns**:

`CatalogV2DataCollection`: List of mempool feerates assets

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_full_mining_pool_tips_summaries_v2"></a>

#### catalog\_full\_mining\_pool\_tips\_summaries\_v2

```python
def catalog_full_mining_pool_tips_summaries_v2(
        assets: Optional[Union[str, List[str]]] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[str] = None,
        next_page_token: Optional[str] = None) -> CatalogV2DataCollection
```

**Arguments**:

- `assets` (`Optional[Union[str, List[str]]]`): Comma separated list of assets. By default all assets are returned.
- `page_size` (`Optional[int]`): Number of items per single page of results.
- `paging_from` (`Optional[str]`): Where does the first page start, at the start of the interval or at the end.
- `next_page_token` (`Optional[str]`): Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.

**Returns**:

`CatalogV2DataCollection`: List of mining pool tips assets

<a id="coinmetrics.api_client.CoinMetricsClient.catalog_full_transaction_tracker_assets_v2"></a>

#### catalog\_full\_transaction\_tracker\_assets\_v2

```python
def catalog_full_transaction_tracker_assets_v2(
        assets: Optional[Union[str, List[str]]] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[str] = None,
        next_page_token: Optional[str] = None) -> CatalogV2DataCollection
```

**Arguments**:

- `assets` (`Optional[Union[str, List[str]]]`): Comma separated list of assets. By default all assets are returned.
- `page_size` (`Optional[int]`): Number of items per single page of results.
- `paging_from` (`Optional[str]`): Where does the first page start, at the start of the interval or at the end.
- `next_page_token` (`Optional[str]`): Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.

**Returns**:

`CatalogV2DataCollection`: List of transaction tracker assets

<a id="coinmetrics.api_client.CoinMetricsClient.get_asset_alerts"></a>

#### get\_asset\_alerts

```python
def get_asset_alerts(
        assets: Union[List[str], str],
        alerts: Union[List[str], str],
        page_size: Optional[int] = None,
        paging_from: Optional[Union[PagingFrom, str]] = "start",
        start_time: Optional[Union[datetime, date, str]] = None,
        end_time: Optional[Union[datetime, date, str]] = None,
        start_inclusive: Optional[bool] = None,
        end_inclusive: Optional[bool] = None,
        timezone: Optional[str] = None,
        include_heartbeats: Optional[bool] = None) -> DataCollection
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
- `include_heartbeats` (`bool`): If set to true, includes information about most recent time asset was successfully evaluated.

**Returns**:

`DataCollection`: Asset alerts timeseries.

<a id="coinmetrics.api_client.CoinMetricsClient.get_defi_balance_sheets"></a>

#### get\_defi\_balance\_sheets

```python
def get_defi_balance_sheets(defi_protocols: Union[str, List[str]],
                            page_size: Optional[int] = None,
                            paging_from: Optional[Union[PagingFrom,
                                                        str]] = "start",
                            start_time: Optional[Union[datetime, date,
                                                       str]] = None,
                            end_time: Optional[Union[datetime, date,
                                                     str]] = None,
                            start_height: Optional[int] = None,
                            end_height: Optional[int] = None,
                            start_inclusive: Optional[bool] = None,
                            end_inclusive: Optional[bool] = None,
                            timezone: Optional[str] = None) -> DataCollection
```

Returns Defi Balance Sheet records for specified DeFi protocols.

**Arguments**:

- `defi_protocols` (`str, List[str]`): list of DeFi protocols like aave_v2_eth or protocol patterns like aave_v2_* or aave_*_eth or *_eth.
- `page_size` (`int`): number of items returned per page when calling the API. If the request times out, try using a smaller number.
- `paging_from` (`PagingFrom, str`): Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
- `start_time` (`datetime, date, str`): Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `end_time` (`datetime, date, str`): End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `start_height` (`int`): The start height indicates the beginning block height for the set of data that are returned. Mutually exclusive with start_time
- `end_height` (`int`): The end height indicates the beginning block height for the set of data that are returned. Mutually exclusive with end_time
- `start_inclusive` (`bool`): Flag to define if start timestamp must be included in the timeseries if present. True by default.
- `end_inclusive` (`bool`): Flag to define if end timestamp must be included in the timeseries if present. True by default.
- `timezone` (`str`): timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.

**Returns**:

`DataCollection`: list of blockchain blocks metadata

<a id="coinmetrics.api_client.CoinMetricsClient.get_asset_chains"></a>

#### get\_asset\_chains

```python
def get_asset_chains(
        assets: Union[List[str], str],
        page_size: Optional[int] = None,
        paging_from: Optional[Union[PagingFrom, str]] = "start",
        start_time: Optional[Union[datetime, date, str]] = None,
        end_time: Optional[Union[datetime, date, str]] = None,
        start_inclusive: Optional[bool] = None,
        end_inclusive: Optional[bool] = None,
        timezone: Optional[str] = None) -> AssetChainsDataCollection
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

`AssetChainsDataCollection`: Asset chains timeseries.

<a id="coinmetrics.api_client.CoinMetricsClient.get_asset_metrics"></a>

#### get\_asset\_metrics

```python
def get_asset_metrics(assets: Union[List[str], str],
                      metrics: Union[List[str], str],
                      frequency: Optional[str] = None,
                      page_size: Optional[int] = None,
                      paging_from: Optional[Union[PagingFrom, str]] = "start",
                      start_time: Optional[Union[datetime, date, str]] = None,
                      end_time: Optional[Union[datetime, date, str]] = None,
                      start_height: Optional[int] = None,
                      end_height: Optional[int] = None,
                      start_inclusive: Optional[bool] = None,
                      end_inclusive: Optional[bool] = None,
                      timezone: Optional[str] = None,
                      sort: Optional[str] = None,
                      limit_per_asset: Optional[int] = None,
                      status: Optional[str] = None,
                      start_hash: Optional[str] = None,
                      end_hash: Optional[str] = None,
                      min_confirmations: Optional[int] = None,
                      null_as_zero: Optional[bool] = None) -> DataCollection
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
- `status` (`str`): Which metric values do you want to see. Applicable only for "reviewable" metrics.
You can find them in the /catalog/metrics endpoint. Default: "all". Supported: "all" "flash" "reviewed" "revised"
- `start_hash` (`str`): The start hash indicates the beginning block height for the set of data that are returned.
Inclusive by default. Mutually exclusive with start_time and start_height.
- `end_hash` (`str`): The end hash indicates the ending block height for the set of data that are returned.
Inclusive by default. Mutually exclusive with end_time and end_height.
- `min_confirmations` (`int`): Specifies how many blocks behind the chain tip block by block metrics
(1b frequency) are based on. Default for btc is 2 and 99 for eth.
- `null_as_zero` (`bool`): Default: false. Nulls are represented as zeros in the response.

**Returns**:

`DataCollection`: Asset Metrics timeseries.

<a id="coinmetrics.api_client.CoinMetricsClient.get_exchange_metrics"></a>

#### get\_exchange\_metrics

```python
def get_exchange_metrics(
        exchanges: Union[List[str], str],
        metrics: Union[List[str], str],
        frequency: Optional[str] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[Union[PagingFrom, str]] = "start",
        start_time: Optional[Union[datetime, date, str]] = None,
        end_time: Optional[Union[datetime, date, str]] = None,
        start_height: Optional[int] = None,
        end_height: Optional[int] = None,
        start_inclusive: Optional[bool] = None,
        end_inclusive: Optional[bool] = None,
        timezone: Optional[str] = None,
        sort: Optional[str] = None,
        limit_per_exchange: Optional[int] = None) -> DataCollection
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

<a id="coinmetrics.api_client.CoinMetricsClient.get_exchange_asset_metrics"></a>

#### get\_exchange\_asset\_metrics

```python
def get_exchange_asset_metrics(
        exchange_assets: Union[List[str], str],
        metrics: Union[List[str], str],
        frequency: Optional[str] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[Union[PagingFrom, str]] = "start",
        start_time: Optional[Union[datetime, date, str]] = None,
        end_time: Optional[Union[datetime, date, str]] = None,
        start_height: Optional[int] = None,
        end_height: Optional[int] = None,
        start_inclusive: Optional[bool] = None,
        end_inclusive: Optional[bool] = None,
        timezone: Optional[str] = None,
        sort: Optional[str] = None,
        limit_per_exchange_asset: Optional[int] = None) -> DataCollection
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

<a id="coinmetrics.api_client.CoinMetricsClient.get_pair_metrics"></a>

#### get\_pair\_metrics

```python
def get_pair_metrics(pairs: Union[List[str], str],
                     metrics: Union[List[str], str],
                     frequency: Optional[str] = None,
                     page_size: Optional[int] = None,
                     paging_from: Optional[Union[PagingFrom, str]] = "start",
                     start_time: Optional[Union[datetime, date, str]] = None,
                     end_time: Optional[Union[datetime, date, str]] = None,
                     start_height: Optional[int] = None,
                     end_height: Optional[int] = None,
                     start_inclusive: Optional[bool] = None,
                     end_inclusive: Optional[bool] = None,
                     timezone: Optional[str] = None,
                     sort: Optional[str] = None,
                     limit_per_pair: Optional[int] = None) -> DataCollection
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

<a id="coinmetrics.api_client.CoinMetricsClient.get_pair_candles"></a>

#### get\_pair\_candles

```python
def get_pair_candles(pairs: Union[List[str], str],
                     frequency: Optional[str] = None,
                     page_size: Optional[int] = None,
                     paging_from: Optional[Union[PagingFrom, str]] = "start",
                     start_time: Optional[Union[datetime, date, str]] = None,
                     end_time: Optional[Union[datetime, date, str]] = None,
                     start_height: Optional[int] = None,
                     end_height: Optional[int] = None,
                     start_inclusive: Optional[bool] = None,
                     end_inclusive: Optional[bool] = None,
                     timezone: Optional[str] = None,
                     limit_per_pair: Optional[int] = None) -> DataCollection
```

Returns candles for specified asset pairs.

Results are ordered by tuple (pair, time).

**Arguments**:

- `pairs` (`list(str), str`): A single asset-asset pairs (e.g. "btc-usd") or a list of asset-asset-pairs to return info for.
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
- `limit_per_pair` (`int`): How many entries _per asset pair_ the result should contain.

**Returns**:

`DataCollection`: Asset pair candles timeseries.

<a id="coinmetrics.api_client.CoinMetricsClient.get_institution_metrics"></a>

#### get\_institution\_metrics

```python
def get_institution_metrics(
        institutions: Union[List[str], str],
        metrics: Union[List[str], str],
        frequency: Optional[str] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[Union[PagingFrom, str]] = "start",
        start_time: Optional[Union[datetime, date, str]] = None,
        end_time: Optional[Union[datetime, date, str]] = None,
        start_height: Optional[int] = None,
        end_height: Optional[int] = None,
        start_inclusive: Optional[bool] = None,
        end_inclusive: Optional[bool] = None,
        timezone: Optional[str] = None,
        sort: Optional[str] = None,
        limit_per_institution: Optional[int] = None) -> DataCollection
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

<a id="coinmetrics.api_client.CoinMetricsClient.get_index_candles"></a>

#### get\_index\_candles

```python
def get_index_candles(indexes: Union[List[str], str],
                      frequency: Optional[str] = None,
                      page_size: Optional[int] = None,
                      paging_from: Optional[Union[PagingFrom, str]] = "start",
                      start_time: Optional[Union[datetime, date, str]] = None,
                      end_time: Optional[Union[datetime, date, str]] = None,
                      start_inclusive: Optional[bool] = None,
                      end_inclusive: Optional[bool] = None,
                      timezone: Optional[str] = None,
                      limit_per_index: Optional[int] = None) -> DataCollection
```

Returns index candles for specified indexes and date range.

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

`DataCollection`: Index Candles timeseries.

<a id="coinmetrics.api_client.CoinMetricsClient.get_index_levels"></a>

#### get\_index\_levels

```python
def get_index_levels(
        indexes: Union[List[str], str],
        frequency: Optional[str] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[Union[PagingFrom, str]] = "start",
        start_time: Optional[Union[datetime, date, str]] = None,
        end_time: Optional[Union[datetime, date, str]] = None,
        start_inclusive: Optional[bool] = None,
        end_inclusive: Optional[bool] = None,
        timezone: Optional[str] = None,
        limit_per_index: Optional[int] = None,
        include_verification: Optional[bool] = None) -> DataCollection
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
- `include_verification`: Default: False set to true, includes information about verification.

**Returns**:

`DataCollection`: Index Levels timeseries.

<a id="coinmetrics.api_client.CoinMetricsClient.get_index_constituents"></a>

#### get\_index\_constituents

```python
def get_index_constituents(indexes: Union[List[str], str],
                           frequency: Optional[str] = None,
                           page_size: Optional[int] = None,
                           paging_from: Optional[Union[PagingFrom,
                                                       str]] = "start",
                           start_time: Optional[Union[datetime, date,
                                                      str]] = None,
                           end_time: Optional[Union[datetime, date,
                                                    str]] = None,
                           start_inclusive: Optional[bool] = None,
                           end_inclusive: Optional[bool] = None,
                           timezone: Optional[str] = None) -> DataCollection
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

<a id="coinmetrics.api_client.CoinMetricsClient.get_market_metrics"></a>

#### get\_market\_metrics

```python
def get_market_metrics(markets: Union[List[str], str],
                       metrics: Union[List[str], str],
                       frequency: Optional[str] = None,
                       page_size: Optional[int] = None,
                       paging_from: Optional[Union[PagingFrom, str]] = "start",
                       start_time: Optional[Union[datetime, date, str]] = None,
                       end_time: Optional[Union[datetime, date, str]] = None,
                       start_inclusive: Optional[bool] = None,
                       end_inclusive: Optional[bool] = None,
                       timezone: Optional[str] = None,
                       limit_per_market: Optional[int] = None,
                       sort: Optional[str] = None) -> DataCollection
```

Returns market metrics for specified markets, frequency and date range.

For more information on market metrics, see: https://docs.coinmetrics.io/api/v4#operation/getTimeseriesMarketMetrics

**Arguments**:

- `markets` (`list(str), str`): list of market ids. Market ids use the following naming convention: `exchangeName-baseAsset-quoteAsset-spot` for spot markets, `exchangeName-futuresSymbol-future` for futures markets, and `exchangeName-optionsSymbol-option` for options markets. e.g., `'coinbase-btc-usd-spot'`, `'bitmex-XBTUSD-future'`
- `metrics` (`list(str), str`): list of metrics, i.e. 'liquidations_reported_future_buy_units_1d'. See market metrics catalog for a list of supported metrics: https://docs.coinmetrics.io/api/v4#operation/getCatalogMarketMetrics
- `frequency` (`str`): frequency of the returned timeseries, e.g 15s, 1d, etc.
- `page_size` (`int`): number of items returned per page when calling the API. If the request times out, try using a smaller number.
- `paging_from` (`PagingFrom, str`): Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
- `start_time` (`datetime, date, str`): Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `end_time` (`datetime, date, str`): End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `start_inclusive` (`bool`): Flag to define if start timestamp must be included in the timeseries if present. True by default.
- `end_inclusive` (`bool`): Flag to define if end timestamp must be included in the timeseries if present. True by default.
- `timezone` (`str`): timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.
- `limit_per_market` (`int`): How many entries _per market_ the result should contain.
- `sort` (`str`): How results will be sorted. Metrics are sorted by (market, time) by default. If you want to sort
1d metrics by (time, market) you should choose time as value for the sort parameter. Sorting by time is useful
if you request metrics for a set of markets.

**Returns**:

`DataCollection`: Market Candles timeseries.

<a id="coinmetrics.api_client.CoinMetricsClient.get_market_candles"></a>

#### get\_market\_candles

```python
def get_market_candles(
        markets: Union[List[str], str],
        frequency: Optional[str] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[Union[PagingFrom, str]] = "start",
        start_time: Optional[Union[datetime, date, str]] = None,
        end_time: Optional[Union[datetime, date, str]] = None,
        start_inclusive: Optional[bool] = None,
        end_inclusive: Optional[bool] = None,
        timezone: Optional[str] = None,
        limit_per_market: Optional[int] = None) -> DataCollection
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

<a id="coinmetrics.api_client.CoinMetricsClient.get_market_trades"></a>

#### get\_market\_trades

```python
def get_market_trades(
        markets: Union[List[str], str],
        page_size: Optional[int] = None,
        paging_from: Optional[Union[PagingFrom, str]] = "start",
        start_time: Optional[Union[datetime, date, str]] = None,
        end_time: Optional[Union[datetime, date, str]] = None,
        start_inclusive: Optional[bool] = None,
        end_inclusive: Optional[bool] = None,
        timezone: Optional[str] = None,
        limit_per_market: Optional[int] = None,
        min_confirmations: Optional[int] = None) -> DataCollection
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
- `min_confirmations` (`int`): Specifies how many blocks behind the chain tip trades are based on. Default is 2.

**Returns**:

`DataCollection`: Market Trades timeseries.

<a id="coinmetrics.api_client.CoinMetricsClient.get_market_open_interest"></a>

#### get\_market\_open\_interest

```python
def get_market_open_interest(
        markets: Union[List[str], str],
        page_size: Optional[int] = None,
        paging_from: Optional[Union[PagingFrom, str]] = "start",
        start_time: Optional[Union[datetime, date, str]] = None,
        end_time: Optional[Union[datetime, date, str]] = None,
        start_inclusive: Optional[bool] = None,
        end_inclusive: Optional[bool] = None,
        timezone: Optional[str] = None,
        limit_per_market: Optional[int] = None) -> DataCollection
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

<a id="coinmetrics.api_client.CoinMetricsClient.get_market_liquidations"></a>

#### get\_market\_liquidations

```python
def get_market_liquidations(
        markets: Union[List[str], str],
        page_size: Optional[int] = None,
        paging_from: Optional[Union[PagingFrom, str]] = "start",
        start_time: Optional[Union[datetime, date, str]] = None,
        end_time: Optional[Union[datetime, date, str]] = None,
        start_inclusive: Optional[bool] = None,
        end_inclusive: Optional[bool] = None,
        timezone: Optional[str] = None,
        limit_per_market: Optional[int] = None) -> DataCollection
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

<a id="coinmetrics.api_client.CoinMetricsClient.get_market_funding_rates"></a>

#### get\_market\_funding\_rates

```python
def get_market_funding_rates(
        markets: Union[List[str], str],
        page_size: Optional[int] = None,
        paging_from: Optional[Union[PagingFrom, str]] = "start",
        start_time: Optional[Union[datetime, date, str]] = None,
        end_time: Optional[Union[datetime, date, str]] = None,
        start_inclusive: Optional[bool] = None,
        end_inclusive: Optional[bool] = None,
        timezone: Optional[str] = None,
        limit_per_market: Optional[int] = None) -> DataCollection
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

<a id="coinmetrics.api_client.CoinMetricsClient.get_market_orderbooks"></a>

#### get\_market\_orderbooks

```python
def get_market_orderbooks(
        markets: Union[List[str], str],
        frequency: Optional[str] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[Union[PagingFrom, str]] = "start",
        start_time: Optional[Union[datetime, date, str]] = None,
        end_time: Optional[Union[datetime, date, str]] = None,
        start_inclusive: Optional[bool] = None,
        end_inclusive: Optional[bool] = None,
        depth_limit: Optional[str] = "100",
        timezone: Optional[str] = None,
        limit_per_market: Optional[int] = None) -> DataCollection
```

Returns market order books for specified markets and date range.

For more information on order books, see: https://docs.coinmetrics.io/info/markets/orderbook

**Arguments**:

- `markets` (`list(str), str`): list of market ids. Market ids use the following naming convention: `exchangeName-baseAsset-quoteAsset-spot` for spot markets, `exchangeName-futuresSymbol-future` for futures markets, and `exchangeName-optionsSymbol-option` for options markets. e.g., `'coinbase-btc-usd-spot'`, `'bitmex-XBTUSD-future'`
- `frequency` (`str`): Default: "10s" The frequency at which market order books and quotes are provided. Supported values: 10s, 1m, 1h, 1d.
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

<a id="coinmetrics.api_client.CoinMetricsClient.get_market_quotes"></a>

#### get\_market\_quotes

```python
def get_market_quotes(
        markets: Union[List[str], str],
        frequency: Optional[str] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[Union[PagingFrom, str]] = "start",
        start_time: Optional[Union[datetime, date, str]] = None,
        end_time: Optional[Union[datetime, date, str]] = None,
        start_inclusive: Optional[bool] = None,
        end_inclusive: Optional[bool] = None,
        timezone: Optional[str] = None,
        limit_per_market: Optional[int] = None,
        include_one_sided: Optional[bool] = None) -> DataCollection
```

Returns market quotes for specified markets and date range.

For more information on quotes, see: https://docs.coinmetrics.io/info/markets/quotes

**Arguments**:

- `markets` (`list(str), str`): list of market ids. Market ids use the following naming convention: `exchangeName-baseAsset-quoteAsset-spot` for spot markets, `exchangeName-futuresSymbol-future` for futures markets, and `exchangeName-optionsSymbol-option` for options markets. e.g., `'coinbase-btc-usd-spot'`, `'bitmex-XBTUSD-future'`
- `frequency` (`str`): Default: "10s" The frequency at which market order books and quotes are provided. Supported values: 10s, 1m, 1h, 1d.
- `page_size` (`int`): number of items returned per page when calling the API. If the request times out, try using a smaller number.
- `paging_from` (`PagingFrom, str`): Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
- `start_time` (`datetime, date, str`): Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `end_time` (`datetime, date, str`): End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `start_inclusive` (`bool`): Flag to define if start timestamp must be included in the timeseries if present. True by default.
- `end_inclusive` (`bool`): Flag to define if end timestamp must be included in the timeseries if present. True by default.
- `timezone` (`str`): timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.
- `limit_per_market` (`int`): How many entries _per market_ the result should contain.
- `include_one_sided` (`bool`): Default: false Include one-side and empty books in quotes response.

**Returns**:

`DataCollection`: Market Quotes timeseries.

<a id="coinmetrics.api_client.CoinMetricsClient.get_market_contract_prices"></a>

#### get\_market\_contract\_prices

```python
def get_market_contract_prices(
        markets: Union[List[str], str],
        page_size: Optional[int] = None,
        paging_from: Optional[Union[PagingFrom, str]] = "start",
        start_time: Optional[Union[datetime, date, str]] = None,
        end_time: Optional[Union[datetime, date, str]] = None,
        start_inclusive: Optional[bool] = None,
        end_inclusive: Optional[bool] = None,
        timezone: Optional[str] = None,
        limit_per_market: Optional[int] = None) -> DataCollection
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

<a id="coinmetrics.api_client.CoinMetricsClient.get_market_implied_volatility"></a>

#### get\_market\_implied\_volatility

```python
def get_market_implied_volatility(
        markets: Union[List[str], str],
        page_size: Optional[int] = None,
        paging_from: Optional[Union[PagingFrom, str]] = "start",
        start_time: Optional[Union[datetime, date, str]] = None,
        end_time: Optional[Union[datetime, date, str]] = None,
        start_inclusive: Optional[bool] = None,
        end_inclusive: Optional[bool] = None,
        timezone: Optional[str] = None,
        limit_per_market: Optional[int] = None) -> DataCollection
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

<a id="coinmetrics.api_client.CoinMetricsClient.get_market_greeks"></a>

#### get\_market\_greeks

```python
def get_market_greeks(
        markets: Union[List[str], str],
        page_size: Optional[int] = None,
        paging_from: Optional[Union[PagingFrom, str]] = "start",
        start_time: Optional[Union[datetime, date, str]] = None,
        end_time: Optional[Union[datetime, date, str]] = None,
        start_inclusive: Optional[bool] = None,
        end_inclusive: Optional[bool] = None,
        timezone: Optional[str] = None,
        limit_per_market: Optional[int] = None) -> DataCollection
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

<a id="coinmetrics.api_client.CoinMetricsClient.get_mining_pool_tips_summary"></a>

#### get\_mining\_pool\_tips\_summary

```python
def get_mining_pool_tips_summary(
        assets: Union[List[str], str],
        page_size: Optional[int] = None,
        paging_from: Optional[Union[PagingFrom, str]] = "start",
        start_time: Optional[Union[datetime, date, str]] = None,
        end_time: Optional[Union[datetime, date, str]] = None,
        start_inclusive: Optional[bool] = None,
        end_inclusive: Optional[bool] = None,
        timezone: Optional[str] = None) -> DataCollection
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

<a id="coinmetrics.api_client.CoinMetricsClient.get_mempool_feerates"></a>

#### get\_mempool\_feerates

```python
def get_mempool_feerates(assets: Union[List[str], str],
                         page_size: Optional[int] = 200,
                         paging_from: Optional[Union[PagingFrom,
                                                     str]] = "start",
                         start_time: Optional[Union[datetime, date,
                                                    str]] = None,
                         end_time: Optional[Union[datetime, date, str]] = None,
                         start_inclusive: Optional[bool] = None,
                         end_inclusive: Optional[bool] = None,
                         timezone: Optional[str] = None) -> DataCollection
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

<a id="coinmetrics.api_client.CoinMetricsClient.get_stream_asset_metrics"></a>

#### get\_stream\_asset\_metrics

```python
def get_stream_asset_metrics(
        assets: Union[List[str], str],
        metrics: Union[List[str], str],
        frequency: Optional[str] = None,
        backfill: Union[Backfill, str] = Backfill.LATEST) -> CmStream
```

Returns timeseries stream of metrics for specified assets.

**Arguments**:

- `assets` (`list(str), str`): list of asset names, e.g. 'btc'
- `metrics` (`list(str), str`): list of _asset-specific_ metric names, e.g. 'PriceUSD'
- `frequency` (`str`): frequency of the returned timeseries, e.g 15s, 1d, etc.
- `backfill` (`str`): What data should be sent upon a connection ("latest" or "none"). By default the latest values are sent just before real-time data.

**Returns**:

`CmStream`: Asset Metrics timeseries stream.

<a id="coinmetrics.api_client.CoinMetricsClient.get_stream_market_trades"></a>

#### get\_stream\_market\_trades

```python
def get_stream_market_trades(
        markets: Union[List[str], str],
        backfill: Union[Backfill, str] = Backfill.LATEST) -> CmStream
```

Returns timeseries stream of market trades.

**Arguments**:

- `markets` (`list(str), str`): list of markets or market patterns like exchange-* or exchange-*-spot or *USDT-future.
- `backfill` (`str`): What data should be sent upon a connection ("latest" or "none"). By default the latest values are sent just before real-time data.

**Returns**:

`CmStream`: Market Trades timeseries stream.

<a id="coinmetrics.api_client.CoinMetricsClient.get_stream_market_orderbooks"></a>

#### get\_stream\_market\_orderbooks

```python
def get_stream_market_orderbooks(
        markets: Union[List[str], str],
        backfill: Union[Backfill, str] = Backfill.LATEST,
        depth_limit: Optional[str] = None) -> CmStream
```

Returns timeseries stream of market orderbooks.

**Arguments**:

- `markets` (`list(str), str`): list of markets or market patterns like exchange-* or exchange-*-spot or *USDT-future.
- `backfill` (`str`): What data should be sent upon a connection ("latest" or "none"). By default the latest values are sent just before real-time data.
- `depth_limit` (`str`): Default: 100. Supported Values: 100 "full_book". Book depth limit.

**Returns**:

`CmStream`: Market Orderbooks timeseries stream.

<a id="coinmetrics.api_client.CoinMetricsClient.get_stream_market_quotes"></a>

#### get\_stream\_market\_quotes

```python
def get_stream_market_quotes(
        markets: Union[List[str], str],
        backfill: Union[Backfill, str] = Backfill.LATEST,
        include_one_sided: Optional[bool] = None) -> CmStream
```

Returns timeseries stream of market quotes.

**Arguments**:

- `markets` (`list(str), str`): list of markets or market patterns like exchange-* or exchange-*-spot or *USDT-future.
- `backfill` (`str`): What data should be sent upon a connection ("latest" or "none"). By default the latest values are sent just before real-time data.
- `include_one_sided` (`bool`): Default: false. Include one-side and empty books in quotes response.

**Returns**:

`CmStream`: Market Quotes timeseries stream.

<a id="coinmetrics.api_client.CoinMetricsClient.get_stream_pair_quotes"></a>

#### get\_stream\_pair\_quotes

```python
def get_stream_pair_quotes(pairs: Union[str, List[str]],
                           aggregation_method: Optional[str] = None,
                           backfill: Optional[str] = None) -> CmStream
```

**Arguments**:

- `pairs` (`Optional[Union[str, List[str]]]`): Comma separated list of asset pairs. Use the /catalog-all/pairs endpoint for the full list of supported asset pairs.
- `aggregation_method` (`str`): The method to use for aggregation.
- `backfill` (`str`): What data should be sent upon a connection. By default the latest values are sent just before real-time data.

**Returns**:

`CmStream`: 

<a id="coinmetrics.api_client.CoinMetricsClient.get_stream_asset_quotes"></a>

#### get\_stream\_asset\_quotes

```python
def get_stream_asset_quotes(assets: Union[str, List[str]],
                            aggregation_method: Optional[str] = None,
                            backfill: Optional[str] = None) -> CmStream
```

**Arguments**:

- `assets` (`Union[str, List[str]]`): Comma separated list of assets. Use the /catalog-all/assets endpoint for the full list of supported assets.
- `aggregation_method` (`str`): The method to use for aggregation.
- `backfill` (`str`): What data should be sent upon a connection. By default the latest values are sent just before real-time data.

**Returns**:

`CmStream`: 

<a id="coinmetrics.api_client.CoinMetricsClient.get_stream_market_candles"></a>

#### get\_stream\_market\_candles

```python
def get_stream_market_candles(
        markets: Union[List[str], str],
        frequency: Optional[str] = None,
        backfill: Union[Backfill, str] = Backfill.LATEST) -> CmStream
```

Returns timeseries stream of market candles.

**Arguments**:

- `markets` (`list(str), str`): list of markets or market patterns like exchange-* or exchange-*-spot or *USDT-future.
- `frequency` (`str`): Candle duration. Supported values are 1m, 5m, 10m, 15m, 30m, 1h, 4h, 1d.
- `backfill` (`str`): What data should be sent upon a connection ("latest" or "none"). By default the latest values are sent just before real-time data.

**Returns**:

`CmStream`: Market Candles timeseries stream.

<a id="coinmetrics.api_client.CoinMetricsClient.get_stream_index_levels"></a>

#### get\_stream\_index\_levels

```python
def get_stream_index_levels(
        indexes: Union[List[str], str],
        include_verification: Optional[bool] = None,
        backfill: Union[Backfill, str] = Backfill.LATEST) -> CmStream
```

Returns timeseries stream of index levels.

**Arguments**:

- `indexes`: list of indxes or market patterns such as CMBIBTC
- `backfill` (`str`): What data should be sent upon a connection ("latest" or "none"). By default the latest values are sent just before real-time data.
- `include_verification`: Default: False If set to true, includes information about verification.

**Returns**:

`CmStream`: Index levels data timeseries stream.

<a id="coinmetrics.api_client.CoinMetricsClient.get_list_of_blocks"></a>

#### get\_list\_of\_blocks

```python
def get_list_of_blocks(asset: str,
                       block_hashes: Optional[Union[List[str], str]] = None,
                       heights: Optional[Union[List[str], str]] = None,
                       page_size: Optional[int] = None,
                       paging_from: Optional[Union[PagingFrom, str]] = "start",
                       start_time: Optional[Union[datetime, date, str]] = None,
                       end_time: Optional[Union[datetime, date, str]] = None,
                       start_height: Optional[int] = None,
                       end_height: Optional[int] = None,
                       start_inclusive: Optional[bool] = None,
                       end_inclusive: Optional[bool] = None,
                       timezone: Optional[str] = None) -> DataCollection
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
- `start_height` (`int`): The start height indicates the beginning block height for the set of data that are returned. Mutually exclusive with start_time
- `end_height` (`int`): The end height indicates the beginning block height for the set of data that are returned. Mutually exclusive with end_time
- `start_inclusive` (`bool`): Flag to define if start timestamp must be included in the timeseries if present. True by default.
- `end_inclusive` (`bool`): Flag to define if end timestamp must be included in the timeseries if present. True by default.
- `timezone` (`str`): timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.

**Returns**:

`DataCollection`: list of blockchain blocks metadata

<a id="coinmetrics.api_client.CoinMetricsClient.get_list_of_accounts"></a>

#### get\_list\_of\_accounts

```python
def get_list_of_accounts(asset: str,
                         accounts: Optional[Union[List[str], str]] = None,
                         page_size: Optional[int] = None,
                         paging_from: Optional[Union[PagingFrom,
                                                     str]] = "start",
                         start_time: Optional[Union[datetime, date,
                                                    str]] = None,
                         end_time: Optional[Union[datetime, date, str]] = None,
                         start_height: Optional[int] = None,
                         end_height: Optional[int] = None,
                         start_chain_sequence_number: Optional[int] = None,
                         end_chain_sequence_number: Optional[int] = None,
                         start_inclusive: Optional[bool] = None,
                         end_inclusive: Optional[bool] = None,
                         timezone: Optional[str] = None) -> DataCollection
```

Returns a list of blockchain accounts with their balances.

**Arguments**:

- `asset` (`str`): Asset name
- `accounts` (`str, list(str)`): Optional comma separated list of accounts to filter a response.
- `page_size` (`int`): number of items returned per page when calling the API. If the request times out, try using a smaller number.
- `paging_from` (`PagingFrom, str`): Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
- `start_time` (`datetime, date, str`): Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `end_time` (`datetime, date, str`): End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `start_height` (`int`): The start height indicates the beginning block height for the set of data that are returned. Mutually exclusive with start_time
- `end_height` (`int`): The end height indicates the beginning block height for the set of data that are returned. Mutually exclusive with end_time
- `start_chain_sequence_number` (`int`): The start height indicates the beginning block height for the set of data that are returned. Mutually exclusive with start_time
- `end_chain_sequence_number` (`int`): The end height indicates the beginning block height for the set of data that are returned. Mutually exclusive with end_time
- `start_inclusive` (`bool`): Flag to define if start timestamp must be included in the timeseries if present. True by default.
- `end_inclusive` (`bool`): Flag to define if end timestamp must be included in the timeseries if present. True by default.
- `timezone` (`str`): timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.

**Returns**:

`DataCollection`: list of blockchain accounts metadata

<a id="coinmetrics.api_client.CoinMetricsClient.get_list_of_transactions"></a>

#### get\_list\_of\_transactions

```python
def get_list_of_transactions(asset: str,
                             transaction_hashes: Optional[Union[List[str],
                                                                str]] = None,
                             block_hashes: Optional[Union[List[str],
                                                          str]] = None,
                             page_size: Optional[int] = None,
                             paging_from: Optional[Union[PagingFrom,
                                                         str]] = "start",
                             start_time: Optional[Union[datetime, date,
                                                        str]] = None,
                             end_time: Optional[Union[datetime, date,
                                                      str]] = None,
                             start_height: Optional[int] = None,
                             end_height: Optional[int] = None,
                             start_inclusive: Optional[bool] = None,
                             end_inclusive: Optional[bool] = None,
                             timezone: Optional[str] = None) -> DataCollection
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
- `start_height` (`int`): The start height indicates the beginning block height for the set of data that are returned. Mutually exclusive with start_time
- `end_height` (`int`): The end height indicates the beginning block height for the set of data that are returned. Mutually exclusive with end_time
- `start_inclusive` (`bool`): Flag to define if start timestamp must be included in the timeseries if present. True by default.
- `end_inclusive` (`bool`): Flag to define if end timestamp must be included in the timeseries if present. True by default.
- `timezone` (`str`): timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.

**Returns**:

`DataCollection`: list of transaction metadata

<a id="coinmetrics.api_client.CoinMetricsClient.get_list_of_balance_updates"></a>

#### get\_list\_of\_balance\_updates

```python
def get_list_of_balance_updates(
        asset: str,
        accounts: Optional[Union[List[str], str]] = None,
        transaction_hashes: Optional[Union[List[str], str]] = None,
        block_hashes: Optional[Union[List[str], str]] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[Union[PagingFrom, str]] = "start",
        start_time: Optional[Union[datetime, date, str]] = None,
        end_time: Optional[Union[datetime, date, str]] = None,
        start_height: Optional[int] = None,
        end_height: Optional[int] = None,
        start_chain_sequence_number: Optional[int] = None,
        end_chain_sequence_number: Optional[int] = None,
        start_inclusive: Optional[bool] = None,
        end_inclusive: Optional[bool] = None,
        timezone: Optional[str] = None) -> DataCollection
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
- `start_height` (`int`): The start height indicates the beginning block height for the set of data that are returned. Mutually exclusive with start_time
- `end_height` (`int`): The end height indicates the beginning block height for the set of data that are returned. Mutually exclusive with end_time
- `start_chain_sequence_number` (`int`): The start height indicates the beginning block height for the set of data that are returned. Mutually exclusive with start_time
- `end_chain_sequence_number` (`int`): The end height indicates the beginning block height for the set of data that are returned. Mutually exclusive with end_time
- `start_inclusive` (`bool`): Flag to define if start timestamp must be included in the timeseries if present. True by default.
- `end_inclusive` (`bool`): Flag to define if end timestamp must be included in the timeseries if present. True by default.
- `timezone` (`str`): timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.

**Returns**:

`DataCollection`: list of balance updates

<a id="coinmetrics.api_client.CoinMetricsClient.get_list_of_blocks_v2"></a>

#### get\_list\_of\_blocks\_v2

```python
def get_list_of_blocks_v2(asset: str,
                          block_hashes: Optional[Union[List[str], str]] = None,
                          heights: Optional[Union[List[str], str]] = None,
                          page_size: Optional[int] = None,
                          paging_from: Optional[Union[PagingFrom,
                                                      str]] = "start",
                          start_time: Optional[Union[datetime, date,
                                                     str]] = None,
                          end_time: Optional[Union[datetime, date,
                                                   str]] = None,
                          start_height: Optional[int] = None,
                          end_height: Optional[int] = None,
                          chain: Optional[bool] = None,
                          start_inclusive: Optional[bool] = None,
                          end_inclusive: Optional[bool] = None,
                          timezone: Optional[str] = None) -> DataCollection
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
- `start_height` (`int`): The start height indicates the beginning block height for the set of data that are returned. Mutually exclusive with start_time
- `end_height` (`int`): The end height indicates the beginning block height for the set of data that are returned. Mutually exclusive with end_time
- `chain` (`str`): Default: "main" Chain type. Supported values are main and all (includes both main and stale).
- `start_inclusive` (`bool`): Flag to define if start timestamp must be included in the timeseries if present. True by default.
- `end_inclusive` (`bool`): Flag to define if end timestamp must be included in the timeseries if present. True by default.
- `timezone` (`str`): timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.

**Returns**:

`DataCollection`: list of blockchain blocks metadata

<a id="coinmetrics.api_client.CoinMetricsClient.get_list_of_accounts_v2"></a>

#### get\_list\_of\_accounts\_v2

```python
def get_list_of_accounts_v2(asset: str,
                            accounts: Optional[Union[List[str], str]] = None,
                            page_size: Optional[int] = None,
                            paging_from: Optional[Union[PagingFrom,
                                                        str]] = "start",
                            start_time: Optional[Union[datetime, date,
                                                       str]] = None,
                            end_time: Optional[Union[datetime, date,
                                                     str]] = None,
                            start_height: Optional[int] = None,
                            end_height: Optional[int] = None,
                            start_chain_sequence_number: Optional[int] = None,
                            end_chain_sequence_number: Optional[int] = None,
                            start_inclusive: Optional[bool] = None,
                            end_inclusive: Optional[bool] = None,
                            timezone: Optional[str] = None) -> DataCollection
```

Returns a list of blockchain accounts with their balances.

**Arguments**:

- `asset` (`str`): Asset name
- `accounts` (`str, list(str)`): Optional comma separated list of accounts to filter a response.
- `page_size` (`int`): number of items returned per page when calling the API. If the request times out, try using a smaller number.
- `paging_from` (`PagingFrom, str`): Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
- `start_time` (`datetime, date, str`): Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `end_time` (`datetime, date, str`): End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `start_height` (`int`): The start height indicates the beginning block height for the set of data that are returned. Mutually exclusive with start_time
- `end_height` (`int`): The end height indicates the beginning block height for the set of data that are returned. Mutually exclusive with end_time
- `start_chain_sequence_number` (`int`): The start height indicates the beginning block height for the set of data that are returned. Mutually exclusive with start_time
- `end_chain_sequence_number` (`int`): The end height indicates the beginning block height for the set of data that are returned. Mutually exclusive with end_time
- `start_inclusive` (`bool`): Flag to define if start timestamp must be included in the timeseries if present. True by default.
- `end_inclusive` (`bool`): Flag to define if end timestamp must be included in the timeseries if present. True by default.
- `timezone` (`str`): timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.

**Returns**:

`DataCollection`: list of blockchain accounts metadata

<a id="coinmetrics.api_client.CoinMetricsClient.get_list_of_sub_accounts_v2"></a>

#### get\_list\_of\_sub\_accounts\_v2

```python
def get_list_of_sub_accounts_v2(
        asset: str,
        accounts: Optional[Union[List[str], str]] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[Union[PagingFrom, str]] = "start",
        start_time: Optional[Union[datetime, date, str]] = None,
        end_time: Optional[Union[datetime, date, str]] = None,
        start_height: Optional[int] = None,
        end_height: Optional[int] = None,
        start_chain_sequence_number: Optional[int] = None,
        end_chain_sequence_number: Optional[int] = None,
        start_inclusive: Optional[bool] = None,
        end_inclusive: Optional[bool] = None,
        timezone: Optional[str] = None) -> DataCollection
```

Returns a list of blockchain sub-accounts with their balances.

**Arguments**:

- `asset` (`str`): Asset name
- `accounts` (`str, list(str)`): Optional comma separated list of accounts to filter a response.
- `page_size` (`int`): number of items returned per page when calling the API. If the request times out, try using a smaller number.
- `paging_from` (`PagingFrom, str`): Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
- `start_time` (`datetime, date, str`): Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `end_time` (`datetime, date, str`): End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `start_height` (`int`): The start height indicates the beginning block height for the set of data that are returned. Mutually exclusive with start_time
- `end_height` (`int`): The end height indicates the beginning block height for the set of data that are returned. Mutually exclusive with end_time
- `start_chain_sequence_number` (`int`): The start height indicates the beginning block height for the set of data that are returned. Mutually exclusive with start_time
- `end_chain_sequence_number` (`int`): The end height indicates the beginning block height for the set of data that are returned. Mutually exclusive with end_time
- `start_inclusive` (`bool`): Flag to define if start timestamp must be included in the timeseries if present. True by default.
- `end_inclusive` (`bool`): Flag to define if end timestamp must be included in the timeseries if present. True by default.
- `timezone` (`str`): timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.

**Returns**:

`DataCollection`: list of blockchain accounts metadata

<a id="coinmetrics.api_client.CoinMetricsClient.get_list_of_transactions_v2"></a>

#### get\_list\_of\_transactions\_v2

```python
def get_list_of_transactions_v2(
        asset: str,
        txids: Optional[Union[List[str], str]] = None,
        block_hashes: Optional[Union[List[str], str]] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[Union[PagingFrom, str]] = "start",
        start_time: Optional[Union[datetime, date, str]] = None,
        end_time: Optional[Union[datetime, date, str]] = None,
        start_height: Optional[int] = None,
        end_height: Optional[int] = None,
        chain: Optional[str] = None,
        start_inclusive: Optional[bool] = None,
        end_inclusive: Optional[bool] = None,
        timezone: Optional[str] = None) -> DataCollection
```

Returns a list of blockchain transactions metadata.

**Arguments**:

- `asset` (`str`): Asset name
- `txids` (`str, list(str)`): Optional comma separated list of transaction identifiers (txid) to filter a response.
- `block_hashes` (`str, list(str)`): Optional comma separated list of block hashes to filter a response.
- `page_size` (`int`): number of items returned per page when calling the API. If the request times out, try using a smaller number.
- `paging_from` (`PagingFrom, str`): Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
- `start_time` (`datetime, date, str`): Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `end_time` (`datetime, date, str`): End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `start_height` (`int`): The start height indicates the beginning block height for the set of data that are returned. Mutually exclusive with start_time
- `end_height` (`int`): The end height indicates the beginning block height for the set of data that are returned. Mutually exclusive with end_time
- `chain` (`str`): Default: "main". Chain type. Supported values are main and all (includes both main and stale).
- `start_inclusive` (`bool`): Flag to define if start timestamp must be included in the timeseries if present. True by default.
- `end_inclusive` (`bool`): Flag to define if end timestamp must be included in the timeseries if present. True by default.
- `timezone` (`str`): timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.

**Returns**:

`DataCollection`: list of transaction metadata

<a id="coinmetrics.api_client.CoinMetricsClient.get_list_of_balance_updates_v2"></a>

#### get\_list\_of\_balance\_updates\_v2

```python
def get_list_of_balance_updates_v2(
        asset: str,
        accounts: Optional[Union[List[str], str]] = None,
        sub_accounts: Optional[Union[List[str], str]] = None,
        limit_per_account: Optional[int] = None,
        txids: Optional[Union[List[str], str]] = None,
        block_hashes: Optional[Union[List[str], str]] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[Union[PagingFrom, str]] = "start",
        start_time: Optional[Union[datetime, date, str]] = None,
        end_time: Optional[Union[datetime, date, str]] = None,
        start_height: Optional[int] = None,
        end_height: Optional[int] = None,
        start_chain_sequence_number: Optional[int] = None,
        end_chain_sequence_number: Optional[int] = None,
        include_sub_accounts: Optional[bool] = None,
        chain: Optional[str] = None,
        start_inclusive: Optional[bool] = None,
        end_inclusive: Optional[bool] = None,
        timezone: Optional[str] = None) -> DataCollection
```

Returns a list of blockchain accounts balance updates.

**Arguments**:

- `asset` (`str`): Asset name
- `accounts` (`str, list(str)`): Optional comma separated list of accounts to filter a response.
- `limit_per_account` (`int`): How many entries per account the result should contain. It is applicable when multiple accounts are requested.
- `txids` (`str, list(str)`): Optional comma separated list of transaction ids to filter a response.
- `block_hashes` (`str, list(str)`): Optional comma separated list of block hashes to filter a response.
- `page_size` (`int`): number of items returned per page when calling the API. If the request times out, try using a smaller number.
- `paging_from` (`PagingFrom, str`): Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
- `start_time` (`datetime, date, str`): Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `end_time` (`datetime, date, str`): End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
- `start_height` (`int`): The start height indicates the beginning block height for the set of data that are returned. Mutually exclusive with start_time
- `end_height` (`int`): The end height indicates the beginning block height for the set of data that are returned. Mutually exclusive with end_time
- `start_chain_sequence_number` (`int`): The start height indicates the beginning block height for the set of data that are returned. Mutually exclusive with start_time
- `end_chain_sequence_number` (`int`): The end height indicates the beginning block height for the set of data that are returned. Mutually exclusive with end_time
- `include_sub_accounts` (`bool`): bool indicating if the response should contain sub-accounts.
- `chain`: Chain type. Supported values are main and all (includes both main and stale).
- `start_inclusive` (`bool`): Flag to define if start timestamp must be included in the timeseries if present. True by default.
- `end_inclusive` (`bool`): Flag to define if end timestamp must be included in the timeseries if present. True by default.
- `timezone` (`str`): timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.

**Returns**:

`DataCollection`: list of balance updates

<a id="coinmetrics.api_client.CoinMetricsClient.get_full_transaction_for_block"></a>

#### get\_full\_transaction\_for\_block

```python
def get_full_transaction_for_block(asset: str, block_hash: str,
                                   txid: str) -> List[Dict[str, Any]]
```

**Arguments**:

- `asset` (`str`): Asset name.
- `block_hash` (`str`): Block hash.
- `txid` (`str`): Transaction identifier (txid).

**Returns**:

`DataCollection`: Blockchain full transaction.

<a id="coinmetrics.api_client.CoinMetricsClient.get_full_block"></a>

#### get\_full\_block

```python
def get_full_block(asset: str, block_hash: str) -> Dict[str, Any]
```

**Arguments**:

- `asset` (`str`): Asset name.
- `block_hash` (`str`): Block hash.

**Returns**:

`Dict[str, Any]`: Blockchain full block.

<a id="coinmetrics.api_client.CoinMetricsClient.get_full_block_v2"></a>

#### get\_full\_block\_v2

```python
def get_full_block_v2(
        asset: str, block_hash: str,
        include_sub_accounts: Optional[bool]) -> List[Dict[str, Any]]
```

Returns a full blockchain block with all transactions and balance updates.

**Arguments**:

- `asset` (`str`): Asset name
- `block_hash` (`str`): block hash
- `include_sub_accounts` (`bool`): Boolean indicating if the response should contain sub-accounts

**Returns**:

`list(dict(str), any)`: blockchain block data

<a id="coinmetrics.api_client.CoinMetricsClient.get_full_transaction"></a>

#### get\_full\_transaction

```python
def get_full_transaction(asset: str, txid: str) -> List[Dict[str, Any]]
```

**Arguments**:

- `asset` (`Optional[str]`): Asset name.
- `txid` (`Optional[str]`): Transaction identifier (txid).

**Returns**:

`DataCollection`: Blockchain full transaction.

<a id="coinmetrics.api_client.CoinMetricsClient.get_full_transaction_v2"></a>

#### get\_full\_transaction\_v2

```python
def get_full_transaction_v2(
        asset: str, txid: str,
        include_sub_accounts: Optional[bool]) -> List[Dict[str, Any]]
```

Returns a full blockchain transaction with all balance updates.

**Arguments**:

- `asset` (`str`): Asset name
- `txid` (`str`): transaction identifier
- `include_sub_accounts` (`bool`): Boolean indicating if the response should contain sub-accounts

**Returns**:

`list(dict(str), any)`: block transaction data

<a id="coinmetrics.api_client.CoinMetricsClient.get_full_transaction_for_block_v2"></a>

#### get\_full\_transaction\_for\_block\_v2

```python
def get_full_transaction_for_block_v2(
        asset: str, block_hash: str, txid: str,
        include_sub_accounts: Optional[bool]) -> List[Dict[str, Any]]
```

Returns a full blockchain transaction with all balance updates for a specific block.

**Arguments**:

- `asset` (`str`): Asset name
- `block_hash` (`str`): block hash
- `txid` (`str`): transaction identifier
- `include_sub_accounts` (`bool`): Boolean indicating if the response should contain sub-accounts

**Returns**:

`list(dict(str, Any))`: block transaction data with balance updates

<a id="coinmetrics.api_client.CoinMetricsClient.get_list_of_balance_updates_for_account_v2"></a>

#### get\_list\_of\_balance\_updates\_for\_account\_v2

```python
def get_list_of_balance_updates_for_account_v2(
        asset: str,
        account: str,
        txids: Optional[Union[str, List[str]]] = None,
        block_hashes: Optional[Union[str, List[str]]] = None,
        include_counterparties: Optional[bool] = None,
        start_time: Optional[Union[datetime, date, str]] = None,
        end_time: Optional[Union[datetime, date, str]] = None,
        start_height: Optional[int] = None,
        end_height: Optional[int] = None,
        start_chain_sequence_number: Optional[int] = None,
        end_chain_sequence_number: Optional[int] = None,
        include_sub_accounts: Optional[bool] = None,
        chain: Optional[str] = None,
        start_inclusive: Optional[bool] = None,
        end_inclusive: Optional[bool] = None,
        timezone: Optional[str] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[str] = None,
        next_page_token: Optional[str] = None) -> DataCollection
```

**Arguments**:

- `asset` (`Optional[str]`): Asset name.
- `account` (`Optional[str]`): Account id.
- `txids` (`Union[str, List[str]]`): Optional comma separated list of transaction identifiers (txid) to filter a response. The list must contain a single element for Community users.
- `block_hashes` (`Union[str, List[str]]`): Optional comma separated list of block hashes to filter a response. The list must contain a single element for Community users.
- `include_counterparties` (`bool`): Include information about the counterparties balance updates.
- `start_time` (`str`): Start of the time interval. This field refers to the `time` field in the response. Multiple formats of ISO 8601 are supported: `2006-01-20T00:00:00Z`, `2006-01-20T00:00:00.000Z`, `2006-01-20T00:00:00.123456Z`, `2006-01-20T00:00:00.123456789Z`, `2006-01-20`, `20060120`. Inclusive by default. Mutually exclusive with `start_height`. UTC timezone by default. `Z` suffix is optional and `timezone` parameter has a priority over it. If `start_time` is omitted, response will include time series from the **earliest** time available. This parameter is disabled for Community users.
- `end_time` (`str`): End of the time interval. This field refers to the `time` field in the response. Multiple formats of ISO 8601 are supported: `2006-01-20T00:00:00Z`, `2006-01-20T00:00:00.000Z`, `2006-01-20T00:00:00.123456Z`, `2006-01-20T00:00:00.123456789Z`, `2006-01-20`, `20060120`. Inclusive by default. Mutually exclusive with `end_height`. UTC timezone by default. `Z` suffix is optional and `timezone` parameter has a priority over it. If `end_time` is omitted, response will include time series up to the **latest** time available. This parameter is disabled for Community users.
- `start_height` (`int`): The start height indicates the beginning block height for the set of data that are returned. Inclusive by default. Mutually exclusive with `start_time`. This parameter is disabled for Community users.
- `end_height` (`int`): The end height indicates the ending block height for the set of data that are returned. Inclusive by default. Mutually exclusive with `end_time`. This parameter is disabled for Community users.
- `start_chain_sequence_number` (`int`): Start of the `chain_sequence_number` interval. This parameter is disabled for Community users.
- `end_chain_sequence_number` (`int`): End of the `chain_sequence_number` interval. This parameter is disabled for Community users.
- `include_sub_accounts` (`bool`): Boolean indicating if the response should contain sub-accounts. This parameter is disabled for Community users.
- `chain` (`str`): Chain type. Supported values are `main` and `all` (includes both main and stale). This parameter is disabled for Community users.
- `start_inclusive` (`bool`): Inclusive or exclusive corresponding `start_*` parameters. This parameter is disabled for Community users.
- `end_inclusive` (`bool`): Inclusive or exclusive corresponding `end_*` parameters. This parameter is disabled for Community users.
- `timezone` (`str`): Timezone name for `start_time` and `end_time` timestamps. This parameter does not modify the output times, which are always `UTC`. Format is defined by TZ database.
- `page_size` (`int`): Number of items per single page of results. This parameter is disabled for Community users.
- `paging_from` (`str`): Where does the first page start, at the start of the interval or at the end.
- `next_page_token` (`str`): Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.

**Returns**:

`DataCollection`: Blockchain balance updates for account.

<a id="coinmetrics.api_client.CoinMetricsClient.get_transaction_tracker"></a>

#### get\_transaction\_tracker

```python
def get_transaction_tracker(
    asset: str,
    addresses: Optional[Union[List[str], str]] = None,
    txids: Optional[Union[List[str], str]] = None,
    replacements_for_txids: Optional[Union[List[str], str]] = None,
    replacements_only: Optional[bool] = None,
    page_size: Optional[int] = None,
    paging_from: Optional[Union[PagingFrom, str]] = "start",
    start_time: Optional[Union[datetime, date, str]] = None,
    end_time: Optional[Union[datetime, date, str]] = None,
    start_inclusive: Optional[bool] = None,
    end_inclusive: Optional[bool] = None,
    timezone: Optional[str] = None,
    unconfirmed_only: Optional[bool] = None
) -> TransactionTrackerDataCollection
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

`TransactionTrackerDataCollection`: status updates for the specified or all transactions.

<a id="coinmetrics.api_client.CoinMetricsClient.get_taxonomy_assets"></a>

#### get\_taxonomy\_assets

```python
def get_taxonomy_assets(assets: Optional[List[str]] = None,
                        class_ids: Optional[List[str]] = None,
                        sector_ids: Optional[List[str]] = None,
                        subsector_ids: Optional[List[str]] = None,
                        classification_start_time: Optional[str] = None,
                        classification_end_time: Optional[str] = None,
                        end_inclusive: Optional[bool] = None,
                        start_inclusive: Optional[bool] = None,
                        page_size: Optional[int] = None,
                        paging_from: Optional[str] = None,
                        version: Optional[str] = None) -> DataCollection
```

Returns assets with information about their sector, industry, and industry group IDs. By default reutrns all

covered assets

**Arguments**:

- `assets` (`Optional[List[str]]`): Asset names
- `class_ids` (`Optional[List[str]]`): List of class identifiers.
- `sector_ids` (`Optional[List[str]]`): Lst of sector identifiers.
- `subsector_ids` (`Optional[List[str]]`): List of subsector identifiers
- `classification_start_time` (`Optional[str]`): Start time for the taxonomy assets. ISO-8601 format date. Inclusive by default
- `classification_end_time` (`Optional[str]`): End time for the taxonomy assets. ISO-8601 format date. Inclusive by default
- `start_inclusive` (`bool`): Flag to define if start timestamp must be included in the timeseries if present. True by default.
- `end_inclusive` (`bool`): Flag to define if end timestamp must be included in the timeseries if present. True by default.
- `page_size` (`Optional[int]`): Page size for # of assets to return, will default to 100
- `paging_from` (`Optional[str]`): Which direction to page from "start" or "end". "end" by default
- `version` (`Optional[str]`): Version to query, default is "latest".

**Returns**:

`Datacollection`: Returns a data collection containing the taxonomy assets

<a id="coinmetrics.api_client.CoinMetricsClient.get_taxonomy_assets_metadata"></a>

#### get\_taxonomy\_assets\_metadata

```python
def get_taxonomy_assets_metadata(
        start_time: Optional[Union[datetime, date, str]] = None,
        end_time: Optional[Union[datetime, date, str]] = None,
        start_inclusive: Optional[bool] = None,
        end_inclusive: Optional[bool] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[str] = None,
        version: Optional[str] = None) -> DataCollection
```

Returns metadata about the assets, sectors, and industries included in the CM taxonomy

**Arguments**:

- `start_time` (`Optional[Union[datetime, date, str]]`): Start time for the taxonomy version file. ISO-8601 format date. Inclusive by default
- `end_time` (`Optional[Union[datetime, date, str]]`): End time for the taxonomy version file. ISO-8601 format date. Exclusive by default
- `start_inclusive` (`str`): Start time of taxonomy version.
- `end_inclusive` (`str`): End time of taxonomy version.
- `page_size` (`Optional[int]`): Page size for # of asset metadata to return, will default to 100
- `paging_from` (`Optional[str]`): Which direction to page from "start" or "end". "end" by default
- `version` (`Optional[str]`): Version to query, default is "latest".

**Returns**:

`Datacollection`: Returns a data collection containing the taxonomy assets

<a id="coinmetrics.api_client.CoinMetricsClient.get_asset_profiles"></a>

#### get\_asset\_profiles

```python
def get_asset_profiles(assets: Optional[Union[List[str], str]] = None,
                       full_names: Optional[Union[List[str], str]] = None,
                       page_size: Optional[int] = None,
                       paging_from: Optional[str] = None) -> DataCollection
```

Returns profile data for assets, ordered by asset

**Arguments**:

- `assets` (`Optional[Union[List[str], str]]`): Returns profile data for assets.
- `full_names` (`Optional[Union[List[str], str]]`): Comma separated list of asset full names. By default profile data for all assets is returned. Mutually exclusive with assets parameter.
- `page_size` (`int`): Number of items per single page of results.
- `paging_from` (`int`): Where does the first page start, at the "start" of the interval or at the "end"

<a id="coinmetrics.api_client.CoinMetricsClient.reference_data_asset_metrics"></a>

#### reference\_data\_asset\_metrics

```python
def reference_data_asset_metrics(
        metrics: Optional[Union[str, List[str]]] = None,
        reviewable: Optional[bool] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[str] = None) -> DataCollection
```

**Arguments**:

- `metrics` (`Optional[Union[str, List[str]]]`): Comma separated list of metrics. By default all metrics are returned.
- `reviewable` (`Optional[bool]`): Limit to human-reviewable metrics. By default all metrics are returned.
- `page_size` (`Optional[int]`): Number of items per single page of results.
- `paging_from` (`Optional[str]`): Where does the first page start, at the start of the interval or at the end.

**Returns**:

`DataCollection`: List of asset metrics metadata.

<a id="coinmetrics.api_client.CoinMetricsClient.reference_data_exchange_metrics"></a>

#### reference\_data\_exchange\_metrics

```python
def reference_data_exchange_metrics(
        metrics: Optional[Union[str, List[str]]] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[str] = None) -> DataCollection
```

**Arguments**:

- `metrics` (`Optional[Union[str, List[str]]]`): Comma separated list of metrics. By default all metrics are returned.
- `page_size` (`Optional[int]`): Number of items per single page of results.
- `paging_from` (`Optional[str]`): Where does the first page start, at the start of the interval or at the end.

**Returns**:

`DataCollection`: List of exchange metrics metadata.

<a id="coinmetrics.api_client.CoinMetricsClient.reference_data_exchange_asset_metrics"></a>

#### reference\_data\_exchange\_asset\_metrics

```python
def reference_data_exchange_asset_metrics(
        metrics: Optional[Union[str, List[str]]] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[str] = None) -> DataCollection
```

**Arguments**:

- `metrics` (`Optional[Union[str, List[str]]]`): Comma separated list of metrics. By default all metrics are returned.
- `page_size` (`Optional[int]`): Number of items per single page of results.
- `paging_from` (`Optional[str]`): Where does the first page start, at the start of the interval or at the end.

**Returns**:

`DataCollection`: List of exchange asset metrics metadata.

<a id="coinmetrics.api_client.CoinMetricsClient.reference_data_pair_metrics"></a>

#### reference\_data\_pair\_metrics

```python
def reference_data_pair_metrics(
        metrics: Optional[Union[str, List[str]]] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[str] = None) -> DataCollection
```

**Arguments**:

- `metrics` (`Optional[Union[str, List[str]]]`): Comma separated list of metrics. By default all metrics are returned.
- `page_size` (`Optional[int]`): Number of items per single page of results.
- `paging_from` (`Optional[str]`): Where does the first page start, at the start of the interval or at the end.

**Returns**:

`DataCollection`: List of pair metrics metadata.

<a id="coinmetrics.api_client.CoinMetricsClient.reference_data_institution_metrics"></a>

#### reference\_data\_institution\_metrics

```python
def reference_data_institution_metrics(
        metrics: Optional[Union[str, List[str]]] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[str] = None) -> DataCollection
```

**Arguments**:

- `metrics` (`Optional[Union[str, List[str]]]`): Comma separated list of metrics. By default all metrics are returned.
- `page_size` (`Optional[int]`): Number of items per single page of results.
- `paging_from` (`Optional[str]`): Where does the first page start, at the start of the interval or at the end.

**Returns**:

`DataCollection`: List of institution metrics metadata.

