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

try:
    import ujson as json
except ImportError:
    # fall back to std json package
    import json  # type: ignore

from coinmetrics._typing import DataReturnType, MessageHandlerType
from coinmetrics.constants import PagingFrom
from coinmetrics._data_collection import DataCollection

logger = getLogger("cm_client")


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
        page_size: int = 1000,
        verify_ssl_certs: bool = True,
    ):
        self._page_size = page_size
        self._api_key_url_str = "api_key={}".format(api_key) if api_key else ""

        self._verify_ssl_certs = verify_ssl_certs

        api_path_prefix = ""
        if not api_key:
            api_path_prefix = "community-"
        self._api_base_url = "https://{}api.coinmetrics.io/v4".format(api_path_prefix)
        self._ws_api_base_url = "wss://{}api.coinmetrics.io/v4".format(api_path_prefix)
        self._http_header = {"Api-Client-Version": version, "Api-Key": api_key}

    def catalog_assets(
        self, assets: Optional[Union[List[str], str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Returns meta information about _available_ assets.

        :param assets: A single asset or a list of assets to return info for. If no assets provided, all available assets are returned.
        :type assets: list(str), str
        :return: Information that is available for requested assets, like: Full name, metrics and available frequencies, markets, exchanges, etc.
        :rtype: list(dict(str, any))
        """
        params: Dict[str, Any] = {"assets": assets}
        return cast(
            List[Dict[str, Any]], self._get_data("catalog/assets", params)["data"]
        )

    def catalog_asset_alerts(
        self,
        assets: Optional[Union[List[str], str]] = None,
        alerts: Optional[Union[List[str], str]] = None,
    ) -> List[Dict[str, Any]]:
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
        return cast(
            List[Dict[str, Any]], self._get_data("catalog/alerts", params)["data"]
        )

    def catalog_asset_pairs(
        self, asset_pairs: Optional[Union[List[str], str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Returns meta information about _available_ asset-asset pairs

        :param asset_pairs: A single asset-asset pair (e.g. "btc-eth") or a list of asset-asset pairs to return info for. If none are provided, all available pairs are returned.
        :type asset_pairs: list(str), str
        :return: Information that is available for requested asset-asset pair like metrics and their respective frequencies and time ranges
        :rtype: list(dict(str, any))
        """
        params: Dict[str, Any] = {"pairs": asset_pairs}
        return cast(
            List[Dict[str, Any]],
            self._get_data("catalog/pairs", params)["data"],
        )

    def catalog_exchanges(
        self, exchanges: Optional[Union[List[str], str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Returns meta information about exchanges.

        :param exchanges: A single exchange name or a list of exchanges to return info for. If no exchanges provided, all available exchanges are returned.
        :type exchanges: list(str), str
        :return: Information that is available for requested exchanges, like: markets, min and max time available.
        :rtype: list(dict(str, any))
        """
        params: Dict[str, Any] = {"exchanges": exchanges}
        return cast(
            List[Dict[str, Any]], self._get_data("catalog/exchanges", params)["data"]
        )

    def catalog_exchange_assets(
        self, exchange_assets: Optional[Union[List[str], str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Returns meta information about _available_ exchange-asset pairs

        :param exchange_assets: A single exchange-asset pair (e.g. "binance-btc") or a list of exchange-asset pairs to return info for. If none are provided, all available pairs are returned.
        :type exchange_assets: list(str), str
        :return: Information that is available for requested exchange-asset pair like metrics and their respective frequencies and time ranges
        :rtype: list(dict(str, any))
        """
        params: Dict[str, Any] = {"exchange_assets": exchange_assets}
        return cast(
            List[Dict[str, Any]],
            self._get_data("catalog/exchange-assets", params)["data"],
        )

    def catalog_indexes(
        self, indexes: Optional[Union[List[str], str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Returns meta information about _available_ indexes.

        :param indexes: A single index name or a list of indexes to return info for. If no indexes provided, all available indexes are returned.
        :type indexes: list(str), str
        :return: Information that is available for requested indexes, like: Full name, and available frequencies.
        :rtype: list(dict(str, any))
        """
        params: Dict[str, Any] = {"indexes": indexes}
        return cast(
            List[Dict[str, Any]],
            self._get_data("catalog/indexes", params)["data"],
        )

    def catalog_institutions(
        self, institutions: Optional[Union[List[str], str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Returns meta information about _available_ institutions

        :param institutions: A single institution (e.g. "grayscale") or a list of institutions to return info for. If none are provided, all available pairs are returned.
        :type institutions: list(str), str
        :return: Information that is available for requested institution like metrics and their respective frequencies and time ranges.
        :rtype: list(dict(str, any))
        """
        params: Dict[str, Any] = {"institutions": institutions}
        return cast(
            List[Dict[str, Any]],
            self._get_data("catalog/institutions", params)["data"],
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
    ) -> List[Dict[str, Any]]:
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
        return cast(
            List[Dict[str, Any]], self._get_data("catalog/markets", params)["data"]
        )

    def catalog_metrics(
        self,
        metrics: Optional[Union[List[str], str]] = None,
        reviewable: Optional[bool] = None,
    ) -> List[Dict[str, Any]]:
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
        return cast(
            List[Dict[str, Any]], self._get_data("catalog/metrics", params)["data"]
        )

    def catalog_full_assets(
        self, assets: Optional[Union[List[str], str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Returns meta information about _supported_ assets.

        :param assets: A single asset or a list of assets to return info for. If no assets provided, all supported assets are returned.
        :type assets: list(str), str
        :return: Information that is supported for requested assets, like: Full name, metrics and supported frequencies, markets, exchanges, etc.
        :rtype: list(dict(str, any))
        """
        params: Dict[str, Any] = {"assets": assets}
        return cast(
            List[Dict[str, Any]], self._get_data("catalog-all/assets", params)["data"]
        )

    def catalog_full_asset_alerts(
        self,
        assets: Optional[Union[List[str], str]] = None,
        alerts: Optional[Union[List[str], str]] = None,
    ) -> List[Dict[str, Any]]:
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
        return cast(
            List[Dict[str, Any]], self._get_data("catalog-all/alerts", params)["data"]
        )

    def catalog_full_asset_pairs(
        self, asset_pairs: Optional[Union[List[str], str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Returns meta information about _supported_ asset-asset pairs

        :param asset_pairs: A single asset-asset pair (e.g. "btc-eth") or a list of asset-asset pairs to return info for. If none are provided, all supported pairs are returned.
        :type asset_pairs: list(str), str
        :return: Information that is supported for requested asset-asset pair like metrics and their respective frequencies and time ranges
        :rtype: list(dict(str, any))
        """
        params: Dict[str, Any] = {"pairs": asset_pairs}
        return cast(
            List[Dict[str, Any]],
            self._get_data("catalog-all/pairs", params)["data"],
        )

    def catalog_full_exchanges(
        self, exchanges: Optional[Union[List[str], str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Returns meta information about exchanges.

        :param exchanges: A single exchange name or a list of exchanges to return info for. If no exchanges provided, all supported exchanges are returned.
        :type exchanges: list(str), str
        :return: Information that is supported for requested exchanges, like: markets, min and max time supported.
        :rtype: list(dict(str, any))
        """
        params: Dict[str, Any] = {"exchanges": exchanges}
        return cast(
            List[Dict[str, Any]],
            self._get_data("catalog-all/exchanges", params)["data"],
        )

    def catalog_full_exchange_assets(
        self, exchange_assets: Optional[Union[List[str], str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Returns meta information about _supported_ exchange-asset pairs

        :param exchange_assets: A single exchange-asset pair (e.g. "binance-btc") or a list of exchange-asset pairs to return info for. If none are provided, all supported pairs are returned.
        :type exchange_assets: list(str), str
        :return: Information that is supported for requested exchange-asset pair like metrics and their respective frequencies and time ranges
        :rtype: list(dict(str, any))
        """
        params: Dict[str, Any] = {"exchange_assets": exchange_assets}
        return cast(
            List[Dict[str, Any]],
            self._get_data("catalog-all/exchange-assets", params)["data"],
        )

    def catalog_full_indexes(
        self, indexes: Optional[Union[List[str], str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Returns meta information about _supported_ indexes.

        :param indexes: A single index name or a list of indexes to return info for. If no indexes provided, all supported indexes are returned.
        :type indexes: list(str), str
        :return: Information that is supported for requested indexes, like: Full name, and supported frequencies.
        :rtype: list(dict(str, any))
        """
        params: Dict[str, Any] = {"indexes": indexes}
        return cast(
            List[Dict[str, Any]],
            self._get_data("catalog-all/indexes", params)["data"],
        )

    def catalog_full_institutions(
        self, institutions: Optional[Union[List[str], str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Returns meta information about _supported_ institutions

        :param institutions: A single institution (e.g. "grayscale") or a list of institutions to return info for. If none are provided, all supported pairs are returned.
        :type institutions: list(str), str
        :return: Information that is supported for requested institution like metrics and their respective frequencies and time ranges.
        :rtype: list(dict(str, any))
        """
        params: Dict[str, Any] = {"institutions": institutions}
        return cast(
            List[Dict[str, Any]],
            self._get_data("catalog-all/institutions", params)["data"],
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
    ) -> List[Dict[str, Any]]:
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
        }
        return cast(
            List[Dict[str, Any]], self._get_data("catalog-all/markets", params)["data"]
        )

    def catalog_full_metrics(
        self,
        metrics: Optional[Union[List[str], str]] = None,
        reviewable: Optional[bool] = None,
    ) -> List[Dict[str, Any]]:
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
        return cast(
            List[Dict[str, Any]], self._get_data("catalog-all/metrics", params)["data"]
        )

    def get_asset_alerts(
        self,
        assets: Union[List[str], str],
        alerts: Union[List[str], str],
        page_size: Optional[int] = None,
        paging_from: Optional[Union[PagingFrom, str]] = None,
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
            "page_size": page_size or self._page_size,
            "paging_from": paging_from,
            "start_time": start_time,
            "end_time": end_time,
            "start_inclusive": start_inclusive,
            "end_inclusive": end_inclusive,
            "timezone": timezone,
        }
        return DataCollection(self._get_data, "timeseries/asset-alerts", params)

    def get_asset_chains(
        self,
        assets: Union[List[str], str],
        page_size: Optional[int] = None,
        paging_from: Optional[Union[PagingFrom, str]] = None,
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
            "page_size": page_size or self._page_size,
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
        paging_from: Optional[Union[PagingFrom, str]] = None,
        start_time: Optional[Union[datetime, date, str]] = None,
        end_time: Optional[Union[datetime, date, str]] = None,
        start_height: Optional[int] = None,
        end_height: Optional[int] = None,
        start_inclusive: Optional[bool] = None,
        end_inclusive: Optional[bool] = None,
        timezone: Optional[str] = None,
        sort: Optional[str] = None,
        limit_per_asset: Optional[int] = None,
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
        :return: Asset Metrics timeseries.
        :rtype: DataCollection
        """

        params: Dict[str, Any] = {
            "assets": assets,
            "metrics": metrics,
            "frequency": frequency,
            "page_size": page_size or self._page_size,
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
        }
        return DataCollection(self._get_data, "timeseries/asset-metrics", params)

    def get_exchange_metrics(
        self,
        exchanges: Union[List[str], str],
        metrics: Union[List[str], str],
        frequency: Optional[str] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[Union[PagingFrom, str]] = None,
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
            "page_size": page_size or self._page_size,
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
        paging_from: Optional[Union[PagingFrom, str]] = None,
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
            "page_size": page_size or self._page_size,
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
        paging_from: Optional[Union[PagingFrom, str]] = None,
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
            "page_size": page_size or self._page_size,
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

    def get_institution_metrics(
        self,
        institutions: Union[List[str], str],
        metrics: Union[List[str], str],
        frequency: Optional[str] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[Union[PagingFrom, str]] = None,
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
            "page_size": page_size or self._page_size,
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

    def get_index_levels(
        self,
        indexes: Union[List[str], str],
        frequency: Optional[str] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[Union[PagingFrom, str]] = None,
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
            "page_size": page_size or self._page_size,
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
        paging_from: Optional[Union[PagingFrom, str]] = None,
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
            "page_size": page_size or self._page_size,
            "paging_from": paging_from,
            "start_time": start_time,
            "end_time": end_time,
            "start_inclusive": start_inclusive,
            "end_inclusive": end_inclusive,
            "timezone": timezone,
        }
        return DataCollection(self._get_data, "timeseries/index-constituents", params)

    def get_market_candles(
        self,
        markets: Union[List[str], str],
        frequency: Optional[str] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[Union[PagingFrom, str]] = None,
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
            "page_size": page_size or self._page_size,
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
        paging_from: Optional[Union[PagingFrom, str]] = None,
        start_time: Optional[Union[datetime, date, str]] = None,
        end_time: Optional[Union[datetime, date, str]] = None,
        start_inclusive: Optional[bool] = None,
        end_inclusive: Optional[bool] = None,
        timezone: Optional[str] = None,
        limit_per_market: Optional[int] = None,
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
        :return: Market Trades timeseries.
        :rtype: DataCollection
        """

        params: Dict[str, Any] = {
            "markets": markets,
            "page_size": page_size or self._page_size,
            "paging_from": paging_from,
            "start_time": start_time,
            "end_time": end_time,
            "start_inclusive": start_inclusive,
            "end_inclusive": end_inclusive,
            "timezone": timezone,
            "limit_per_market": limit_per_market,
        }
        return DataCollection(self._get_data, "timeseries/market-trades", params)

    def get_market_open_interest(
        self,
        markets: Union[List[str], str],
        page_size: Optional[int] = None,
        paging_from: Optional[Union[PagingFrom, str]] = None,
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
            "page_size": page_size or self._page_size,
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
        paging_from: Optional[Union[PagingFrom, str]] = None,
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
            "page_size": page_size or self._page_size,
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
        paging_from: Optional[Union[PagingFrom, str]] = None,
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
            "page_size": page_size or self._page_size,
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
        paging_from: Optional[Union[PagingFrom, str]] = None,
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
            "page_size": page_size or self._page_size,
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
        paging_from: Optional[Union[PagingFrom, str]] = None,
        start_time: Optional[Union[datetime, date, str]] = None,
        end_time: Optional[Union[datetime, date, str]] = None,
        start_inclusive: Optional[bool] = None,
        end_inclusive: Optional[bool] = None,
        timezone: Optional[str] = None,
        limit_per_market: Optional[int] = None,
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
        :return: Market Quotes timeseries.
        :rtype: DataCollection
        """

        params: Dict[str, Any] = {
            "markets": markets,
            "page_size": page_size or self._page_size,
            "paging_from": paging_from,
            "start_time": start_time,
            "end_time": end_time,
            "start_inclusive": start_inclusive,
            "end_inclusive": end_inclusive,
            "timezone": timezone,
            "limit_per_market": limit_per_market,
        }
        return DataCollection(self._get_data, "timeseries/market-quotes", params)

    def get_market_contract_prices(
        self,
        markets: Union[List[str], str],
        page_size: Optional[int] = None,
        paging_from: Optional[Union[PagingFrom, str]] = None,
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
            "page_size": page_size or self._page_size,
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
        paging_from: Optional[Union[PagingFrom, str]] = None,
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
            "page_size": page_size or self._page_size,
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
        paging_from: Optional[Union[PagingFrom, str]] = None,
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
            "page_size": page_size or self._page_size,
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
        paging_from: Optional[Union[PagingFrom, str]] = None,
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
            "page_size": page_size or self._page_size,
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
        paging_from: Optional[Union[PagingFrom, str]] = None,
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
            "page_size": page_size or self._page_size,
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
        backfill: Optional[str] = None,
    ) -> CmStream:
        """
        Returns timeseries stream of metrics for specified assets.

        :param assets: list of asset names, e.g. 'btc'
        :type assets: list(str), str
        :param metrics: list of _asset-specific_ metric names, e.g. 'PriceUSD'
        :type metrics: list(str), str
        :param frequency: frequency of the returned timeseries, e.g 15s, 1d, etc.
        :type frequency: str
        :param backfill: What data should be sent upon a connection. By default the latest values are sent just before real-time data.
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
        backfill: Union[List[str], str],
    ) -> CmStream:
        """
        Returns timeseries stream of market trades.

        :param markets: list of markets or market patterns like exchange-* or exchange-*-spot or *USDT-future.
        :type markets: list(str), str
        :param backfill: What data should be sent upon a connection. By default the latest values are sent just before real-time data.
        :type backfill: str
        :return: Market Trades timeseries stream.
        :rtype: CmStream
        """

        params: Dict[str, Any] = {"markets": markets, "backfill": backfill}
        return self._get_stream_data("timeseries-stream/market-trades", params)

    def get_stream_market_orderbooks(
        self,
        markets: Union[List[str], str],
        backfill: Union[List[str], str],
    ) -> CmStream:
        """
        Returns timeseries stream of market orderbooks.

        :param markets: list of markets or market patterns like exchange-* or exchange-*-spot or *USDT-future.
        :type markets: list(str), str
        :param backfill: What data should be sent upon a connection. By default the latest values are sent just before real-time data.
        :type backfill: str
        :return: Market Orderbooks timeseries stream.
        :rtype: CmStream
        """

        params: Dict[str, Any] = {"markets": markets, "backfill": backfill}
        return self._get_stream_data("timeseries-stream/market-orderbooks", params)

    def get_stream_market_quotes(
        self,
        markets: Union[List[str], str],
        backfill: Union[List[str], str],
    ) -> CmStream:
        """
        Returns timeseries stream of market quotes.

        :param markets: list of markets or market patterns like exchange-* or exchange-*-spot or *USDT-future.
        :type markets: list(str), str
        :param backfill: What data should be sent upon a connection. By default the latest values are sent just before real-time data.
        :type backfill: str
        :return: Market Quotes timeseries stream.
        :rtype: CmStream
        """

        params: Dict[str, Any] = {"markets": markets, "backfill": backfill}
        return self._get_stream_data("timeseries-stream/market-quotes", params)

    def get_list_of_blocks(
        self,
        asset: str,
        block_hashes: Optional[Union[List[str], str]] = None,
        heights: Optional[Union[List[str], str]] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[Union[PagingFrom, str]] = None,
        start_time: Optional[Union[datetime, date, str]] = None,
        end_time: Optional[Union[datetime, date, str]] = None,
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
            "page_size": page_size or self._page_size,
            "paging_from": paging_from,
            "start_time": start_time,
            "end_time": end_time,
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
        paging_from: Optional[Union[PagingFrom, str]] = None,
        start_time: Optional[Union[datetime, date, str]] = None,
        end_time: Optional[Union[datetime, date, str]] = None,
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
            "page_size": page_size or self._page_size,
            "paging_from": paging_from,
            "start_time": start_time,
            "end_time": end_time,
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
        paging_from: Optional[Union[PagingFrom, str]] = None,
        start_time: Optional[Union[datetime, date, str]] = None,
        end_time: Optional[Union[datetime, date, str]] = None,
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
            "page_size": page_size or self._page_size,
            "paging_from": paging_from,
            "start_time": start_time,
            "end_time": end_time,
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
        paging_from: Optional[Union[PagingFrom, str]] = None,
        start_time: Optional[Union[datetime, date, str]] = None,
        end_time: Optional[Union[datetime, date, str]] = None,
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
            "page_size": page_size or self._page_size,
            "paging_from": paging_from,
            "start_time": start_time,
            "end_time": end_time,
            "start_inclusive": start_inclusive,
            "end_inclusive": end_inclusive,
            "timezone": timezone,
        }
        return DataCollection(
            self._get_data, f"blockchain/{asset}/balance-updates", params
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

    def get_transaction_tracker(
        self,
        asset: str,
        txids: Optional[Union[List[str], str]] = None,
        replacements_for_txids: Optional[Union[List[str], str]] = None,
        replacements_only: Optional[bool] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[Union[PagingFrom, str]] = None,
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
            "page_size": page_size or self._page_size,
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
        resp = self._send_request(actual_url)
        try:
            data = json.loads(resp.content)
        except ValueError:
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
        return requests.get(
            actual_url, verify=self._verify_ssl_certs, headers=self._http_header
        )
