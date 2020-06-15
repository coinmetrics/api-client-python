from copy import deepcopy
from typing import Any, Dict, List, Optional, Iterator, cast

from coinmetrics._client_types import DATA_RETRIEVAL_FUNC_TYPE, URL_PARAMS_TYPES


class DataCollection:
    def __init__(
            self,
            data_retrieval_function: DATA_RETRIEVAL_FUNC_TYPE,
            endpoint: str,
            url_params: Dict[str, URL_PARAMS_TYPES]
    ) -> None:
        self._data_retrieval_function = data_retrieval_function
        self._endpoint = endpoint
        self._url_params = url_params
        self._next_page_token: Optional[str] = ''
        self._current_data_iterator: Optional[Iterator[Any]] = None

    def first_page(self) -> List[Dict[str, Any]]:
        return cast(List[Dict[str, Any]], self._data_retrieval_function(self._endpoint, self._url_params)['data'])

    def __next__(self) -> Any:
        try:
            if self._current_data_iterator is not None:
                return next(self._current_data_iterator)
        except StopIteration:
            if self._next_page_token is None:
                raise StopIteration

        url_params = deepcopy(self._url_params)
        if self._next_page_token:
            url_params['next_page_token'] = self._next_page_token
        api_response = self._data_retrieval_function(self._endpoint, url_params)
        self._next_page_token = cast(Optional[str], api_response.get('next_page_token'))
        self._current_data_iterator = iter(api_response['data'])
        return next(self._current_data_iterator)

    def __iter__(self) -> 'DataCollection':
        return self
