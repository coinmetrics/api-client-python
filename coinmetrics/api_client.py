import logging
import socket
from datetime import date, datetime
from logging import getLogger
from typing import Any, Dict, List, Optional, Union, cast
from urllib.parse import urlencode

import requests
from requests import HTTPError, Response
import websocket  # type: ignore

from coinmetrics._utils import retry, transform_url_params_values_to_str
from coinmetrics import __version__ as version
from coinmetrics._exceptions import CoinMetricsClientQueryParamsException

try:
    import ujson as json
except ImportError:
    # fall back to std json package
    import json  # type: ignore

from coinmetrics._typing import (
    DataReturnType,
    MessageHandlerType,
)
from coinmetrics.constants import PagingFrom, Backfill
from coinmetrics._data_collection import DataCollection
from coinmetrics._catalogs import (
    CatalogAssetsData,
    CatalogAssetAlertsData,
    CatalogAssetPairsData,
    CatalogAssetPairCandlesData,
    CatalogExchangeAssetsData,
    CatalogExchangesData,
    CatalogIndexesData,
    CatalogInstitutionsData,
    CatalogMarketsData,
    CatalogMetricsData,
    CatalogMarketMetricsData,
    CatalogMarketCandlesData,
    CatalogMarketTradesData,
    CatalogExchangeAssetMetricsData,
    CatalogPairMetricsData,
    CatalogInstitutionMetricsData,
    CatalogMarketOrderbooksData,
)

logger = getLogger("cm_client")

try:
    import pandas as pd  # type: ignore
except ImportError:
    pd = None
    logger.warning(
        "Pandas export is unavailable. Install pandas to unlock dataframe functions."
    )


class CmStream:
    def __init__(self, ws_url: str):
        self.ws_url = ws_url

    def run(
        self, on_message: MessageHandlerType = None, on_error: MessageHandlerType = None
    ) -> None:
        if on_message is None:
            on_message = self._on_message
        if on_error is None:
            on_error = self._on_error

        ws = websocket.WebSocketApp(
            self.ws_url, on_message=on_message, on_error=on_error
        )
        self.ws = ws
        self.ws.run_forever()

    def _on_message(self, stream: websocket.WebSocketApp, message: str) -> None:
        print(f"{message}")

    def _on_error(self, stream: websocket.WebSocketApp, message: str) -> None:
        data = json.loads(message)
        print(f"{data['error']}")


