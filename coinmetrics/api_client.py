import socket
from datetime import date, datetime
from logging import getLogger
from typing import Any, Dict, List, Optional, Union, cast
from urllib.parse import urlencode

import requests
from requests import HTTPError, Response

from coinmetrics._utils import retry, transform_url_params_values_to_str

try:
    import ujson as json
except ImportError:
    # fall back to std json package
    import json  # type: ignore

from coinmetrics._typing import DataReturnType
from coinmetrics.constants import PagingFrom
from coinmetrics._data_collection import DataCollection

logger = getLogger("cm_client")


class CoinMetricsClient:
    def __init__(
        self, api_key: str = "", page_size: int = 1000,
    ):
        self._page_size = page_size
        self._api_key_url_str = "api_key={}".format(api_key) if api_key else ""

        api_path_prefix = ""
        if not api_key:
            api_path_prefix = "community-"
        self._api_base_url = "https://{}api.coinmetrics.io/v4".format(api_path_prefix)

    def catalog_assets(
        self, assets: Optional[Union[List[str], str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Returns meta information about assets.

        :param assets: A single asset or a list of assets to return info for. If no assets provided, all available assets are returned.
        :type assets: list(str), str
        :return: Information that is available for requested assets, like: Full name, metrics and available frequencies, markets, exchanges, etc.
        :rtype: list(dict(str, any))
        """

        return cast(
            List[Dict[str, Any]],
            self._get_data("catalog/assets", {"assets": assets})["data"],
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
        return cast(
            List[Dict[str, Any]],
            self._get_data("catalog/exchanges", {"exchanges": exchanges})["data"],
        )

    def catalog_indexes(
        self, indexes: Optional[Union[List[str], str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Returns meta information about indexes.

        :param indexes: A single index name or a list of indexes to return info for. If no indexes provided, all available indexes are returned.
        :type indexes: list(str), str
        :return: Information that is available for requested indexes, like: Full name, and available frequencies.
        :rtype: list(dict(str, any))
        """
        return cast(
            List[Dict[str, Any]],
            self._get_data("catalog/indexes", {"indexes": indexes})["data"],
        )

    def catalog_markets(
        self,
        exchange: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Returns list of markets that correspond to a filter. If no filter is set, returns all available assets.

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
        Returns list of available metrics along with information for them like
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
        }
        return DataCollection(self._get_data, "timeseries/index-levels", params)

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
    ) -> DataCollection:
        """
        Returns market candles for specified markets, frequency and date range.

        :param markets: list of market names, e.g. 'coinbase-btc-usd-spot'
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
    ) -> DataCollection:
        """
        Returns market trades for specified markets and date range.

        :param markets: list of market names, e.g. 'coinbase-btc-usd-spot'
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
        }
        return DataCollection(self._get_data, "timeseries/market-trades", params)

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
    ) -> DataCollection:
        """
        Returns market quotes for specified markets and date range.

        :param markets: list of market names, e.g. 'coinbase-btc-usd-spot'
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
        }
        return DataCollection(self._get_data, "timeseries/market-quotes", params)

    def get_market_orderbooks(
        self,
        markets: Union[List[str], str],
        page_size: Optional[int] = None,
        paging_from: Optional[Union[PagingFrom, str]] = None,
        start_time: Optional[Union[datetime, date, str]] = None,
        end_time: Optional[Union[datetime, date, str]] = None,
        start_inclusive: Optional[bool] = None,
        end_inclusive: Optional[bool] = None,
        timezone: Optional[str] = None,
    ) -> DataCollection:
        """
        Returns market order books for specified markets and date range.

        :param markets: list of market names, e.g. 'coinbase-btc-usd-spot'
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
            "timezone": timezone,
        }
        return DataCollection(self._get_data, "timeseries/market-orderbooks", params)

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
    ) -> DataCollection:
        """
        Returns asset metrics books for specified assets, metrics, date range and frequency.

        :param assets: list of asset names, e.g. 'btc'
        :type assets: list(str), str
        :param metrics: list of metric names, e.g. 'PriceUSD'
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
        }
        return DataCollection(self._get_data, "timeseries/asset-metrics", params)

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
        Returns asset metrics books for specified assets, metrics, date range and frequency.

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
        :return: Asset Metrics timeseries.
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
                logger.error(
                    "error found for the query: %s, error content: %s", actual_url, data
                )
                resp.raise_for_status()
            return cast(DataReturnType, data)

    @retry((socket.gaierror, HTTPError), retries=5, wait_time_between_retries=5)
    def _send_request(self, actual_url: str) -> Response:
        return requests.get(actual_url)
