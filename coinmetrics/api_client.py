from datetime import datetime, date
from enum import Enum
from logging import getLogger
from typing import Dict, Union, List, Any, Optional
from urllib.parse import urlencode

import requests

from coinmetrics.constants import ApiBranch, PagingFrom, API_BASE
from coinmetrics.data_collection import DataCollection


logger = getLogger()


class CoinMetricsClient:
    def __init__(self, api_key, api_branch=ApiBranch.PRODUCTION, version=4):
        self.api_key = api_key
        self.api_base_url = f'{API_BASE[api_branch]}/v{version}'

    def catalog_markets(self, exchange: str = None, base: str = None, quote: str = None, asset: str = None) -> List[Dict[str, Any]]:
        params = {'exchange': exchange, 'base': base, 'quote': quote, 'asset': asset}
        return self._get_data('catalog/markets', self._transform_url_params_values_to_str(params))['data']

    def catalog_metrics(self, metrics: Union[List[str], str] = None, reviewable: bool = None) -> List[Dict[str, Any]]:
        params = {'metrics': metrics, 'reviewable': reviewable}
        return self._get_data('catalog/metrics', self._transform_url_params_values_to_str(params))['data']

    def get_market_candles(
            self,
            markets: Union[List[str], str],
            frequency: str = None,
            page_size: int = None,
            paging_from: PagingFrom = None,
            start_time: Union[datetime, date, str] = None,
            end_time: Union[datetime, date, str] = None,
    ) -> DataCollection:
        params = {'page_size': page_size, 'frequency': frequency, 'paging_from': paging_from, 'start_time': start_time,
                  'end_time': end_time, 'markets': markets, }
        params = self._transform_url_params_values_to_str(params)
        return DataCollection(self._get_data, 'timeseries/market-candles', params)

    def get_market_trades(
            self,
            markets: Union[List[str], str],
            page_size: int = None,
            paging_from: PagingFrom = None,
            start_time: Union[datetime, date, str] = None,
            end_time: Union[datetime, date, str] = None,
    ) -> DataCollection:
        params = {'page_size': page_size, 'paging_from': paging_from, 'start_time': start_time, 'end_time': end_time,
                  'markets': markets, }
        params = self._transform_url_params_values_to_str(params)
        return DataCollection(self._get_data, 'timeseries/market-trades', params)

    def get_market_books(
            self,
            markets: Union[List[str], str],
            page_size: int = None,
            paging_from: PagingFrom = None,
            start_time: Union[datetime, date, str] = None,
            end_time: Union[datetime, date, str] = None,
    ) -> DataCollection:
        params = {'page_size': page_size, 'paging_from': paging_from, 'start_time': start_time, 'end_time': end_time,
                  'markets': markets, }
        params = self._transform_url_params_values_to_str(params)
        return DataCollection(self._get_data, 'timeseries/market-orderbooks', params)

    def get_asset_metrics(
            self,
            assets: Union[List[str], str],
            metrics: Union[List[str], str],
            frequency: str = None,
            page_size: int = None,
            paging_from: PagingFrom = None,
            start_time: Union[datetime, date, str] = None,
            end_time: Union[datetime, date, str] = None,
    ) -> DataCollection:
        params = {'frequency': frequency, 'page_size': page_size, 'paging_from': paging_from, 'start_time': start_time,
                  'end_time': end_time, 'assets': assets, 'metrics': metrics, }
        params = self._transform_url_params_values_to_str(params)
        return DataCollection(self._get_data, 'timeseries/asset-metrics', params)

    def _get_data(self, url: str, params: Dict[str, str]) -> Dict[Any, Any]:
        if params:
            params_str = f'&{urlencode(params)}'
        else:
            params_str = ''

        actual_url = f'{self.api_base_url}/{url}?api_key={self.api_key}{params_str}'
        resp = requests.get(actual_url)
        try:
            resp.raise_for_status()
            data = resp.json()
            if 'error' in data:
                logger.error('error found for the query: %s, error content: %s', actual_url, data)
            return data
        except Exception:
            logger.info('response: %s', resp.content)
            raise

    def _transform_url_params_values_to_str(self, params: Dict[str, Optional[Any]]) -> Dict[str, str]:
        processed_params = {}
        for param_name, param_value in params.items():
            if param_value is None:
                continue
            if isinstance(param_value, (datetime, date)):
                if param_name.endswith('_time'):
                    processed_params[param_name] = param_value.isoformat()
                else:
                    raise ValueError(f'`{param_name}` doesn\'t support {type(param_value)} objects')
            elif isinstance(param_value, (list, tuple)):
                processed_params[param_name] = self._format_list_args(param_value)
            elif isinstance(param_value, Enum):
                processed_params[param_name] = param_value.value
            elif isinstance(param_value, bool):
                processed_params[param_name] = 'true' if param_value else 'false'
            else:
                processed_params[param_name] = param_value
        return  processed_params

    @staticmethod
    def _format_list_args(url_args: Union[List[str], str]) -> str:
        return ','.join(url_args) if isinstance(url_args, (list, tuple)) else url_args