class CoinMetricsClient:
    def __init__(
        self,
        api_key: str = "",
        verify_ssl_certs: Union[bool, str] = True,
        proxy_url: Optional[str] = None,
        session: Optional[requests.Session] = None,
        debug_mode: bool = False,
        verbose: bool = False,
    ):
        self._api_key_url_str = "api_key={}".format(api_key) if api_key else ""

        self._verify_ssl_certs = verify_ssl_certs

        api_path_prefix = ""
        if not api_key:
            api_path_prefix = "community-"
        self._api_base_url = "https://{}api.coinmetrics.io/v4".format(api_path_prefix)
        self._ws_api_base_url = "wss://{}api.coinmetrics.io/v4".format(api_path_prefix)
        self._http_header = {"Api-Client-Version": version}
        self._proxies = {"http": proxy_url, "https": proxy_url}
        if session is None:
            self._session = requests.Session()
            self._session.verify = self._verify_ssl_certs
            self._session.headers.update({"Api-Client-Version": version})
            self._session.proxies.update({"http": proxy_url, "https": proxy_url})  # type: ignore
        else:
            self._session = session

        self.debug_mode = debug_mode
        self.verbose = verbose

        if self.verbose:
            logger.setLevel(level=logging.INFO)
            format = logging.Formatter("[%(levelname)s] %(asctime)s - %(message)s")
            handler = logging.StreamHandler()
            handler.setFormatter(fmt=format)
            logger.addHandler(handler)

        if self.debug_mode:
            logger.setLevel(level=logging.DEBUG)
            format = logging.Formatter("[%(levelname)s] %(asctime)s - %(message)s")
            handler = logging.StreamHandler()
            handler.setFormatter(fmt=format)
            logger.addHandler(handler)
            file_name = f"cm_api_client_debug_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.txt"
            file_handler = logging.FileHandler(file_name)
            file_handler.setFormatter(fmt=format)
            logger.addHandler(file_handler)
            logger.debug(
                msg=f"Starting API Client debugging session. logging to stdout and {file_name}"
            )
            logger.debug(msg=f"Using coinmetrics version {version}")
            state_of_client = self.__dict__.copy()
            del state_of_client["_api_key_url_str"]
            logger.debug(
                msg=f"Current state of API Client, excluding API KEY: {state_of_client}"
            )

    def catalog_assets(
            self,
            assets: Optional[Union[List[str], str]] = None,
            include: Optional[Union[List[str], str]] = None,
            exclude: Optional[Union[List[str], str]] = None
    ) -> CatalogAssetsData:
        """
        Returns meta information about _available_ assets.

        :param assets: A single asset or a list of assets to return info for. If no assets provided, all available assets are returned.
        :type assets: list(str), str
        :param include: list of fields to include in response. Supported values are metrics, markets, exchanges. Included by default if omitted.
        :type include: list(str), str
        :param exclude: list of fields to include in response. Supported values are metrics, markets, exchanges. Included by default if omitted.
        :type exclude: list(str), str
        :return: Information that is available for requested assets, like: Full name, metrics and available frequencies, markets, exchanges, etc.
        :rtype: list(dict(str, any))
        """
        params: Dict[str, Any] = {"assets": assets,
                                  "include": include,
                                  "exclude": exclude}
        return CatalogAssetsData(self._get_data("catalog/assets", params)["data"])

    def catalog_asset_alerts(
        self,
        assets: Optional[Union[List[str], str]] = None,
        alerts: Optional[Union[List[str], str]] = None,
    ) -> CatalogAssetAlertsData:
        """
        Returns meta information about _available_ assets.

        :param assets: A single asset or a list of assets to return info for. If no assets provided, all available assets are returned.
        :type assets: list(str), str
        :param alerts: A single alert or alert name to return info for. If no alerts provided, all available alerts are returned.
        :type alerts: list(str), str
        :return: Information that is available for requested assets alerts.
        :rtype: list(dict(str, any))
        """
        params: Dict[str, Any] = {"assets": assets, "alerts": alerts}
        return CatalogAssetAlertsData(self._get_data("catalog/alerts", params)["data"])

    def catalog_asset_pairs(
        self, asset_pairs: Optional[Union[List[str], str]] = None
    ) -> CatalogAssetPairsData:
        """
        Returns meta information about _available_ asset-asset pairs

        :param asset_pairs: A single asset-asset pair (e.g. "btc-eth") or a list of asset-asset pairs to return info for. If none are provided, all available pairs are returned.
        :type asset_pairs: list(str), str
        :return: Information that is available for requested asset-asset pair like metrics and their respective frequencies and time ranges
        :rtype: list(dict(str, any))
        """
        params: Dict[str, Any] = {"pairs": asset_pairs}
        return CatalogAssetPairsData(self._get_data("catalog/pairs", params)["data"])

    def catalog_asset_metrics(
        self,
        metrics: Optional[Union[List[str], str]] = None,
        reviewable: Optional[bool] = None,
    ) -> CatalogMetricsData:
        """
        Returns list of _available_ asset metrics along with information for them like
        description, category, precision and assets for which a metric is available.

        :param metrics: A single asset metric name or a list of metrics to return info for. If no metrics provided, all available metrics are returned.
        :type metrics: list(str), str
        :param reviewable: Show only reviewable or non-reviewable by human metrics. By default all metrics are shown.
        :type reviewable: bool
        :return: Information about asset metrics that correspond to a filter along with meta information like: description, category, precision and assets for which a metric is available.
        :rtype: list(dict(str, any))
        """
        params: Dict[str, Any] = {"metrics": metrics, "reviewable": reviewable}
        return CatalogMetricsData(
            self._get_data("catalog/asset-metrics", params)["data"]
        )

    def catalog_exchange_metrics(
        self,
        metrics: Optional[Union[List[str], str]] = None,
        reviewable: Optional[bool] = None,
    ) -> CatalogMetricsData:
        """
        Returns list of _available_ exchange metrics along with information for them like
        description, category, precision and assets for which a metric is available.

        :param metrics: A single exchange metric name or a list of metrics to return info for. If no metrics provided, all available metrics are returned.
        :type metrics: list(str), str
        :param reviewable: Show only reviewable or non-reviewable by human metrics. By default all metrics are shown.
        :type reviewable: bool
        :return: Information about exchange metrics that correspond to a filter along with meta information like: description, category, precision and assets for which a metric is available.
        :rtype: list(dict(str, any))
        """
        params: Dict[str, Any] = {"metrics": metrics, "reviewable": reviewable}
        return CatalogMetricsData(
            self._get_data("catalog/exchange-metrics", params)["data"]
        )

    def catalog_exchange_asset_metrics(
        self,
        metrics: Optional[Union[List[str], str]] = None,
        reviewable: Optional[bool] = None,
    ) -> CatalogExchangeAssetMetricsData:
        """
        Returns list of _available_ exchange metrics along with information for them like
        description, category, precision and assets for which a metric is available.

        :param metrics: A single exchange metric name or a list of metrics to return info for. If no metrics provided, all available metrics are returned.
        :type metrics: list(str), str
        :param reviewable: Show only reviewable or non-reviewable by human metrics. By default all metrics are shown.
        :type reviewable: bool
        :return: Information about exchange metrics that correspond to a filter along with meta information like: description, category, precision and assets for which a metric is available.
        :rtype: list(dict(str, any))
        """
        params: Dict[str, Any] = {"metrics": metrics, "reviewable": reviewable}
        return CatalogExchangeAssetMetricsData(
            self._get_data("catalog/exchange-asset-metrics", params)["data"]
        )

    def catalog_pair_metrics(
        self,
        metrics: Optional[Union[List[str], str]] = None,
        reviewable: Optional[bool] = None,
    ) -> CatalogPairMetricsData:
        """
        Returns list of _available_ pair metrics along with information for them like
        description, category, precision and assets for which a metric is available.

        :param metrics: A single pair metric name or a list of metrics to return info for. If no metrics provided, all available metrics are returned.
        :type metrics: list(str), str
        :param reviewable: Show only reviewable or non-reviewable by human metrics. By default all metrics are shown.
        :type reviewable: bool
        :return: Information about pair metrics that correspond to a filter along with meta information like: description, category, precision and assets for which a metric is available.
        :rtype: list(dict(str, any))
        """
        params: Dict[str, Any] = {"metrics": metrics, "reviewable": reviewable}
        return CatalogPairMetricsData(
            self._get_data("catalog/pair-metrics", params)["data"]
        )

    def catalog_institution_metrics(
        self,
        metrics: Optional[Union[List[str], str]] = None,
        reviewable: Optional[bool] = None,
    ) -> CatalogInstitutionMetricsData:
        """
        Returns list of _available_ institution metrics along with information for them like
        description, category, precision and assets for which a metric is available.

        :param metrics: A single institution metric name or a list of metrics to return info for. If no metrics provided, all available metrics are returned.
        :type metrics: list(str), str
        :param reviewable: Show only reviewable or non-reviewable by human metrics. By default all metrics are shown.
        :type reviewable: bool
        :return: Information about institution metrics that correspond to a filter along with meta information like: description, category, precision and assets for which a metric is available.
        :rtype: list(dict(str, any))
        """
        params: Dict[str, Any] = {"metrics": metrics, "reviewable": reviewable}
        return CatalogInstitutionMetricsData(
            self._get_data("catalog/institution-metrics", params)["data"]
        )

    def catalog_asset_pair_candles(
        self, asset_pairs: Optional[Union[List[str], str]] = None
    ) -> CatalogAssetPairCandlesData:
        """
        Returns meta information about _available_ asset-asset pairs

        :param asset_pairs: A single asset-asset pair (e.g. "btc-eth") or a list of asset-asset pairs to return info for. If none are provided, all available pairs are returned.
        :type asset_pairs: list(str), str
        :return: Returns a list of available asset pair candles along with the time ranges of available data per candle duration.
        :rtype: list(dict(str, any))
        """
        params: Dict[str, Any] = {"pairs": asset_pairs}
        return CatalogAssetPairCandlesData(
            self._get_data("catalog/pair-candles", params)["data"]
        )

    def catalog_exchanges(
        self, exchanges: Optional[Union[List[str], str]] = None
    ) -> CatalogExchangesData:
        """
        Returns meta information about exchanges.

        :param exchanges: A single exchange name or a list of exchanges to return info for. If no exchanges provided, all available exchanges are returned.
        :type exchanges: list(str), str
        :return: Information that is available for requested exchanges, like: markets, min and max time available.
        :rtype: list(dict(str, any))
        """
        params: Dict[str, Any] = {"exchanges": exchanges}
        return CatalogExchangesData(self._get_data("catalog/exchanges", params)["data"])

    def catalog_exchange_assets(
        self, exchange_assets: Optional[Union[List[str], str]] = None
    ) -> CatalogExchangeAssetsData:
        """
        Returns meta information about _available_ exchange-asset pairs

        :param exchange_assets: A single exchange-asset pair (e.g. "binance-btc") or a list of exchange-asset pairs to return info for. If none are provided, all available pairs are returned.
        :type exchange_assets: list(str), str
        :return: Information that is available for requested exchange-asset pair like metrics and their respective frequencies and time ranges
        :rtype: list(dict(str, any))
        """
        params: Dict[str, Any] = {"exchange_assets": exchange_assets}
        return CatalogExchangeAssetsData(
            self._get_data("catalog/exchange-assets", params)["data"]
        )

    def catalog_indexes(
        self, indexes: Optional[Union[List[str], str]] = None
    ) -> CatalogIndexesData:
        """
        Returns meta information about _available_ indexes.

        :param indexes: A single index name or a list of indexes to return info for. If no indexes provided, all available indexes are returned.
        :type indexes: list(str), str
        :return: Information that is available for requested indexes, like: Full name, and available frequencies.
        :rtype: list(dict(str, any))
        """
        params: Dict[str, Any] = {"indexes": indexes}
        return CatalogIndexesData(self._get_data("catalog/indexes", params)["data"])

    def catalog_index_candles(
        self, indexes: Optional[Union[List[str], str]] = None
    ) -> CatalogMarketCandlesData:
        """
        Returns meta information about _available_ index candles.

        :param indexes: A single index name or a list of indexes to return info for. If no indexes provided, all available index candles are returned.
        :type indexes: list(str), str
        :return: Information that is available for requested index candles, like: Full name, and available frequencies.
        :rtype: list(dict(str, any))
        """
        params: Dict[str, Any] = {"indexes": indexes}
        return CatalogMarketCandlesData(
            self._get_data("catalog/index-candles", params)["data"]
        )

    def catalog_institutions(
        self, institutions: Optional[Union[List[str], str]] = None
    ) -> CatalogInstitutionsData:
        """
        Returns meta information about _available_ institutions

        :param institutions: A single institution (e.g. "grayscale") or a list of institutions to return info for. If none are provided, all available pairs are returned.
        :type institutions: list(str), str
        :return: Information that is available for requested institution like metrics and their respective frequencies and time ranges.
        :rtype: list(dict(str, any))
        """
        params: Dict[str, Any] = {"institutions": institutions}
        return CatalogInstitutionsData(
            self._get_data("catalog/institutions", params)["data"]
        )

    def catalog_markets(
        self,
        markets: Optional[Union[List[str], str]] = None,
        market_type: Optional[str] = None,
        exchange: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None,
        include: Optional[Union[List[str], str]] = None,
        exclude: Optional[Union[List[str], str]] = None
    ) -> CatalogMarketsData:
        """
        Returns list of _available_ markets that correspond to a filter. If no filter is set, returns all available assets.

        :param markets: list of market names, e.g. 'coinbase-btc-usd-spot'
        :type markets: list(str), str
        :param market_type: Type of market: "spot", "future", "option"
        :type market_type: str
        :param exchange: name of the exchange
        :type exchange: str
        :param base: name of base asset
        :type base: str
        :param quote: name of quote asset
        :type quote: str
        :param asset: name of either base or quote asset
        :type asset: str
        :param symbol: name of a symbol. Usually used for futures contracts.
        :type symbol: str
        :param include: list of fields to include in response. Supported values are trades, orderbooks,
        quotes, funding_rates, openinterest, liquidations. Included by default if omitted.
        :type include: list(str), str
        :param exclude: list of fields to exclude from response. Supported values are trades, orderbooks,
         quotes, funding_rates, openinterest, liquidations. Included by default if omitted.
        :type exclude: list(str), str
        :return: Information about markets that correspond to a filter along with meta information like: type of market and min and max available time frames.
        :rtype: list(dict(str, any))
        """
        params: Dict[str, Any] = {
            "markets": markets,
            "type": market_type,
            "exchange": exchange,
            "base": base,
            "quote": quote,
            "asset": asset,
            "symbol": symbol,
            "include": include,
            "exclude": exclude
        }
        return CatalogMarketsData(self._get_data("catalog/markets", params)["data"])

    def catalog_market_trades(
        self,
        markets: Optional[Union[List[str], str]] = None,
        market_type: Optional[str] = None,
        exchange: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None,
    ) -> CatalogMarketTradesData:
        """
        Returns a list of markets with trades support along with the time ranges of available data.

        :param markets: list of market names, e.g. 'coinbase-btc-usd-spot'
        :type markets: list(str), str
        :param market_type: Type of market: "spot", "future", "option"
        :type market_type: str
        :param exchange: name of the exchange
        :type exchange: str
        :param base: name of base asset
        :type base: str
        :param quote: name of quote asset
        :type quote: str
        :param asset: name of either base or quote asset
        :type asset: str
        :param symbol: name of a symbol. Usually used for futures contracts.
        :type symbol: str
        :return: Information about market trades that are available for the provided filter, as well as the time frames they are available
        :rtype: list(dict(str, any))
        """
        params: Dict[str, Any] = {
            "markets": markets,
            "type": market_type,
            "exchange": exchange,
            "base": base,
            "quote": quote,
            "asset": asset,
            "symbol": symbol,
        }
        return CatalogMarketTradesData(
            self._get_data("catalog/market-trades", params)["data"]
        )

    def catalog_metrics(
        self,
        metrics: Optional[Union[List[str], str]] = None,
        reviewable: Optional[bool] = None,
    ) -> CatalogMetricsData:
        """
        Returns list of _available_ metrics along with information for them like
        description, category, precision and assets for which a metric is available.

        :param metrics: A single metric name or a list of metrics to return info for. If no metrics provided, all available metrics are returned.
        :type metrics: list(str), str
        :param reviewable: Show only reviewable or non-reviewable by human metrics. By default all metrics are shown.
        :type reviewable: bool
        :return: Information about metrics that correspond to a filter along with meta information like: description, category, precision and assets for which a metric is available.
        :rtype: list(dict(str, any))
        """
        params: Dict[str, Any] = {"metrics": metrics, "reviewable": reviewable}
        return CatalogMetricsData(self._get_data("catalog/metrics", params)["data"])

    def catalog_market_metrics(
        self,
        markets: Optional[Union[List[str], str]] = None,
        market_type: Optional[str] = None,
        exchange: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None,
    ) -> CatalogMarketMetricsData:
        """
        Returns list of _available_ markets with metrics support along woth time ranges of available data per metric.

        :param markets: list of market names, e.g. 'coinbase-btc-usd-spot'
        :type markets: list(str), str
        :param market_type: Type of market: "spot", "future", "option"
        :type market_type: str
        :param exchange: name of the exchange
        :type exchange: str
        :param base: name of base asset
        :type base: str
        :param quote: name of quote asset
        :type quote: str
        :param asset: name of either base or quote asset
        :type asset: str
        :param symbol: name of a symbol. Usually used for futures contracts.
        :type symbol: str
        :return: Information about markets that correspond to a filter along with meta information like: type of market and min and max available time frames.
        :rtype: list(dict(str, any))
        """
        params: Dict[str, Any] = {
            "markets": markets,
            "type": market_type,
            "exchange": exchange,
            "base": base,
            "quote": quote,
            "asset": asset,
            "symbol": symbol,
        }
        return CatalogMarketMetricsData(
            self._get_data("catalog/market-metrics", params)["data"]
        )

    def catalog_market_candles(
        self,
        markets: Optional[Union[List[str], str]] = None,
        market_type: Optional[str] = None,
        exchange: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None,
    ) -> CatalogMarketCandlesData:
        """
        Returns list of _available_ markets with candles support along woth time ranges of available data per metric.

        :param markets: list of market names, e.g. 'coinbase-btc-usd-spot'
        :type markets: list(str), str
        :param market_type: Type of market: "spot", "future", "option"
        :type market_type: str
        :param exchange: name of the exchange
        :type exchange: str
        :param base: name of base asset
        :type base: str
        :param quote: name of quote asset
        :type quote: str
        :param asset: name of either base or quote asset
        :type asset: str
        :param symbol: name of a symbol. Usually used for futures contracts.
        :type symbol: str
        :return: Information about markets that correspond to a filter along with meta information like: type of market and min and max available time frames.
        :rtype: list(dict(str, any))
        """
        params: Dict[str, Any] = {
            "markets": markets,
            "type": market_type,
            "exchange": exchange,
            "base": base,
            "quote": quote,
            "asset": asset,
            "symbol": symbol,
        }
        return CatalogMarketCandlesData(
            self._get_data("catalog/market-candles", params)["data"]
        )

    def catalog_market_orderbooks(
        self,
        markets: Optional[Union[List[str], str]] = None,
        market_type: Optional[str] = None,
        exchange: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None,
    ) -> CatalogMarketOrderbooksData:
        """
        Returns a list of markets with orderbooks support along with the time ranges of available data.

        :param markets: list of market names, e.g. 'coinbase-btc-usd-spot'
        :type markets: list(str), str
        :param market_type: Type of market: "spot", "future", "option"
        :type market_type: str
        :param exchange: name of the exchange
        :type exchange: str
        :param base: name of base asset
        :type base: str
        :param quote: name of quote asset
        :type quote: str
        :param asset: name of either base or quote asset
        :type asset: str
        :param symbol: name of a symbol. Usually used for futures contracts.
        :type symbol: str
        :return: Information about markets orderbooks that correspond to a filter
        :rtype: list(dict(str, any))
        """
        params: Dict[str, Any] = {
            "markets": markets,
            "type": market_type,
            "exchange": exchange,
            "base": base,
            "quote": quote,
            "asset": asset,
            "symbol": symbol,
        }
        return CatalogMarketOrderbooksData(
            self._get_data("catalog/market-orderbooks", params)["data"]
        )

    def catalog_market_quotes(
        self,
        markets: Optional[Union[List[str], str]] = None,
        market_type: Optional[str] = None,
        exchange: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None,
    ) -> CatalogMarketTradesData:
        """
        Returns a list of markets with quotes support along with the time ranges of available data.

        :param markets: list of market names, e.g. 'coinbase-btc-usd-spot'
        :type markets: list(str), str
        :param market_type: Type of market: "spot", "future", "option"
        :type market_type: str
        :param exchange: name of the exchange
        :type exchange: str
        :param base: name of base asset
        :type base: str
        :param quote: name of quote asset
        :type quote: str
        :param asset: name of either base or quote asset
        :type asset: str
        :param symbol: name of a symbol. Usually used for futures contracts.
        :type symbol: str
        :return: Information about markets quotes that correspond to a filter
        :rtype: list(dict(str, any))
        """
        params: Dict[str, Any] = {
            "markets": markets,
            "type": market_type,
            "exchange": exchange,
            "base": base,
            "quote": quote,
            "asset": asset,
            "symbol": symbol,
        }
        return CatalogMarketTradesData(
            self._get_data("catalog/market-quotes", params)["data"]
        )

    def catalog_market_funding_rates(
        self,
        markets: Optional[Union[List[str], str]] = None,
        market_type: Optional[str] = None,
        exchange: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None,
    ) -> CatalogMarketTradesData:
        """
        Returns a list of markets with funding rates support along with the time ranges of available data.

        :param markets: list of market names, e.g. 'coinbase-btc-usd-spot'
        :type markets: list(str), str
        :param market_type: Type of market: "spot", "future", "option"
        :type market_type: str
        :param exchange: name of the exchange
        :type exchange: str
        :param base: name of base asset
        :type base: str
        :param quote: name of quote asset
        :type quote: str
        :param asset: name of either base or quote asset
        :type asset: str
        :param symbol: name of a symbol. Usually used for futures contracts.
        :type symbol: str
        :return: Information about funding rates that correspond to a filter
        :rtype: list(dict(str, any))
        """
        params: Dict[str, Any] = {
            "markets": markets,
            "type": market_type,
            "exchange": exchange,
            "base": base,
            "quote": quote,
            "asset": asset,
            "symbol": symbol,
        }
        return CatalogMarketTradesData(
            self._get_data("catalog/market-funding-rates", params)["data"]
        )

    def catalog_market_greeks(
        self,
        markets: Optional[Union[List[str], str]] = None,
        market_type: Optional[str] = None,
        exchange: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None,
    ) -> CatalogMarketTradesData:
        """
        Returns a list of markets with greeks support along with the time ranges of available data.

        :param markets: list of market names, e.g. 'coinbase-btc-usd-spot'
        :type markets: list(str), str
        :param market_type: Type of market: "spot", "future", "option"
        :type market_type: str
        :param exchange: name of the exchange
        :type exchange: str
        :param base: name of base asset
        :type base: str
        :param quote: name of quote asset
        :type quote: str
        :param asset: name of either base or quote asset
        :type asset: str
        :param symbol: name of a symbol. Usually used for futures contracts.
        :type symbol: str
        :return: Information about market greeks that correspond to the filter
        :rtype: list(dict(str, any))
        """
        params: Dict[str, Any] = {
            "markets": markets,
            "type": market_type,
            "exchange": exchange,
            "base": base,
            "quote": quote,
            "asset": asset,
            "symbol": symbol,
        }
        return CatalogMarketTradesData(
            self._get_data("catalog/market-greeks", params)["data"]
        )

    def catalog_market_open_interest(
        self,
        markets: Optional[Union[List[str], str]] = None,
        market_type: Optional[str] = None,
        exchange: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None,
    ) -> CatalogMarketTradesData:
        """
        Returns a list of markets with open interest support along with the time ranges of available data.

        :param markets: list of market names, e.g. 'coinbase-btc-usd-spot'
        :type markets: list(str), str
        :param market_type: Type of market: "spot", "future", "option"
        :type market_type: str
        :param exchange: name of the exchange
        :type exchange: str
        :param base: name of base asset
        :type base: str
        :param quote: name of quote asset
        :type quote: str
        :param asset: name of either base or quote asset
        :type asset: str
        :param symbol: name of a symbol. Usually used for futures contracts.
        :type symbol: str
        :return: Information about market open interest that correspond to a filter
        :rtype: list(dict(str, any))
        """
        params: Dict[str, Any] = {
            "markets": markets,
            "type": market_type,
            "exchange": exchange,
            "base": base,
            "quote": quote,
            "asset": asset,
            "symbol": symbol,
        }
        return CatalogMarketTradesData(
            self._get_data("catalog/market-openinterest", params)["data"]
        )

    def catalog_market_liquidations(
        self,
        markets: Optional[Union[List[str], str]] = None,
        market_type: Optional[str] = None,
        exchange: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None,
    ) -> CatalogMarketTradesData:
        """
        Returns a list of markets with liquidations support along with the time ranges of available data.

        :param markets: list of market names, e.g. 'coinbase-btc-usd-spot'
        :type markets: list(str), str
        :param market_type: Type of market: "spot", "future", "option"
        :type market_type: str
        :param exchange: name of the exchange
        :type exchange: str
        :param base: name of base asset
        :type base: str
        :param quote: name of quote asset
        :type quote: str
        :param asset: name of either base or quote asset
        :type asset: str
        :param symbol: name of a symbol. Usually used for futures contracts.
        :type symbol: str
        :return: Information about market liquidations that correspond to a filter
        :rtype: list(dict(str, any))
        """
        params: Dict[str, Any] = {
            "markets": markets,
            "type": market_type,
            "exchange": exchange,
            "base": base,
            "quote": quote,
            "asset": asset,
            "symbol": symbol,
        }
        return CatalogMarketTradesData(
            self._get_data("catalog/market-liquidations", params)["data"]
        )

    def catalog_full_assets(
            self,
            assets: Optional[Union[List[str], str]] = None,
            include: Optional[Union[List[str], str]] = None,
            exclude: Optional[Union[List[str], str]] = None
    ) -> CatalogAssetsData:
        """
        Returns meta information about _supported_ assets.
        :param assets: A single asset or a list of assets to return info for. If no assets provided, all supported assets are returned.
        :type assets: list(str), str
        :param include: list of fields to include in response. Supported values are metrics, markets,
        exchanges. Included by default if omitted.
        :type include: list(str), str
        :param exclude:  list of fields to exclude from response. Supported values are metrics, markets,
        exchanges. Included by default if omitted.
        :type exclude: list(str), str
        :return: Information that is supported for requested assets, like: Full name, metrics and supported frequencies, markets, exchanges, etc.
        :rtype: list(dict(str, any))
        """
        params: Dict[str, Any] = {
            "assets": assets,
            "include": include,
            "exclude": exclude
        }
        return CatalogAssetsData(self._get_data("catalog-all/assets", params)["data"])

    def catalog_full_asset_metrics(
        self,
        metrics: Optional[Union[List[str], str]] = None,
        reviewable: Optional[bool] = None,
    ) -> CatalogMetricsData:
        """
        Returns list of all _available_ asset metrics along with information for them like
        description, category, precision and assets for which a metric is available.

        :param metrics: A single asset metric name or a list of metrics to return info for. If no metrics provided, all available metrics are returned.
        :type metrics: list(str), str
        :param reviewable: Show only reviewable or non-reviewable by human metrics. By default all metrics are shown.
        :type reviewable: bool
        :return: Information about asset metrics that correspond to a filter along with meta information like: description, category, precision and assets for which a metric is available.
        :rtype: list(dict(str, any))
        """
        params: Dict[str, Any] = {"metrics": metrics, "reviewable": reviewable}
        return CatalogMetricsData(
            self._get_data("catalog-all/asset-metrics", params)["data"]
        )

    def catalog_full_asset_alerts(
        self,
        assets: Optional[Union[List[str], str]] = None,
        alerts: Optional[Union[List[str], str]] = None,
    ) -> CatalogAssetAlertsData:
        """
        Returns meta information about _supported_ assets.

        :param assets: A single asset or a list of assets to return info for. If no assets provided, all available assets are returned.
        :type assets: list(str), str
        :param alerts: A single alert or alert name to return info for. If no alerts provided, all available alerts are returned.
        :type alerts: list(str), str
        :return: Information that is available for requested assets alerts.
        :rtype: list(dict(str, any))
        """
        params: Dict[str, Any] = {"assets": assets, "alerts": alerts}
        return CatalogAssetAlertsData(
            self._get_data("catalog-all/alerts", params)["data"]
        )

    def catalog_full_asset_pairs(
        self,
        asset_pairs: Optional[Union[List[str], str]] = None,
    ) -> CatalogAssetPairsData:
        """
        Returns meta information about _supported_ asset-asset pairs

        :param asset_pairs: A single asset-asset pair (e.g. "btc-eth") or a list of asset-asset pairs to return info for. If none are provided, all supported pairs are returned.
        :type asset_pairs: list(str), str
        :return: Information that is supported for requested asset-asset pair like metrics and their respective frequencies and time ranges
        :rtype: list(dict(str, any))
        """
        params: Dict[str, Any] = {"pairs": asset_pairs}
        return CatalogAssetPairsData(
            self._get_data("catalog-all/pairs", params)["data"]
        )

    def catalog_full_pair_metrics(
        self,
        metrics: Optional[Union[List[str], str]] = None,
        reviewable: Optional[bool] = None,
    ) -> CatalogPairMetricsData:
        """
        Returns list of all _available_ pair metrics along with information for them like
        description, category, precision and assets for which a metric is available.

        :param metrics: A single pair metric name or a list of metrics to return info for. If no metrics provided, all available metrics are returned.
        :type metrics: list(str), str
        :param reviewable: Show only reviewable or non-reviewable by human metrics. By default all metrics are shown.
        :type reviewable: bool
        :return: Information about pair metrics that correspond to a filter along with meta information like: description, category, precision and assets for which a metric is available.
        :rtype: list(dict(str, any))
        """
        params: Dict[str, Any] = {"metrics": metrics, "reviewable": reviewable}
        return CatalogPairMetricsData(
            self._get_data("catalog-all/pair-metrics", params)["data"]
        )

    def catalog_full_institution_metrics(
        self,
        metrics: Optional[Union[List[str], str]] = None,
        reviewable: Optional[bool] = None,
    ) -> CatalogInstitutionMetricsData:
        """
        Returns list of _available_ institution metrics along with information for them like
        description, category, precision and assets for which a metric is available.

        :param metrics: A single institution metric name or a list of metrics to return info for. If no metrics provided, all available metrics are returned.
        :type metrics: list(str), str
        :param reviewable: Show only reviewable or non-reviewable by human metrics. By default all metrics are shown.
        :type reviewable: bool
        :return: Information about institution metrics that correspond to a filter along with meta information like: description, category, precision and assets for which a metric is available.
        :rtype: list(dict(str, any))
        """
        params: Dict[str, Any] = {"metrics": metrics, "reviewable": reviewable}
        return CatalogInstitutionMetricsData(
            self._get_data("catalog-all/institution-metrics", params)["data"]
        )

    def catalog_full_asset_pair_candles(
        self, asset_pairs: Optional[Union[List[str], str]] = None
    ) -> CatalogAssetPairCandlesData:
        """
        Returns meta information about _available_ asset-asset pairs

        :param asset_pairs: A single asset-asset pair (e.g. "btc-eth") or a list of asset-asset pairs to return info for. If none are provided, all available pairs are returned.
        :type asset_pairs: list(str), str
        :return: Returns a list of available asset pair candles along with the time ranges of available data per candle duration.
        :rtype: list(dict(str, any))
        """
        params: Dict[str, Any] = {"pairs": asset_pairs}
        return CatalogAssetPairCandlesData(
            self._get_data("catalog-all/pair-candles", params)["data"]
        )

    def catalog_full_exchanges(
        self,
        exchanges: Optional[Union[List[str], str]] = None,
    ) -> CatalogExchangesData:
        """
        Returns meta information about exchanges.

        :param exchanges: A single exchange name or a list of exchanges to return info for. If no exchanges provided,
         all supported exchanges are returned.
        :type exchanges: list(str), str
        :return: Information that is supported for requested exchanges, like: markets, min and max time supported.
        :rtype: list(dict(str, any))
        """
        params: Dict[str, Any] = {"exchanges": exchanges}
        return CatalogExchangesData(
            self._get_data("catalog-all/exchanges", params)["data"]
        )

    def catalog_full_exchange_assets(
        self, exchange_assets: Optional[Union[List[str], str]] = None
    ) -> CatalogExchangeAssetsData:
        """
        Returns meta information about _supported_ exchange-asset pairs

        :param exchange_assets: A single exchange-asset pair (e.g. "binance-btc") or a list of exchange-asset pairs to return info for. If none are provided, all supported pairs are returned.
        :type exchange_assets: list(str), str
        :return: Information that is supported for requested exchange-asset pair like metrics and their respective frequencies and time ranges
        :rtype: list(dict(str, any))
        """
        params: Dict[str, Any] = {"exchange_assets": exchange_assets}
        return CatalogExchangeAssetsData(
            self._get_data("catalog-all/exchange-assets", params)["data"]
        )

    def catalog_full_exchange_metrics(
        self,
        metrics: Optional[Union[List[str], str]] = None,
        reviewable: Optional[bool] = None,
    ) -> CatalogMetricsData:
        """
        Returns list of all _available_ exchange metrics along with information for them like
        description, category, precision and assets for which a metric is available.

        :param metrics: A single exchange metric name or a list of metrics to return info for. If no metrics provided, all available metrics are returned.
        :type metrics: list(str), str
        :param reviewable: Show only reviewable or non-reviewable by human metrics. By default all metrics are shown.
        :type reviewable: bool
        :return: Information about exchange metrics that correspond to a filter along with meta information like: description, category, precision and assets for which a metric is available.
        :rtype: list(dict(str, any))
        """
        params: Dict[str, Any] = {"metrics": metrics, "reviewable": reviewable}
        return CatalogMetricsData(
            self._get_data("catalog-all/exchange-metrics", params)["data"]
        )

    def catalog_full_exchange_asset_metrics(
        self,
        metrics: Optional[Union[List[str], str]] = None,
        reviewable: Optional[bool] = None,
    ) -> CatalogExchangeAssetMetricsData:
        """
        Returns list of _available_ exchange metrics along with information for them like
        description, category, precision and assets for which a metric is available.

        :param metrics: A single exchange metric name or a list of metrics to return info for. If no metrics provided, all available metrics are returned.
        :type metrics: list(str), str
        :param reviewable: Show only reviewable or non-reviewable by human metrics. By default all metrics are shown.
        :type reviewable: bool
        :return: Information about exchange metrics that correspond to a filter along with meta information like: description, category, precision and assets for which a metric is available.
        :rtype: list(dict(str, any))
        """
        params: Dict[str, Any] = {"metrics": metrics, "reviewable": reviewable}
        return CatalogExchangeAssetMetricsData(
            self._get_data("catalog-all/exchange-asset-metrics", params)["data"]
        )

    def catalog_full_indexes(
        self, indexes: Optional[Union[List[str], str]] = None
    ) -> CatalogIndexesData:
        """
        Returns meta information about _supported_ indexes.

        :param indexes: A single index name or a list of indexes to return info for. If no indexes provided, all supported indexes are returned.
        :type indexes: list(str), str
        :return: Information that is supported for requested indexes, like: Full name, and supported frequencies.
        :rtype: list(dict(str, any))
        """
        params: Dict[str, Any] = {"indexes": indexes}
        return CatalogIndexesData(self._get_data("catalog-all/indexes", params)["data"])

    def catalog_full_index_candles(
        self, indexes: Optional[Union[List[str], str]] = None
    ) -> CatalogMarketCandlesData:
        """
        Returns meta information about _supported_ index candles.

        :param indexes: A single index name or a list of indexes to return info for. If no indexes provided, all supported indexes are returned.
        :type indexes: list(str), str
        :return: Information that is supported for requested index candles, like: Full name, and supported frequencies.
        :rtype: list(dict(str, any))
        """
        params: Dict[str, Any] = {"indexes": indexes}
        return CatalogMarketCandlesData(
            self._get_data("catalog-all/index-candles", params)["data"]
        )

    def catalog_full_institutions(
        self, institutions: Optional[Union[List[str], str]] = None
    ) -> CatalogInstitutionsData:
        """
        Returns meta information about _supported_ institutions

        :param institutions: A single institution (e.g. "grayscale") or a list of institutions to return info for. If none are provided, all supported pairs are returned.
        :type institutions: list(str), str
        :return: Information that is supported for requested institution like metrics and their respective frequencies and time ranges.
        :rtype: list(dict(str, any))
        """
        params: Dict[str, Any] = {"institutions": institutions}
        return CatalogInstitutionsData(
            self._get_data("catalog-all/institutions", params)["data"]
        )

    def catalog_full_markets(
        self,
        markets: Optional[Union[List[str], str]] = None,
        market_type: Optional[str] = None,
        exchange: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None,
        include: Optional[str] = None,
        exclude: Optional[str] = None
    ) -> CatalogMarketsData:
        """
        Returns list of _supported_ markets that correspond to a filter. If no filter is set, returns all supported assets.

        :param markets: list of market names, e.g. 'coinbase-btc-usd-spot'
        :type markets: list(str), str
        :param market_type: Type of market: "spot", "future", "option"
        :type market_type: str
        :param exchange: name of the exchange
        :type exchange: str
        :param base: name of base asset
        :type base: str
        :param quote: name of quote asset
        :type quote: str
        :param asset: name of either base or quote asset
        :type asset: str
        :param symbol: name of a symbol. Usually used for futures contracts.
        :type symbol: str
        :param include: ist of fields to include in response. Supported values are trades, orderbooks, quotes,
         funding_rates, openinterest, liquidations. Included by default if omitted.
        :type include: list(str), str
        :param exclude: list of fields to exclude from response. Supported values are trades, orderbooks, quotes,
         funding_rates, openinterest, liquidations. Included by default if omitted.
        :type exclude: list(str), str
        :return: Information about markets that correspond to a filter along with meta information like: type of market and min and max supported time frames.
        :rtype: list(dict(str, any))
        """
        params: Dict[str, Any] = {
            "markets": markets,
            "type": market_type,
            "exchange": exchange,
            "base": base,
            "quote": quote,
            "asset": asset,
            "symbol": symbol,
            "include": include,
            "exclude": exclude
        }
        return CatalogMarketsData(self._get_data("catalog-all/markets", params)["data"])

    def catalog_full_market_trades(
        self,
        markets: Optional[Union[List[str], str]] = None,
        market_type: Optional[str] = None,
        exchange: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None,
    ) -> CatalogMarketTradesData:
        """
        Returns a list of all markets with trades support along with the time ranges of available data.

        :param markets: list of market names, e.g. 'coinbase-btc-usd-spot'
        :type markets: list(str), str
        :param market_type: Type of market: "spot", "future", "option"
        :type market_type: str
        :param exchange: name of the exchange
        :type exchange: str
        :param base: name of base asset
        :type base: str
        :param quote: name of quote asset
        :type quote: str
        :param asset: name of either base or quote asset
        :type asset: str
        :param symbol: name of a symbol. Usually used for futures contracts.
        :type symbol: str
        :return: Information about market trades that are available for the provided filter, as well as the time frames they are available
        :rtype: list(dict(str, any))
        """
        params: Dict[str, Any] = {
            "markets": markets,
            "type": market_type,
            "exchange": exchange,
            "base": base,
            "quote": quote,
            "asset": asset,
            "symbol": symbol,
        }
        return CatalogMarketTradesData(
            self._get_data("catalog-all/market-trades", params)["data"]
        )

    def catalog_full_metrics(
        self,
        metrics: Optional[Union[List[str], str]] = None,
        reviewable: Optional[bool] = None,
    ) -> CatalogMetricsData:
        """
        Returns list of _supported_ metrics along with information for them like
        description, category, precision and assets for which a metric is supported.

        :param metrics: A single metric name or a list of metrics to return info for. If no metrics provided, all supported metrics are returned.
        :type metrics: list(str), str
        :param reviewable: Show only reviewable or non-reviewable by human metrics. By default all metrics are shown.
        :type reviewable: bool
        :return: Information about metrics that correspond to a filter along with meta information like: description, category, precision and assets for which a metric is supported.
        :rtype: list(dict(str, any))
        """
        params: Dict[str, Any] = {"metrics": metrics, "reviewable": reviewable}
        return CatalogMetricsData(self._get_data("catalog-all/metrics", params)["data"])

    def catalog_full_market_metrics(
        self,
        markets: Optional[Union[List[str], str]] = None,
        market_type: Optional[str] = None,
        exchange: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None,
    ) -> CatalogMarketMetricsData:
        """
        Returns list of _supported_ markets with metrics support along woth time ranges of available data per metric.

        :param markets: list of market names, e.g. 'coinbase-btc-usd-spot'
        :type markets: list(str), str
        :param market_type: Type of market: "spot", "future", "option"
        :type market_type: str
        :param exchange: name of the exchange
        :type exchange: str
        :param base: name of base asset
        :type base: str
        :param quote: name of quote asset
        :type quote: str
        :param asset: name of either base or quote asset
        :type asset: str
        :param symbol: name of a symbol. Usually used for futures contracts.
        :type symbol: str
        :return: Information about markets that correspond to a filter along with meta information like: type of market and min and max available time frames.
        :rtype: list(dict(str, any))
        """
        params: Dict[str, Any] = {
            "markets": markets,
            "type": market_type,
            "exchange": exchange,
            "base": base,
            "quote": quote,
            "asset": asset,
            "symbol": symbol,
        }
        return CatalogMarketMetricsData(
            self._get_data("catalog-all/market-metrics", params)["data"]
        )

    def catalog_full_market_candles(
        self,
        markets: Optional[Union[List[str], str]] = None,
        market_type: Optional[str] = None,
        exchange: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None,
    ) -> CatalogMarketCandlesData:
        """
        Returns list of _available_ markets with candles support along woth time ranges of available data per metric.

        :param markets: list of market names, e.g. 'coinbase-btc-usd-spot'
        :type markets: list(str), str
        :param market_type: Type of market: "spot", "future", "option"
        :type market_type: str
        :param exchange: name of the exchange
        :type exchange: str
        :param base: name of base asset
        :type base: str
        :param quote: name of quote asset
        :type quote: str
        :param asset: name of either base or quote asset
        :type asset: str
        :param symbol: name of a symbol. Usually used for futures contracts.
        :type symbol: str
        :return: Information about markets that correspond to a filter along with meta information like: type of market and min and max available time frames.
        :rtype: list(dict(str, any))
        """
        params: Dict[str, Any] = {
            "markets": markets,
            "type": market_type,
            "exchange": exchange,
            "base": base,
            "quote": quote,
            "asset": asset,
            "symbol": symbol,
        }
        return CatalogMarketCandlesData(
            self._get_data("catalog-all/market-candles", params)["data"]
        )

    def catalog_full_market_orderbooks(
        self,
        markets: Optional[Union[List[str], str]] = None,
        market_type: Optional[str] = None,
        exchange: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None,
    ) -> CatalogMarketTradesData:
        """
        Returns a list of markets with orderbooks support along with the time ranges of available data.

        :param markets: list of market names, e.g. 'coinbase-btc-usd-spot'
        :type markets: list(str), str
        :param market_type: Type of market: "spot", "future", "option"
        :type market_type: str
        :param exchange: name of the exchange
        :type exchange: str
        :param base: name of base asset
        :type base: str
        :param quote: name of quote asset
        :type quote: str
        :param asset: name of either base or quote asset
        :type asset: str
        :param symbol: name of a symbol. Usually used for futures contracts.
        :type symbol: str
        :return: Information about markets orderbooks that correspond to a filter
        :rtype: list(dict(str, any))
        """
        params: Dict[str, Any] = {
            "markets": markets,
            "type": market_type,
            "exchange": exchange,
            "base": base,
            "quote": quote,
            "asset": asset,
            "symbol": symbol,
        }
        return CatalogMarketTradesData(
            self._get_data("catalog-all/market-orderbooks", params)["data"]
        )

    def catalog_full_market_quotes(
        self,
        markets: Optional[Union[List[str], str]] = None,
        market_type: Optional[str] = None,
        exchange: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None,
    ) -> CatalogMarketTradesData:
        """
        Returns a list of markets with quotes support along with the time ranges of available data.

        :param markets: list of market names, e.g. 'coinbase-btc-usd-spot'
        :type markets: list(str), str
        :param market_type: Type of market: "spot", "future", "option"
        :type market_type: str
        :param exchange: name of the exchange
        :type exchange: str
        :param base: name of base asset
        :type base: str
        :param quote: name of quote asset
        :type quote: str
        :param asset: name of either base or quote asset
        :type asset: str
        :param symbol: name of a symbol. Usually used for futures contracts.
        :type symbol: str
        :return: Information about markets quotes that correspond to a filter
        :rtype: list(dict(str, any))
        """
        params: Dict[str, Any] = {
            "markets": markets,
            "type": market_type,
            "exchange": exchange,
            "base": base,
            "quote": quote,
            "asset": asset,
            "symbol": symbol,
        }
        return CatalogMarketTradesData(
            self._get_data("catalog-all/market-quotes", params)["data"]
        )

    def catalog_full_market_funding_rates(
        self,
        markets: Optional[Union[List[str], str]] = None,
        market_type: Optional[str] = None,
        exchange: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None,
    ) -> CatalogMarketTradesData:
        """
        Returns a list of all markets with funding rates support along with the time ranges of available data.

        :param markets: list of market names, e.g. 'coinbase-btc-usd-spot'
        :type markets: list(str), str
        :param market_type: Type of market: "spot", "future", "option"
        :type market_type: str
        :param exchange: name of the exchange
        :type exchange: str
        :param base: name of base asset
        :type base: str
        :param quote: name of quote asset
        :type quote: str
        :param asset: name of either base or quote asset
        :type asset: str
        :param symbol: name of a symbol. Usually used for futures contracts.
        :type symbol: str
        :return: Information about funding rates that correspond to a filter
        :rtype: list(dict(str, any))
        """
        params: Dict[str, Any] = {
            "markets": markets,
            "type": market_type,
            "exchange": exchange,
            "base": base,
            "quote": quote,
            "asset": asset,
            "symbol": symbol,
        }
        return CatalogMarketTradesData(
            self._get_data("catalog-all/market-funding-rates", params)["data"]
        )

    def catalog_full_market_greeks(
        self,
        markets: Optional[Union[List[str], str]] = None,
        market_type: Optional[str] = None,
        exchange: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None,
    ) -> CatalogMarketTradesData:
        """
        Returns a list of all markets with greeks support along with the time ranges of available data.

        :param markets: list of market names, e.g. 'coinbase-btc-usd-spot'
        :type markets: list(str), str
        :param market_type: Type of market: "spot", "future", "option"
        :type market_type: str
        :param exchange: name of the exchange
        :type exchange: str
        :param base: name of base asset
        :type base: str
        :param quote: name of quote asset
        :type quote: str
        :param asset: name of either base or quote asset
        :type asset: str
        :param symbol: name of a symbol. Usually used for futures contracts.
        :type symbol: str
        :return: Information about market greeks that correspond to the filter
        :rtype: list(dict(str, any))
        """
        params: Dict[str, Any] = {
            "markets": markets,
            "type": market_type,
            "exchange": exchange,
            "base": base,
            "quote": quote,
            "asset": asset,
            "symbol": symbol,
        }
        return CatalogMarketTradesData(
            self._get_data("catalog-all/market-greeks", params)["data"]
        )

    def catalog_full_market_open_interest(
        self,
        markets: Optional[Union[List[str], str]] = None,
        market_type: Optional[str] = None,
        exchange: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None,
    ) -> CatalogMarketTradesData:
        """
        Returns a list of markets with open interest support along with the time ranges of available data.

        :param markets: list of market names, e.g. 'coinbase-btc-usd-spot'
        :type markets: list(str), str
        :param market_type: Type of market: "spot", "future", "option"
        :type market_type: str
        :param exchange: name of the exchange
        :type exchange: str
        :param base: name of base asset
        :type base: str
        :param quote: name of quote asset
        :type quote: str
        :param asset: name of either base or quote asset
        :type asset: str
        :param symbol: name of a symbol. Usually used for futures contracts.
        :type symbol: str
        :return: Information about market open interest that correspond to a filter
        :rtype: list(dict(str, any))
        """
        params: Dict[str, Any] = {
            "markets": markets,
            "type": market_type,
            "exchange": exchange,
            "base": base,
            "quote": quote,
            "asset": asset,
            "symbol": symbol,
        }
        return CatalogMarketTradesData(
            self._get_data("catalog-all/market-openinterest", params)["data"]
        )

    def catalog_full_market_liquidations(
        self,
        markets: Optional[Union[List[str], str]] = None,
        market_type: Optional[str] = None,
        exchange: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None,
    ) -> CatalogMarketTradesData:
        """
        Returns a list of all markets with liquidations support along with the time ranges of available data.

        :param markets: list of market names, e.g. 'coinbase-btc-usd-spot'
        :type markets: list(str), str
        :param market_type: Type of market: "spot", "future", "option"
        :type market_type: str
        :param exchange: name of the exchange
        :type exchange: str
        :param base: name of base asset
        :type base: str
        :param quote: name of quote asset
        :type quote: str
        :param asset: name of either base or quote asset
        :type asset: str
        :param symbol: name of a symbol. Usually used for futures contracts.
        :type symbol: str
        :return: Information about market liquidations that correspond to a filter
        :rtype: list(dict(str, any))
        """
        params: Dict[str, Any] = {
            "markets": markets,
            "type": market_type,
            "exchange": exchange,
            "base": base,
            "quote": quote,
            "asset": asset,
            "symbol": symbol,
        }
        return CatalogMarketTradesData(
            self._get_data("catalog-all/market-liquidations", params)["data"]
        )

    def get_asset_alerts(
        self,
        assets: Union[List[str], str],
        alerts: Union[List[str], str],
        page_size: Optional[int] = None,
        paging_from: Optional[Union[PagingFrom, str]] = "start",
        start_time: Optional[Union[datetime, date, str]] = None,
        end_time: Optional[Union[datetime, date, str]] = None,
        start_inclusive: Optional[bool] = None,
        end_inclusive: Optional[bool] = None,
        timezone: Optional[str] = None,
    ) -> DataCollection:
        """
        Returns asset alerts for the specified assets.

        :param assets: list of asset names, e.g. 'btc'
        :type assets: list(str), str
        :param alerts: list of asset alert names
        :type alerts: list(str), str
        :param page_size: number of items returned per page when calling the API. If the request times out, try using a smaller number.
        :type page_size: int
        :param paging_from: Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
        :type paging_from: PagingFrom, str
        :param start_time: Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type end_time: datetime, date, str
        :param start_inclusive: Flag to define if start timestamp must be included in the timeseries if present. True by default.
        :type start_inclusive: bool
        :param end_inclusive: Flag to define if end timestamp must be included in the timeseries if present. True by default.
        :type end_inclusive: bool
        :param timezone: timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.
        :type timezone: str
        :return: Asset alerts timeseries.
        :rtype: DataCollection
        """

        params: Dict[str, Any] = {
            "assets": assets,
            "alerts": alerts,
            "page_size": page_size,
            "paging_from": paging_from,
            "start_time": start_time,
            "end_time": end_time,
            "start_inclusive": start_inclusive,
            "end_inclusive": end_inclusive,
            "timezone": timezone,
        }
        return DataCollection(self._get_data, "timeseries/asset-alerts", params)

    def get_defi_balance_sheets(
        self,
        defi_protocols: Union[str, List[str]],
        page_size: Optional[int] = None,
        paging_from: Optional[Union[PagingFrom, str]] = "start",
        start_time: Optional[Union[datetime, date, str]] = None,
        end_time: Optional[Union[datetime, date, str]] = None,
        start_height: Optional[int] = None,
        end_height: Optional[int] = None,
        start_inclusive: Optional[bool] = None,
        end_inclusive: Optional[bool] = None,
        timezone: Optional[str] = None,
    ) -> DataCollection:
        """
        Returns Defi Balance Sheet records for specified DeFi protocols.

        :param defi_protocols:  list of DeFi protocols like aave_v2_eth or protocol patterns like aave_v2_* or aave_*_eth or *_eth.
        :type defi_protocols: str, List[str]
        :param page_size: number of items returned per page when calling the API. If the request times out, try using a smaller number.
        :type page_size: int
        :param paging_from: Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
        :type paging_from: PagingFrom, str
        :param start_time: Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type end_time: datetime, date, str
        :param start_height: The start height indicates the beginning block height for the set of data that are returned. Mutually exclusive with start_time
        :type start_height: int
        :param end_height: The end height indicates the beginning block height for the set of data that are returned. Mutually exclusive with end_time
        :type end_height: int
        :param start_inclusive: Flag to define if start timestamp must be included in the timeseries if present. True by default.
        :type start_inclusive: bool
        :param end_inclusive: Flag to define if end timestamp must be included in the timeseries if present. True by default.
        :type end_inclusive: bool
        :param timezone: timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.
        :type timezone: str
        :return: list of blockchain blocks metadata
        :rtype: DataCollection
        """
        params: Dict[str, Any] = {
            "defi_protocols": defi_protocols,
            "page_size": page_size,
            "paging_from": paging_from,
            "start_time": start_time,
            "end_time": end_time,
            "start_height": start_height,
            "end_height": end_height,
            "start_inclusive": start_inclusive,
            "end_inclusive": end_inclusive,
            "timezone": timezone,
        }
        return DataCollection(self._get_data, "timeseries/defi-balance-sheets", params)

    def get_asset_chains(
        self,
        assets: Union[List[str], str],
        page_size: Optional[int] = None,
        paging_from: Optional[Union[PagingFrom, str]] = "start",
        start_time: Optional[Union[datetime, date, str]] = None,
        end_time: Optional[Union[datetime, date, str]] = None,
        start_inclusive: Optional[bool] = None,
        end_inclusive: Optional[bool] = None,
        timezone: Optional[str] = None,
    ) -> DataCollection:
        """
        Returns the chains of blocks for the specified assets.

        :param assets: list of asset names, e.g. 'btc'
        :type assets: list(str), str
        :param page_size: number of items returned per page when calling the API. If the request times out, try using a smaller number.
        :type page_size: int
        :param paging_from: Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
        :type paging_from: PagingFrom, str
        :param start_time: Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type end_time: datetime, date, str
        :param start_inclusive: Flag to define if start timestamp must be included in the timeseries if present. True by default.
        :type start_inclusive: bool
        :param end_inclusive: Flag to define if end timestamp must be included in the timeseries if present. True by default.
        :type end_inclusive: bool
        :param timezone: timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.
        :type timezone: str
        :return: Asset chains timeseries.
        :rtype: DataCollection
        """

        params: Dict[str, Any] = {
            "assets": assets,
            "page_size": page_size,
            "paging_from": paging_from,
            "start_time": start_time,
            "end_time": end_time,
            "start_inclusive": start_inclusive,
            "end_inclusive": end_inclusive,
            "timezone": timezone,
        }
        return DataCollection(self._get_data, "timeseries/asset-chains", params)

    def get_asset_metrics(
        self,
        assets: Union[List[str], str],
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
        null_as_zero: Optional[bool] = None,
    ) -> DataCollection:
        """
        Returns requested metrics for specified assets.

        :param assets: list of asset names, e.g. 'btc'
        :type assets: list(str), str
        :param metrics: list of _asset-specific_ metric names, e.g. 'PriceUSD'
        :type metrics: list(str), str
        :param frequency: frequency of the returned timeseries, e.g 15s, 1d, etc.
        :type frequency: str
        :param page_size: number of items returned per page when calling the API. If the request times out, try using a smaller number.
        :type page_size: int
        :param paging_from: Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
        :type paging_from: PagingFrom, str
        :param start_time: Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type end_time: datetime, date, str
        :param start_height: Start block of the timeseries (only applicable when querying with frequency 1b).
        :type start_height: int
        :param end_height: End block of the timeseries (only applicable when querying with frequency 1b).
        :type end_height: int
        :param start_inclusive: Flag to define if start timestamp must be included in the timeseries if present. True by default.
        :type start_inclusive: bool
        :param end_inclusive: Flag to define if end timestamp must be included in the timeseries if present. True by default.
        :type end_inclusive: bool
        :param timezone: timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.
        :type timezone: str
        :param sort: How results will be sorted, e.g. "asset", "height", or "time". Default is "asset". Metrics with 1b frequency are sorted by (asset, height, block_hash) tuples by default. Metrics with other frequencies are sorted by (asset, time) by default. If you want to sort 1d metrics by (time, asset) you should choose time as value for the sort parameter. Sorting by time is useful if you request metrics for a set of assets.
        :type sort: str
        :param limit_per_asset: How many entries _per asset_ the result should contain.
        :type limit_per_asset: int
        :param status: Which metric values do you want to see. Applicable only for "reviewable" metrics.
        You can find them in the /catalog/metrics endpoint. Default: "all". Supported: "all" "flash" "reviewed" "revised"
        :type status: str
        :param start_hash: The start hash indicates the beginning block height for the set of data that are returned.
        Inclusive by default. Mutually exclusive with start_time and start_height.
        :type start_hash: str
        :param end_hash: The end hash indicates the ending block height for the set of data that are returned.
        Inclusive by default. Mutually exclusive with end_time and end_height.
        :type end_hash: str
        :param min_confirmations: Specifies how many blocks behind the chain tip block by block metrics
        (1b frequency) are based on. Default for btc is 2 and 99 for eth.
        :type min_confirmations: int
        :param null_as_zero: Default: false. Nulls are represented as zeros in the response.
        :type null_as_zero: bool
        :return: Asset Metrics timeseries.
        :rtype: DataCollection
        """

        params: Dict[str, Any] = {
            "assets": assets,
            "metrics": metrics,
            "frequency": frequency,
            "page_size": page_size,
            "paging_from": paging_from,
            "start_time": start_time,
            "end_time": end_time,
            "start_height": start_height,
            "end_height": end_height,
            "start_inclusive": start_inclusive,
            "end_inclusive": end_inclusive,
            "timezone": timezone,
            "sort": sort,
            "limit_per_asset": limit_per_asset,
            "status": status,
            "start_hash": start_hash,
            "end_hash": end_hash,
            "min_confirmations": min_confirmations,
            "null_as_zero": null_as_zero,
        }
        return DataCollection(self._get_data, "timeseries/asset-metrics", params)

    def get_exchange_metrics(
        self,
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
        limit_per_exchange: Optional[int] = None,
    ) -> DataCollection:
        """
        Returns metrics for specified exchanges.

        :param exchanges: A single exchange name or a list of exchanges to return info for.
        :type exchanges: list(str), str
        :param metrics: list of _exchange-specific_ metric names, e.g. 'open_interest_reported_future_usd'. To find a list of available metrics for a given exchange, call `client.catalog_exchanges()`
        :type metrics: list(str), str
        :param frequency: frequency of the returned timeseries, e.g 15s, 1d, etc.
        :type frequency: str
        :param page_size: number of items returned per page when calling the API. If the request times out, try using a smaller number.
        :type page_size: int
        :param paging_from: Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
        :type paging_from: PagingFrom, str
        :param start_time: Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type end_time: datetime, date, str
        :param start_height: Start block of the timeseries (only applicable when querying with frequency 1b).
        :type start_height: int
        :param end_height: End block of the timeseries (only applicable when querying with frequency 1b).
        :type end_height: int
        :param start_inclusive: Flag to define if start timestamp must be included in the timeseries if present. True by default.
        :type start_inclusive: bool
        :param end_inclusive: Flag to define if end timestamp must be included in the timeseries if present. True by default.
        :type end_inclusive: bool
        :param timezone: timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.
        :type timezone: str
        :param sort: How results will be sorted, e.g. 'exchange', 'time'. Metrics are sorted by 'exchange' by default.
        :type sort: str
        :param limit_per_exchange: How many entries _per exchange_ the result should contain.
        :type limit_per_exchange: int
        :return: Asset Metrics timeseries.
        :rtype: DataCollection
        """

        params: Dict[str, Any] = {
            "exchanges": exchanges,
            "metrics": metrics,
            "frequency": frequency,
            "page_size": page_size,
            "paging_from": paging_from,
            "start_time": start_time,
            "end_time": end_time,
            "start_height": start_height,
            "end_height": end_height,
            "start_inclusive": start_inclusive,
            "end_inclusive": end_inclusive,
            "timezone": timezone,
            "sort": sort,
            "limit_per_exchange": limit_per_exchange,
        }
        return DataCollection(self._get_data, "timeseries/exchange-metrics", params)

    def get_exchange_asset_metrics(
        self,
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
        limit_per_exchange_asset: Optional[int] = None,
    ) -> DataCollection:
        """
        Returns metrics for specified exchange-asset.

        :param exchange_assets: A single exchange-asset pairs (e.g. "binance-btc" or a list of exchange-asset-pair to return info for.
        :type exchange_assets: list(str), str
        :param metrics: list of _exchange-specific_ metric names, e.g. 'open_interest_reported_future_usd'. To find a list of available metrics for a given exchange, call `client.catalog_exchanges()`
        :type metrics: list(str), str
        :param frequency: frequency of the returned timeseries, e.g 15s, 1d, etc.
        :type frequency: str
        :param page_size: number of items returned per page when calling the API. If the request times out, try using a smaller number.
        :type page_size: int
        :param paging_from: Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
        :type paging_from: PagingFrom, str
        :param start_time: Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type end_time: datetime, date, str
        :param start_height: Start block of the timeseries (only applicable when querying with frequency 1b).
        :type start_height: int
        :param end_height: End block of the timeseries (only applicable when querying with frequency 1b).
        :type end_height: int
        :param start_inclusive: Flag to define if start timestamp must be included in the timeseries if present. True by default.
        :type start_inclusive: bool
        :param end_inclusive: Flag to define if end timestamp must be included in the timeseries if present. True by default.
        :type end_inclusive: bool
        :param timezone: timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.
        :type timezone: str
        :param sort: How results will be sorted, e.g. "exchange_asset", "time". Default is "exchange_asset".
        :type sort: str
        :param limit_per_exchange_asset: How many entries _per exchange-asset_ the result should contain.
        :type limit_per_exchange_asset: int
        :return: Exchange-Asset Metrics timeseries.
        :rtype: DataCollection
        """

        params: Dict[str, Any] = {
            "exchange_assets": exchange_assets,
            "metrics": metrics,
            "frequency": frequency,
            "page_size": page_size,
            "paging_from": paging_from,
            "start_time": start_time,
            "end_time": end_time,
            "start_height": start_height,
            "end_height": end_height,
            "start_inclusive": start_inclusive,
            "end_inclusive": end_inclusive,
            "timezone": timezone,
            "sort": sort,
            "limit_per_exchange_asset": limit_per_exchange_asset,
        }
        return DataCollection(
            self._get_data, "timeseries/exchange-asset-metrics", params
        )

    def get_pair_metrics(
        self,
        pairs: Union[List[str], str],
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
        limit_per_pair: Optional[int] = None,
    ) -> DataCollection:
        """
        Returns metrics books for specified asset-asset pairs.

        :param pairs: A single asset-asset pairs (e.g. "btc-usd") or a list of asset-asset-pairs to return info for.
        :type pairs: list(str), str
        :param metrics: list of _exchange-specific_ metric names, e.g. 'open_interest_reported_future_usd'. To find a list of available metrics for a given exchange, call `client.catalog_exchanges()`
        :type metrics: list(str), str
        :param frequency: frequency of the returned timeseries, e.g 15s, 1d, etc.
        :type frequency: str
        :param page_size: number of items returned per page when calling the API. If the request times out, try using a smaller number.
        :type page_size: int
        :param paging_from: Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
        :type paging_from: PagingFrom, str
        :param start_time: Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type end_time: datetime, date, str
        :param start_height: Start block of the timeseries (only applicable when querying with frequency 1b).
        :type start_height: int
        :param end_height: End block of the timeseries (only applicable when querying with frequency 1b).
        :type end_height: int
        :param start_inclusive: Flag to define if start timestamp must be included in the timeseries if present. True by default.
        :type start_inclusive: bool
        :param end_inclusive: Flag to define if end timestamp must be included in the timeseries if present. True by default.
        :type end_inclusive: bool
        :param timezone: timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.
        :type timezone: str
        :param sort: How results will be sorted, e.g."pair", "time". "pair" by default
        :type sort: str
        :param limit_per_pair: How many entries _per asset pair_ the result should contain.
        :type limit_per_pair: int
        :return: Exchange-Asset Metrics timeseries.
        :rtype: DataCollection
        """

        params: Dict[str, Any] = {
            "pairs": pairs,
            "metrics": metrics,
            "frequency": frequency,
            "page_size": page_size,
            "paging_from": paging_from,
            "start_time": start_time,
            "end_time": end_time,
            "start_height": start_height,
            "end_height": end_height,
            "start_inclusive": start_inclusive,
            "end_inclusive": end_inclusive,
            "timezone": timezone,
            "sort": sort,
            "limit_per_pair": limit_per_pair,
        }
        return DataCollection(self._get_data, "timeseries/pair-metrics", params)

    def get_pair_candles(
        self,
        pairs: Union[List[str], str],
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
        limit_per_pair: Optional[int] = None,
    ) -> DataCollection:
        """
        Returns candles for specified asset pairs.
        Results are ordered by tuple (pair, time).

        :param pairs: A single asset-asset pairs (e.g. "btc-usd") or a list of asset-asset-pairs to return info for.
        :type pairs: list(str), str
        :param frequency: frequency of the returned timeseries, e.g 15s, 1d, etc.
        :type frequency: str
        :param page_size: number of items returned per page when calling the API. If the request times out, try using a smaller number.
        :type page_size: int
        :param paging_from: Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
        :type paging_from: PagingFrom, str
        :param start_time: Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type end_time: datetime, date, str
        :param start_height: Start block of the timeseries (only applicable when querying with frequency 1b).
        :type start_height: int
        :param end_height: End block of the timeseries (only applicable when querying with frequency 1b).
        :type end_height: int
        :param start_inclusive: Flag to define if start timestamp must be included in the timeseries if present. True by default.
        :type start_inclusive: bool
        :param end_inclusive: Flag to define if end timestamp must be included in the timeseries if present. True by default.
        :type end_inclusive: bool
        :param timezone: timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.
        :type timezone: str
        :param limit_per_pair: How many entries _per asset pair_ the result should contain.
        :type limit_per_pair: int
        :return: Asset pair candles timeseries.
        :rtype: DataCollection
        """

        params: Dict[str, Any] = {
            "pairs": pairs,
            "frequency": frequency,
            "page_size": page_size,
            "paging_from": paging_from,
            "start_time": start_time,
            "end_time": end_time,
            "start_height": start_height,
            "end_height": end_height,
            "start_inclusive": start_inclusive,
            "end_inclusive": end_inclusive,
            "timezone": timezone,
            "limit_per_pair": limit_per_pair,
        }
        return DataCollection(self._get_data, "timeseries/pair-candles", params)

    def get_institution_metrics(
        self,
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
        limit_per_institution: Optional[int] = None,
    ) -> DataCollection:
        """
        Returns metrics for specified institutions.

        :param institutions: A single institution name or a list of institutions to return info for.
        :type institutions: list(str), str
        :param metrics: list of _institution-specific_ metric names, e.g. 'gbtc_total_assets'
        :type metrics: list(str), str
        :param frequency: frequency of the returned timeseries, e.g 15s, 1d, etc.
        :type frequency: str
        :param page_size: number of items returned per page when calling the API. If the request times out, try using a smaller number.
        :type page_size: int
        :param paging_from: Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
        :type paging_from: PagingFrom, str
        :param start_time: Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type end_time: datetime, date, str
        :param start_height: Start block of the timeseries (only applicable when querying with frequency 1b).
        :type start_height: int
        :param end_height: End block of the timeseries (only applicable when querying with frequency 1b).
        :type end_height: int
        :param start_inclusive: Flag to define if start timestamp must be included in the timeseries if present. True by default.
        :type start_inclusive: bool
        :param end_inclusive: Flag to define if end timestamp must be included in the timeseries if present. True by default.
        :type end_inclusive: bool
        :param timezone: timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.
        :type timezone: str
        :param sort: How results will be sorted, e.g. "institution", or "time". Default is "institution".
        :type sort: str
        :param limit_per_institution: How many entries _per institution_ the result should contain.
        :type limit_per_institution: int
        :return: Asset Metrics timeseries.
        :rtype: DataCollection
        """

        params: Dict[str, Any] = {
            "institutions": institutions,
            "metrics": metrics,
            "frequency": frequency,
            "page_size": page_size,
            "paging_from": paging_from,
            "start_time": start_time,
            "end_time": end_time,
            "start_height": start_height,
            "end_height": end_height,
            "start_inclusive": start_inclusive,
            "end_inclusive": end_inclusive,
            "timezone": timezone,
            "sort": sort,
            "limit_per_institution": limit_per_institution,
        }
        return DataCollection(self._get_data, "timeseries/institution-metrics", params)

    def get_index_candles(
        self,
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
    ) -> DataCollection:
        """
        Returns index candles for specified indexes and date range.

        :param indexes: list of index names, e.g. 'CMBI10'
        :type indexes: list(str), str
        :param frequency: frequency of the returned timeseries, e.g 15s, 1d, etc.
        :type frequency: str
        :param page_size: number of items returned per page when calling the API. If the request times out, try using a smaller number.
        :type page_size: int
        :param paging_from: Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
        :type paging_from: PagingFrom, str
        :param start_time: Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type end_time: datetime, date, str
        :param start_inclusive: Flag to define if start timestamp must be included in the timeseries if present. True by default.
        :type start_inclusive: bool
        :param end_inclusive: Flag to define if end timestamp must be included in the timeseries if present. True by default.
        :type end_inclusive: bool
        :param timezone: timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.
        :type timezone: str
        :param limit_per_index: How many entries _per index_ the result should contain.
        :type limit_per_index: int
        :return: Index Candles timeseries.
        :rtype: DataCollection
        """

        params: Dict[str, Any] = {
            "indexes": indexes,
            "frequency": frequency,
            "page_size": page_size,
            "paging_from": paging_from,
            "start_time": start_time,
            "end_time": end_time,
            "start_inclusive": start_inclusive,
            "end_inclusive": end_inclusive,
            "timezone": timezone,
            "limit_per_index": limit_per_index,
        }
        return DataCollection(self._get_data, "timeseries/index-candles", params)

    def get_index_levels(
        self,
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
    ) -> DataCollection:
        """
        Returns index levels for specified indexes and date range.

        :param indexes: list of index names, e.g. 'CMBI10'
        :type indexes: list(str), str
        :param frequency: frequency of the returned timeseries, e.g 15s, 1d, etc.
        :type frequency: str
        :param page_size: number of items returned per page when calling the API. If the request times out, try using a smaller number.
        :type page_size: int
        :param paging_from: Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
        :type paging_from: PagingFrom, str
        :param start_time: Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type end_time: datetime, date, str
        :param start_inclusive: Flag to define if start timestamp must be included in the timeseries if present. True by default.
        :type start_inclusive: bool
        :param end_inclusive: Flag to define if end timestamp must be included in the timeseries if present. True by default.
        :type end_inclusive: bool
        :param timezone: timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.
        :type timezone: str
        :param limit_per_index: How many entries _per index_ the result should contain.
        :type limit_per_index: int
        :return: Index Levels timeseries.
        :rtype: DataCollection
        """

        params: Dict[str, Any] = {
            "indexes": indexes,
            "frequency": frequency,
            "page_size": page_size,
            "paging_from": paging_from,
            "start_time": start_time,
            "end_time": end_time,
            "start_inclusive": start_inclusive,
            "end_inclusive": end_inclusive,
            "timezone": timezone,
            "limit_per_index": limit_per_index,
        }
        return DataCollection(self._get_data, "timeseries/index-levels", params)

    def get_index_constituents(
        self,
        indexes: Union[List[str], str],
        frequency: Optional[str] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[Union[PagingFrom, str]] = "start",
        start_time: Optional[Union[datetime, date, str]] = None,
        end_time: Optional[Union[datetime, date, str]] = None,
        start_inclusive: Optional[bool] = None,
        end_inclusive: Optional[bool] = None,
        timezone: Optional[str] = None,
    ) -> DataCollection:
        """
        Returns index constituents for specified indexes and date range.

        :param indexes: list of index names, e.g. 'CMBI10'
        :type indexes: list(str), str
        :param frequency: frequency of the returned timeseries, e.g 15s, 1d, etc.
        :type frequency: str
        :param page_size: number of items returned per page when calling the API. If the request times out, try using a smaller number.
        :type page_size: int
        :param paging_from: Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
        :type paging_from: PagingFrom, str
        :param start_time: Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type end_time: datetime, date, str
        :param start_inclusive: Flag to define if start timestamp must be included in the timeseries if present. True by default.
        :type start_inclusive: bool
        :param end_inclusive: Flag to define if end timestamp must be included in the timeseries if present. True by default.
        :type end_inclusive: bool
        :param timezone: timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.
        :type timezone: str
        :return: Index Constituents timeseries.
        :rtype: DataCollection
        """

        params: Dict[str, Any] = {
            "indexes": indexes,
            "frequency": frequency,
            "page_size": page_size,
            "paging_from": paging_from,
            "start_time": start_time,
            "end_time": end_time,
            "start_inclusive": start_inclusive,
            "end_inclusive": end_inclusive,
            "timezone": timezone,
        }
        return DataCollection(self._get_data, "timeseries/index-constituents", params)

    def get_market_metrics(
        self,
        markets: Union[List[str], str],
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
        sort: Optional[str] = None
    ) -> DataCollection:
        """
        Returns market metrics for specified markets, frequency and date range.
        For more information on market metrics, see: https://docs.coinmetrics.io/api/v4#operation/getTimeseriesMarketMetrics

        :param markets: list of market ids. Market ids use the following naming convention: `exchangeName-baseAsset-quoteAsset-spot` for spot markets, `exchangeName-futuresSymbol-future` for futures markets, and `exchangeName-optionsSymbol-option` for options markets. e.g., `'coinbase-btc-usd-spot'`, `'bitmex-XBTUSD-future'`
        :type markets: list(str), str
        :param metrics: list of metrics, i.e. 'liquidations_reported_future_buy_units_1d'. See market metrics catalog for a list of supported metrics: https://docs.coinmetrics.io/api/v4#operation/getCatalogMarketMetrics
        :type metrics: list(str), str
        :param frequency: frequency of the returned timeseries, e.g 15s, 1d, etc.
        :type frequency: str
        :param page_size: number of items returned per page when calling the API. If the request times out, try using a smaller number.
        :type page_size: int
        :param paging_from: Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
        :type paging_from: PagingFrom, str
        :param start_time: Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type end_time: datetime, date, str
        :param start_inclusive: Flag to define if start timestamp must be included in the timeseries if present. True by default.
        :type start_inclusive: bool
        :param end_inclusive: Flag to define if end timestamp must be included in the timeseries if present. True by default.
        :type end_inclusive: bool
        :param timezone: timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.
        :type timezone: str
        :param limit_per_market: How many entries _per market_ the result should contain.
        :type limit_per_market: int
        :param sort: How results will be sorted. Metrics are sorted by (market, time) by default. If you want to sort
        1d metrics by (time, market) you should choose time as value for the sort parameter. Sorting by time is useful
        if you request metrics for a set of markets.
        :type sort: str
        :return: Market Candles timeseries.
        :rtype: DataCollection
        """

        params: Dict[str, Any] = {
            "markets": markets,
            "metrics": metrics,
            "frequency": frequency,
            "page_size": page_size,
            "paging_from": paging_from,
            "start_time": start_time,
            "end_time": end_time,
            "start_inclusive": start_inclusive,
            "end_inclusive": end_inclusive,
            "timezone": timezone,
            "limit_per_market": limit_per_market,
            "sort": sort
        }
        return DataCollection(self._get_data, "timeseries/market-metrics", params)

    def get_market_candles(
        self,
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
    ) -> DataCollection:
        """
        Returns market candles for specified markets, frequency and date range.
        For more information on market candles, see: https://docs.coinmetrics.io/info/markets/candles

        :param markets: list of market ids. Market ids use the following naming convention: `exchangeName-baseAsset-quoteAsset-spot` for spot markets, `exchangeName-futuresSymbol-future` for futures markets, and `exchangeName-optionsSymbol-option` for options markets. e.g., `'coinbase-btc-usd-spot'`, `'bitmex-XBTUSD-future'`
        :type markets: list(str), str
        :param frequency: frequency of the returned timeseries, e.g 15s, 1d, etc.
        :type frequency: str
        :param page_size: number of items returned per page when calling the API. If the request times out, try using a smaller number.
        :type page_size: int
        :param paging_from: Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
        :type paging_from: PagingFrom, str
        :param start_time: Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type end_time: datetime, date, str
        :param start_inclusive: Flag to define if start timestamp must be included in the timeseries if present. True by default.
        :type start_inclusive: bool
        :param end_inclusive: Flag to define if end timestamp must be included in the timeseries if present. True by default.
        :type end_inclusive: bool
        :param timezone: timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.
        :type timezone: str
        :param limit_per_market: How many entries _per market_ the result should contain.
        :type limit_per_market: int
        :return: Market Candles timeseries.
        :rtype: DataCollection
        """

        params: Dict[str, Any] = {
            "markets": markets,
            "frequency": frequency,
            "page_size": page_size,
            "paging_from": paging_from,
            "start_time": start_time,
            "end_time": end_time,
            "start_inclusive": start_inclusive,
            "end_inclusive": end_inclusive,
            "timezone": timezone,
            "limit_per_market": limit_per_market,
        }
        return DataCollection(self._get_data, "timeseries/market-candles", params)

    def get_market_trades(
        self,
        markets: Union[List[str], str],
        page_size: Optional[int] = None,
        paging_from: Optional[Union[PagingFrom, str]] = "start",
        start_time: Optional[Union[datetime, date, str]] = None,
        end_time: Optional[Union[datetime, date, str]] = None,
        start_inclusive: Optional[bool] = None,
        end_inclusive: Optional[bool] = None,
        timezone: Optional[str] = None,
        limit_per_market: Optional[int] = None,
        min_confirmations: Optional[int] = None
    ) -> DataCollection:
        """
        Returns market trades for specified markets and date range.
        For more information on market trades, see: https://docs.coinmetrics.io/info/markets/trades

        :param markets: list of market ids. Market ids use the following naming convention: `exchangeName-baseAsset-quoteAsset-spot` for spot markets, `exchangeName-futuresSymbol-future` for futures markets, and `exchangeName-optionsSymbol-option` for options markets. e.g., `'coinbase-btc-usd-spot'`, `'bitmex-XBTUSD-future'`
        :type markets: list(str), str
        :param page_size: number of items returned per page when calling the API. If the request times out, try using a smaller number.
        :type page_size: int
        :param paging_from: Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
        :type paging_from: PagingFrom, str
        :param start_time: Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type end_time: datetime, date, str
        :param start_inclusive: Flag to define if start timestamp must be included in the timeseries if present. True by default.
        :type start_inclusive: bool
        :param end_inclusive: Flag to define if end timestamp must be included in the timeseries if present. True by default.
        :type end_inclusive: bool
        :param timezone: timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.
        :type timezone: str
        :param limit_per_market: How many entries _per market_ the result should contain.
        :type limit_per_market: int
        :param min_confirmations: Specifies how many blocks behind the chain tip trades are based on. Default is 2.
        :type min_confirmations: int
        :return: Market Trades timeseries.
        :rtype: DataCollection
        """

        params: Dict[str, Any] = {
            "markets": markets,
            "page_size": page_size,
            "paging_from": paging_from,
            "start_time": start_time,
            "end_time": end_time,
            "start_inclusive": start_inclusive,
            "end_inclusive": end_inclusive,
            "timezone": timezone,
            "limit_per_market": limit_per_market,
            "min_confirmations": min_confirmations,
        }
        return DataCollection(self._get_data, "timeseries/market-trades", params)

    def get_market_open_interest(
        self,
        markets: Union[List[str], str],
        page_size: Optional[int] = None,
        paging_from: Optional[Union[PagingFrom, str]] = "start",
        start_time: Optional[Union[datetime, date, str]] = None,
        end_time: Optional[Union[datetime, date, str]] = None,
        start_inclusive: Optional[bool] = None,
        end_inclusive: Optional[bool] = None,
        timezone: Optional[str] = None,
        limit_per_market: Optional[int] = None,
    ) -> DataCollection:
        """
        Returns market open interest for specified markets and date range.
        For more information on open interest, see: https://docs.coinmetrics.io/info/markets/openinterest

        :param markets: list of market ids. Market ids use the following naming convention: `exchangeName-baseAsset-quoteAsset-spot` for spot markets, `exchangeName-futuresSymbol-future` for futures markets, and `exchangeName-optionsSymbol-option` for options markets. e.g., `'coinbase-btc-usd-spot'`, `'bitmex-XBTUSD-future'`
        :type markets: list(str), str
        :param page_size: number of items returned per page when calling the API. If the request times out, try using a smaller number.
        :type page_size: int
        :param paging_from: Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
        :type paging_from: PagingFrom, str
        :param start_time: Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type end_time: datetime, date, str
        :param start_inclusive: Flag to define if start timestamp must be included in the timeseries if present. True by default.
        :type start_inclusive: bool
        :param end_inclusive: Flag to define if end timestamp must be included in the timeseries if present. True by default.
        :type end_inclusive: bool
        :param timezone: timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.
        :type timezone: str
        :param limit_per_market: How many entries _per market_ the result should contain.
        :type limit_per_market: int
        :return: Market Open Interest timeseries.
        :rtype: DataCollection
        """

        params: Dict[str, Any] = {
            "markets": markets,
            "page_size": page_size,
            "paging_from": paging_from,
            "start_time": start_time,
            "end_time": end_time,
            "start_inclusive": start_inclusive,
            "end_inclusive": end_inclusive,
            "timezone": timezone,
            "limit_per_market": limit_per_market,
        }
        return DataCollection(self._get_data, "timeseries/market-openinterest", params)

    def get_market_liquidations(
        self,
        markets: Union[List[str], str],
        page_size: Optional[int] = None,
        paging_from: Optional[Union[PagingFrom, str]] = "start",
        start_time: Optional[Union[datetime, date, str]] = None,
        end_time: Optional[Union[datetime, date, str]] = None,
        start_inclusive: Optional[bool] = None,
        end_inclusive: Optional[bool] = None,
        timezone: Optional[str] = None,
        limit_per_market: Optional[int] = None,
    ) -> DataCollection:
        """
        Returns market liquidations for specified markets and date range.
        For more information on liquidations, see: https://docs.coinmetrics.io/info/markets/liquidations

        :param markets: list of market ids. Market ids use the following naming convention: `exchangeName-baseAsset-quoteAsset-spot` for spot markets, `exchangeName-futuresSymbol-future` for futures markets, and `exchangeName-optionsSymbol-option` for options markets. e.g., `'coinbase-btc-usd-spot'`, `'bitmex-XBTUSD-future'`
        :type markets: list(str), str
        :param page_size: number of items returned per page when calling the API. If the request times out, try using a smaller number.
        :type page_size: int
        :param paging_from: Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
        :type paging_from: PagingFrom, str
        :param start_time: Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type end_time: datetime, date, str
        :param start_inclusive: Flag to define if start timestamp must be included in the timeseries if present. True by default.
        :type start_inclusive: bool
        :param end_inclusive: Flag to define if end timestamp must be included in the timeseries if present. True by default.
        :type end_inclusive: bool
        :param timezone: timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.
        :type timezone: str
        :param limit_per_market: How many entries _per market_ the result should contain.
        :type limit_per_market: int
        :return: Market Liquidations timeseries.
        :rtype: DataCollection
        """

        params: Dict[str, Any] = {
            "markets": markets,
            "page_size": page_size,
            "paging_from": paging_from,
            "start_time": start_time,
            "end_time": end_time,
            "start_inclusive": start_inclusive,
            "end_inclusive": end_inclusive,
            "timezone": timezone,
            "limit_per_market": limit_per_market,
        }
        return DataCollection(self._get_data, "timeseries/market-liquidations", params)

    def get_market_funding_rates(
        self,
        markets: Union[List[str], str],
        page_size: Optional[int] = None,
        paging_from: Optional[Union[PagingFrom, str]] = "start",
        start_time: Optional[Union[datetime, date, str]] = None,
        end_time: Optional[Union[datetime, date, str]] = None,
        start_inclusive: Optional[bool] = None,
        end_inclusive: Optional[bool] = None,
        timezone: Optional[str] = None,
        limit_per_market: Optional[int] = None,
    ) -> DataCollection:
        """
        Returns market funding rates for specified markets and date range.
        For more information on funding rates, see: https://docs.coinmetrics.io/info/markets/fundingrates

        :param markets: list of market ids. Market ids use the following naming convention: `exchangeName-baseAsset-quoteAsset-spot` for spot markets, `exchangeName-futuresSymbol-future` for futures markets, and `exchangeName-optionsSymbol-option` for options markets. e.g., `'coinbase-btc-usd-spot'`, `'bitmex-XBTUSD-future'`
        :type markets: list(str), str
        :param page_size: number of items returned per page when calling the API. If the request times out, try using a smaller number.
        :type page_size: int
        :param paging_from: Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
        :type paging_from: PagingFrom, str
        :param start_time: Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type end_time: datetime, date, str
        :param start_inclusive: Flag to define if start timestamp must be included in the timeseries if present. True by default.
        :type start_inclusive: bool
        :param end_inclusive: Flag to define if end timestamp must be included in the timeseries if present. True by default.
        :type end_inclusive: bool
        :param timezone: timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.
        :type timezone: str
        :param limit_per_market: How many entries _per market_ the result should contain.
        :type limit_per_market: int
        :return: Market Funding Rates timeseries.
        :rtype: DataCollection
        """

        params: Dict[str, Any] = {
            "markets": markets,
            "page_size": page_size,
            "paging_from": paging_from,
            "start_time": start_time,
            "end_time": end_time,
            "start_inclusive": start_inclusive,
            "end_inclusive": end_inclusive,
            "timezone": timezone,
            "limit_per_market": limit_per_market,
        }
        return DataCollection(self._get_data, "timeseries/market-funding-rates", params)

    def get_market_orderbooks(
        self,
        markets: Union[List[str], str],
        page_size: Optional[int] = None,
        paging_from: Optional[Union[PagingFrom, str]] = "start",
        start_time: Optional[Union[datetime, date, str]] = None,
        end_time: Optional[Union[datetime, date, str]] = None,
        start_inclusive: Optional[bool] = None,
        end_inclusive: Optional[bool] = None,
        depth_limit: Optional[str] = "100",
        timezone: Optional[str] = None,
        limit_per_market: Optional[int] = None,
    ) -> DataCollection:
        """
        Returns market order books for specified markets and date range.
        For more information on order books, see: https://docs.coinmetrics.io/info/markets/orderbook

        :param markets: list of market ids. Market ids use the following naming convention: `exchangeName-baseAsset-quoteAsset-spot` for spot markets, `exchangeName-futuresSymbol-future` for futures markets, and `exchangeName-optionsSymbol-option` for options markets. e.g., `'coinbase-btc-usd-spot'`, `'bitmex-XBTUSD-future'`
        :type markets: list(str), str
        :param page_size: number of items returned per page when calling the API. If the request times out, try using a smaller number.
        :type page_size: int
        :param paging_from: Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
        :type paging_from: PagingFrom, str
        :param start_time: Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type end_time: datetime, date, str
        :param start_inclusive: Flag to define if start timestamp must be included in the timeseries if present. True by default.
        :type start_inclusive: bool
        :param end_inclusive: Flag to define if end timestamp must be included in the timeseries if present. True by default.
        :type end_inclusive: bool
        :param depth_limit: book depth limit, 100 levels max or full book that is not limited and provided as is from the exchange. Full book snapshots are collected once per hour
        :type depth_limit: str
        :param timezone: timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.
        :type timezone: str
        :param limit_per_market: How many entries _per market_ the result should contain.
        :type limit_per_market: int
        :return: Market Order Books timeseries.
        :rtype: DataCollection
        """

        params: Dict[str, Any] = {
            "markets": markets,
            "page_size": page_size,
            "paging_from": paging_from,
            "start_time": start_time,
            "end_time": end_time,
            "start_inclusive": start_inclusive,
            "end_inclusive": end_inclusive,
            "limit_per_market": limit_per_market,
            "depth_limit": depth_limit,
            "timezone": timezone,
        }
        return DataCollection(self._get_data, "timeseries/market-orderbooks", params)

    def get_market_quotes(
        self,
        markets: Union[List[str], str],
        page_size: Optional[int] = None,
        paging_from: Optional[Union[PagingFrom, str]] = "start",
        start_time: Optional[Union[datetime, date, str]] = None,
        end_time: Optional[Union[datetime, date, str]] = None,
        start_inclusive: Optional[bool] = None,
        end_inclusive: Optional[bool] = None,
        timezone: Optional[str] = None,
        limit_per_market: Optional[int] = None,
        include_one_sided: Optional[bool] = None
    ) -> DataCollection:
        """
        Returns market quotes for specified markets and date range.
        For more information on quotes, see: https://docs.coinmetrics.io/info/markets/quotes

        :param markets: list of market ids. Market ids use the following naming convention: `exchangeName-baseAsset-quoteAsset-spot` for spot markets, `exchangeName-futuresSymbol-future` for futures markets, and `exchangeName-optionsSymbol-option` for options markets. e.g., `'coinbase-btc-usd-spot'`, `'bitmex-XBTUSD-future'`
        :type markets: list(str), str
        :param page_size: number of items returned per page when calling the API. If the request times out, try using a smaller number.
        :type page_size: int
        :param paging_from: Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
        :type paging_from: PagingFrom, str
        :param start_time: Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type end_time: datetime, date, str
        :param start_inclusive: Flag to define if start timestamp must be included in the timeseries if present. True by default.
        :type start_inclusive: bool
        :param end_inclusive: Flag to define if end timestamp must be included in the timeseries if present. True by default.
        :type end_inclusive: bool
        :param timezone: timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.
        :type timezone: str
        :param limit_per_market: How many entries _per market_ the result should contain.
        :type limit_per_market: int
        :param include_one_sided: Default: false Include one-side and empty books in quotes response.
        :type include_one_sided: bool
        :return: Market Quotes timeseries.
        :rtype: DataCollection
        """

        params: Dict[str, Any] = {
            "markets": markets,
            "page_size": page_size,
            "paging_from": paging_from,
            "start_time": start_time,
            "end_time": end_time,
            "start_inclusive": start_inclusive,
            "end_inclusive": end_inclusive,
            "timezone": timezone,
            "limit_per_market": limit_per_market,
            "include_one_sided": include_one_sided
        }
        return DataCollection(self._get_data, "timeseries/market-quotes", params)

    def get_market_contract_prices(
        self,
        markets: Union[List[str], str],
        page_size: Optional[int] = None,
        paging_from: Optional[Union[PagingFrom, str]] = "start",
        start_time: Optional[Union[datetime, date, str]] = None,
        end_time: Optional[Union[datetime, date, str]] = None,
        start_inclusive: Optional[bool] = None,
        end_inclusive: Optional[bool] = None,
        timezone: Optional[str] = None,
        limit_per_market: Optional[int] = None,
    ) -> DataCollection:
        """
        Returns contract prices for specified markets. This includes index price and mark price that are used by the exchange for settlement and risk management purposes.

        :param markets: list of market ids. Market ids use the following naming convention: `exchangeName-baseAsset-quoteAsset-spot` for spot markets, `exchangeName-futuresSymbol-future` for futures markets, and `exchangeName-optionsSymbol-option` for options markets. e.g., `'coinbase-btc-usd-spot'`, `'bitmex-XBTUSD-future', 'deribit-ETH-25MAR22-1200-P-option'`
        :type markets: list(str), str
        :param page_size: number of items returned per page when calling the API. If the request times out, try using a smaller number.
        :type page_size: int
        :param paging_from: Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
        :type paging_from: PagingFrom, str
        :param start_time: Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type end_time: datetime, date, str
        :param start_inclusive: Flag to define if start timestamp must be included in the timeseries if present. True by default.
        :type start_inclusive: bool
        :param end_inclusive: Flag to define if end timestamp must be included in the timeseries if present. True by default.
        :type end_inclusive: bool
        :param timezone: timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.
        :type timezone: str
        :param limit_per_market: How many entries _per market_ the result should contain.
        :type limit_per_market: int
        :return: Market Contract Prices timeseries.
        :rtype: DataCollection
        """

        params: Dict[str, Any] = {
            "markets": markets,
            "page_size": page_size,
            "paging_from": paging_from,
            "start_time": start_time,
            "end_time": end_time,
            "start_inclusive": start_inclusive,
            "end_inclusive": end_inclusive,
            "timezone": timezone,
            "limit_per_market": limit_per_market,
        }
        return DataCollection(
            self._get_data, "timeseries/market-contract-prices", params
        )

    def get_market_implied_volatility(
        self,
        markets: Union[List[str], str],
        page_size: Optional[int] = None,
        paging_from: Optional[Union[PagingFrom, str]] = "start",
        start_time: Optional[Union[datetime, date, str]] = None,
        end_time: Optional[Union[datetime, date, str]] = None,
        start_inclusive: Optional[bool] = None,
        end_inclusive: Optional[bool] = None,
        timezone: Optional[str] = None,
        limit_per_market: Optional[int] = None,
    ) -> DataCollection:
        """
        Returns implied volatility for specified markets.

        :param markets: list of market ids. Market ids use the following naming convention: `exchangeName-baseAsset-quoteAsset-spot` for spot markets, `exchangeName-futuresSymbol-future` for futures markets, and `exchangeName-optionsSymbol-option` for options markets. e.g., `'coinbase-btc-usd-spot'`, `'bitmex-XBTUSD-future', 'deribit-ETH-25MAR22-1200-P-option'`
        :type markets: list(str), str
        :param page_size: number of items returned per page when calling the API. If the request times out, try using a smaller number.
        :type page_size: int
        :param paging_from: Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
        :type paging_from: PagingFrom, str
        :param start_time: Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type end_time: datetime, date, str
        :param start_inclusive: Flag to define if start timestamp must be included in the timeseries if present. True by default.
        :type start_inclusive: bool
        :param end_inclusive: Flag to define if end timestamp must be included in the timeseries if present. True by default.
        :type end_inclusive: bool
        :param timezone: timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.
        :type timezone: str
        :param limit_per_market: How many entries _per market_ the result should contain.
        :type limit_per_market: int
        :return: Market Volatility timeseries.
        :rtype: DataCollection
        """

        params: Dict[str, Any] = {
            "markets": markets,
            "page_size": page_size,
            "paging_from": paging_from,
            "start_time": start_time,
            "end_time": end_time,
            "start_inclusive": start_inclusive,
            "end_inclusive": end_inclusive,
            "timezone": timezone,
            "limit_per_market": limit_per_market,
        }
        return DataCollection(
            self._get_data, "timeseries/market-implied-volatility", params
        )

    def get_market_greeks(
        self,
        markets: Union[List[str], str],
        page_size: Optional[int] = None,
        paging_from: Optional[Union[PagingFrom, str]] = "start",
        start_time: Optional[Union[datetime, date, str]] = None,
        end_time: Optional[Union[datetime, date, str]] = None,
        start_inclusive: Optional[bool] = None,
        end_inclusive: Optional[bool] = None,
        timezone: Optional[str] = None,
        limit_per_market: Optional[int] = None,
    ) -> DataCollection:
        """
        Returns greeks for option markets.

        :param markets: list of market ids. Market ids use the following naming convention: `exchangeName-baseAsset-quoteAsset-spot` for spot markets, `exchangeName-futuresSymbol-future` for futures markets, and `exchangeName-optionsSymbol-option` for options markets. e.g., `'coinbase-btc-usd-spot'`, `'bitmex-XBTUSD-future', 'deribit-ETH-25MAR22-1200-P-option'`
        :type markets: list(str), str
        :param page_size: number of items returned per page when calling the API. If the request times out, try using a smaller number.
        :type page_size: int
        :param paging_from: Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
        :type paging_from: PagingFrom, str
        :param start_time: Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type end_time: datetime, date, str
        :param start_inclusive: Flag to define if start timestamp must be included in the timeseries if present. True by default.
        :type start_inclusive: bool
        :param end_inclusive: Flag to define if end timestamp must be included in the timeseries if present. True by default.
        :type end_inclusive: bool
        :param timezone: timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.
        :type timezone: str
        :param limit_per_market: How many entries _per market_ the result should contain.
        :type limit_per_market: int
        :return: Market Volatility timeseries.
        :rtype: DataCollection
        """

        params: Dict[str, Any] = {
            "markets": markets,
            "page_size": page_size,
            "paging_from": paging_from,
            "start_time": start_time,
            "end_time": end_time,
            "start_inclusive": start_inclusive,
            "end_inclusive": end_inclusive,
            "timezone": timezone,
            "limit_per_market": limit_per_market,
        }
        return DataCollection(self._get_data, "timeseries/market-greeks", params)

    def get_mining_pool_tips_summary(
        self,
        assets: Union[List[str], str],
        page_size: Optional[int] = None,
        paging_from: Optional[Union[PagingFrom, str]] = "start",
        start_time: Optional[Union[datetime, date, str]] = None,
        end_time: Optional[Union[datetime, date, str]] = None,
        start_inclusive: Optional[bool] = None,
        end_inclusive: Optional[bool] = None,
        timezone: Optional[str] = None,
    ) -> DataCollection:
        """
        Returns mining pool tips summaries for specified assets.

        :param assets: list of asset names, e.g. 'btc'
        :type assets: list(str), str
        :param page_size: number of items returned per page when calling the API. If the request times out, try using a smaller number.
        :type page_size: int
        :param paging_from: Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
        :type paging_from: PagingFrom, str
        :param start_time: Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type end_time: datetime, date, str
        :param start_inclusive: Flag to define if start timestamp must be included in the timeseries if present. True by default.
        :type start_inclusive: bool
        :param end_inclusive: Flag to define if end timestamp must be included in the timeseries if present. True by default.
        :type end_inclusive: bool
        :param timezone: timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.
        :type timezone: str
        :return: Mining Pool Tips timeseries.
        :rtype: DataCollection
        """

        params: Dict[str, Any] = {
            "assets": assets,
            "page_size": page_size,
            "paging_from": paging_from,
            "start_time": start_time,
            "end_time": end_time,
            "start_inclusive": start_inclusive,
            "end_inclusive": end_inclusive,
            "timezone": timezone,
        }
        return DataCollection(
            self._get_data, "timeseries/mining-pool-tips-summary", params
        )

    def get_mempool_feerates(
        self,
        assets: Union[List[str], str],
        page_size: Optional[int] = 200,
        paging_from: Optional[Union[PagingFrom, str]] = "start",
        start_time: Optional[Union[datetime, date, str]] = None,
        end_time: Optional[Union[datetime, date, str]] = None,
        start_inclusive: Optional[bool] = None,
        end_inclusive: Optional[bool] = None,
        timezone: Optional[str] = None,
    ) -> DataCollection:
        """
        Returns mempool feerates for the specified assets. Note: for this method, page_size must be <= 200.

        :param assets: list of asset names, e.g. 'btc'
        :type assets: list(str), str
        :param page_size: number of items returned per page when calling the API. If the request times out, try using a smaller number.
        :type page_size: int
        :param paging_from: Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
        :type paging_from: PagingFrom, str
        :param start_time: Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type end_time: datetime, date, str
        :param start_inclusive: Flag to define if start timestamp must be included in the timeseries if present. True by default.
        :type start_inclusive: bool
        :param end_inclusive: Flag to define if end timestamp must be included in the timeseries if present. True by default.
        :type end_inclusive: bool
        :param timezone: timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.
        :type timezone: str
        :return: Mempool Fee Rates timeseries.
        :rtype: DataCollection
        """

        params: Dict[str, Any] = {
            "assets": assets,
            "page_size": page_size,
            "paging_from": paging_from,
            "start_time": start_time,
            "end_time": end_time,
            "start_inclusive": start_inclusive,
            "end_inclusive": end_inclusive,
            "timezone": timezone,
        }
        return DataCollection(self._get_data, "timeseries/mempool-feerates", params)

    def get_stream_asset_metrics(
        self,
        assets: Union[List[str], str],
        metrics: Union[List[str], str],
        frequency: Optional[str] = None,
        backfill: Union[Backfill, str] = Backfill.LATEST,
    ) -> CmStream:
        """
        Returns timeseries stream of metrics for specified assets.

        :param assets: list of asset names, e.g. 'btc'
        :type assets: list(str), str
        :param metrics: list of _asset-specific_ metric names, e.g. 'PriceUSD'
        :type metrics: list(str), str
        :param frequency: frequency of the returned timeseries, e.g 15s, 1d, etc.
        :type frequency: str
        :param backfill: What data should be sent upon a connection ("latest" or "none"). By default the latest values are sent just before real-time data.
        :type backfill: str
        :return: Asset Metrics timeseries stream.
        :rtype: CmStream
        """

        params: Dict[str, Any] = {
            "assets": assets,
            "metrics": metrics,
            "frequency": frequency,
            "backfill": backfill,
        }
        return self._get_stream_data("timeseries-stream/asset-metrics", params)

    def get_stream_market_trades(
        self,
        markets: Union[List[str], str],
        backfill: Union[Backfill, str] = Backfill.LATEST,
    ) -> CmStream:
        """
        Returns timeseries stream of market trades.

        :param markets: list of markets or market patterns like exchange-* or exchange-*-spot or *USDT-future.
        :type markets: list(str), str
        :param backfill: What data should be sent upon a connection ("latest" or "none"). By default the latest values are sent just before real-time data.
        :type backfill: str
        :return: Market Trades timeseries stream.
        :rtype: CmStream
        """

        params: Dict[str, Any] = {"markets": markets, "backfill": backfill}
        return self._get_stream_data("timeseries-stream/market-trades", params)

    def get_stream_market_orderbooks(
        self,
        markets: Union[List[str], str],
        backfill: Union[Backfill, str] = Backfill.LATEST,
        depth_limit: Optional[str] = None
    ) -> CmStream:
        """
        Returns timeseries stream of market orderbooks.

        :param markets: list of markets or market patterns like exchange-* or exchange-*-spot or *USDT-future.
        :type markets: list(str), str
        :param backfill: What data should be sent upon a connection ("latest" or "none"). By default the latest values are sent just before real-time data.
        :type backfill: str
        :param depth_limit: Default: 100. Supported Values: 100 "full_book". Book depth limit.
        :type depth_limit: str
        :return: Market Orderbooks timeseries stream.
        :rtype: CmStream
        """

        params: Dict[str, Any] = {
            "markets": markets,
            "backfill": backfill,
            "depth_limit": depth_limit
        }
        return self._get_stream_data("timeseries-stream/market-orderbooks", params)

    def get_stream_market_quotes(
        self,
        markets: Union[List[str], str],
        backfill: Union[Backfill, str] = Backfill.LATEST,
        include_one_sided: Optional[bool] = None
    ) -> CmStream:
        """
        Returns timeseries stream of market quotes.

        :param markets: list of markets or market patterns like exchange-* or exchange-*-spot or *USDT-future.
        :type markets: list(str), str
        :param backfill: What data should be sent upon a connection ("latest" or "none"). By default the latest values are sent just before real-time data.
        :type backfill: str
        :param include_one_sided: Default: false. Include one-side and empty books in quotes response.
        :type include_one_sided: bool
        :return: Market Quotes timeseries stream.
        :rtype: CmStream
        """

        params: Dict[str, Any] = {
            "markets": markets,
            "backfill": backfill,
            "include_one_sided": include_one_sided
        }
        return self._get_stream_data("timeseries-stream/market-quotes", params)

    def get_stream_market_candles(
        self,
        markets: Union[List[str], str],
        frequency: Optional[str] = None,
        backfill: Union[Backfill, str] = Backfill.LATEST,
    ) -> CmStream:
        """
        Returns timeseries stream of market candles.

        :param markets: list of markets or market patterns like exchange-* or exchange-*-spot or *USDT-future.
        :type markets: list(str), str
        :param frequency: Candle duration. Supported values are 1m, 5m, 10m, 15m, 30m, 1h, 4h, 1d.
        :type frequency: str
        :param backfill: What data should be sent upon a connection ("latest" or "none"). By default the latest values are sent just before real-time data.
        :type backfill: str
        :return: Market Candles timeseries stream.
        :rtype: CmStream
        """

        params: Dict[str, Any] = {
            "markets": markets,
            "backfill": backfill,
            "frequency": frequency,
        }
        return self._get_stream_data("timeseries-stream/market-candles", params)

    def get_stream_index_levels(
        self,
        indexes: Union[List[str], str],
        backfill: Union[Backfill, str] = Backfill.LATEST,
    ) -> CmStream:
        """
        Returns timeseries stream of index levels.

        :param indexes: list of indxes or market patterns such as CMBIBTC
        :type markets: list(str), str
        :param backfill: What data should be sent upon a connection ("latest" or "none"). By default the latest values are sent just before real-time data.
        :type backfill: str
        :return: Index levels data timeseries stream.
        :rtype: CmStream
        """

        params: Dict[str, Any] = {
            "indexes": indexes,
            "backfill": backfill,
        }
        return self._get_stream_data("timeseries-stream/index-levels", params)

    def get_list_of_blocks(
        self,
        asset: str,
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
        timezone: Optional[str] = None,
    ) -> DataCollection:
        """
        Returns a list of blockchain blocks metadata.

        :param asset: Asset name
        :type asset: str
        :param block_hashes: Optional comma separated list of block hashes to filter a response.
        :type block_hashes: str, list(str)
        :param heights: Optional comma separated list of block heights to filter a response.
        :type heights: str, list(str)
        :param page_size: number of items returned per page when calling the API. If the request times out, try using a smaller number.
        :type page_size: int
        :param paging_from: Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
        :type paging_from: PagingFrom, str
        :param start_time: Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type end_time: datetime, date, str
        :param start_height: The start height indicates the beginning block height for the set of data that are returned. Mutually exclusive with start_time
        :type start_height: int
        :param end_height: The end height indicates the beginning block height for the set of data that are returned. Mutually exclusive with end_time
        :type end_height: int
        :param start_inclusive: Flag to define if start timestamp must be included in the timeseries if present. True by default.
        :type start_inclusive: bool
        :param end_inclusive: Flag to define if end timestamp must be included in the timeseries if present. True by default.
        :type end_inclusive: bool
        :param timezone: timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.
        :type timezone: str
        :return: list of blockchain blocks metadata
        :rtype: DataCollection
        """
        params: Dict[str, Any] = {
            "asset": asset,
            "block_hashes": block_hashes,
            "heights": heights,
            "page_size": page_size,
            "paging_from": paging_from,
            "start_time": start_time,
            "end_time": end_time,
            "start_height": start_height,
            "end_height": end_height,
            "start_inclusive": start_inclusive,
            "end_inclusive": end_inclusive,
            "timezone": timezone,
        }
        return DataCollection(self._get_data, f"blockchain/{asset}/blocks", params)

    def get_list_of_accounts(
        self,
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
        timezone: Optional[str] = None,
    ) -> DataCollection:
        """
        Returns a list of blockchain accounts with their balances.

        :param asset: Asset name
        :type asset: str
        :param accounts: Optional comma separated list of accounts to filter a response.
        :type accounts: str, list(str)
        :param page_size: number of items returned per page when calling the API. If the request times out, try using a smaller number.
        :type page_size: int
        :param paging_from: Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
        :type paging_from: PagingFrom, str
        :param start_time: Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type end_time: datetime, date, str
        :param start_height: The start height indicates the beginning block height for the set of data that are returned. Mutually exclusive with start_time
        :type start_height: int
        :param end_height: The end height indicates the beginning block height for the set of data that are returned. Mutually exclusive with end_time
        :type end_height: int
        :param start_chain_sequence_number: The start height indicates the beginning block height for the set of data that are returned. Mutually exclusive with start_time
        :type start_chain_sequence_number: int
        :param end_chain_sequence_number: The end height indicates the beginning block height for the set of data that are returned. Mutually exclusive with end_time
        :type end_chain_sequence_number: int
        :param start_inclusive: Flag to define if start timestamp must be included in the timeseries if present. True by default.
        :type start_inclusive: bool
        :param end_inclusive: Flag to define if end timestamp must be included in the timeseries if present. True by default.
        :type end_inclusive: bool
        :param timezone: timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.
        :type timezone: str
        :return: list of blockchain accounts metadata
        :rtype: DataCollection
        """
        params: Dict[str, Any] = {
            "asset": asset,
            "accounts": accounts,
            "page_size": page_size,
            "paging_from": paging_from,
            "start_time": start_time,
            "end_time": end_time,
            "start_height": start_height,
            "end_height": end_height,
            "start_chain_sequence_number": start_chain_sequence_number,
            "end_chain_sequence_number": end_chain_sequence_number,
            "start_inclusive": start_inclusive,
            "end_inclusive": end_inclusive,
            "timezone": timezone,
        }
        return DataCollection(self._get_data, f"blockchain/{asset}/accounts", params)

    def get_list_of_transactions(
        self,
        asset: str,
        transaction_hashes: Optional[Union[List[str], str]] = None,
        block_hashes: Optional[Union[List[str], str]] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[Union[PagingFrom, str]] = "start",
        start_time: Optional[Union[datetime, date, str]] = None,
        end_time: Optional[Union[datetime, date, str]] = None,
        start_height: Optional[int] = None,
        end_height: Optional[int] = None,
        start_inclusive: Optional[bool] = None,
        end_inclusive: Optional[bool] = None,
        timezone: Optional[str] = None,
    ) -> DataCollection:
        """
        Returns a list of blockchain transactions metadata.

        :param asset: Asset name
        :type asset: str
        :param transaction_hashes: Optional comma separated list of transaction hashes to filter a response.
        :type transaction_hashes: str, list(str)
        :param block_hashes: Optional comma separated list of block hashes to filter a response.
        :type block_hashes: str, list(str)
        :param page_size: number of items returned per page when calling the API. If the request times out, try using a smaller number.
        :type page_size: int
        :param paging_from: Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
        :type paging_from: PagingFrom, str
        :param start_time: Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type end_time: datetime, date, str
        :param start_height: The start height indicates the beginning block height for the set of data that are returned. Mutually exclusive with start_time
        :type start_height: int
        :param end_height: The end height indicates the beginning block height for the set of data that are returned. Mutually exclusive with end_time
        :type end_height: int
        :param start_inclusive: Flag to define if start timestamp must be included in the timeseries if present. True by default.
        :type start_inclusive: bool
        :param end_inclusive: Flag to define if end timestamp must be included in the timeseries if present. True by default.
        :type end_inclusive: bool
        :param timezone: timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.
        :type timezone: str
        :return: list of transaction metadata
        :rtype: DataCollection
        """
        params: Dict[str, Any] = {
            "asset": asset,
            "transaction_hashes": transaction_hashes,
            "block_hashes": block_hashes,
            "page_size": page_size,
            "paging_from": paging_from,
            "start_time": start_time,
            "end_time": end_time,
            "start_height": start_height,
            "end_height": end_height,
            "start_inclusive": start_inclusive,
            "end_inclusive": end_inclusive,
            "timezone": timezone,
        }
        return DataCollection(
            self._get_data, f"blockchain/{asset}/transactions", params
        )

    def get_list_of_balance_updates(
        self,
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
        timezone: Optional[str] = None,
    ) -> DataCollection:
        """
        Returns a list of blockchain accounts balance updates.

        :param asset: Asset name
        :type asset: str
        :param accounts: Optional comma separated list of accounts to filter a response.
        :type accounts: str, list(str)
        :param transaction_hashes: Optional comma separated list of transaction hashes to filter a response.
        :type transaction_hashes: str, list(str)
        :param block_hashes: Optional comma separated list of block hashes to filter a response.
        :type block_hashes: str, list(str)
        :param page_size: number of items returned per page when calling the API. If the request times out, try using a smaller number.
        :type page_size: int
        :param paging_from: Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
        :type paging_from: PagingFrom, str
        :param start_time: Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type end_time: datetime, date, str
        :param start_height: The start height indicates the beginning block height for the set of data that are returned. Mutually exclusive with start_time
        :type start_height: int
        :param end_height: The end height indicates the beginning block height for the set of data that are returned. Mutually exclusive with end_time
        :type end_height: int
        :param start_chain_sequence_number: The start height indicates the beginning block height for the set of data that are returned. Mutually exclusive with start_time
        :type start_chain_sequence_number: int
        :param end_chain_sequence_number: The end height indicates the beginning block height for the set of data that are returned. Mutually exclusive with end_time
        :type end_chain_sequence_number: int
        :param start_inclusive: Flag to define if start timestamp must be included in the timeseries if present. True by default.
        :type start_inclusive: bool
        :param end_inclusive: Flag to define if end timestamp must be included in the timeseries if present. True by default.
        :type end_inclusive: bool
        :param timezone: timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.
        :type timezone: str
        :return: list of balance updates
        :rtype: DataCollection
        """
        params: Dict[str, Any] = {
            "asset": asset,
            "accounts": accounts,
            "transaction_hashes": transaction_hashes,
            "block_hashes": block_hashes,
            "page_size": page_size,
            "paging_from": paging_from,
            "start_time": start_time,
            "end_time": end_time,
            "start_height": start_height,
            "end_height": end_height,
            "start_chain_sequence_number": start_chain_sequence_number,
            "end_chain_sequence_number": end_chain_sequence_number,
            "start_inclusive": start_inclusive,
            "end_inclusive": end_inclusive,
            "timezone": timezone,
        }
        return DataCollection(
            self._get_data, f"blockchain/{asset}/balance-updates", params
        )

    def get_list_of_blocks_v2(
        self,
        asset: str,
        block_hashes: Optional[Union[List[str], str]] = None,
        heights: Optional[Union[List[str], str]] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[Union[PagingFrom, str]] = "start",
        start_time: Optional[Union[datetime, date, str]] = None,
        end_time: Optional[Union[datetime, date, str]] = None,
        start_height: Optional[int] = None,
        end_height: Optional[int] = None,
        chain: Optional[bool] = None,
        start_inclusive: Optional[bool] = None,
        end_inclusive: Optional[bool] = None,
        timezone: Optional[str] = None,
    ) -> DataCollection:
        """
        Returns a list of blockchain blocks metadata.

        :param asset: Asset name
        :type asset: str
        :param block_hashes: Optional comma separated list of block hashes to filter a response.
        :type block_hashes: str, list(str)
        :param heights: Optional comma separated list of block heights to filter a response.
        :type heights: str, list(str)
        :param page_size: number of items returned per page when calling the API. If the request times out, try using a smaller number.
        :type page_size: int
        :param paging_from: Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
        :type paging_from: PagingFrom, str
        :param start_time: Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type end_time: datetime, date, str
        :param start_height: The start height indicates the beginning block height for the set of data that are returned. Mutually exclusive with start_time
        :type start_height: int
        :param end_height: The end height indicates the beginning block height for the set of data that are returned. Mutually exclusive with end_time
        :type end_height: int
        :param chain: Default: "main" Chain type. Supported values are main and all (includes both main and stale).
        :type chain: str
        :param start_inclusive: Flag to define if start timestamp must be included in the timeseries if present. True by default.
        :type start_inclusive: bool
        :param end_inclusive: Flag to define if end timestamp must be included in the timeseries if present. True by default.
        :type end_inclusive: bool
        :param timezone: timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.
        :type timezone: str
        :return: list of blockchain blocks metadata
        :rtype: DataCollection
        """
        params: Dict[str, Any] = {
            "asset": asset,
            "block_hashes": block_hashes,
            "heights": heights,
            "page_size": page_size,
            "paging_from": paging_from,
            "start_time": start_time,
            "end_time": end_time,
            "start_height": start_height,
            "end_height": end_height,
            "chain": chain,
            "start_inclusive": start_inclusive,
            "end_inclusive": end_inclusive,
            "timezone": timezone,
        }
        return DataCollection(self._get_data, f"blockchain-v2/{asset}/blocks", params)

    def get_list_of_accounts_v2(
        self,
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
        timezone: Optional[str] = None,
    ) -> DataCollection:
        """
        Returns a list of blockchain accounts with their balances.

        :param asset: Asset name
        :type asset: str
        :param accounts: Optional comma separated list of accounts to filter a response.
        :type accounts: str, list(str)
        :param page_size: number of items returned per page when calling the API. If the request times out, try using a smaller number.
        :type page_size: int
        :param paging_from: Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
        :type paging_from: PagingFrom, str
        :param start_time: Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type end_time: datetime, date, str
        :param start_height: The start height indicates the beginning block height for the set of data that are returned. Mutually exclusive with start_time
        :type start_height: int
        :param end_height: The end height indicates the beginning block height for the set of data that are returned. Mutually exclusive with end_time
        :type end_height: int
        :param start_chain_sequence_number: The start height indicates the beginning block height for the set of data that are returned. Mutually exclusive with start_time
        :type start_chain_sequence_number: int
        :param end_chain_sequence_number: The end height indicates the beginning block height for the set of data that are returned. Mutually exclusive with end_time
        :type end_chain_sequence_number: int
        :param start_inclusive: Flag to define if start timestamp must be included in the timeseries if present. True by default.
        :type start_inclusive: bool
        :param end_inclusive: Flag to define if end timestamp must be included in the timeseries if present. True by default.
        :type end_inclusive: bool
        :param timezone: timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.
        :type timezone: str
        :return: list of blockchain accounts metadata
        :rtype: DataCollection
        """
        params: Dict[str, Any] = {
            "asset": asset,
            "accounts": accounts,
            "page_size": page_size,
            "paging_from": paging_from,
            "start_time": start_time,
            "end_time": end_time,
            "start_height": start_height,
            "end_height": end_height,
            "start_chain_sequence_number": start_chain_sequence_number,
            "end_chain_sequence_number": end_chain_sequence_number,
            "start_inclusive": start_inclusive,
            "end_inclusive": end_inclusive,
            "timezone": timezone,
        }
        return DataCollection(self._get_data, f"blockchain-v2/{asset}/accounts", params)

    def get_list_of_sub_accounts_v2(
        self,
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
        timezone: Optional[str] = None,
    ) -> DataCollection:
        """
        Returns a list of blockchain sub-accounts with their balances.

        :param asset: Asset name
        :type asset: str
        :param accounts: Optional comma separated list of accounts to filter a response.
        :type accounts: str, list(str)
        :param page_size: number of items returned per page when calling the API. If the request times out, try using a smaller number.
        :type page_size: int
        :param paging_from: Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
        :type paging_from: PagingFrom, str
        :param start_time: Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type end_time: datetime, date, str
        :param start_height: The start height indicates the beginning block height for the set of data that are returned. Mutually exclusive with start_time
        :type start_height: int
        :param end_height: The end height indicates the beginning block height for the set of data that are returned. Mutually exclusive with end_time
        :type end_height: int
        :param start_chain_sequence_number: The start height indicates the beginning block height for the set of data that are returned. Mutually exclusive with start_time
        :type start_chain_sequence_number: int
        :param end_chain_sequence_number: The end height indicates the beginning block height for the set of data that are returned. Mutually exclusive with end_time
        :type end_chain_sequence_number: int
        :param start_inclusive: Flag to define if start timestamp must be included in the timeseries if present. True by default.
        :type start_inclusive: bool
        :param end_inclusive: Flag to define if end timestamp must be included in the timeseries if present. True by default.
        :type end_inclusive: bool
        :param timezone: timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.
        :type timezone: str
        :return: list of blockchain accounts metadata
        :rtype: DataCollection
        """
        params: Dict[str, Any] = {
            "asset": asset,
            "accounts": accounts,
            "page_size": page_size,
            "paging_from": paging_from,
            "start_time": start_time,
            "end_time": end_time,
            "start_height": start_height,
            "end_height": end_height,
            "start_chain_sequence_number": start_chain_sequence_number,
            "end_chain_sequence_number": end_chain_sequence_number,
            "start_inclusive": start_inclusive,
            "end_inclusive": end_inclusive,
            "timezone": timezone,
        }
        return DataCollection(
            self._get_data, f"blockchain-v2/{asset}/sub-accounts", params
        )

    def get_list_of_transactions_v2(
        self,
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
        timezone: Optional[str] = None,
    ) -> DataCollection:
        """
        Returns a list of blockchain transactions metadata.

        :param asset: Asset name
        :type asset: str
        :param txids: Optional comma separated list of transaction identifiers (txid) to filter a response.
        :type txids: str, list(str)
        :param block_hashes: Optional comma separated list of block hashes to filter a response.
        :type block_hashes: str, list(str)
        :param page_size: number of items returned per page when calling the API. If the request times out, try using a smaller number.
        :type page_size: int
        :param paging_from: Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
        :type paging_from: PagingFrom, str
        :param start_time: Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type end_time: datetime, date, str
        :param start_height: The start height indicates the beginning block height for the set of data that are returned. Mutually exclusive with start_time
        :type start_height: int
        :param end_height: The end height indicates the beginning block height for the set of data that are returned. Mutually exclusive with end_time
        :type end_height: int
        :param chain: Default: "main". Chain type. Supported values are main and all (includes both main and stale).
        :type chain: str
        :param start_inclusive: Flag to define if start timestamp must be included in the timeseries if present. True by default.
        :type start_inclusive: bool
        :param end_inclusive: Flag to define if end timestamp must be included in the timeseries if present. True by default.
        :type end_inclusive: bool
        :param timezone: timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.
        :type timezone: str
        :return: list of transaction metadata
        :rtype: DataCollection
        """
        params: Dict[str, Any] = {
            "asset": asset,
            "txids": txids,
            "block_hashes": block_hashes,
            "page_size": page_size,
            "paging_from": paging_from,
            "start_time": start_time,
            "end_time": end_time,
            "start_height": start_height,
            "end_height": end_height,
            "chain": chain,
            "start_inclusive": start_inclusive,
            "end_inclusive": end_inclusive,
            "timezone": timezone,
        }
        return DataCollection(
            self._get_data, f"blockchain-v2/{asset}/transactions", params
        )

    def get_list_of_balance_updates_v2(
        self,
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
        timezone: Optional[str] = None,
    ) -> DataCollection:
        """
        Returns a list of blockchain accounts balance updates.

        :param asset: Asset name
        :type asset: str
        :param accounts: Optional comma separated list of accounts to filter a response.
        :type accounts: str, list(str)
        :param limit_per_account: How many entries per account the result should contain. It is applicable when multiple accounts are requested.
        :type limit_per_account: int
        :param txids: Optional comma separated list of transaction ids to filter a response.
        :type txids: str, list(str)
        :param block_hashes: Optional comma separated list of block hashes to filter a response.
        :type block_hashes: str, list(str)
        :param page_size: number of items returned per page when calling the API. If the request times out, try using a smaller number.
        :type page_size: int
        :param paging_from: Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
        :type paging_from: PagingFrom, str
        :param start_time: Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type end_time: datetime, date, str
        :param start_height: The start height indicates the beginning block height for the set of data that are returned. Mutually exclusive with start_time
        :type start_height: int
        :param end_height: The end height indicates the beginning block height for the set of data that are returned. Mutually exclusive with end_time
        :type end_height: int
        :param start_chain_sequence_number: The start height indicates the beginning block height for the set of data that are returned. Mutually exclusive with start_time
        :type start_chain_sequence_number: int
        :param end_chain_sequence_number: The end height indicates the beginning block height for the set of data that are returned. Mutually exclusive with end_time
        :type end_chain_sequence_number: int
        :param include_sub_accounts: bool indicating if the response should contain sub-accounts.
        :type include_sub_accounts: bool
        :param chain: Chain type. Supported values are main and all (includes both main and stale).
        :type: str
        :param start_inclusive: Flag to define if start timestamp must be included in the timeseries if present. True by default.
        :type start_inclusive: bool
        :param end_inclusive: Flag to define if end timestamp must be included in the timeseries if present. True by default.
        :type end_inclusive: bool
        :param timezone: timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.
        :type timezone: str
        :return: list of balance updates
        :rtype: DataCollection
        """
        params: Dict[str, Any] = {
            "asset": asset,
            "accounts": accounts,
            "limit_per_account": limit_per_account,
            "sub_accounts": sub_accounts,
            "txids": txids,
            "block_hashes": block_hashes,
            "page_size": page_size,
            "paging_from": paging_from,
            "start_time": start_time,
            "end_time": end_time,
            "start_height": start_height,
            "end_height": end_height,
            "start_chain_sequence_number": start_chain_sequence_number,
            "end_chain_sequence_number": end_chain_sequence_number,
            "include_sub_accounts": include_sub_accounts,
            "chain": chain,
            "start_inclusive": start_inclusive,
            "end_inclusive": end_inclusive,
            "timezone": timezone,
        }
        return DataCollection(
            self._get_data, f"blockchain-v2/{asset}/balance-updates", params
        )

    def get_full_block(self, asset: str, block_hash: str) -> List[Dict[str, Any]]:
        """
        Returns a full blockchain block with all transactions and balance updates.

        :param asset: Asset name
        :type asset: str
        :param block_hash: block hash
        :type block_hash: str
        :return: blockchain block data
        :rtype: list(dict(str), any)
        """
        params: Dict[str, Any] = {"asset": asset, "block_hash": block_hash}

        return cast(
            List[Dict[str, Any]],
            self._get_data(f"blockchain/{asset}/blocks/{block_hash}", params),
        )

    def get_full_transaction(
        self, asset: str, transaction_hash: str
    ) -> List[Dict[str, Any]]:
        """
        Returns a full blockchain transaction with all balance updates.

        :param asset: Asset name
        :type asset: str
        :param transaction_hash: transaction hash
        :type transaction_hash: str
        :return: block transaction data
        :rtype: list(dict(str), any)
        """
        params: Dict[str, Any] = {"asset": asset, "transaction_hash": transaction_hash}
        return cast(
            List[Dict[str, Any]],
            self._get_data(
                f"blockchain/{asset}/transactions/{transaction_hash}", params
            ),
        )

    def get_full_transaction_for_block(
        self, asset: str, block_hash: str, transaction_hash: str
    ) -> List[Dict[str, Any]]:
        """
        Returns a full blockchain transaction with all balance updates for a specific block.

        :param asset: Asset name
        :type asset: str
        :param block_hash: block hash
        :type block_hash: str
        :param transaction_hash: transaction hash
        :type transaction_hash: str
        :return: block transaction data with balance updates
        :rtype: list(dict(str, Any))
        """
        params: Dict[str, Any] = {
            "asset": asset,
            "block_hash": block_hash,
            "transaction_hash": transaction_hash,
        }
        return cast(
            List[Dict[str, Any]],
            self._get_data(
                f"blockchain/{asset}/blocks/{block_hash}/transactions/{transaction_hash}",
                params,
            ),
        )

    def get_full_block_v2(
        self, asset: str, block_hash: str, include_sub_accounts: Optional[bool]
    ) -> List[Dict[str, Any]]:
        """
        Returns a full blockchain block with all transactions and balance updates.

        :param asset: Asset name
        :type asset: str
        :param block_hash: block hash
        :type block_hash: str
        :param include_sub_accounts: Boolean indicating if the response should contain sub-accounts
        :type include_sub_accounts: bool
        :return: blockchain block data
        :rtype: list(dict(str), any)
        """
        params: Dict[str, Any] = {
            "asset": asset,
            "block_hash": block_hash,
            "include_sub_accounts": include_sub_accounts,
        }

        return cast(
            List[Dict[str, Any]],
            self._get_data(f"blockchain-v2/{asset}/blocks/{block_hash}", params),
        )

    def get_full_transaction_v2(
        self, asset: str, txid: str, include_sub_accounts: Optional[bool]
    ) -> List[Dict[str, Any]]:
        """
        Returns a full blockchain transaction with all balance updates.

        :param asset: Asset name
        :type asset: str
        :param txid: transaction identifier
        :type txid: str
        :param include_sub_accounts: Boolean indicating if the response should contain sub-accounts
        :type include_sub_accounts: bool
        :return: block transaction data
        :rtype: list(dict(str), any)
        """
        params: Dict[str, Any] = {
            "asset": asset,
            "txid": txid,
            "include_sub_accounts": include_sub_accounts,
        }
        return cast(
            List[Dict[str, Any]],
            self._get_data(f"blockchain-v2/{asset}/transactions/{txid}", params),
        )

    def get_full_transaction_for_block_v2(
        self,
        asset: str,
        block_hash: str,
        txid: str,
        include_sub_accounts: Optional[bool],
    ) -> List[Dict[str, Any]]:
        """
        Returns a full blockchain transaction with all balance updates for a specific block.

        :param asset: Asset name
        :type asset: str
        :param block_hash: block hash
        :type block_hash: str
        :param txid: transaction identifier
        :type txid: str
        :param include_sub_accounts: Boolean indicating if the response should contain sub-accounts
        :type include_sub_accounts: bool
        :return: block transaction data with balance updates
        :rtype: list(dict(str, Any))
        """
        params: Dict[str, Any] = {
            "asset": asset,
            "block_hash": block_hash,
            "txid": txid,
            "include_sub_accounts": include_sub_accounts,
        }
        return cast(
            List[Dict[str, Any]],
            self._get_data(
                f"blockchain-v2/{asset}/blocks/{block_hash}/transactions/{txid}",
                params,
            ),
        )

    def get_transaction_tracker(
        self,
        asset: str,
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
    ) -> DataCollection:
        """
        Returns status updates for the specified or all transactions.

        :param asset: Asset name
        :type asset: str
        :param txids: Optional comma separated list of transaction identifiers (txid) to track.
        :type txids: str, list(str)
        :param replacements_for_txids: Optional comma separated list of transaction identifiers (txid) to get the corresponding replacement transactions for. Mutually exclusive with txids.
        :type replacements_for_txids: str, list(str)
        :param replacements_only: Boolean indicating if the response should contain only the replacement transactions.
        :type replacements_only: bool
        :param page_size: number of items returned per page when calling the API. If the request times out, try using a smaller number.
        :type page_size: int
        :param paging_from: Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
        :type paging_from: PagingFrom, str
        :param start_time: Start time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789Z, 2006-01-20, 20060120
        :type end_time: datetime, date, str
        :param start_inclusive: Flag to define if start timestamp must be included in the timeseries if present. True by default.
        :type start_inclusive: bool
        :param end_inclusive: Flag to define if end timestamp must be included in the timeseries if present. True by default.
        :type end_inclusive: bool
        :param timezone: timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.
        :type timezone: str
        :return: status updates for the specified or all transactions.
        :rtype: DataCollection
        """
        params: Dict[str, Any] = {
            "asset": asset,
            "txids": txids,
            "replacements_for_txids": replacements_for_txids,
            "replacements_only": replacements_only,
            "page_size": page_size,
            "paging_from": paging_from,
            "start_time": start_time,
            "end_time": end_time,
            "start_inclusive": start_inclusive,
            "end_inclusive": end_inclusive,
            "timezone": timezone,
        }
        return DataCollection(
            self._get_data, f"blockchain/{asset}/transaction-tracker", params
        )

    def get_taxonomy_assets(
        self,
        assets: Optional[List[str]] = None,
        class_ids: Optional[List[str]] = None,
        sector_ids: Optional[List[str]] = None,
        subsector_ids: Optional[List[str]] = None,
        classification_start_time: Optional[str] = None,
        classification_end_time: Optional[str] = None,
        end_inclusive: Optional[bool] = None,
        start_inclusive: Optional[bool] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[str] = None,
        version: Optional[str] = None,
    ) -> DataCollection:
        """
        Returns assets with information about their sector, industry, and industry group IDs. By default reutrns all
        covered assets

        :param assets: Asset names
        :type assets: Optional[List[str]]
        :param class_ids: List of class identifiers.
        :type class_ids: Optional[List[str]]
        :param sector_ids: Lst of sector identifiers.
        :type sector_ids: Optional[List[str]]
        :param subsector_ids: List of subsector identifiers
        :type subsector_ids: Optional[List[str]]
        :param classification_start_time: Start time for the taxonomy assets. ISO-8601 format date. Inclusive by default
        :type classification_start_time: Optional[str]
        :param classification_end_time: End time for the taxonomy assets. ISO-8601 format date. Inclusive by default
        :type classification_end_time: Optional[str]
        :param start_inclusive: Flag to define if start timestamp must be included in the timeseries if present. True by default.
        :type start_inclusive: bool
        :param end_inclusive: Flag to define if end timestamp must be included in the timeseries if present. True by default.
        :type end_inclusive: bool
        :param page_size: Page size for # of assets to return, will default to 100
        :type page_size: Optional[int]
        :param paging_from: Which direction to page from "start" or "end". "end" by default
        :type paging_from: Optional[str]
        :param version: Version to query, default is "latest".
        :type version: Optional[str]
        :return: Returns a data collection containing the taxonomy assets
        :rtype: Datacollection
        """
        params: Dict[str, Any] = {
            "assets": assets,
            "class_ids": class_ids,
            "sector_ids": sector_ids,
            "subsector_ids": subsector_ids,
            "classification_start_time": classification_start_time,
            "classification_end_time": classification_end_time,
            "end_inclusive": end_inclusive,
            "start_inclusive": start_inclusive,
            "page_size": page_size,
            "paging_from": paging_from,
            "version": version,
        }
        return DataCollection(self._get_data, "/taxonomy/assets", params)

    def get_taxonomy_assets_metadata(
        self,
        start_time: Optional[Union[datetime, date, str]] = None,
        end_time: Optional[Union[datetime, date, str]] = None,
        start_inclusive: Optional[bool] = None,
        end_inclusive: Optional[bool] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[str] = None,
        version: Optional[str] = None,
    ) -> DataCollection:
        """
        Returns metadata about the assets, sectors, and industries included in the CM taxonomy
        :param start_time: Start time for the taxonomy version file. ISO-8601 format date. Inclusive by default
        :type start_time: Optional[Union[datetime, date, str]]
        :param end_time: End time for the taxonomy version file. ISO-8601 format date. Exclusive by default
        :type end_time: Optional[Union[datetime, date, str]]
        :param start_inclusive: Start time of taxonomy version.
        :type start_inclusive: str
        :param end_inclusive: End time of taxonomy version.
        :type end_inclusive: str
        :param page_size: Page size for # of asset metadata to return, will default to 100
        :type page_size: Optional[int]
        :param paging_from: Which direction to page from "start" or "end". "end" by default
        :type paging_from: Optional[str]
        :param version: Version to query, default is "latest".
        :type version: Optional[str]
        :return: Returns a data collection containing the taxonomy assets
        :rtype: Datacollection
        """
        params: Dict[str, Any] = {
            "start_time": start_time,
            "end_time": end_time,
            "start_inclusive": start_inclusive,
            "end_inclusive": end_inclusive,
            "page_size": page_size,
            "paging_from": paging_from,
            "version": version,
        }
        return DataCollection(self._get_data, "/taxonomy-metadata/assets", params)

    def get_asset_profiles(
        self,
        assets: Optional[Union[List[str], str]] = None,
        full_names: Optional[Union[List[str], str]] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[str] = None,
    ) -> DataCollection:
        """
        Returns profile data for assets, ordered by asset
        :param assets: Returns profile data for assets.
        :type assets: Optional[Union[List[str], str]]
        :param full_names: Comma separated list of asset full names. By default profile data for all assets is returned. Mutually exclusive with assets parameter.
        :type full_names: Optional[Union[List[str], str]]
        :param page_size: Number of items per single page of results.
        :type page_size: int
        :param paging_from: Where does the first page start, at the "start" of the interval or at the "end"
        :type paging_from: int
        """
        params: Dict[str, Any] = {
            "assets": assets,
            "full_names": full_names,
            "page_size": page_size,
            "paging_from": paging_from,
        }
        return DataCollection(self._get_data, "/profile/assets", params)

    def _get_data(self, url: str, params: Dict[str, Any]) -> DataReturnType:
        if params:
            params_str = "&{}".format(
                urlencode(transform_url_params_values_to_str(params))
            )
        else:
            params_str = ""
        actual_url = "{}/{}?{}{}".format(
            self._api_base_url, url, self._api_key_url_str, params_str
        )

        if self.verbose:
            logger.info(
                msg=f"Attempting to call url: {url.split('api_key')[0]} with params: {params}"
            )
            start_time = datetime.now()
            resp = self._send_request(actual_url)
            logger.info(
                f"Response status code: {resp.status_code} for url: {resp.url} "
                f"took: {datetime.now() - start_time} response body size (bytes): {len(resp.content)}"
            )
        elif self.debug_mode:
            logger.debug(
                msg=f"Attempting to call url: {url.split('api_key')[0]} with params: {params}"
            )
            start_time = datetime.now()
            resp = self._send_request(actual_url)
            logger.debug(
                f"Response status code: {resp.status_code} for url: {resp.url} "
                f"took: {datetime.now() - start_time} response body size (bytes): {len(resp.content)}"
            )
        else:
            resp = self._send_request(actual_url)
        try:
            data = json.loads(resp.content)
        except ValueError:
            if resp.status_code == 414:
                raise CoinMetricsClientQueryParamsException(response=resp)
            else:
                resp.raise_for_status()
                raise
        else:
            if "error" in data:
                error_msg = (
                    f"Error found for the query: \n {actual_url}\n"
                    f"Error details: {data['error']}"
                )
                logger.error(error_msg)
                resp.raise_for_status()
            return cast(DataReturnType, data)

    def _get_stream_data(self, url: str, params: Dict[str, Any]) -> CmStream:
        if params:
            params_str = "&{}".format(
                urlencode(transform_url_params_values_to_str(params))
            )
        else:
            params_str = ""
        actual_url = "{}/{}?{}{}".format(
            self._ws_api_base_url, url, self._api_key_url_str, params_str
        )
        return CmStream(ws_url=actual_url)

    @retry((socket.gaierror, HTTPError), retries=5, wait_time_between_retries=5)
    def _send_request(self, actual_url: str) -> Response:
        return self._session.get(
            actual_url,
            headers=self._session.headers,
            proxies=self._session.proxies,
            verify=self._session.verify,
        )
