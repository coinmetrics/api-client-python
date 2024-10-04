import logging
import socket
import time
from datetime import date, datetime
from logging import getLogger
from typing import Dict, List, Optional, Union, cast, Callable, Any
from types import FrameType
from urllib.parse import urlencode
import signal
import requests
from requests import HTTPError, Response
import websocket

from coinmetrics._utils import retry, transform_url_params_values_to_str
from coinmetrics import __version__ as version
from coinmetrics._exceptions import CoinMetricsClientQueryParamsException
from coinmetrics._typing import (
    DataReturnType,
    MessageHandlerType,
)
from coinmetrics.constants import PagingFrom, Backfill
from coinmetrics._data_collection import DataCollection, AssetChainsDataCollection, TransactionTrackerDataCollection, CatalogV2DataCollection
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
    CatalogAssetChainsData,
    CatalogMempoolFeeratesData,
    CatalogMiningPoolTipsData,
    CatalogTransactionTrackerData,
    CatalogMarketContractPrices,
    CatalogMarketImpliedVolatility,
)

from importlib import import_module
ujson_found = True
try:
    json = import_module('ujson')
except ModuleNotFoundError:
    ujson_found = False

if not ujson_found:
    import json
else:
    import ujson as json
logger = getLogger("cm_client")


class CmStream:
    def __init__(self, ws_url: str):
        self.ws_url = ws_url
        self._stop_event_received = False
        self._events_handlers_set = False

    def run(
            self,
            on_message: MessageHandlerType = None,
            on_error: MessageHandlerType = None,
            on_close: Optional[Callable[[websocket.WebSocketApp, int, str], None]] = None,
            reconnect: bool = True
    ) -> None:
        if on_message is None:
            on_message = self._on_message
        if on_error is None:
            on_error = self._on_error
        if on_close is None:
            on_close = self._on_close

        ws = websocket.WebSocketApp(
            self.ws_url, on_message=on_message, on_error=on_error, on_close=on_close
        )
        self.ws = ws

        self._stop_event_received = False
        self._register_signal_handlers([signal.SIGINT])
        self.ws.run_forever(reconnect=reconnect)

    def _register_signal_handlers(self, signal_types: List[int]) -> None:
        if self._events_handlers_set:
            return
        for signal_type in signal_types:
            previous_handler = signal.getsignal(signal_type)
            if callable(previous_handler):
                def handler(signum: int, frame: Optional[FrameType]) -> None:
                    self._stop_event_received = True
                    previous_handler(signum, frame)
                signal.signal(signal_type, handler)

        self._events_handlers_set = True

    def _on_message(self, stream: websocket.WebSocketApp, message: str) -> None:
        print(f"{message}")

    def _on_error(self, stream: websocket.WebSocketApp, message: str) -> None:
        print(f"{message}")

    def _on_close(self, *args: Any, **kwargs: Any) -> None:
        return


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
        exclude: Optional[Union[List[str], str]] = None,
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
        params: Dict[str, Any] = {
            "assets": assets,
            "include": include,
            "exclude": exclude,
        }
        logger.warning("/catalog/ endpoints will be deprecated in the future. Consider using /catalog-v2/ and /reference-data/ endpoints instead.")
        return CatalogAssetsData(self._get_data("catalog/assets", params)["data"])

    def catalog_asset_alerts(
        self,
        assets: Optional[Union[str, List[str]]] = None,
        alerts: Optional[Union[str, List[str]]] = None,
    ) -> CatalogAssetAlertsData:
        """
        :param assets: Comma separated list of assets. By default all assets are returned.
        :type assets: Union[str, List[str]]
        :param alerts: Comma separated list of asset alert names. By default all asset alerts are returned.
        :type alerts: Union[str, List[str]]
        :return: List of asset alerts.
        :rtype: CatalogAssetAlertsData
        """
        params: Dict[str, Any] = {
            "assets": assets,
            "alerts": alerts,
        }
        logger.warning("/catalog/ endpoints will be deprecated in the future. Consider using /catalog-v2/ and /reference-data/ endpoints instead.")
        return CatalogAssetAlertsData(
            self._get_data("catalog/asset-alerts", params)["data"]
        )

    def catalog_asset_chains(
            self,
            assets: Optional[Union[str, List[str]]] = None,
    ) -> CatalogAssetChainsData:
        """
        :param assets: Comma separated list of assets. By default all assets are returned.
        :type assets: Optional[Union[str, List[str]]]

        :return: List of asset chains assets
        :rtype: CatalogAssetChainsData
        """
        params: Dict[str, Any] = {
            "assets": assets,
        }
        logger.warning("/catalog/ endpoints will be deprecated in the future. Consider using /catalog-v2/ and /reference-data/ endpoints instead.")
        return CatalogAssetChainsData(self._get_data("catalog/asset-chains", params)['data'])

    def catalog_mempool_feerates(
            self,
            assets: Optional[Union[str, List[str]]] = None,
    ) -> CatalogMempoolFeeratesData:
        """
        :param assets: Comma separated list of assets. By default all assets are returned.
        :type assets: Optional[Union[str, List[str]]]

        :return: List of mempool feerates assets
        :rtype: CatalogMempoolFeeratesData
        """
        params: Dict[str, Any] = {
            "assets": assets,
        }
        logger.warning("/catalog/ endpoints will be deprecated in the future. Consider using /catalog-v2/ and /reference-data/ endpoints instead.")
        return CatalogMempoolFeeratesData(self._get_data("catalog/mempool-feerates", params)['data'])

    def catalog_mining_pool_tips_summaries(
            self,
            assets: Optional[Union[str, List[str]]] = None,
    ) -> CatalogMiningPoolTipsData:
        """
        :param assets: Comma separated list of assets. By default all assets are returned.
        :type assets: Optional[Union[str, List[str]]]

        :return: List of mining pool tips assets
        :rtype: CatalogMiningPoolTipsData
        """
        params: Dict[str, Any] = {
            "assets": assets,
        }
        logger.warning("/catalog/ endpoints will be deprecated in the future. Consider using /catalog-v2/ and /reference-data/ endpoints instead.")

        return CatalogMiningPoolTipsData(self._get_data("catalog/mining-pool-tips-summary", params)['data'])

    def catalog_transaction_tracker_assets(
            self,
            assets: Optional[Union[str, List[str]]] = None,
    ) -> CatalogTransactionTrackerData:
        """
        :param assets: Comma separated list of assets. By default all assets are returned.
        :type assets: Optional[Union[str, List[str]]]

        :return: List of transaction tracker assets
        :rtype: CatalogTransactionTrackerData
        """
        params: Dict[str, Any] = {
            "assets": assets,
        }
        logger.warning("/catalog/ endpoints will be deprecated in the future. Consider using /catalog-v2/ and /reference-data/ endpoints instead.")

        return CatalogTransactionTrackerData(self._get_data("catalog/transaction-tracker", params)['data'])

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
        logger.warning("/catalog/ endpoints will be deprecated in the future. Consider using /catalog-v2/ and /reference-data/ endpoints instead.")
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
        logger.warning("/catalog/ endpoints will be deprecated in the future. Consider using /catalog-v2/ and /reference-data/ endpoints instead.")
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
        logger.warning("/catalog/ endpoints will be deprecated in the future. Consider using /catalog-v2/ and /reference-data/ endpoints instead.")
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
        logger.warning("/catalog/ endpoints will be deprecated in the future. Consider using /catalog-v2/ and /reference-data/ endpoints instead.")
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
        logger.warning("/catalog/ endpoints will be deprecated in the future. Consider using /catalog-v2/ and /reference-data/ endpoints instead.")
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
        logger.warning("/catalog/ endpoints will be deprecated in the future. Consider using /catalog-v2/ and /reference-data/ endpoints instead.")
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
        logger.warning("/catalog/ endpoints will be deprecated in the future. Consider using /catalog-v2/ and /reference-data/ endpoints instead.")
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
        logger.warning("/catalog/ endpoints will be deprecated in the future. Consider using /catalog-v2/ and /reference-data/ endpoints instead.")
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
        logger.warning("/catalog/ endpoints will be deprecated in the future. Consider using /catalog-v2/ and /reference-data/ endpoints instead.")
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
        logger.warning("/catalog/ endpoints will be deprecated in the future. Consider using /catalog-v2/ and /reference-data/ endpoints instead.")
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
        logger.warning("/catalog/ endpoints will be deprecated in the future. Consider using /catalog-v2/ and /reference-data/ endpoints instead.")
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
        logger.warning("/catalog/ endpoints will be deprecated in the future. Consider using /catalog-v2/ and /reference-data/ endpoints instead.")
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
        exclude: Optional[Union[List[str], str]] = None,
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
            "exclude": exclude,
        }
        logger.warning("/catalog/ endpoints will be deprecated in the future. Consider using /catalog-v2/ and /reference-data/ endpoints instead.")
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
        logger.warning("/catalog/ endpoints will be deprecated in the future. Consider using /catalog-v2/ and /reference-data/ endpoints instead.")
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
        logger.warning("/catalog/ endpoints will be deprecated in the future. Consider using /catalog-v2/ and /reference-data/ endpoints instead.")
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
        logger.warning("/catalog/ endpoints will be deprecated in the future. Consider using /catalog-v2/ and /reference-data/ endpoints instead.")
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
        logger.warning("/catalog/ endpoints will be deprecated in the future. Consider using /catalog-v2/ and /reference-data/ endpoints instead.")
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
        logger.warning("/catalog/ endpoints will be deprecated in the future. Consider using /catalog-v2/ and /reference-data/ endpoints instead.")
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
        logger.warning("/catalog/ endpoints will be deprecated in the future. Consider using /catalog-v2/ and /reference-data/ endpoints instead.")
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
        logger.warning("/catalog/ endpoints will be deprecated in the future. Consider using /catalog-v2/ and /reference-data/ endpoints instead.")
        return CatalogMarketTradesData(
            self._get_data("catalog/market-funding-rates", params)["data"]
        )

    def catalog_market_contract_prices(
            self,
            markets: Optional[Union[str, List[str]]] = None,
            exchange: Optional[str] = None,
            type: Optional[str] = None,
            base: Optional[str] = None,
            quote: Optional[str] = None,
            asset: Optional[str] = None,
            symbol: Optional[str] = None,
            format: Optional[str] = None,
            limit: Optional[str] = None,
    ) -> CatalogMarketContractPrices:
        """
        :param markets: Comma separated list of markets. By default all markets are returned.
        :type markets: Optional[Union[str, List[str]]]
        :param exchange: Unique name of an exchange.
        :type exchange: Optional[str]
        :param type: Type of markets.
        :type type: Optional[str]
        :param base: Base asset of markets.
        :type base: Optional[str]
        :param quote: Quote asset of markets.
        :type quote: Optional[str]
        :param asset: Any asset of markets.
        :type asset: Optional[str]
        :param symbol: Symbol of derivative markets, full instrument name.
        :type symbol: Optional[str]
        :param format: Format of the response. Supported values are `json`, `json_stream`.
        :type format: Optional[str]
        :param limit: Limit of response items. `none` means no limit.
        :type limit: Optional[str]

        :return: List of contract prices statistics.
        :rtype: CatalogMarketContractPrices
        """
        params: Dict[str, Any] = {
            "markets": markets,
            "exchange": exchange,
            "type": type,
            "base": base,
            "quote": quote,
            "asset": asset,
            "symbol": symbol,
            "format": format,
            "limit": limit,
        }
        logger.warning("/catalog/ endpoints will be deprecated in the future. Consider using /catalog-v2/ and /reference-data/ endpoints instead.")
        return CatalogMarketContractPrices(self._get_data("catalog/market-contract-prices", params)['data'])

    def catalog_market_implied_volatility(
            self,
            markets: Optional[Union[str, List[str]]] = None,
            exchange: Optional[str] = None,
            type: Optional[str] = None,
            base: Optional[str] = None,
            quote: Optional[str] = None,
            asset: Optional[str] = None,
            symbol: Optional[str] = None,
            format: Optional[str] = None,
            limit: Optional[str] = None,
    ) -> CatalogMarketImpliedVolatility:
        """
        :param markets: Comma separated list of markets. By default all markets are returned.
        :type markets: Optional[Union[str, List[str]]]
        :param exchange: Unique name of an exchange.
        :type exchange: Optional[str]
        :param type: Type of markets.
        :type type: Optional[str]
        :param base: Base asset of markets.
        :type base: Optional[str]
        :param quote: Quote asset of markets.
        :type quote: Optional[str]
        :param asset: Any asset of markets.
        :type asset: Optional[str]
        :param symbol: Symbol of derivative markets, full instrument name.
        :type symbol: Optional[str]
        :param format: Format of the response. Supported values are `json`, `json_stream`.
        :type format: Optional[str]
        :param limit: Limit of response items. `none` means no limit.
        :type limit: Optional[str]

        :return: List of implied volatility statistics.
        :rtype: CatalogMarketImpliedVolatility
        """
        params: Dict[str, Any] = {
            "markets": markets,
            "exchange": exchange,
            "type": type,
            "base": base,
            "quote": quote,
            "asset": asset,
            "symbol": symbol,
            "format": format,
            "limit": limit,
        }
        logger.warning("/catalog/ endpoints will be deprecated in the future. Consider using /catalog-v2/ and /reference-data/ endpoints instead.")
        return CatalogMarketImpliedVolatility(self._get_data("catalog/market-implied-volatility", params)['data'])

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
        logger.warning("/catalog/ endpoints will be deprecated in the future. Consider using /catalog-v2/ and /reference-data/ endpoints instead.")
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
        logger.warning("/catalog/ endpoints will be deprecated in the future. Consider using /catalog-v2/ and /reference-data/ endpoints instead.")
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
        logger.warning("/catalog/ endpoints will be deprecated in the future. Consider using /catalog-v2/ and /reference-data/ endpoints instead.")
        return CatalogMarketTradesData(
            self._get_data("catalog/market-liquidations", params)["data"]
        )

    def catalog_full_assets(
        self,
        assets: Optional[Union[List[str], str]] = None,
        include: Optional[Union[List[str], str]] = None,
        exclude: Optional[Union[List[str], str]] = None,
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
            "exclude": exclude,
        }
        logger.warning("/catalog/ endpoints will be deprecated in the future. Consider using /catalog-v2/ and /reference-data/ endpoints instead.")
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
        logger.warning("/catalog/ endpoints will be deprecated in the future. Consider using /catalog-v2/ and /reference-data/ endpoints instead.")
        return CatalogMetricsData(
            self._get_data("catalog-all/asset-metrics", params)["data"]
        )

    def catalog_full_asset_alerts(
        self,
        assets: Optional[Union[str, List[str]]] = None,
        alerts: Optional[Union[str, List[str]]] = None,
    ) -> CatalogAssetAlertsData:
        """
        :param assets: Comma separated list of assets. By default all assets are returned.
        :type assets: Union[str, List[str]]
        :param alerts: Comma separated list of asset alert names. By default all asset alerts are returned.
        :type alerts: Union[str, List[str]]
        :return: List of asset alerts.
        :rtype: CatalogAssetAlertsData
        """
        params: Dict[str, Any] = {
            "assets": assets,
            "alerts": alerts,
        }
        logger.warning("/catalog/ endpoints will be deprecated in the future. Consider using /catalog-v2/ and /reference-data/ endpoints instead.")
        return CatalogAssetAlertsData(
            self._get_data("catalog-all/asset-alerts", params)["data"]
        )

    def catalog_full_asset_chains(
            self,
            assets: Optional[Union[str, List[str]]] = None,
    ) -> CatalogAssetChainsData:
        """
        :param assets: Comma separated list of assets. By default all assets are returned.
        :type assets: Optional[Union[str, List[str]]]

        :return: List of asset chains assets
        :rtype: CatalogAssetChainsData
        """
        params: Dict[str, Any] = {
            "assets": assets,
        }
        logger.warning("/catalog/ endpoints will be deprecated in the future. Consider using /catalog-v2/ and /reference-data/ endpoints instead.")
        return CatalogAssetChainsData(self._get_data("catalog-all/asset-chains", params)['data'])

    def catalog_full_mempool_feerates(
            self,
            assets: Optional[Union[str, List[str]]] = None,
    ) -> CatalogMempoolFeeratesData:
        """
        :param assets: Comma separated list of assets. By default all assets are returned.
        :type assets: Optional[Union[str, List[str]]]

        :return: List of mempool feerates assets
        :rtype: CatalogMempoolFeeratesData
        """
        params: Dict[str, Any] = {
            "assets": assets,
        }
        logger.warning("/catalog/ endpoints will be deprecated in the future. Consider using /catalog-v2/ and /reference-data/ endpoints instead.")
        return CatalogMempoolFeeratesData(self._get_data("catalog-all/mempool-feerates", params)['data'])

    def catalog_full_mining_pool_tips_summaries(
            self,
            assets: Optional[Union[str, List[str]]] = None,
    ) -> CatalogMiningPoolTipsData:
        """
        :param assets: Comma separated list of assets. By default all assets are returned.
        :type assets: Optional[Union[str, List[str]]]

        :return: List of mining pool tips assets
        :rtype: CatalogMiningPoolTipsData
        """
        params: Dict[str, Any] = {
            "assets": assets,
        }
        logger.warning("/catalog/ endpoints will be deprecated in the future. Consider using /catalog-v2/ and /reference-data/ endpoints instead.")
        return CatalogMiningPoolTipsData(self._get_data("catalog-all/mining-pool-tips-summary", params)['data'])

    def catalog_full_transaction_tracker_assets(
            self,
            assets: Optional[Union[str, List[str]]] = None,
    ) -> CatalogTransactionTrackerData:
        """
        :param assets: Comma separated list of assets. By default all assets are returned.
        :type assets: Optional[Union[str, List[str]]]

        :return: List of transaction tracker assets
        :rtype: CatalogTransactionTrackerData
        """
        params: Dict[str, Any] = {
            "assets": assets,
        }
        logger.warning("/catalog/ endpoints will be deprecated in the future. Consider using /catalog-v2/ and /reference-data/ endpoints instead.")
        return CatalogTransactionTrackerData(self._get_data("catalog-all/transaction-tracker", params)['data'])

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
        logger.warning(
            "/catalog/ endpoints will be deprecated in the future. Consider using /catalog-v2/ and /reference-data/ endpoints instead."
        )
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
        logger.warning(
            "/catalog/ endpoints will be deprecated in the future. Consider using /catalog-v2/ and /reference-data/ endpoints instead."
        )
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
        logger.warning(
            "/catalog/ endpoints will be deprecated in the future. Consider using /catalog-v2/ and /reference-data/ endpoints instead."
        )
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
        logger.warning(
            "/catalog/ endpoints will be deprecated in the future. Consider using /catalog-v2/ and /reference-data/ endpoints instead."
        )
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
        logger.warning(
            "/catalog/ endpoints will be deprecated in the future. Consider using /catalog-v2/ and /reference-data/ endpoints instead."
        )
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
        logger.warning(
            "/catalog/ endpoints will be deprecated in the future. Consider using /catalog-v2/ and /reference-data/ endpoints instead."
        )
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
        logger.warning(
            "/catalog/ endpoints will be deprecated in the future. Consider using /catalog-v2/ and /reference-data/ endpoints instead."
        )
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
        logger.warning(
            "/catalog/ endpoints will be deprecated in the future. Consider using /catalog-v2/ and /reference-data/ endpoints instead."
        )
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
        logger.warning(
            "/catalog/ endpoints will be deprecated in the future. Consider using /catalog-v2/ and /reference-data/ endpoints instead."
        )
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
        logger.warning(
            "/catalog/ endpoints will be deprecated in the future. Consider using /catalog-v2/ and /reference-data/ endpoints instead."
        )
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
        logger.warning(
            "/catalog/ endpoints will be deprecated in the future. Consider using /catalog-v2/ and /reference-data/ endpoints instead."
        )
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
        exclude: Optional[str] = None,
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
            "exclude": exclude,
        }
        logger.warning(
            "/catalog/ endpoints will be deprecated in the future. Consider using /catalog-v2/ and /reference-data/ endpoints instead."
        )
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
        logger.warning(
            "/catalog/ endpoints will be deprecated in the future. Consider using /catalog-v2/ and /reference-data/ endpoints instead."
        )
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
        logger.warning(
            "/catalog/ endpoints will be deprecated in the future. Consider using /catalog-v2/ and /reference-data/ endpoints instead."
        )
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
        logger.warning(
            "/catalog/ endpoints will be deprecated in the future. Consider using /catalog-v2/ and /reference-data/ endpoints instead."
        )
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
        logger.warning(
            "/catalog/ endpoints will be deprecated in the future. Consider using /catalog-v2/ and /reference-data/ endpoints instead."
        )
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
        logger.warning(
            "/catalog/ endpoints will be deprecated in the future. Consider using /catalog-v2/ and /reference-data/ endpoints instead."
        )
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
        logger.warning(
            "/catalog/ endpoints will be deprecated in the future. Consider using /catalog-v2/ and /reference-data/ endpoints instead."
        )
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
        logger.warning(
            "/catalog/ endpoints will be deprecated in the future. Consider using /catalog-v2/ and /reference-data/ endpoints instead."
        )
        return CatalogMarketTradesData(
            self._get_data("catalog-all/market-funding-rates", params)["data"]
        )

    def catalog_full_market_contract_prices(
            self,
            markets: Optional[Union[str, List[str]]] = None,
            exchange: Optional[str] = None,
            type: Optional[str] = None,
            base: Optional[str] = None,
            quote: Optional[str] = None,
            asset: Optional[str] = None,
            symbol: Optional[str] = None,
            format: Optional[str] = None,
            limit: Optional[str] = None,
    ) -> CatalogMarketContractPrices:
        """
        :param markets: Comma separated list of markets. By default all markets are returned.
        :type markets: Optional[Union[str, List[str]]]
        :param exchange: Unique name of an exchange.
        :type exchange: Optional[str]
        :param type: Type of markets.
        :type type: Optional[str]
        :param base: Base asset of markets.
        :type base: Optional[str]
        :param quote: Quote asset of markets.
        :type quote: Optional[str]
        :param asset: Any asset of markets.
        :type asset: Optional[str]
        :param symbol: Symbol of derivative markets, full instrument name.
        :type symbol: Optional[str]
        :param format: Format of the response. Supported values are `json`, `json_stream`.
        :type format: Optional[str]
        :param limit: Limit of response items. `none` means no limit.
        :type limit: Optional[str]

        :return: List of contract prices statistics.
        :rtype: CatalogMarketContractPrices
        """
        params: Dict[str, Any] = {
            "markets": markets,
            "exchange": exchange,
            "type": type,
            "base": base,
            "quote": quote,
            "asset": asset,
            "symbol": symbol,
            "format": format,
            "limit": limit,
        }
        logger.warning(
            "/catalog/ endpoints will be deprecated in the future. Consider using /catalog-v2/ and /reference-data/ endpoints instead."
        )
        return CatalogMarketContractPrices(self._get_data("catalog-all/market-contract-prices", params)['data'])

    def catalog_full_contract_prices_v2(
            self,
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
            next_page_token: Optional[str] = None,
    ) -> CatalogV2DataCollection:
        """
        :param markets: Comma separated list of markets. By default all markets are returned.
        :type markets: Optional[Union[str, List[str]]]
        :param exchange: Unique name of an exchange.
        :type exchange: Optional[str]
        :param market_type: Type of markets.
        :type market_type: Optional[str]
        :param base: Base asset of markets.
        :type base: Optional[str]
        :param quote: Quote asset of markets.
        :type quote: Optional[str]
        :param asset: Any asset of markets.
        :type asset: Optional[str]
        :param symbol: Symbol of derivative markets, full instrument name.
        :type symbol: Optional[str]
        :param format: Format of the response. Supported values are `json`, `json_stream`.
        :type format: Optional[str]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]
        :param next_page_token: Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
        :type next_page_token: Optional[str]

        :return: List of contract prices statistics.
        :rtype: CatalogV2DataCollection
        """
        params: Dict[str, Any] = {
            "markets": markets,
            "exchange": exchange,
            "type": market_type,
            "base": base,
            "quote": quote,
            "asset": asset,
            "symbol": symbol,
            "format": format,
            "page_size": page_size,
            "paging_from": paging_from,
            "next_page_token": next_page_token,
        }
        return CatalogV2DataCollection(self._get_data, "/catalog-all-v2/market-contract-prices", params)

    def catalog_full_market_implied_volatility(
            self,
            markets: Optional[Union[str, List[str]]] = None,
            exchange: Optional[str] = None,
            type: Optional[str] = None,
            base: Optional[str] = None,
            quote: Optional[str] = None,
            asset: Optional[str] = None,
            symbol: Optional[str] = None,
            format: Optional[str] = None,
            limit: Optional[str] = None,
    ) -> CatalogMarketImpliedVolatility:
        """
        :param markets: Comma separated list of markets. By default all markets are returned.
        :type markets: Optional[Union[str, List[str]]]
        :param exchange: Unique name of an exchange.
        :type exchange: Optional[str]
        :param type: Type of markets.
        :type type: Optional[str]
        :param base: Base asset of markets.
        :type base: Optional[str]
        :param quote: Quote asset of markets.
        :type quote: Optional[str]
        :param asset: Any asset of markets.
        :type asset: Optional[str]
        :param symbol: Symbol of derivative markets, full instrument name.
        :type symbol: Optional[str]
        :param format: Format of the response. Supported values are `json`, `json_stream`.
        :type format: Optional[str]
        :param limit: Limit of response items. `none` means no limit.
        :type limit: Optional[str]

        :return: List of implied volatility statistics.
        :rtype: CatalogMarketImpliedVolatility
        """
        params: Dict[str, Any] = {
            "markets": markets,
            "exchange": exchange,
            "type": type,
            "base": base,
            "quote": quote,
            "asset": asset,
            "symbol": symbol,
            "format": format,
            "limit": limit,
        }
        logger.warning(
            "/catalog/ endpoints will be deprecated in the future. Consider using /catalog-v2/ and /reference-data/ endpoints instead."
        )
        return CatalogMarketImpliedVolatility(self._get_data("catalog-all/market-implied-volatility", params)['data'])

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
        logger.warning(
            "/catalog/ endpoints will be deprecated in the future. Consider using /catalog-v2/ and /reference-data/ endpoints instead."
        )
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
        logger.warning(
            "/catalog/ endpoints will be deprecated in the future. Consider using /catalog-v2/ and /reference-data/ endpoints instead."
        )
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
        logger.warning(
            "/catalog/ endpoints will be deprecated in the future. Consider using /catalog-v2/ and /reference-data/ endpoints instead."
        )
        return CatalogMarketTradesData(
            self._get_data("catalog-all/market-liquidations", params)["data"]
        )

    def catalog_market_trades_v2(
            self,
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
            next_page_token: Optional[str] = None,
    ) -> CatalogV2DataCollection:
        """
        :param markets: Comma separated list of markets. By default all markets are returned.
        :type markets: Optional[Union[str, List[str]]]
        :param exchange: Unique name of an exchange.
        :type exchange: Optional[str]
        :param market_type: Type of markets.
        :type market_type: Optional[str]
        :param base: Base asset of markets.
        :type base: Optional[str]
        :param quote: Quote asset of markets.
        :type quote: Optional[str]
        :param asset: Any asset of markets.
        :type asset: Optional[str]
        :param symbol: Symbol of derivative markets, full instrument name.
        :type symbol: Optional[str]
        :param format: Format of the response. Supported values are `json`, `json_stream`.
        :type format: Optional[str]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]
        :param next_page_token: Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
        :type next_page_token: Optional[str]

        :return: List of market trades statistics.
        :rtype: CatalogV2DataCollection
        """
        params: Dict[str, Any] = {
            "markets": markets,
            "exchange": exchange,
            "type": market_type,
            "base": base,
            "quote": quote,
            "asset": asset,
            "symbol": symbol,
            "format": format,
            "page_size": page_size,
            "paging_from": paging_from,
            "next_page_token": next_page_token,
        }
        return CatalogV2DataCollection(self._get_data, "/catalog-v2/market-trades", params, client=self)

    def catalog_market_candles_v2(
            self,
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
            next_page_token: Optional[str] = None,
    ) -> CatalogV2DataCollection:
        """
        :param markets: Comma separated list of markets. By default all markets are returned.
        :type markets: Optional[Union[str, List[str]]]
        :param exchange: Unique name of an exchange.
        :type exchange: Optional[str]
        :param market_type: Type of markets.
        :type market_type: Optional[str]
        :param base: Base asset of markets.
        :type base: Optional[str]
        :param quote: Quote asset of markets.
        :type quote: Optional[str]
        :param asset: Any asset of markets.
        :type asset: Optional[str]
        :param symbol: Symbol of derivative markets, full instrument name.
        :type symbol: Optional[str]
        :param format: Format of the response. Supported values are `json`, `json_stream`.
        :type format: Optional[str]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]
        :param next_page_token: Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
        :type next_page_token: Optional[str]

        :return: List of market candles statistics.
        :rtype: CatalogV2DataCollection
        """
        params: Dict[str, Any] = {
            "markets": markets,
            "exchange": exchange,
            "type": market_type,
            "base": base,
            "quote": quote,
            "asset": asset,
            "symbol": symbol,
            "format": format,
            "page_size": page_size,
            "paging_from": paging_from,
            "next_page_token": next_page_token,
        }
        return CatalogV2DataCollection(
            self._get_data,
            "/catalog-v2/market-candles",
            params,
            iterable_col="frequencies",
            iterable_key="frequency",
            client=self
        )

    def catalog_market_orderbooks_v2(
            self,
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
            next_page_token: Optional[str] = None,
    ) -> CatalogV2DataCollection:
        """
        :param markets: Comma separated list of markets. By default all markets are returned.
        :type markets: Optional[Union[str, List[str]]]
        :param exchange: Unique name of an exchange.
        :type exchange: Optional[str]
        :param market_type: Type of markets.
        :type market_type: Optional[str]
        :param base: Base asset of markets.
        :type base: Optional[str]
        :param quote: Quote asset of markets.
        :type quote: Optional[str]
        :param asset: Any asset of markets.
        :type asset: Optional[str]
        :param symbol: Symbol of derivative markets, full instrument name.
        :type symbol: Optional[str]
        :param format: Format of the response. Supported values are `json`, `json_stream`.
        :type format: Optional[str]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]
        :param next_page_token: Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
        :type next_page_token: Optional[str]

        :return: List of market orderbooks statistics.
        :rtype: CatalogV2DataCollection
        """
        params: Dict[str, Any] = {
            "markets": markets,
            "exchange": exchange,
            "type": market_type,
            "base": base,
            "quote": quote,
            "asset": asset,
            "symbol": symbol,
            "format": format,
            "page_size": page_size,
            "paging_from": paging_from,
            "next_page_token": next_page_token,
        }
        return CatalogV2DataCollection(
            self._get_data,
            "/catalog-v2/market-orderbooks",
            params,
            iterable_key="depth",
            iterable_col="depths",
            client=self
        )

    def catalog_market_quotes_v2(
            self,
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
            next_page_token: Optional[str] = None,
    ) -> CatalogV2DataCollection:
        """
        :param markets: Comma separated list of markets. By default all markets are returned.
        :type markets: Optional[Union[str, List[str]]]
        :param exchange: Unique name of an exchange.
        :type exchange: Optional[str]
        :param market_type: Type of markets.
        :type market_type: Optional[str]
        :param base: Base asset of markets.
        :type base: Optional[str]
        :param quote: Quote asset of markets.
        :type quote: Optional[str]
        :param asset: Any asset of markets.
        :type asset: Optional[str]
        :param symbol: Symbol of derivative markets, full instrument name.
        :type symbol: Optional[str]
        :param format: Format of the response. Supported values are `json`, `json_stream`.
        :type format: Optional[str]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]
        :param next_page_token: Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
        :type next_page_token: Optional[str]

        :return: List of market quotes statistics.
        :rtype: CatalogV2DataCollection
        """
        params: Dict[str, Any] = {
            "markets": markets,
            "exchange": exchange,
            "type": market_type,
            "base": base,
            "quote": quote,
            "asset": asset,
            "symbol": symbol,
            "format": format,
            "page_size": page_size,
            "paging_from": paging_from,
            "next_page_token": next_page_token,
        }
        return CatalogV2DataCollection(self._get_data, "/catalog-v2/market-quotes", params, client=self)

    def catalog_market_funding_rates_v2(
            self,
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
            next_page_token: Optional[str] = None,
    ) -> CatalogV2DataCollection:
        """
        :param markets: Comma separated list of markets. By default all markets are returned.
        :type markets: Optional[Union[str, List[str]]]
        :param exchange: Unique name of an exchange.
        :type exchange: Optional[str]
        :param market_type: Type of markets.
        :type market_type: Optional[str]
        :param base: Base asset of markets.
        :type base: Optional[str]
        :param quote: Quote asset of markets.
        :type quote: Optional[str]
        :param asset: Any asset of markets.
        :type asset: Optional[str]
        :param symbol: Symbol of derivative markets, full instrument name.
        :type symbol: Optional[str]
        :param format: Format of the response. Supported values are `json`, `json_stream`.
        :type format: Optional[str]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]
        :param next_page_token: Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
        :type next_page_token: Optional[str]

        :return: List of market funding rates statistics.
        :rtype: CatalogV2DataCollection
        """
        params: Dict[str, Any] = {
            "markets": markets,
            "exchange": exchange,
            "type": market_type,
            "base": base,
            "quote": quote,
            "asset": asset,
            "symbol": symbol,
            "format": format,
            "page_size": page_size,
            "paging_from": paging_from,
            "next_page_token": next_page_token,
        }
        return CatalogV2DataCollection(self._get_data, "/catalog-v2/market-funding-rates", params, client=self)

    def catalog_market_funding_rates_predicted_v2(
            self,
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
            next_page_token: Optional[str] = None,
    ) -> CatalogV2DataCollection:
        """
        :param markets: Comma separated list of markets. By default all markets are returned.
        :type markets: Optional[Union[str, List[str]]]
        :param exchange: Unique name of an exchange.
        :type exchange: Optional[str]
        :param market_type: Type of markets.
        :type market_type: Optional[str]
        :param base: Base asset of markets.
        :type base: Optional[str]
        :param quote: Quote asset of markets.
        :type quote: Optional[str]
        :param asset: Any asset of markets.
        :type asset: Optional[str]
        :param symbol: Symbol of derivative markets, full instrument name.
        :type symbol: Optional[str]
        :param format: Format of the response. Supported values are `json`, `json_stream`.
        :type format: Optional[str]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]
        :param next_page_token: Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
        :type next_page_token: Optional[str]

        :return: List of market funding rates statistics.
        :rtype: CatalogV2DataCollection
        """
        params: Dict[str, Any] = {
            "markets": markets,
            "exchange": exchange,
            "type": market_type,
            "base": base,
            "quote": quote,
            "asset": asset,
            "symbol": symbol,
            "format": format,
            "page_size": page_size,
            "paging_from": paging_from,
            "next_page_token": next_page_token,
        }
        return CatalogV2DataCollection(self._get_data, "/catalog-v2/market-funding-rates-predicted", params, client=self)

    def catalog_market_contract_prices_v2(
            self,
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
            next_page_token: Optional[str] = None,
    ) -> CatalogV2DataCollection:
        """
        :param markets: Comma separated list of markets. By default all markets are returned.
        :type markets: Optional[Union[str, List[str]]]
        :param exchange: Unique name of an exchange.
        :type exchange: Optional[str]
        :param market_type: Type of markets.
        :type market_type: Optional[str]
        :param base: Base asset of markets.
        :type base: Optional[str]
        :param quote: Quote asset of markets.
        :type quote: Optional[str]
        :param asset: Any asset of markets.
        :type asset: Optional[str]
        :param symbol: Symbol of derivative markets, full instrument name.
        :type symbol: Optional[str]
        :param format: Format of the response. Supported values are `json`, `json_stream`.
        :type format: Optional[str]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]
        :param next_page_token: Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
        :type next_page_token: Optional[str]

        :return: List of contract prices statistics.
        :rtype: CatalogV2DataCollection
        """
        params: Dict[str, Any] = {
            "markets": markets,
            "exchange": exchange,
            "type": market_type,
            "base": base,
            "quote": quote,
            "asset": asset,
            "symbol": symbol,
            "format": format,
            "page_size": page_size,
            "paging_from": paging_from,
            "next_page_token": next_page_token,
        }
        return CatalogV2DataCollection(self._get_data, "/catalog-v2/market-contract-prices", params, client=self)

    def catalog_market_implied_volatility_v2(
            self,
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
            next_page_token: Optional[str] = None,
    ) -> CatalogV2DataCollection:
        """
        :param markets: Comma separated list of markets. By default all markets are returned.
        :type markets: Optional[Union[str, List[str]]]
        :param exchange: Unique name of an exchange.
        :type exchange: Optional[str]
        :param market_type: Type of markets.
        :type market_type: Optional[str]
        :param base: Base asset of markets.
        :type base: Optional[str]
        :param quote: Quote asset of markets.
        :type quote: Optional[str]
        :param asset: Any asset of markets.
        :type asset: Optional[str]
        :param symbol: Symbol of derivative markets, full instrument name.
        :type symbol: Optional[str]
        :param format: Format of the response. Supported values are `json`, `json_stream`.
        :type format: Optional[str]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]
        :param next_page_token: Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
        :type next_page_token: Optional[str]

        :return: List of implied volatility statistics.
        :rtype: CatalogV2DataCollection
        """
        params: Dict[str, Any] = {
            "markets": markets,
            "exchange": exchange,
            "type": market_type,
            "base": base,
            "quote": quote,
            "asset": asset,
            "symbol": symbol,
            "format": format,
            "page_size": page_size,
            "paging_from": paging_from,
            "next_page_token": next_page_token,
        }
        return CatalogV2DataCollection(self._get_data, "/catalog-v2/market-implied-volatility", params, client=self)

    def catalog_market_greeks_v2(
            self,
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
            next_page_token: Optional[str] = None,
    ) -> CatalogV2DataCollection:
        """
        :param markets: Comma separated list of markets. By default all markets are returned.
        :type markets: Optional[Union[str, List[str]]]
        :param exchange: Unique name of an exchange.
        :type exchange: Optional[str]
        :param market_type: Type of markets.
        :type market_type: Optional[str]
        :param base: Base asset of markets.
        :type base: Optional[str]
        :param quote: Quote asset of markets.
        :type quote: Optional[str]
        :param asset: Any asset of markets.
        :type asset: Optional[str]
        :param symbol: Symbol of derivative markets, full instrument name.
        :type symbol: Optional[str]
        :param format: Format of the response. Supported values are `json`, `json_stream`.
        :type format: Optional[str]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]
        :param next_page_token: Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
        :type next_page_token: Optional[str]

        :return: List of greeks statistics.
        :rtype: CatalogV2DataCollection
        """
        params: Dict[str, Any] = {
            "markets": markets,
            "exchange": exchange,
            "type": market_type,
            "base": base,
            "quote": quote,
            "asset": asset,
            "symbol": symbol,
            "format": format,
            "page_size": page_size,
            "paging_from": paging_from,
            "next_page_token": next_page_token,
        }
        return CatalogV2DataCollection(self._get_data, "/catalog-v2/market-greeks", params, client=self)

    def catalog_market_open_interest_v2(
            self,
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
            next_page_token: Optional[str] = None,
    ) -> CatalogV2DataCollection:
        """
        :param markets: Comma separated list of markets. By default all markets are returned.
        :type markets: Optional[Union[str, List[str]]]
        :param exchange: Unique name of an exchange.
        :type exchange: Optional[str]
        :param market_type: Type of markets.
        :type market_type: Optional[str]
        :param base: Base asset of markets.
        :type base: Optional[str]
        :param quote: Quote asset of markets.
        :type quote: Optional[str]
        :param asset: Any asset of markets.
        :type asset: Optional[str]
        :param symbol: Symbol of derivative markets, full instrument name.
        :type symbol: Optional[str]
        :param format: Format of the response. Supported values are `json`, `json_stream`.
        :type format: Optional[str]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]
        :param next_page_token: Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
        :type next_page_token: Optional[str]

        :return: List of market open interest statistics.
        :rtype: CatalogV2DataCollection
        """
        params: Dict[str, Any] = {
            "markets": markets,
            "exchange": exchange,
            "type": market_type,
            "base": base,
            "quote": quote,
            "asset": asset,
            "symbol": symbol,
            "format": format,
            "page_size": page_size,
            "paging_from": paging_from,
            "next_page_token": next_page_token,
        }
        return CatalogV2DataCollection(self._get_data, "/catalog-v2/market-openinterest", params, client=self)

    def catalog_market_liquidations_v2(
            self,
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
            next_page_token: Optional[str] = None,
    ) -> CatalogV2DataCollection:
        """
        :param markets: Comma separated list of markets. By default all markets are returned.
        :type markets: Optional[Union[str, List[str]]]
        :param exchange: Unique name of an exchange.
        :type exchange: Optional[str]
        :param market_type: Type of markets.
        :type market_type: Optional[str]
        :param base: Base asset of markets.
        :type base: Optional[str]
        :param quote: Quote asset of markets.
        :type quote: Optional[str]
        :param asset: Any asset of markets.
        :type asset: Optional[str]
        :param symbol: Symbol of derivative markets, full instrument name.
        :type symbol: Optional[str]
        :param format: Format of the response. Supported values are `json`, `json_stream`.
        :type format: Optional[str]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]
        :param next_page_token: Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
        :type next_page_token: Optional[str]

        :return: List of market liquidations statistics.
        :rtype: CatalogV2DataCollection
        """
        params: Dict[str, Any] = {
            "markets": markets,
            "exchange": exchange,
            "type": market_type,
            "base": base,
            "quote": quote,
            "asset": asset,
            "symbol": symbol,
            "format": format,
            "page_size": page_size,
            "paging_from": paging_from,
            "next_page_token": next_page_token,
        }
        return CatalogV2DataCollection(self._get_data, "/catalog-v2/market-liquidations", params, client=self)

    def catalog_market_metrics_v2(
            self,
            markets: Optional[Union[str, List[str]]] = None,
            metrics: Optional[Union[str, List[str]]] = None,
            exchange: Optional[str] = None,
            market_type: Optional[str] = None,
            base: Optional[str] = None,
            quote: Optional[str] = None,
            asset: Optional[str] = None,
            symbol: Optional[str] = None,
            format: Optional[str] = None,
            page_size: Optional[int] = None,
            paging_from: Optional[str] = None,
            next_page_token: Optional[str] = None,
    ) -> CatalogV2DataCollection:
        """
        :param markets: Comma separated list of markets. By default all markets are returned.
        :type markets: Optional[Union[str, List[str]]]
        :param metrics: Comma separated list of metrics. By default all metrics are returned.
        :type metrics: Optional[Union[str, List[str]]]
        :param exchange: Unique name of an exchange.
        :type exchange: Optional[str]
        :param market_type: Type of markets.
        :type market_type: Optional[str]
        :param base: Base asset of markets.
        :type base: Optional[str]
        :param quote: Quote asset of markets.
        :type quote: Optional[str]
        :param asset: Any asset of markets.
        :type asset: Optional[str]
        :param symbol: Symbol of derivative markets, full instrument name.
        :type symbol: Optional[str]
        :param format: Format of the response. Supported values are `json`, `json_stream`.
        :type format: Optional[str]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]
        :param next_page_token: Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
        :type next_page_token: Optional[str]

        :return: List of market metrics statistics.
        :rtype: CatalogV2DataCollection
        """
        params: Dict[str, Any] = {
            "markets": markets,
            "metrics": metrics,
            "exchange": exchange,
            "type": market_type,
            "base": base,
            "quote": quote,
            "asset": asset,
            "symbol": symbol,
            "format": format,
            "page_size": page_size,
            "paging_from": paging_from,
            "next_page_token": next_page_token,
        }
        return CatalogV2DataCollection(
            self._get_data,
            "/catalog-v2/market-metrics",
            params,
            metric_type='market',
            iterable_col="frequencies",
            iterable_key="frequency",
            explode_on="metrics",
            assign_to="metric",
            client=self
        )

    def catalog_full_market_trades_v2(
            self,
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
            next_page_token: Optional[str] = None,
    ) -> CatalogV2DataCollection:
        """
        :param markets: Comma separated list of markets. By default all markets are returned.
        :type markets: Optional[Union[str, List[str]]]
        :param exchange: Unique name of an exchange.
        :type exchange: Optional[str]
        :param market_type: Type of markets.
        :type market_type: Optional[str]
        :param base: Base asset of markets.
        :type base: Optional[str]
        :param quote: Quote asset of markets.
        :type quote: Optional[str]
        :param asset: Any asset of markets.
        :type asset: Optional[str]
        :param symbol: Symbol of derivative markets, full instrument name.
        :type symbol: Optional[str]
        :param format: Format of the response. Supported values are `json`, `json_stream`.
        :type format: Optional[str]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]
        :param next_page_token: Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
        :type next_page_token: Optional[str]

        :return: List of market trades statistics.
        :rtype: CatalogV2DataCollection
        """
        params: Dict[str, Any] = {
            "markets": markets,
            "exchange": exchange,
            "type": market_type,
            "base": base,
            "quote": quote,
            "asset": asset,
            "symbol": symbol,
            "format": format,
            "page_size": page_size,
            "paging_from": paging_from,
            "next_page_token": next_page_token,
        }
        return CatalogV2DataCollection(self._get_data, "/catalog-all-v2/market-trades", params, client=self)

    def catalog_full_market_candles_v2(
            self,
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
            next_page_token: Optional[str] = None,
    ) -> CatalogV2DataCollection:
        """
        :param markets: Comma separated list of markets. By default all markets are returned.
        :type markets: Optional[Union[str, List[str]]]
        :param exchange: Unique name of an exchange.
        :type exchange: Optional[str]
        :param market_type: Type of markets.
        :type market_type: Optional[str]
        :param base: Base asset of markets.
        :type base: Optional[str]
        :param quote: Quote asset of markets.
        :type quote: Optional[str]
        :param asset: Any asset of markets.
        :type asset: Optional[str]
        :param symbol: Symbol of derivative markets, full instrument name.
        :type symbol: Optional[str]
        :param format: Format of the response. Supported values are `json`, `json_stream`.
        :type format: Optional[str]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]
        :param next_page_token: Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
        :type next_page_token: Optional[str]

        :return: List of market candles statistics.
        :rtype: CatalogV2DataCollection
        """
        params: Dict[str, Any] = {
            "markets": markets,
            "exchange": exchange,
            "type": market_type,
            "base": base,
            "quote": quote,
            "asset": asset,
            "symbol": symbol,
            "format": format,
            "page_size": page_size,
            "paging_from": paging_from,
            "next_page_token": next_page_token,
        }
        return CatalogV2DataCollection(
            self._get_data,
            "/catalog-all-v2/market-candles",
            params,
            iterable_col="frequencies",
            iterable_key="frequency",
            client=self
        )

    def catalog_full_market_orderbooks_v2(
            self,
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
            next_page_token: Optional[str] = None,
    ) -> CatalogV2DataCollection:
        """
        :param markets: Comma separated list of markets. By default all markets are returned.
        :type markets: Optional[Union[str, List[str]]]
        :param exchange: Unique name of an exchange.
        :type exchange: Optional[str]
        :param market_type: Type of markets.
        :type market_type: Optional[str]
        :param base: Base asset of markets.
        :type base: Optional[str]
        :param quote: Quote asset of markets.
        :type quote: Optional[str]
        :param asset: Any asset of markets.
        :type asset: Optional[str]
        :param symbol: Symbol of derivative markets, full instrument name.
        :type symbol: Optional[str]
        :param format: Format of the response. Supported values are `json`, `json_stream`.
        :type format: Optional[str]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]
        :param next_page_token: Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
        :type next_page_token: Optional[str]

        :return: List of market orderbooks statistics.
        :rtype: CatalogV2DataCollection
        """
        params: Dict[str, Any] = {
            "markets": markets,
            "exchange": exchange,
            "type": market_type,
            "base": base,
            "quote": quote,
            "asset": asset,
            "symbol": symbol,
            "format": format,
            "page_size": page_size,
            "paging_from": paging_from,
            "next_page_token": next_page_token,
        }
        return CatalogV2DataCollection(
            self._get_data,
            "/catalog-all-v2/market-orderbooks",
            params,
            iterable_key="depth",
            iterable_col="depths",
            client=self
        )

    def catalog_full_market_quotes_v2(
            self,
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
            next_page_token: Optional[str] = None,
    ) -> CatalogV2DataCollection:
        """
        :param markets: Comma separated list of markets. By default all markets are returned.
        :type markets: Optional[Union[str, List[str]]]
        :param exchange: Unique name of an exchange.
        :type exchange: Optional[str]
        :param market_type: Type of markets.
        :type market_type: Optional[str]
        :param base: Base asset of markets.
        :type base: Optional[str]
        :param quote: Quote asset of markets.
        :type quote: Optional[str]
        :param asset: Any asset of markets.
        :type asset: Optional[str]
        :param symbol: Symbol of derivative markets, full instrument name.
        :type symbol: Optional[str]
        :param format: Format of the response. Supported values are `json`, `json_stream`.
        :type format: Optional[str]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]
        :param next_page_token: Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
        :type next_page_token: Optional[str]

        :return: List of market quotes statistics.
        :rtype: CatalogV2DataCollection
        """
        params: Dict[str, Any] = {
            "markets": markets,
            "exchange": exchange,
            "type": market_type,
            "base": base,
            "quote": quote,
            "asset": asset,
            "symbol": symbol,
            "format": format,
            "page_size": page_size,
            "paging_from": paging_from,
            "next_page_token": next_page_token,
        }
        return CatalogV2DataCollection(self._get_data, "/catalog-all-v2/market-quotes", params, client=self)

    def catalog_full_market_funding_rates_v2(
            self,
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
            next_page_token: Optional[str] = None,
    ) -> CatalogV2DataCollection:
        """
        :param markets: Comma separated list of markets. By default all markets are returned.
        :type markets: Optional[Union[str, List[str]]]
        :param exchange: Unique name of an exchange.
        :type exchange: Optional[str]
        :param market_type: Type of markets.
        :type market_type: Optional[str]
        :param base: Base asset of markets.
        :type base: Optional[str]
        :param quote: Quote asset of markets.
        :type quote: Optional[str]
        :param asset: Any asset of markets.
        :type asset: Optional[str]
        :param symbol: Symbol of derivative markets, full instrument name.
        :type symbol: Optional[str]
        :param format: Format of the response. Supported values are `json`, `json_stream`.
        :type format: Optional[str]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]
        :param next_page_token: Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
        :type next_page_token: Optional[str]

        :return: List of market funding rates statistics.
        :rtype: CatalogV2DataCollection
        """
        params: Dict[str, Any] = {
            "markets": markets,
            "exchange": exchange,
            "type": market_type,
            "base": base,
            "quote": quote,
            "asset": asset,
            "symbol": symbol,
            "format": format,
            "page_size": page_size,
            "paging_from": paging_from,
            "next_page_token": next_page_token,
        }
        return CatalogV2DataCollection(self._get_data, "/catalog-all-v2/market-funding-rates", params, client=self)

    def catalog_full_market_funding_rates_predicted_v2(
            self,
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
            next_page_token: Optional[str] = None,
    ) -> CatalogV2DataCollection:
        """
        :param markets: Comma separated list of markets. By default all markets are returned.
        :type markets: Optional[Union[str, List[str]]]
        :param exchange: Unique name of an exchange.
        :type exchange: Optional[str]
        :param market_type: Type of markets.
        :type market_type: Optional[str]
        :param base: Base asset of markets.
        :type base: Optional[str]
        :param quote: Quote asset of markets.
        :type quote: Optional[str]
        :param asset: Any asset of markets.
        :type asset: Optional[str]
        :param symbol: Symbol of derivative markets, full instrument name.
        :type symbol: Optional[str]
        :param format: Format of the response. Supported values are `json`, `json_stream`.
        :type format: Optional[str]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]
        :param next_page_token: Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
        :type next_page_token: Optional[str]

        :return: List of market funding rates statistics.
        :rtype: CatalogV2DataCollection
        """
        params: Dict[str, Any] = {
            "markets": markets,
            "exchange": exchange,
            "type": market_type,
            "base": base,
            "quote": quote,
            "asset": asset,
            "symbol": symbol,
            "format": format,
            "page_size": page_size,
            "paging_from": paging_from,
            "next_page_token": next_page_token,
        }
        return CatalogV2DataCollection(self._get_data, "/catalog-all-v2/market-funding-rates-predicted", params, client=self)

    def catalog_full_market_contract_prices_v2(
            self,
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
            next_page_token: Optional[str] = None,
    ) -> CatalogV2DataCollection:
        """
        :param markets: Comma separated list of markets. By default all markets are returned.
        :type markets: Optional[Union[str, List[str]]]
        :param exchange: Unique name of an exchange.
        :type exchange: Optional[str]
        :param market_type: Type of markets.
        :type market_type: Optional[str]
        :param base: Base asset of markets.
        :type base: Optional[str]
        :param quote: Quote asset of markets.
        :type quote: Optional[str]
        :param asset: Any asset of markets.
        :type asset: Optional[str]
        :param symbol: Symbol of derivative markets, full instrument name.
        :type symbol: Optional[str]
        :param format: Format of the response. Supported values are `json`, `json_stream`.
        :type format: Optional[str]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]
        :param next_page_token: Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
        :type next_page_token: Optional[str]

        :return: List of contract prices statistics.
        :rtype: CatalogV2DataCollection
        """
        params: Dict[str, Any] = {
            "markets": markets,
            "exchange": exchange,
            "type": market_type,
            "base": base,
            "quote": quote,
            "asset": asset,
            "symbol": symbol,
            "format": format,
            "page_size": page_size,
            "paging_from": paging_from,
            "next_page_token": next_page_token,
        }
        return CatalogV2DataCollection(self._get_data, "/catalog-all-v2/market-contract-prices", params, client=self)

    def catalog_full_market_implied_volatility_v2(
            self,
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
            next_page_token: Optional[str] = None,
    ) -> CatalogV2DataCollection:
        """
        :param markets: Comma separated list of markets. By default all markets are returned.
        :type markets: Optional[Union[str, List[str]]]
        :param exchange: Unique name of an exchange.
        :type exchange: Optional[str]
        :param market_type: Type of markets.
        :type market_type: Optional[str]
        :param base: Base asset of markets.
        :type base: Optional[str]
        :param quote: Quote asset of markets.
        :type quote: Optional[str]
        :param asset: Any asset of markets.
        :type asset: Optional[str]
        :param symbol: Symbol of derivative markets, full instrument name.
        :type symbol: Optional[str]
        :param format: Format of the response. Supported values are `json`, `json_stream`.
        :type format: Optional[str]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]
        :param next_page_token: Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
        :type next_page_token: Optional[str]

        :return: List of implied volatility statistics.
        :rtype: CatalogV2DataCollection
        """
        params: Dict[str, Any] = {
            "markets": markets,
            "exchange": exchange,
            "type": market_type,
            "base": base,
            "quote": quote,
            "asset": asset,
            "symbol": symbol,
            "format": format,
            "page_size": page_size,
            "paging_from": paging_from,
            "next_page_token": next_page_token,
        }
        return CatalogV2DataCollection(self._get_data, "/catalog-all-v2/market-implied-volatility", params, client=self)

    def catalog_full_market_greeks_v2(
            self,
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
            next_page_token: Optional[str] = None,
    ) -> CatalogV2DataCollection:
        """
        :param markets: Comma separated list of markets. By default all markets are returned.
        :type markets: Optional[Union[str, List[str]]]
        :param exchange: Unique name of an exchange.
        :type exchange: Optional[str]
        :param market_type: Type of markets.
        :type market_type: Optional[str]
        :param base: Base asset of markets.
        :type base: Optional[str]
        :param quote: Quote asset of markets.
        :type quote: Optional[str]
        :param asset: Any asset of markets.
        :type asset: Optional[str]
        :param symbol: Symbol of derivative markets, full instrument name.
        :type symbol: Optional[str]
        :param format: Format of the response. Supported values are `json`, `json_stream`.
        :type format: Optional[str]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]
        :param next_page_token: Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
        :type next_page_token: Optional[str]

        :return: List of greeks statistics.
        :rtype: CatalogV2DataCollection
        """
        params: Dict[str, Any] = {
            "markets": markets,
            "exchange": exchange,
            "type": market_type,
            "base": base,
            "quote": quote,
            "asset": asset,
            "symbol": symbol,
            "format": format,
            "page_size": page_size,
            "paging_from": paging_from,
            "next_page_token": next_page_token,
        }
        return CatalogV2DataCollection(self._get_data, "/catalog-all-v2/market-greeks", params, client=self)

    def catalog_full_market_open_interest_v2(
            self,
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
            next_page_token: Optional[str] = None,
    ) -> CatalogV2DataCollection:
        """
        :param markets: Comma separated list of markets. By default all markets are returned.
        :type markets: Optional[Union[str, List[str]]]
        :param exchange: Unique name of an exchange.
        :type exchange: Optional[str]
        :param market_type: Type of markets.
        :type market_type: Optional[str]
        :param base: Base asset of markets.
        :type base: Optional[str]
        :param quote: Quote asset of markets.
        :type quote: Optional[str]
        :param asset: Any asset of markets.
        :type asset: Optional[str]
        :param symbol: Symbol of derivative markets, full instrument name.
        :type symbol: Optional[str]
        :param format: Format of the response. Supported values are `json`, `json_stream`.
        :type format: Optional[str]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]
        :param next_page_token: Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
        :type next_page_token: Optional[str]

        :return: List of market open interest statistics.
        :rtype: CatalogV2DataCollection
        """
        params: Dict[str, Any] = {
            "markets": markets,
            "exchange": exchange,
            "type": market_type,
            "base": base,
            "quote": quote,
            "asset": asset,
            "symbol": symbol,
            "format": format,
            "page_size": page_size,
            "paging_from": paging_from,
            "next_page_token": next_page_token,
        }
        return CatalogV2DataCollection(self._get_data, "/catalog-all-v2/market-openinterest", params, client=self)

    def catalog_full_market_liquidations_v2(
            self,
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
            next_page_token: Optional[str] = None,
    ) -> CatalogV2DataCollection:
        """
        :param markets: Comma separated list of markets. By default all markets are returned.
        :type markets: Optional[Union[str, List[str]]]
        :param exchange: Unique name of an exchange.
        :type exchange: Optional[str]
        :param market_type: Type of markets.
        :type market_type: Optional[str]
        :param base: Base asset of markets.
        :type base: Optional[str]
        :param quote: Quote asset of markets.
        :type quote: Optional[str]
        :param asset: Any asset of markets.
        :type asset: Optional[str]
        :param symbol: Symbol of derivative markets, full instrument name.
        :type symbol: Optional[str]
        :param format: Format of the response. Supported values are `json`, `json_stream`.
        :type format: Optional[str]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]
        :param next_page_token: Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
        :type next_page_token: Optional[str]

        :return: List of market liquidations statistics.
        :rtype: CatalogV2DataCollection
        """
        params: Dict[str, Any] = {
            "markets": markets,
            "exchange": exchange,
            "type": market_type,
            "base": base,
            "quote": quote,
            "asset": asset,
            "symbol": symbol,
            "format": format,
            "page_size": page_size,
            "paging_from": paging_from,
            "next_page_token": next_page_token,
        }
        return CatalogV2DataCollection(self._get_data, "/catalog-all-v2/market-liquidations", params, client=self)

    def catalog_full_market_metrics_v2(
            self,
            markets: Optional[Union[str, List[str]]] = None,
            metrics: Optional[Union[str, List[str]]] = None,
            exchange: Optional[str] = None,
            market_type: Optional[str] = None,
            base: Optional[str] = None,
            quote: Optional[str] = None,
            asset: Optional[str] = None,
            symbol: Optional[str] = None,
            format: Optional[str] = None,
            page_size: Optional[int] = None,
            paging_from: Optional[str] = None,
            next_page_token: Optional[str] = None,
    ) -> CatalogV2DataCollection:
        """
        :param markets: Comma separated list of markets. By default all markets are returned.
        :type markets: Optional[Union[str, List[str]]]
        :param metrics: Comma separated list of metrics. By default all metrics are returned.
        :type metrics: Optional[Union[str, List[str]]]
        :param exchange: Unique name of an exchange.
        :type exchange: Optional[str]
        :param market_type: Type of markets.
        :type market_type: Optional[str]
        :param base: Base asset of markets.
        :type base: Optional[str]
        :param quote: Quote asset of markets.
        :type quote: Optional[str]
        :param asset: Any asset of markets.
        :type asset: Optional[str]
        :param symbol: Symbol of derivative markets, full instrument name.
        :type symbol: Optional[str]
        :param format: Format of the response. Supported values are `json`, `json_stream`.
        :type format: Optional[str]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]
        :param next_page_token: Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
        :type next_page_token: Optional[str]

        :return: List of market metrics statistics.
        :rtype: CatalogV2DataCollection
        """
        params: Dict[str, Any] = {
            "markets": markets,
            "metrics": metrics,
            "exchange": exchange,
            "type": market_type,
            "base": base,
            "quote": quote,
            "asset": asset,
            "symbol": symbol,
            "format": format,
            "page_size": page_size,
            "paging_from": paging_from,
            "next_page_token": next_page_token,
        }
        return CatalogV2DataCollection(
            self._get_data,
            "/catalog-all-v2/market-metrics",
            params,
            metric_type='market',
            iterable_col="frequencies",
            iterable_key="frequency",
            explode_on="metrics",
            assign_to="metric",
            client=self
        )

    def catalog_asset_metrics_v2(
            self,
            assets: Optional[Union[str, List[str]]] = None,
            metrics: Optional[Union[str, List[str]]] = None,
            reviewable: Optional[bool] = None,
            page_size: Optional[int] = None,
            paging_from: Optional[str] = None,
            next_page_token: Optional[str] = None,
            format: Optional[str] = None,
    ) -> CatalogV2DataCollection:
        """
        :param assets: Comma separated list of assets. By default all assets are returned.
        :type assets: Optional[Union[str, List[str]]]
        :param metrics: Comma separated list of metrics. By default all metrics are returned.
        :type metrics: Optional[Union[str, List[str]]]
        :param reviewable: Limit to human-reviewable metrics. By default all metrics are returned.
        :type reviewable: Optional[bool]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]
        :param next_page_token: Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
        :type next_page_token: Optional[str]
        :param format: Format of the response. Supported values are `json`, `json_stream`.
        :type format: Optional[str]

        :return: List of asset metrics.
        :rtype: CatalogV2DataCollection
        """
        params: Dict[str, Any] = {
            "assets": assets,
            "metrics": metrics,
            "reviewable": reviewable,
            "page_size": page_size,
            "paging_from": paging_from,
            "next_page_token": next_page_token,
            "format": format,
        }
        return CatalogV2DataCollection(
            self._get_data,
            "/catalog-v2/asset-metrics",
            params,
            metric_type="asset",
            iterable_col="frequencies",
            iterable_key="frequency",
            explode_on="metrics",
            assign_to="metric",
            nested_catalog_columns=["frequency", "min_time", "max_time", "min_height", "max_height", "min_hash", "max_hash", "community"],
            client=self
        )

    def catalog_full_asset_metrics_v2(
            self,
            assets: Optional[Union[str, List[str]]] = None,
            metrics: Optional[Union[str, List[str]]] = None,
            reviewable: Optional[bool] = None,
            page_size: Optional[int] = None,
            paging_from: Optional[str] = None,
            next_page_token: Optional[str] = None,
            format: Optional[str] = None,
    ) -> CatalogV2DataCollection:
        """
        :param assets: Comma separated list of assets. By default all assets are returned.
        :type assets: Optional[Union[str, List[str]]]
        :param metrics: Comma separated list of metrics. By default all metrics are returned.
        :type metrics: Optional[Union[str, List[str]]]
        :param reviewable: Limit to human-reviewable metrics. By default all metrics are returned.
        :type reviewable: Optional[bool]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]
        :param next_page_token: Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
        :type next_page_token: Optional[str]
        :param format: Format of the response. Supported values are `json`, `json_stream`.
        :type format: Optional[str]

        :return: List of asset metrics.
        :rtype: CatalogV2DataCollection
        """
        params: Dict[str, Any] = {
            "assets": assets,
            "metrics": metrics,
            "reviewable": reviewable,
            "page_size": page_size,
            "paging_from": paging_from,
            "next_page_token": next_page_token,
            "format": format,
        }
        return CatalogV2DataCollection(
            self._get_data,
            "/catalog-all-v2/asset-metrics",
            params,
            metric_type="asset",
            iterable_col="frequencies",
            iterable_key="frequency",
            explode_on="metrics",
            assign_to="metric",
            nested_catalog_columns=["frequency", "min_time", "max_time", "min_height", "max_height", "min_hash", "max_hash", "community"],
            client=self
        )

    def catalog_exchange_metrics_v2(
            self,
            exchanges: Optional[Union[str, List[str]]] = None,
            metrics: Optional[Union[str, List[str]]] = None,
            reviewable: Optional[bool] = None,
            page_size: Optional[int] = None,
            paging_from: Optional[str] = None,
            next_page_token: Optional[str] = None,
            format: Optional[str] = None,
    ) -> CatalogV2DataCollection:
        """
        :param exchanges: Comma separated list of exchanges. By default all exchanges are returned.
        :type exchanges: Optional[Union[str, List[str]]]
        :param metrics: Comma separated list of metrics. By default all metrics are returned.
        :type metrics: Optional[Union[str, List[str]]]
        :param reviewable: Limit to human-reviewable metrics. By default all metrics are returned.
        :type reviewable: Optional[bool]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]
        :param next_page_token: Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
        :type next_page_token: Optional[str]
        :param format: Format of the response. Supported values are `json`, `json_stream`.
        :type format: Optional[str]

        :return: List of exchange metrics.
        :rtype: CatalogV2DataCollection
        """
        params: Dict[str, Any] = {
            "exchanges": exchanges,
            "metrics": metrics,
            "reviewable": reviewable,
            "page_size": page_size,
            "paging_from": paging_from,
            "next_page_token": next_page_token,
            "format": format,
        }
        return CatalogV2DataCollection(
            self._get_data,
            "/catalog-v2/exchange-metrics",
            params,
            metric_type="exchange",
            iterable_col="frequencies",
            iterable_key="frequency",
            explode_on="metrics",
            assign_to="metric",
            client=self
        )

    def catalog_full_exchange_metrics_v2(
            self,
            exchanges: Optional[Union[str, List[str]]] = None,
            metrics: Optional[Union[str, List[str]]] = None,
            reviewable: Optional[bool] = None,
            page_size: Optional[int] = None,
            paging_from: Optional[str] = None,
            next_page_token: Optional[str] = None,
            format: Optional[str] = None,
    ) -> CatalogV2DataCollection:
        """
        :param exchanges: Comma separated list of exchanges. By default all exchanges are returned.
        :type exchanges: Optional[Union[str, List[str]]]
        :param metrics: Comma separated list of metrics. By default all metrics are returned.
        :type metrics: Optional[Union[str, List[str]]]
        :param reviewable: Limit to human-reviewable metrics. By default all metrics are returned.
        :type reviewable: Optional[bool]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]
        :param next_page_token: Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
        :type next_page_token: Optional[str]
        :param format: Format of the response. Supported values are `json`, `json_stream`.
        :type format: Optional[str]

        :return: List of exchange metrics.
        :rtype: CatalogV2DataCollection
        """
        params: Dict[str, Any] = {
            "exchanges": exchanges,
            "metrics": metrics,
            "reviewable": reviewable,
            "page_size": page_size,
            "paging_from": paging_from,
            "next_page_token": next_page_token,
            "format": format,
        }
        return CatalogV2DataCollection(
            self._get_data,
            "/catalog-all-v2/exchange-metrics",
            params,
            metric_type="exchange",
            iterable_col="frequencies",
            iterable_key="frequency",
            explode_on="metrics",
            assign_to="metric",
            client=self
        )

    def catalog_exchange_asset_metrics_v2(
            self,
            exchange_assets: Optional[Union[str, List[str]]] = None,
            metrics: Optional[Union[str, List[str]]] = None,
            reviewable: Optional[bool] = None,
            page_size: Optional[int] = None,
            paging_from: Optional[str] = None,
            next_page_token: Optional[str] = None,
            format: Optional[str] = None,
    ) -> CatalogV2DataCollection:
        """
        :param exchange_assets: Comma separated list of exchange-assets. By default, all exchange-assets pairs are returned.
        :type exchange_assets: Optional[Union[str, List[str]]]
        :param metrics: Comma separated list of metrics. By default all metrics are returned.
        :type metrics: Optional[Union[str, List[str]]]
        :param reviewable: Limit to human-reviewable metrics. By default all metrics are returned.
        :type reviewable: Optional[bool]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]
        :param next_page_token: Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
        :type next_page_token: Optional[str]
        :param format: Format of the response. Supported values are `json`, `json_stream`.
        :type format: Optional[str]

        :return: List of exchange-asset metrics.
        :rtype: CatalogV2DataCollection
        """
        params: Dict[str, Any] = {
            "exchange_assets": exchange_assets,
            "metrics": metrics,
            "reviewable": reviewable,
            "page_size": page_size,
            "paging_from": paging_from,
            "next_page_token": next_page_token,
            "format": format,
        }
        return CatalogV2DataCollection(
            self._get_data,
            "/catalog-v2/exchange-asset-metrics",
            params,
            metric_type="exchange_asset",
            iterable_col="frequencies",
            iterable_key="frequency",
            explode_on="metrics",
            assign_to="metric",
            client=self
        )

    def catalog_full_exchange_asset_metrics_v2(
            self,
            exchange_assets: Optional[Union[str, List[str]]] = None,
            metrics: Optional[Union[str, List[str]]] = None,
            reviewable: Optional[bool] = None,
            page_size: Optional[int] = None,
            paging_from: Optional[str] = None,
            next_page_token: Optional[str] = None,
            format: Optional[str] = None,
    ) -> CatalogV2DataCollection:
        """
        :param exchange_assets: Comma separated list of exchange-assets. By default, all exchange-assets pairs are returned.
        :type exchange_assets: Optional[Union[str, List[str]]]
        :param metrics: Comma separated list of metrics. By default all metrics are returned.
        :type metrics: Optional[Union[str, List[str]]]
        :param reviewable: Limit to human-reviewable metrics. By default all metrics are returned.
        :type reviewable: Optional[bool]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]
        :param next_page_token: Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
        :type next_page_token: Optional[str]
        :param format: Format of the response. Supported values are `json`, `json_stream`.
        :type format: Optional[str]

        :return: List of exchange-asset metrics.
        :rtype: CatalogV2DataCollection
        """
        params: Dict[str, Any] = {
            "exchange_assets": exchange_assets,
            "metrics": metrics,
            "reviewable": reviewable,
            "page_size": page_size,
            "paging_from": paging_from,
            "next_page_token": next_page_token,
            "format": format,
        }
        return CatalogV2DataCollection(
            self._get_data,
            "/catalog-all-v2/exchange-asset-metrics",
            params,
            metric_type="exchange_asset",
            iterable_col="frequencies",
            iterable_key="frequency",
            explode_on="metrics",
            assign_to="metric",
            client=self
        )

    def catalog_pair_metrics_v2(
            self,
            pairs: Optional[Union[str, List[str]]] = None,
            metrics: Optional[Union[str, List[str]]] = None,
            reviewable: Optional[bool] = None,
            page_size: Optional[int] = None,
            paging_from: Optional[str] = None,
            next_page_token: Optional[str] = None,
            format: Optional[str] = None,
    ) -> CatalogV2DataCollection:
        """
        :param pairs: Comma separated list of asset pairs. By default, all asset pairs are returned.
        :type pairs: Optional[Union[str, List[str]]]
        :param metrics: Comma separated list of metrics. By default all metrics are returned.
        :type metrics: Optional[Union[str, List[str]]]
        :param reviewable: Limit to human-reviewable metrics. By default all metrics are returned.
        :type reviewable: Optional[bool]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]
        :param next_page_token: Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
        :type next_page_token: Optional[str]
        :param format: Format of the response. Supported values are `json`, `json_stream`.
        :type format: Optional[str]

        :return: List of pair metrics.
        :rtype: CatalogV2DataCollection
        """
        params: Dict[str, Any] = {
            "pairs": pairs,
            "metrics": metrics,
            "reviewable": reviewable,
            "page_size": page_size,
            "paging_from": paging_from,
            "next_page_token": next_page_token,
            "format": format,
        }
        return CatalogV2DataCollection(
            self._get_data,
            "/catalog-v2/pair-metrics",
            params,
            metric_type="pair",
            iterable_col="frequencies",
            iterable_key="frequency",
            explode_on="metrics",
            assign_to="metric",
            client=self
        )

    def catalog_full_pair_metrics_v2(
            self,
            pairs: Optional[Union[str, List[str]]] = None,
            metrics: Optional[Union[str, List[str]]] = None,
            reviewable: Optional[bool] = None,
            page_size: Optional[int] = None,
            paging_from: Optional[str] = None,
            next_page_token: Optional[str] = None,
            format: Optional[str] = None,
    ) -> CatalogV2DataCollection:
        """
        :param pairs: Comma separated list of asset pairs. By default, all asset pairs are returned.
        :type pairs: Optional[Union[str, List[str]]]
        :param metrics: Comma separated list of metrics. By default all metrics are returned.
        :type metrics: Optional[Union[str, List[str]]]
        :param reviewable: Limit to human-reviewable metrics. By default all metrics are returned.
        :type reviewable: Optional[bool]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]
        :param next_page_token: Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
        :type next_page_token: Optional[str]
        :param format: Format of the response. Supported values are `json`, `json_stream`.
        :type format: Optional[str]

        :return: List of pair metrics.
        :rtype: CatalogV2DataCollection
        """
        params: Dict[str, Any] = {
            "pairs": pairs,
            "metrics": metrics,
            "reviewable": reviewable,
            "page_size": page_size,
            "paging_from": paging_from,
            "next_page_token": next_page_token,
            "format": format,
        }
        return CatalogV2DataCollection(
            self._get_data,
            "/catalog-all-v2/pair-metrics",
            params,
            metric_type="pair",
            iterable_col="frequencies",
            iterable_key="frequency",
            explode_on="metrics",
            assign_to="metric",
            client=self
        )

    def catalog_institution_metrics_v2(
            self,
            institutions: Optional[Union[str, List[str]]] = None,
            metrics: Optional[Union[str, List[str]]] = None,
            reviewable: Optional[bool] = None,
            page_size: Optional[int] = None,
            paging_from: Optional[str] = None,
            next_page_token: Optional[str] = None,
            format: Optional[str] = None,
    ) -> CatalogV2DataCollection:
        """
        :param institutions: Comma separated list of institutions. By default, all institutions are returned.
        :type institutions: Optional[Union[str, List[str]]]
        :param metrics: Comma separated list of metrics. By default all metrics are returned.
        :type metrics: Optional[Union[str, List[str]]]
        :param reviewable: Limit to human-reviewable metrics. By default all metrics are returned.
        :type reviewable: Optional[bool]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]
        :param next_page_token: Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
        :type next_page_token: Optional[str]
        :param format: Format of the response. Supported values are `json`, `json_stream`.
        :type format: Optional[str]

        :return: List of institution metrics.
        :rtype: CatalogV2DataCollection
        """
        params: Dict[str, Any] = {
            "institutions": institutions,
            "metrics": metrics,
            "reviewable": reviewable,
            "page_size": page_size,
            "paging_from": paging_from,
            "next_page_token": next_page_token,
            "format": format,
        }
        return CatalogV2DataCollection(
            self._get_data,
            "/catalog-v2/institution-metrics",
            params,
            metric_type="institution",
            iterable_col="frequencies",
            iterable_key="frequency",
            explode_on="metrics",
            assign_to="metric",
            client=self
        )

    def catalog_full_institution_metrics_v2(
            self,
            institutions: Optional[Union[str, List[str]]] = None,
            metrics: Optional[Union[str, List[str]]] = None,
            reviewable: Optional[bool] = None,
            page_size: Optional[int] = None,
            paging_from: Optional[str] = None,
            next_page_token: Optional[str] = None,
            format: Optional[str] = None,
    ) -> CatalogV2DataCollection:
        """
        :param institutions: Comma separated list of institutions. By default, all institutions are returned.
        :type institutions: Optional[Union[str, List[str]]]
        :param metrics: Comma separated list of metrics. By default all metrics are returned.
        :type metrics: Optional[Union[str, List[str]]]
        :param reviewable: Limit to human-reviewable metrics. By default all metrics are returned.
        :type reviewable: Optional[bool]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]
        :param next_page_token: Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
        :type next_page_token: Optional[str]
        :param format: Format of the response. Supported values are `json`, `json_stream`.
        :type format: Optional[str]

        :return: List of institution metrics.
        :rtype: CatalogV2DataCollection
        """
        params: Dict[str, Any] = {
            "institutions": institutions,
            "metrics": metrics,
            "reviewable": reviewable,
            "page_size": page_size,
            "paging_from": paging_from,
            "next_page_token": next_page_token,
            "format": format,
        }
        return CatalogV2DataCollection(
            self._get_data,
            "/catalog-all-v2/institution-metrics",
            params,
            metric_type="institution",
            iterable_col="frequencies",
            iterable_key="frequency",
            explode_on="metrics",
            assign_to="metric",
            client=self
        )

    def catalog_pair_candles_v2(
            self,
            pairs: Optional[Union[str, List[str]]] = None,
            page_size: Optional[int] = None,
            paging_from: Optional[str] = None,
            next_page_token: Optional[str] = None,
    ) -> CatalogV2DataCollection:
        """
        :param pairs: Comma separated list of asset pairs. By default, all asset pairs are returned.
        :type pairs: Optional[Union[str, List[str]]]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]
        :param next_page_token: Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
        :type next_page_token: Optional[str]

        :return: List of asset pair candles statistics.
        :rtype: CatalogV2DataCollection
        """
        params: Dict[str, Any] = {
            "pairs": pairs,
            "page_size": page_size,
            "paging_from": paging_from,
            "next_page_token": next_page_token,
        }
        return CatalogV2DataCollection(
            self._get_data,
            "/catalog-v2/pair-candles",
            params,
            iterable_col="frequencies",
            iterable_key="frequency",
            client=self
        )

    def catalog_index_candles_v2(
            self,
            indexes: Optional[Union[str, List[str]]] = None,
            page_size: Optional[int] = None,
            paging_from: Optional[str] = None,
            next_page_token: Optional[str] = None,
    ) -> CatalogV2DataCollection:
        """
        :param indexes: Comma separated list of indexes. By default all assets are returned.
        :type indexes: Optional[Union[str, List[str]]]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]
        :param next_page_token: Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
        :type next_page_token: Optional[str]

        :return: List of index candles statistics.
        :rtype: CatalogV2DataCollection
        """
        params: Dict[str, Any] = {
            "indexes": indexes,
            "page_size": page_size,
            "paging_from": paging_from,
            "next_page_token": next_page_token,
        }
        return CatalogV2DataCollection(
            self._get_data,
            "/catalog-v2/index-candles",
            params,
            iterable_col="frequencies",
            iterable_key="frequency",
            client=self
        )

    def catalog_index_levels_v2(
            self,
            indexes: Optional[Union[str, List[str]]] = None,
            page_size: Optional[int] = None,
            paging_from: Optional[str] = None,
            next_page_token: Optional[str] = None,
    ) -> CatalogV2DataCollection:
        """
        :param indexes: Comma separated list of indexes. By default all indexes are returned.
        :type indexes: Optional[Union[str, List[str]]]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]
        :param next_page_token: Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
        :type next_page_token: Optional[str]

        :return: List of index levels.
        :rtype: CatalogV2DataCollection
        """
        params: Dict[str, Any] = {
            "indexes": indexes,
            "page_size": page_size,
            "paging_from": paging_from,
            "next_page_token": next_page_token,
        }
        return CatalogV2DataCollection(
            self._get_data,
            "/catalog-v2/index-levels",
            params,
            iterable_col="frequencies",
            iterable_key="frequency",
            client=self
        )

    def catalog_asset_chains_v2(
            self,
            assets: Optional[Union[str, List[str]]] = None,
            page_size: Optional[int] = None,
            paging_from: Optional[str] = None,
            next_page_token: Optional[str] = None,
    ) -> CatalogV2DataCollection:
        """
        :param assets: Comma separated list of assets. By default all assets are returned.
        :type assets: Optional[Union[str, List[str]]]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]
        :param next_page_token: Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
        :type next_page_token: Optional[str]

        :return: List of asset chains assets
        :rtype: CatalogV2DataCollection
        """
        params: Dict[str, Any] = {
            "assets": assets,
            "page_size": page_size,
            "paging_from": paging_from,
            "next_page_token": next_page_token,
        }
        return CatalogV2DataCollection(self._get_data, "/catalog-v2/asset-chains", params, client=self)

    def catalog_mempool_feerates_v2(
            self,
            assets: Optional[Union[str, List[str]]] = None,
            page_size: Optional[int] = None,
            paging_from: Optional[str] = None,
            next_page_token: Optional[str] = None,
    ) -> CatalogV2DataCollection:
        """
        :param assets: Comma separated list of assets. By default all assets are returned.
        :type assets: Optional[Union[str, List[str]]]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]
        :param next_page_token: Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
        :type next_page_token: Optional[str]

        :return: List of mempool feerates assets
        :rtype: CatalogV2DataCollection
        """
        params: Dict[str, Any] = {
            "assets": assets,
            "page_size": page_size,
            "paging_from": paging_from,
            "next_page_token": next_page_token,
        }
        return CatalogV2DataCollection(self._get_data, "/catalog-v2/mempool-feerates", params, client=self)

    def catalog_mining_pool_tips_summaries_v2(
            self,
            assets: Optional[Union[str, List[str]]] = None,
            page_size: Optional[int] = None,
            paging_from: Optional[str] = None,
            next_page_token: Optional[str] = None,
    ) -> CatalogV2DataCollection:
        """
        :param assets: Comma separated list of assets. By default all assets are returned.
        :type assets: Optional[Union[str, List[str]]]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]
        :param next_page_token: Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
        :type next_page_token: Optional[str]

        :return: List of mining pool tips assets
        :rtype: CatalogV2DataCollection
        """
        params: Dict[str, Any] = {
            "assets": assets,
            "page_size": page_size,
            "paging_from": paging_from,
            "next_page_token": next_page_token,
        }
        return CatalogV2DataCollection(self._get_data, "/catalog-v2/mining-pool-tips-summary", params, client=self)

    def catalog_transaction_tracker_assets_v2(
            self,
            assets: Optional[Union[str, List[str]]] = None,
            page_size: Optional[int] = None,
            paging_from: Optional[str] = None,
            next_page_token: Optional[str] = None,
    ) -> CatalogV2DataCollection:
        """
        :param assets: Comma separated list of assets. By default all assets are returned.
        :type assets: Optional[Union[str, List[str]]]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]
        :param next_page_token: Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
        :type next_page_token: Optional[str]

        :return: List of transaction tracker assets
        :rtype: CatalogV2DataCollection
        """
        params: Dict[str, Any] = {
            "assets": assets,
            "page_size": page_size,
            "paging_from": paging_from,
            "next_page_token": next_page_token,
        }
        return CatalogV2DataCollection(self._get_data, "/catalog-v2/transaction-tracker", params, client=self)

    def catalog_full_pair_candles_v2(
            self,
            pairs: Optional[Union[str, List[str]]] = None,
            page_size: Optional[int] = None,
            paging_from: Optional[str] = None,
            next_page_token: Optional[str] = None,
    ) -> CatalogV2DataCollection:
        """
        :param pairs: Comma separated list of asset pairs. By default, all asset pairs are returned.
        :type pairs: Optional[Union[str, List[str]]]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]
        :param next_page_token: Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
        :type next_page_token: Optional[str]

        :return: List of asset pair candles statistics.
        :rtype: CatalogV2DataCollection
        """
        params: Dict[str, Any] = {
            "pairs": pairs,
            "page_size": page_size,
            "paging_from": paging_from,
            "next_page_token": next_page_token,
        }
        return CatalogV2DataCollection(self._get_data, "/catalog-all-v2/pair-candles", params, client=self)

    def catalog_full_index_candles_v2(
            self,
            indexes: Optional[Union[str, List[str]]] = None,
            page_size: Optional[int] = None,
            paging_from: Optional[str] = None,
            next_page_token: Optional[str] = None,
    ) -> CatalogV2DataCollection:
        """
        :param indexes: Comma separated list of indexes. By default all assets are returned.
        :type indexes: Optional[Union[str, List[str]]]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]
        :param next_page_token: Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
        :type next_page_token: Optional[str]

        :return: List of index candles statistics.
        :rtype: CatalogV2DataCollection
        """
        params: Dict[str, Any] = {
            "indexes": indexes,
            "page_size": page_size,
            "paging_from": paging_from,
            "next_page_token": next_page_token,
        }
        return CatalogV2DataCollection(
            self._get_data,
            "/catalog-all-v2/index-candles",
            params,
            iterable_col="frequencies",
            iterable_key="frequency",
            client=self
        )

    def catalog_full_index_levels_v2(
            self,
            indexes: Optional[Union[str, List[str]]] = None,
            page_size: Optional[int] = None,
            paging_from: Optional[str] = None,
            next_page_token: Optional[str] = None,
    ) -> CatalogV2DataCollection:
        """
        :param indexes: Comma separated list of indexes. By default all indexes are returned.
        :type indexes: Optional[Union[str, List[str]]]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]
        :param next_page_token: Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
        :type next_page_token: Optional[str]

        :return: List of index levels.
        :rtype: CatalogV2DataCollection
        """
        params: Dict[str, Any] = {
            "indexes": indexes,
            "page_size": page_size,
            "paging_from": paging_from,
            "next_page_token": next_page_token,
        }
        return CatalogV2DataCollection(
            self._get_data,
            "/catalog-all-v2/index-levels",
            params,
            client=self
        )

    def catalog_full_asset_chains_v2(
            self,
            assets: Optional[Union[str, List[str]]] = None,
            page_size: Optional[int] = None,
            paging_from: Optional[str] = None,
            next_page_token: Optional[str] = None,
    ) -> CatalogV2DataCollection:
        """
        :param assets: Comma separated list of assets. By default all assets are returned.
        :type assets: Optional[Union[str, List[str]]]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]
        :param next_page_token: Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
        :type next_page_token: Optional[str]

        :return: List of asset chains assets
        :rtype: CatalogV2DataCollection
        """
        params: Dict[str, Any] = {
            "assets": assets,
            "page_size": page_size,
            "paging_from": paging_from,
            "next_page_token": next_page_token,
        }
        return CatalogV2DataCollection(self._get_data, "/catalog-all-v2/asset-chains", params, client=self)

    def catalog_full_mempool_feerates_v2(
            self,
            assets: Optional[Union[str, List[str]]] = None,
            page_size: Optional[int] = None,
            paging_from: Optional[str] = None,
            next_page_token: Optional[str] = None,
    ) -> CatalogV2DataCollection:
        """
        :param assets: Comma separated list of assets. By default all assets are returned.
        :type assets: Optional[Union[str, List[str]]]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]
        :param next_page_token: Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
        :type next_page_token: Optional[str]

        :return: List of mempool feerates assets
        :rtype: CatalogV2DataCollection
        """
        params: Dict[str, Any] = {
            "assets": assets,
            "page_size": page_size,
            "paging_from": paging_from,
            "next_page_token": next_page_token,
        }
        return CatalogV2DataCollection(self._get_data, "/catalog-all-v2/mempool-feerates", params, client=self)

    def catalog_full_mining_pool_tips_summaries_v2(
            self,
            assets: Optional[Union[str, List[str]]] = None,
            page_size: Optional[int] = None,
            paging_from: Optional[str] = None,
            next_page_token: Optional[str] = None,
    ) -> CatalogV2DataCollection:
        """
        :param assets: Comma separated list of assets. By default all assets are returned.
        :type assets: Optional[Union[str, List[str]]]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]
        :param next_page_token: Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
        :type next_page_token: Optional[str]

        :return: List of mining pool tips assets
        :rtype: CatalogV2DataCollection
        """
        params: Dict[str, Any] = {
            "assets": assets,
            "page_size": page_size,
            "paging_from": paging_from,
            "next_page_token": next_page_token,
        }
        return CatalogV2DataCollection(self._get_data, "/catalog-all-v2/mining-pool-tips-summary", params, client=self)

    def catalog_full_transaction_tracker_assets_v2(
            self,
            assets: Optional[Union[str, List[str]]] = None,
            page_size: Optional[int] = None,
            paging_from: Optional[str] = None,
            next_page_token: Optional[str] = None,
    ) -> CatalogV2DataCollection:
        """
        :param assets: Comma separated list of assets. By default all assets are returned.
        :type assets: Optional[Union[str, List[str]]]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]
        :param next_page_token: Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
        :type next_page_token: Optional[str]

        :return: List of transaction tracker assets
        :rtype: CatalogV2DataCollection
        """
        params: Dict[str, Any] = {
            "assets": assets,
            "page_size": page_size,
            "paging_from": paging_from,
            "next_page_token": next_page_token,
        }
        return CatalogV2DataCollection(self._get_data, "/catalog-all-v2/transaction-tracker", params, client=self)

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
        include_heartbeats: Optional[bool] = None
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
        :param start_time: Start time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
        :type end_time: datetime, date, str
        :param start_inclusive: Flag to define if start timestamp must be included in the timeseries if present. True by default.
        :type start_inclusive: bool
        :param end_inclusive: Flag to define if end timestamp must be included in the timeseries if present. True by default.
        :type end_inclusive: bool
        :param timezone: timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.
        :type timezone: str
        :param include_heartbeats:  If set to true, includes information about most recent time asset was successfully evaluated.
        :type include_heartbeats: bool
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
            "include_heartbeats": include_heartbeats
        }
        return DataCollection(self._get_data, "timeseries/asset-alerts", params, client=self)

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
        :param start_time: Start time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
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
        return DataCollection(self._get_data, "timeseries/defi-balance-sheets", params, client=self)

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
    ) -> AssetChainsDataCollection:
        """
        Returns the chains of blocks for the specified assets.

        :param assets: list of asset names, e.g. 'btc'
        :type assets: list(str), str
        :param page_size: number of items returned per page when calling the API. If the request times out, try using a smaller number.
        :type page_size: int
        :param paging_from: Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
        :type paging_from: PagingFrom, str
        :param start_time: Start time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
        :type end_time: datetime, date, str
        :param start_inclusive: Flag to define if start timestamp must be included in the timeseries if present. True by default.
        :type start_inclusive: bool
        :param end_inclusive: Flag to define if end timestamp must be included in the timeseries if present. True by default.
        :type end_inclusive: bool
        :param timezone: timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.
        :type timezone: str
        :return: Asset chains timeseries.
        :rtype: AssetChainsDataCollection
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
        return AssetChainsDataCollection(self._get_data, "timeseries/asset-chains", params, client=self)

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
        ignore_forbidden_errors: Optional[bool] = None,
        ignore_unsupported_errors: Optional[bool] = None,
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
        :param start_time: Start time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
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
        :param ignore_forbidden_errors: Default: false. Ignore HTTP 403 Forbidden errors
        :type ignore_forbidden_errors: bool
        :param ignore_unsupported_errors: Default: false. Ignore errors for unsupported assets, metrics or frequencies.
        :type ignore_unsupported_errors: bool
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
            "ignore_forbidden_errors": ignore_forbidden_errors,
            "ignore_unsupported_errors": ignore_unsupported_errors
        }
        return DataCollection(self._get_data, "timeseries/asset-metrics", params, client=self)

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
        :param start_time: Start time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
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
        return DataCollection(self._get_data, "timeseries/exchange-metrics", params, client=self)

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
        :param start_time: Start time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
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
        :param start_time: Start time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
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
        return DataCollection(self._get_data, "timeseries/pair-metrics", params, client=self)

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
        :param start_time: Start time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
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
        return DataCollection(self._get_data, "timeseries/pair-candles", params, client=self)

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
        :param start_time: Start time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
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
        return DataCollection(self._get_data, "timeseries/institution-metrics", params, client=self)

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
        :param start_time: Start time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
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
        return DataCollection(self._get_data, "timeseries/index-candles", params, client=self)

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
        include_verification: Optional[bool] = None
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
        :param start_time: Start time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
        :type end_time: datetime, date, str
        :param start_inclusive: Flag to define if start timestamp must be included in the timeseries if present. True by default.
        :type start_inclusive: bool
        :param end_inclusive: Flag to define if end timestamp must be included in the timeseries if present. True by default.
        :type end_inclusive: bool
        :param timezone: timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.
        :type timezone: str
        :param limit_per_index: How many entries _per index_ the result should contain.
        :type limit_per_index: int
        :param include_verification: Default: False set to true, includes information about verification.
        :type: bool
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
            "include_verification": include_verification
        }
        return DataCollection(self._get_data, "timeseries/index-levels", params, client=self)

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
        :param start_time: Start time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
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
        return DataCollection(self._get_data, "timeseries/index-constituents", params, client=self)

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
        sort: Optional[str] = None,
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
        :param start_time: Start time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
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
            "sort": sort,
        }
        return DataCollection(self._get_data, "timeseries/market-metrics", params, client=self)

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
        :param start_time: Start time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
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
        return DataCollection(self._get_data, "timeseries/market-candles", params, client=self)

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
        min_confirmations: Optional[int] = None,
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
        :param start_time: Start time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
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
        return DataCollection(self._get_data, "timeseries/market-trades", params, client=self)

    def get_market_open_interest(
        self,
        markets: Union[List[str], str],
        page_size: Optional[int] = None,
        paging_from: Optional[Union[PagingFrom, str]] = "start",
        start_time: Optional[Union[datetime, date, str]] = None,
        end_time: Optional[Union[datetime, date, str]] = None,
        start_inclusive: Optional[bool] = None,
        end_inclusive: Optional[bool] = None,
        granularity: Optional[str] = None,
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
        :param start_time: Start time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
        :type end_time: datetime, date, str
        :param start_inclusive: Flag to define if start timestamp must be included in the timeseries if present. True by default.
        :type start_inclusive: bool
        :param end_inclusive: Flag to define if end timestamp must be included in the timeseries if present. True by default.
        :type end_inclusive: bool
        :param granularity: Downsampling granularity of market open interest. Supported values are raw, 1m, 1h, and 1d.
        :type granularity: str
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
            "granularity": granularity,
            "timezone": timezone,
            "limit_per_market": limit_per_market,
        }
        return DataCollection(self._get_data, "timeseries/market-openinterest", params, client=self)

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
        :param start_time: Start time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
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
        return DataCollection(self._get_data, "timeseries/market-liquidations", params, client=self)

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
        :param start_time: Start time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
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
        return DataCollection(self._get_data, "timeseries/market-funding-rates", params, client=self)

    def get_predicted_market_funding_rates(
        self,
        markets: Union[List[str], str],
        start_time: Optional[Union[datetime, date, str]] = None,
        end_time: Optional[Union[datetime, date, str]] = None,
        start_inclusive: Optional[bool] = None,
        end_inclusive: Optional[bool] = None,
        timezone: Optional[str] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[Union[PagingFrom, str]] = "start",
        limit_per_market: Optional[int] = None,
    ) -> DataCollection:
        """
        Returns predicted funding rates for specified futures markets. Results are ordered by tuple (market, time).
        For more information on funding rates, see: https://docs.coinmetrics.io/info/markets/fundingrates

        :param markets: list of market ids. Market ids use the following naming convention: `exchangeName-baseAsset-quoteAsset-spot` for spot markets, `exchangeName-futuresSymbol-future` for futures markets, and `exchangeName-optionsSymbol-option` for options markets. e.g., `'coinbase-btc-usd-spot'`, `'bitmex-XBTUSD-future'`
        :type markets: list(str), str
        :param page_size: number of items returned per page when calling the API. If the request times out, try using a smaller number.
        :type page_size: int
        :param paging_from: Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
        :type paging_from: PagingFrom, str
        :param start_time: Start time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
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
        return DataCollection(self._get_data, "timeseries/market-funding-rates-predicted", params, client=self)

    def get_market_orderbooks(
        self,
        markets: Union[List[str], str],
        granularity: Optional[str] = None,
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
        :param granularity: Downsampling granularity of market order books and quotes. Supported values are raw, 1m, 1h, and 1d.
        :type granularity: str
        :param page_size: number of items returned per page when calling the API. If the request times out, try using a smaller number.
        :type page_size: int
        :param paging_from: Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
        :type paging_from: PagingFrom, str
        :param start_time: Start time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
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
            "granularity": granularity,
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
        return DataCollection(self._get_data, "timeseries/market-orderbooks", params, client=self)

    def get_market_quotes(
        self,
        markets: Union[List[str], str],
        granularity: Optional[str] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[Union[PagingFrom, str]] = "start",
        start_time: Optional[Union[datetime, date, str]] = None,
        end_time: Optional[Union[datetime, date, str]] = None,
        start_inclusive: Optional[bool] = None,
        end_inclusive: Optional[bool] = None,
        timezone: Optional[str] = None,
        limit_per_market: Optional[int] = None,
        include_one_sided: Optional[bool] = None,
    ) -> DataCollection:
        """
        Returns market quotes for specified markets and date range.
        For more information on quotes, see: https://docs.coinmetrics.io/info/markets/quotes

        :param markets: list of market ids. Market ids use the following naming convention: `exchangeName-baseAsset-quoteAsset-spot` for spot markets, `exchangeName-futuresSymbol-future` for futures markets, and `exchangeName-optionsSymbol-option` for options markets. e.g., `'coinbase-btc-usd-spot'`, `'bitmex-XBTUSD-future'`
        :type markets: list(str), str
        :param granularity: Downsampling granularity of market order books and quotes. Supported values are raw, 1m, 1h, and 1d.
        :type granularity:
        :param page_size: number of items returned per page when calling the API. If the request times out, try using a smaller number.
        :type page_size: int
        :param paging_from: Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
        :type paging_from: PagingFrom, str
        :param start_time: Start time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
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
            "granularity": granularity,
            "page_size": page_size,
            "paging_from": paging_from,
            "start_time": start_time,
            "end_time": end_time,
            "start_inclusive": start_inclusive,
            "end_inclusive": end_inclusive,
            "timezone": timezone,
            "limit_per_market": limit_per_market,
            "include_one_sided": include_one_sided,
        }
        return DataCollection(self._get_data, "timeseries/market-quotes", params, client=self)

    def get_market_contract_prices(
        self,
        markets: Union[List[str], str],
        page_size: Optional[int] = None,
        paging_from: Optional[Union[PagingFrom, str]] = "start",
        start_time: Optional[Union[datetime, date, str]] = None,
        end_time: Optional[Union[datetime, date, str]] = None,
        start_inclusive: Optional[bool] = None,
        end_inclusive: Optional[bool] = None,
        granularity: Optional[str] = None,
        timezone: Optional[str] = None,
        limit_per_market: Optional[int] = None,
        frequency: Optional[str] = None
    ) -> DataCollection:
        """
        Returns contract prices for specified markets. This includes index price and mark price that are used by the exchange for settlement and risk management purposes.

        :param markets: list of market ids. Market ids use the following naming convention: `exchangeName-baseAsset-quoteAsset-spot` for spot markets, `exchangeName-futuresSymbol-future` for futures markets, and `exchangeName-optionsSymbol-option` for options markets. e.g., `'coinbase-btc-usd-spot'`, `'bitmex-XBTUSD-future', 'deribit-ETH-25MAR22-1200-P-option'`
        :type markets: list(str), str
        :param page_size: number of items returned per page when calling the API. If the request times out, try using a smaller number.
        :type page_size: int
        :param paging_from: Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
        :type paging_from: PagingFrom, str
        :param start_time: Start time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
        :type end_time: datetime, date, str
        :param start_inclusive: Flag to define if start timestamp must be included in the timeseries if present. True by default.
        :type start_inclusive: bool
        :param end_inclusive: Flag to define if end timestamp must be included in the timeseries if present. True by default.
        :type end_inclusive: bool
        :param granularity: Downsampling granularity of market contract prices. Supported values are raw, 1m, 1h, and 1d.
        :type granularity: str
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
            "granularity": granularity,
            "timezone": timezone,
            "limit_per_market": limit_per_market,
            "frequency": frequency
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
        granularity: Optional[str] = None,
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
        :param start_time: Start time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
        :type end_time: datetime, date, str
        :param start_inclusive: Flag to define if start timestamp must be included in the timeseries if present. True by default.
        :type start_inclusive: bool
        :param end_inclusive: Flag to define if end timestamp must be included in the timeseries if present. True by default.
        :type end_inclusive: bool
        :param granularity: Downsampling granularity of market implied volatility. Supported values are raw, 1m, 1h, and 1d.
        :type granularity: str - one of raw, 1m, 1h, and 1d
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
            "granularity": granularity,
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
        granularity: Optional[str] = None,
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
        :param start_time: Start time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
        :type end_time: datetime, date, str
        :param start_inclusive: Flag to define if start timestamp must be included in the timeseries if present. True by default.
        :type start_inclusive: bool
        :param end_inclusive: Flag to define if end timestamp must be included in the timeseries if present. True by default.
        :type end_inclusive: bool
        :param granularity: Downsampling granularity of market greeks. Supported values are raw, 1m, 1h, and 1d
        :type granularity: str - one of raw, 1m, 1h, and 1d
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
            "granularity": granularity,
            "timezone": timezone,
            "limit_per_market": limit_per_market,
        }
        return DataCollection(self._get_data, "timeseries/market-greeks", params, client=self)

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
        :param start_time: Start time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
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
        :param start_time: Start time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
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
        return DataCollection(self._get_data, "timeseries/mempool-feerates", params, client=self)

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
        depth_limit: Optional[str] = None,
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
            "depth_limit": depth_limit,
        }
        return self._get_stream_data("timeseries-stream/market-orderbooks", params)

    def get_stream_market_quotes(
        self,
        markets: Union[List[str], str],
        backfill: Union[Backfill, str] = Backfill.LATEST,
        include_one_sided: Optional[bool] = None,
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
            "include_one_sided": include_one_sided,
        }
        return self._get_stream_data("timeseries-stream/market-quotes", params)

    def get_stream_pair_quotes(
        self,
        pairs: Union[str, List[str]],
        aggregation_method: Optional[str] = None,
        backfill: Optional[str] = None,
    ) -> CmStream:
        """
        :param pairs: Comma separated list of asset pairs. Use the /catalog-all/pairs endpoint for the full list of supported asset pairs.
        :type pairs: Optional[Union[str, List[str]]]
        :param aggregation_method: The method to use for aggregation.
        :type aggregation_method: str
        :param backfill: What data should be sent upon a connection. By default the latest values are sent just before real-time data.
        :type backfill: str
        :return:
        :rtype: CmStream
        """
        params: Dict[str, Any] = {
            "pairs": pairs,
            "aggregation_method": aggregation_method,
            "backfill": backfill,
        }
        return self._get_stream_data("timeseries-stream/pair-quotes", params)

    def get_stream_asset_quotes(
        self,
        assets: Union[str, List[str]],
        aggregation_method: Optional[str] = None,
        backfill: Optional[str] = None,
    ) -> CmStream:
        """
        :param assets: Comma separated list of assets. Use the /catalog-all/assets endpoint for the full list of supported assets.
        :type assets: Union[str, List[str]]
        :param aggregation_method: The method to use for aggregation.
        :type aggregation_method: str
        :param backfill: What data should be sent upon a connection. By default the latest values are sent just before real-time data.
        :type backfill: str
        :return:
        :rtype: CmStream
        """
        params: Dict[str, Any] = {
            "assets": assets,
            "aggregation_method": aggregation_method,
            "backfill": backfill,
        }
        return self._get_stream_data("/timeseries-stream/asset-quotes", params)

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
        include_verification: Optional[bool] = None,
        backfill: Union[Backfill, str] = Backfill.LATEST,
    ) -> CmStream:
        """
        Returns timeseries stream of index levels.

        :param indexes: list of indxes or market patterns such as CMBIBTC
        :type indexes: list(str), str
        :param backfill: What data should be sent upon a connection ("latest" or "none"). By default the latest values are sent just before real-time data.
        :type backfill: str
        :param include_verification: Default: False If set to true, includes information about verification.
        :return: Index levels data timeseries stream.
        :rtype: CmStream
        """

        params: Dict[str, Any] = {
            "indexes": indexes,
            "backfill": backfill,
            "include_verification": include_verification
        }
        return self._get_stream_data("timeseries-stream/index-levels", params)

    def get_stream_market_liquidations(
        self,
        markets: Union[str, List[str]],
        backfill: Optional[str] = None,
    ) -> CmStream:
        """
        Returns timeseries stream for market liquidations

        :param markets: Comma separated list of markets or market patterns like `exchange-*` or `exchange-*-spot` or `*USDT-future`. Use the /catalog-all/markets endpoint for the full list of supported markets.
        :type markets: Union[str, List[str]]
        :param backfill: What data should be sent upon a connection. By default the latest values are sent just before real-time data.
        :type backfill: Optional[str]
        :return: Market liquidations timeseries stream
        :rtype: CmStream
        """
        params: Dict[str, Any] = {
            "markets": markets,
            "backfill": backfill,
        }
        return self._get_stream_data("/timeseries-stream/market-liquidations", params)

    def get_stream_market_open_interest(
            self,
            markets: Union[str, List[str]],
            backfill: Optional[str] = None,
    ) -> CmStream:
        """
        :param markets: Comma separated list of markets or market patterns like `exchange-*` or `exchange-*-spot` or `*USDT-future`. Use the /catalog-all/markets endpoint for the full list of supported markets.
        :type markets: Union[str, List[str]]
        :param backfill: What data should be sent upon a connection. By default the latest values are sent just before real-time data.
        :type backfill: Optional[str]
        :return:
        :rtype: CmStream
        """
        params: Dict[str, Any] = {
            "markets": markets,
            "backfill": backfill,
        }
        return self._get_stream_data("/timeseries-stream/market-openinterest", params)

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
        :param start_time: Start time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
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
        return DataCollection(self._get_data, f"blockchain-v2/{asset}/blocks", params, client=self)

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
        :param start_time: Start time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
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
        return DataCollection(self._get_data, f"blockchain-v2/{asset}/accounts", params, client=self)

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
        :param start_time: Start time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
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
        :param start_time: Start time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
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
        :param start_time: Start time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
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

    def get_list_of_balance_updates_for_account_v2(
            self,
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
            next_page_token: Optional[str] = None,
    ) -> DataCollection:
        """
        :param asset: Asset name.
        :type asset: Optional[str]
        :param account: Account id.
        :type account: Optional[str]
        :param txids: Optional comma separated list of transaction identifiers (txid) to filter a response. The list must contain a single element for Community users.
        :type txids: Union[str, List[str]]
        :param block_hashes: Optional comma separated list of block hashes to filter a response. The list must contain a single element for Community users.
        :type block_hashes: Union[str, List[str]]
        :param include_counterparties: Include information about the counterparties balance updates.
        :type include_counterparties: bool
        :param start_time: Start of the time interval. This field refers to the `time` field in the response. Multiple formats of ISO 8601 are supported: `2006-01-20T00:00:00Z`, `2006-01-20T00:00:00.000Z`, `2006-01-20T00:00:00.123456Z`, `2006-01-20T00:00:00.123456789, 2006-01-20, 20060120Z`, `2006-01-20`, `20060120`. Inclusive by default. Mutually exclusive with `start_height`. UTC timezone by default. `Z` suffix is optional and `timezone` parameter has a priority over it. If `start_time` is omitted, response will include time series from the **earliest** time available. This parameter is disabled for Community users.
        :type start_time: str
        :param end_time: End of the time interval. This field refers to the `time` field in the response. Multiple formats of ISO 8601 are supported: `2006-01-20T00:00:00Z`, `2006-01-20T00:00:00.000Z`, `2006-01-20T00:00:00.123456Z`, `2006-01-20T00:00:00.123456789, 2006-01-20, 20060120Z`, `2006-01-20`, `20060120`. Inclusive by default. Mutually exclusive with `end_height`. UTC timezone by default. `Z` suffix is optional and `timezone` parameter has a priority over it. If `end_time` is omitted, response will include time series up to the **latest** time available. This parameter is disabled for Community users.
        :type end_time: str
        :param start_height: The start height indicates the beginning block height for the set of data that are returned. Inclusive by default. Mutually exclusive with `start_time`. This parameter is disabled for Community users.
        :type start_height: int
        :param end_height: The end height indicates the ending block height for the set of data that are returned. Inclusive by default. Mutually exclusive with `end_time`. This parameter is disabled for Community users.
        :type end_height: int
        :param start_chain_sequence_number: Start of the `chain_sequence_number` interval. This parameter is disabled for Community users.
        :type start_chain_sequence_number: int
        :param end_chain_sequence_number: End of the `chain_sequence_number` interval. This parameter is disabled for Community users.
        :type end_chain_sequence_number: int
        :param include_sub_accounts: Boolean indicating if the response should contain sub-accounts. This parameter is disabled for Community users.
        :type include_sub_accounts: bool
        :param chain: Chain type. Supported values are `main` and `all` (includes both main and stale). This parameter is disabled for Community users.
        :type chain: str
        :param start_inclusive: Inclusive or exclusive corresponding `start_*` parameters. This parameter is disabled for Community users.
        :type start_inclusive: bool
        :param end_inclusive: Inclusive or exclusive corresponding `end_*` parameters. This parameter is disabled for Community users.
        :type end_inclusive: bool
        :param timezone: Timezone name for `start_time` and `end_time` timestamps. This parameter does not modify the output times, which are always `UTC`. Format is defined by TZ database.
        :type timezone: str
        :param page_size: Number of items per single page of results. This parameter is disabled for Community users.
        :type page_size: int
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: str
        :param next_page_token: Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
        :type next_page_token: str

        :return: Blockchain balance updates for account.
        :rtype: DataCollection
        """
        params: Dict[str, Any] = {
            "asset": asset,
            "account": account,
            "txids": txids,
            "block_hashes": block_hashes,
            "include_counterparties": include_counterparties,
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
            "page_size": page_size,
            "paging_from": paging_from,
            "next_page_token": next_page_token,
        }
        return DataCollection(self._get_data, f"blockchain-v2/{asset}/accounts/{account}/balance-updates", params, client=self)

    def get_transaction_tracker(
        self,
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
    ) -> TransactionTrackerDataCollection:
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
        :param start_time: Start time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
        :type start_time: datetime, date, str
        :param end_time: End time of the timeseries (string or datetime). Datetime object may be timezone naive or aware. Multiple formats of ISO 8601 are supported: 2006-01-20T00:00:00Z, 2006-01-20T00:00:00.000Z, 2006-01-20T00:00:00.123456Z, 2006-01-20T00:00:00.123456789, 2006-01-20, 20060120
        :type end_time: datetime, date, str
        :param start_inclusive: Flag to define if start timestamp must be included in the timeseries if present. True by default.
        :type start_inclusive: bool
        :param end_inclusive: Flag to define if end timestamp must be included in the timeseries if present. True by default.
        :type end_inclusive: bool
        :param timezone: timezone of the start/end times in db format for example: "America/Chicago". Default value is "UTC". For more details check out API documentation page.
        :type timezone: str
        :return: status updates for the specified or all transactions.
        :rtype: TransactionTrackerDataCollection
        """
        params: Dict[str, Any] = {
            "asset": asset,
            "addresses": addresses,
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
            "unconfirmed_only": unconfirmed_only
        }
        return TransactionTrackerDataCollection(
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
        return DataCollection(self._get_data, "/taxonomy/assets", params, client=self)

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
        return DataCollection(self._get_data, "/taxonomy-metadata/assets", params, client=self)

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
        return DataCollection(self._get_data, "/profile/assets", params, client=self)

    def reference_data_asset_metrics(
            self,
            metrics: Optional[Union[str, List[str]]] = None,
            reviewable: Optional[bool] = None,
            page_size: Optional[int] = None,
            paging_from: Optional[str] = None,
    ) -> DataCollection:
        """
        :param metrics: Comma separated list of metrics. By default all metrics are returned.
        :type metrics: Optional[Union[str, List[str]]]
        :param reviewable: Limit to human-reviewable metrics. By default all metrics are returned.
        :type reviewable: Optional[bool]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]

        :return: List of asset metrics metadata.
        :rtype: DataCollection
        """
        params: Dict[str, Any] = {
            "metrics": metrics,
            "reviewable": reviewable,
            "page_size": page_size,
            "paging_from": paging_from,
        }
        return DataCollection(
            self._get_data,
            "/reference-data/asset-metrics",
            params,
            columns_to_store=[
                'metric', 'full_name', 'description', 'product', 'category',
                'subcategory', 'unit', 'data_type', 'type'
            ]
        )

    def reference_data_markets(
            self,
            markets: Optional[Union[str, List[str]]] = None,
            exchange: Optional[str] = None,
            type: Optional[str] = None,
            base: Optional[str] = None,
            quote: Optional[str] = None,
            asset: Optional[str] = None,
            symbol: Optional[str] = None,
            page_size: Optional[int] = None,
            paging_from: Optional[str] = None,
            next_page_token: Optional[str] = None,
    ) -> DataCollection:
        """
        :param markets: Comma separated list of markets. By default all markets are returned.
        :type markets: Optional[Union[str, List[str]]]
        :param exchange: Unique name of an exchange.
        :type exchange: Optional[str]
        :param type: Type of markets.
        :type type: Optional[str]
        :param base: Base asset of markets.
        :type base: Optional[str]
        :param quote: Quote asset of markets.
        :type quote: Optional[str]
        :param asset: Any asset of markets.
        :type asset: Optional[str]
        :param symbol: Symbol of derivative markets, full instrument name.
        :type symbol: Optional[str]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]
        :param next_page_token: Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
        :type next_page_token: Optional[str]

        :return: List of markets metadata.
        :rtype: DataCollection
        """
        params: Dict[str, Any] = {
            "markets": markets,
            "exchange": exchange,
            "type": type,
            "base": base,
            "quote": quote,
            "asset": asset,
            "symbol": symbol,
            "page_size": page_size,
            "paging_from": paging_from,
            "next_page_token": next_page_token,
        }
        return DataCollection(
            self._get_data,
            "/reference-data/markets",
            params,
            columns_to_store=[
                'market', 'exchange', 'base', 'quote', 'pair', 'symbol', 'type', 'size_asset', 'margin_asset',
                'strike', 'option_contract_type', 'is_european', 'contract_size', 'tick_size', 'multiplier_size',
                'listing', 'expiration', 'settlement_price', 'pool_config_id', 'contract_address', 'fee',
                'price_includes_fee', 'variable_fee', 'base_address', 'quote_address', 'status',
                'order_amount_increment', 'order_amount_min', 'order_amount_max', 'order_price_increment',
                'order_price_min', 'order_price_max', 'order_size_min', 'order_taker_fee', 'order_maker_fee',
                'margin_trading_enabled', 'experimental', 'base_native', 'quote_native']
        )

    def reference_data_exchange_metrics(
            self,
            metrics: Optional[Union[str, List[str]]] = None,
            page_size: Optional[int] = None,
            paging_from: Optional[str] = None,
    ) -> DataCollection:
        """
        :param metrics: Comma separated list of metrics. By default all metrics are returned.
        :type metrics: Optional[Union[str, List[str]]]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]

        :return: List of exchange metrics metadata.
        :rtype: DataCollection
        """
        params: Dict[str, Any] = {
            "metrics": metrics,
            "page_size": page_size,
            "paging_from": paging_from,
        }
        return DataCollection(
            self._get_data,
            "/reference-data/exchange-metrics",
            params,
            columns_to_store=[
                'metric', 'full_name', 'description', 'product', 'category',
                'subcategory', 'unit', 'data_type', 'type'
            ]
        )

    def reference_data_exchange_asset_metrics(
            self,
            metrics: Optional[Union[str, List[str]]] = None,
            page_size: Optional[int] = None,
            paging_from: Optional[str] = None,
    ) -> DataCollection:
        """
        :param metrics: Comma separated list of metrics. By default all metrics are returned.
        :type metrics: Optional[Union[str, List[str]]]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]

        :return: List of exchange asset metrics metadata.
        :rtype: DataCollection
        """
        params: Dict[str, Any] = {
            "metrics": metrics,
            "page_size": page_size,
            "paging_from": paging_from,
        }
        return DataCollection(
            self._get_data,
            "/reference-data/exchange-asset-metrics",
            params,
            columns_to_store=[
                'metric', 'full_name', 'description', 'product', 'category',
                'subcategory', 'unit', 'data_type', 'type'
            ]
        )

    def reference_data_pair_metrics(
            self,
            metrics: Optional[Union[str, List[str]]] = None,
            page_size: Optional[int] = None,
            paging_from: Optional[str] = None,
    ) -> DataCollection:
        """
        :param metrics: Comma separated list of metrics. By default all metrics are returned.
        :type metrics: Optional[Union[str, List[str]]]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]

        :return: List of pair metrics metadata.
        :rtype: DataCollection
        """
        params: Dict[str, Any] = {
            "metrics": metrics,
            "page_size": page_size,
            "paging_from": paging_from,
        }
        return DataCollection(
            self._get_data,
            "/reference-data/pair-metrics",
            params,
            columns_to_store=[
                'metric', 'full_name', 'description', 'product', 'category',
                'subcategory', 'unit', 'data_type', 'type'
            ]
        )

    def reference_data_institution_metrics(
            self,
            metrics: Optional[Union[str, List[str]]] = None,
            page_size: Optional[int] = None,
            paging_from: Optional[str] = None,
    ) -> DataCollection:
        """
        :param metrics: Comma separated list of metrics. By default all metrics are returned.
        :type metrics: Optional[Union[str, List[str]]]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]

        :return: List of institution metrics metadata.
        :rtype: DataCollection
        """
        params: Dict[str, Any] = {
            "metrics": metrics,
            "page_size": page_size,
            "paging_from": paging_from,
        }
        return DataCollection(
            self._get_data,
            "/reference-data/institution-metrics",
            params,
            columns_to_store=[
                'metric', 'full_name', 'description', 'product', 'category',
                'subcategory', 'unit', 'data_type', 'type'
            ]
        )

    def reference_data_assets(
            self,
            assets: Optional[Union[str, List[str]]] = None,
            page_size: Optional[int] = None,
            paging_from: Optional[str] = None,
            next_page_token: Optional[str] = None,
    ) -> DataCollection:
        """
        :param assets: Comma separated list of assets. By default all assets are returned.
        :type assets: Optional[Union[str, List[str]]]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]
        :param next_page_token: Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
        :type next_page_token: Optional[str]

        :return: List of assets metadata.
        :rtype: DataCollection
        """
        params: Dict[str, Any] = {
            "assets": assets,
            "page_size": page_size,
            "paging_from": paging_from,
            "next_page_token": next_page_token,
        }
        return DataCollection(
            self._get_data,
            "/reference-data/assets",
            params,
            columns_to_store=['asset', 'full_name']
        )

    def reference_data_exchanges(
            self,
            exchanges: Optional[Union[str, List[str]]] = None,
            page_size: Optional[int] = None,
            paging_from: Optional[str] = None,
            next_page_token: Optional[str] = None,
    ) -> DataCollection:
        """
        :param exchanges: Comma separated list of exchanges. By default all exchanges are returned.
        :type exchanges: Optional[Union[str, List[str]]]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]
        :param next_page_token: Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
        :type next_page_token: Optional[str]

        :return: List of exchanges metadata.
        :rtype: DataCollection
        """
        params: Dict[str, Any] = {
            "exchanges": exchanges,
            "page_size": page_size,
            "paging_from": paging_from,
            "next_page_token": next_page_token,
        }
        return DataCollection(
            self._get_data,
            "/reference-data/exchanges",
            params,
            columns_to_store=['exchange', 'full_name']
        )

    def reference_data_indexes(
            self,
            indexes: Optional[Union[str, List[str]]] = None,
            page_size: Optional[int] = None,
            paging_from: Optional[str] = None,
            next_page_token: Optional[str] = None,
    ) -> DataCollection:
        """
        :param indexes: Comma separated list of indexes. By default all indexes are returned.
        :type indexes: Optional[Union[str, List[str]]]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]
        :param next_page_token: Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
        :type next_page_token: Optional[str]

        :return: List of indexes metadata.
        :rtype: DataCollection
        """
        params: Dict[str, Any] = {
            "indexes": indexes,
            "page_size": page_size,
            "paging_from": paging_from,
            "next_page_token": next_page_token,
        }
        return DataCollection(
            self._get_data,
            "/reference-data/indexes",
            params,
            columns_to_store=["index", "full_name"]
        )

    def reference_data_pairs(
            self,
            pairs: Optional[Union[str, List[str]]] = None,
            page_size: Optional[int] = None,
            paging_from: Optional[str] = None,
            next_page_token: Optional[str] = None,
    ) -> DataCollection:
        """
        :param pairs: Comma separated list of asset pairs. By default, all asset pairs are returned.
        :type pairs: Optional[Union[str, List[str]]]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]
        :param next_page_token: Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
        :type next_page_token: Optional[str]

        :return: List of pairs metadata.
        :rtype: DataCollection
        """
        params: Dict[str, Any] = {
            "pairs": pairs,
            "page_size": page_size,
            "paging_from": paging_from,
            "next_page_token": next_page_token,
        }
        return DataCollection(
            self._get_data,
            "/reference-data/pairs",
            params,
            columns_to_store=["pair", "full_name"]
        )

    def reference_data_market_metrics(
            self,
            metrics: Optional[Union[str, List[str]]] = None,
            page_size: Optional[int] = None,
            paging_from: Optional[str] = None,
            next_page_token: Optional[str] = None,
    ) -> DataCollection:
        """
        :param metrics: Comma separated list of metrics. By default all metrics are returned.
        :type metrics: Optional[Union[str, List[str]]]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]
        :param next_page_token: Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
        :type next_page_token: Optional[str]

        :return: List of market metrics metadata.
        :rtype: DataCollection
        """
        params: Dict[str, Any] = {
            "metrics": metrics,
            "page_size": page_size,
            "paging_from": paging_from,
            "next_page_token": next_page_token,
        }
        return DataCollection(
            self._get_data,
            "/reference-data/market-metrics",
            params,
            columns_to_store=[
                'metric', 'full_name', 'description', 'product', 'category',
                'subcategory', 'unit', 'data_type', 'type'
            ]
        )

    def security_master_assets(
            self,
            assets: Optional[Union[str, List[str]]] = None,
            codes: Optional[Union[str, List[str]]] = None,
            page_size: Optional[int] = None,
            paging_from: Optional[str] = None,
            next_page_token: Optional[str] = None,
    ) -> DataCollection:
        """
        :param assets: Comma-separated list of assets to query. Mutually exclusive with `codes`.
        :type assets: Optional[Union[str, List[str]]]
        :param codes: Comma-separated list of ten-digit alphanumeric identifying codes. Mutually exclusive with `assets`.
        :type codes: Optional[Union[str, List[str]]]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]
        :param next_page_token: Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
        :type next_page_token: Optional[str]

        :return: List of assets and their metadata in security master
        :rtype: DataCollection
        """
        params: Dict[str, Any] = {
            "assets": assets,
            "codes": codes,
            "page_size": page_size,
            "paging_from": paging_from,
            "next_page_token": next_page_token,
        }
        return DataCollection(
            self._get_data,
            "/security-master/assets",
            params,
            columns_to_store=[
                'asset', 'code', 'description', 'overview', 'website', 'whitepaper',
                'consensus_mechanism', 'decimals', 'creation_date', 'type', 'parent_asset',
                'pricing_asset', 'erc20_token_contract', 'fiat'
            ]
        )

    def security_master_markets(
            self,
            type: Optional[str] = None,
            markets: Optional[Union[str, List[str]]] = None,
            symbol: Optional[str] = None,
            exchange: Optional[str] = None,
            base: Optional[str] = None,
            quote: Optional[str] = None,
            page_size: Optional[int] = None,
            paging_from: Optional[str] = None,
            next_page_token: Optional[str] = None,
    ) -> DataCollection:
        """
        :param type: Type of markets.
        :type type: Optional[str]
        :param markets: List of markets.
        :type markets: Optional[Union[str, List[str]]]
        :param symbol: Symbol of derivative markets, full instrument name.
        :type symbol: Optional[str]
        :param exchange: Unique name of an exchange.
        :type exchange: Optional[str]
        :param base: Base asset of markets.
        :type base: Optional[str]
        :param quote: Quote asset of markets.
        :type quote: Optional[str]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]
        :param next_page_token: Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
        :type next_page_token: Optional[str]

        :return: List of security master entries.
        :rtype: DataCollection
        """
        params: Dict[str, Any] = {
            "type": type,
            "markets": markets,
            "symbol": symbol,
            "exchange": exchange,
            "base": base,
            "quote": quote,
            "page_size": page_size,
            "paging_from": paging_from,
            "next_page_token": next_page_token,
        }
        return DataCollection(
            self._get_data,
            "/security-master/markets",
            params,
            columns_to_store=[
                'market', 'code', 'pair', 'trades_min_time', 'trades_max_time',
                'orderbooks_min_time', 'orderbooks_max_time',
                'quotes_min_time', 'quotes_max_time',
                'funding_rates_min_time', 'funding_rates_max_time',
                'openinterest_min_time', 'openinterest_max_time',
                'liquidations_min_time', 'liquidations_max_time',
                'exchange', 'base', 'quote', 'symbol', 'type',
                'size_asset', 'margin_asset', 'strike', 'option_contract_type',
                'is_european', 'contract_size', 'tick_size', 'multiplier_size',
                'listing', 'expiration', 'settlement_price', 'pool_config_id',
                'contract_address', 'fee', 'price_includes_fee', 'variable_fee',
                'base_address', 'quote_address', 'status', 'order_amount_increment',
                'order_amount_min', 'order_amount_max', 'order_price_increment',
                'order_price_min', 'order_price_max', 'order_size_min',
                'order_taker_fee', 'order_maker_fee', 'margin_trading_enabled',
                'experimental', 'price_open', 'price_close', 'price_high',
                'price_low', 'vwap', 'volume', 'candle_usd_volume', 'candle_trades_count',
                'base_native', 'quote_native'
            ]
        )

    def get_snapshots_of_asset_metric_constituents(
            self,
            metric: str,
            at_time: Optional[str] = None,
            end_time: Optional[Union[datetime, date, str]] = None,
            start_time: Optional[Union[datetime, date, str]] = None,
            next_page_token: Optional[str] = None,
            page_size: Optional[int] = None,
            paging_from: Optional[str] = None) -> DataCollection:
        """
        :param metric: Target metric name.
        :type metric: str
        :param at_time: Returns constituents at a specified date. \
        Value `now` can be specified to get the current constituents. \
        Mutually exclusive with `start_time` and/or `end_time`.

        :type at_time: Optional[str]
        :param end_time: Start of the time interval, inclusive. \
        Multiple formats of ISO 8601 are supported: `2006-01-20T00:00:00Z`, `2006-01-20T00:00:00.000Z`, `2006-01-20T00:00:00.123456Z`, `2006-01-20T00:00:00.123456789, 2006-01-20, 20060120Z`, `2006-01-20`, `20060120`. \
        Mutually exclusive with `at_time`.

        :type end_time: Optional[Union[datetime, date, str]]
        :param start_time: End of the time interval, inclusive. \
        Multiple formats of ISO 8601 are supported: `2006-01-20T00:00:00Z`, `2006-01-20T00:00:00.000Z`, `2006-01-20T00:00:00.123456Z`, `2006-01-20T00:00:00.123456789, 2006-01-20, 20060120Z`, `2006-01-20`, `20060120`. \
        Mutually exclusive with `at_time`.

        :type start_time: Optional[Union[datetime, date, str]]
        :param next_page_token: Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
        :type next_page_token: Optional[str]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]

        :return: Snapshots of asset metric constituents.
        :rtype: DataCollection
        """
        params: Dict[str, Any] = {
            "metric": metric,
            "at_time": at_time,
            "end_time": end_time,
            "start_time": start_time,
            "next_page_token": next_page_token,
            "page_size": page_size,
            "paging_from": paging_from,
        }
        return DataCollection(self._get_data, "/constituent-snapshots/asset-metrics", params, client=self)

    def get_timeframes_of_asset_metric_constituents(
            self,
            metric: str,
            constituents: Optional[Union[str, List[str]]] = None,
            end_time: Optional[Union[datetime, date, str]] = None,
            start_time: Optional[Union[datetime, date, str]] = None,
            next_page_token: Optional[str] = None,
            page_size: Optional[int] = None,
            paging_from: Optional[str] = None) -> DataCollection:
        """
        :param metric: Target metric name.
        :type metric: str
        :param constituents: Comma separated list of constituents. By default all constituents are returned.
        Different asset metrics may have different constituents.
        For example, constituents for `volume_trusted_spot_usd_1d` are exchanges.

        :type constituents: Optional[Union[str, List[str]]]
        :param end_time: Start of the time interval, inclusive. \
        Multiple formats of ISO 8601 are supported: `2006-01-20T00:00:00Z`, `2006-01-20T00:00:00.000Z`, `2006-01-20T00:00:00.123456Z`, `2006-01-20T00:00:00.123456789, 2006-01-20, 20060120Z`, `2006-01-20`, `20060120`. \
        Mutually exclusive with `at_time`.

        :type end_time: Optional[Union[datetime, date, str]]
        :param start_time: End of the time interval, inclusive. \
        Multiple formats of ISO 8601 are supported: `2006-01-20T00:00:00Z`, `2006-01-20T00:00:00.000Z`, `2006-01-20T00:00:00.123456Z`, `2006-01-20T00:00:00.123456789, 2006-01-20, 20060120Z`, `2006-01-20`, `20060120`. \
        Mutually exclusive with `at_time`.

        :type start_time: Optional[Union[datetime, date, str]]
        :param next_page_token: Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
        :type next_page_token: Optional[str]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param paging_from: Where does the first page start, at the start of the interval or at the end.
        :type paging_from: Optional[str]

        :return: List of timeframes.
        :rtype: DataCollection
        """
        params: Dict[str, Any] = {
            "metric": metric,
            "constituents": constituents,
            "end_time": end_time,
            "start_time": start_time,
            "next_page_token": next_page_token,
            "page_size": page_size,
            "paging_from": paging_from,
        }
        return DataCollection(self._get_data, "/constituent-timeframes/asset-metrics", params, client=self)

    def blockchain_metadata_tags(
            self,
            type: Optional[str] = None,
            page_size: Optional[int] = None,
            next_page_token: Optional[str] = None,
    ) -> DataCollection:
        """
        :param type: The type of a tag.
        :type type: Optional[str]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param next_page_token: Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
        :type next_page_token: Optional[str]

        :return: List of tags.
        :rtype: DataCollection
        """
        params: Dict[str, Any] = {
            "type": type,
            "page_size": page_size,
            "next_page_token": next_page_token,
        }
        return DataCollection(self._get_data, "blockchain-metadata/tags", params, client=self)

    def blockchain_metadata_tagged_entities(
            self,
            tags: Optional[Union[str, List[str]]] = None,
            entities: Optional[Union[str, List[str]]] = None,
            locations: Optional[Union[str, List[str]]] = None,
            page_size: Optional[int] = None,
            next_page_token: Optional[str] = None,
    ) -> DataCollection:
        """
        :param tags: Comma separated list of tags. Mutually exclusive with `entities` parameter. Currently a single tag is allowed per each request.
        :type tags: Optional[Union[str, List[str]]]
        :param entities: Comma separated list of entities. Mutually exclusive with `tags` parameter.
        :type entities: Optional[Union[str, List[str]]]
        :param locations: Comma separated list of entity locations (asset representation where the entity has been tagged). Currently a single entity location is allowed per each request.
        :type locations: Optional[Union[str, List[str]]]
        :param page_size: Number of items per single page of results.
        :type page_size: Optional[int]
        :param next_page_token: Token for receiving the results from the next page of a query. Should not be used directly. To iterate through pages just use `next_page_url` response field.
        :type next_page_token: Optional[str]

        :return: List of tagged entities. Ordered by tuple `(entity, tag, location, start_time)` if requested by providing `entities` parameter. Ordered by tuple `(tag, location, entity, started_time)` if requested by providing `tags` parameter.
        :rtype: DataCollection
        """
        params: Dict[str, Any] = {
            "tags": tags,
            "entities": entities,
            "locations": locations,
            "page_size": page_size,
            "next_page_token": next_page_token,
        }
        return DataCollection(self._get_data, "blockchain-metadata/tagged-entities", params, client=self)

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
        response = self._session.get(
            actual_url,
            headers=self._session.headers,
            proxies=self._session.proxies,
            verify=self._session.verify,
        )
        if response.status_code == 429 or response.headers.get("x-ratelimit-remaining", None) == "0":
            logger.info("Sleeping for a rate limit window because 429 (too many requests) error was returned. Please"
                        "see Coin Metrics APIV4 documentation for more information: https://docs.coinmetrics.io/api/v4/#tag/Rate-limits")
            time.sleep(int(response.headers["x-ratelimit-reset"]))
            response = self._send_request(actual_url=actual_url)
        return response
