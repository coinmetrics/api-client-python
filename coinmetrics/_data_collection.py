import pathlib
from copy import deepcopy
from io import StringIO
from logging import getLogger
from typing import Any, Dict, List, Optional, Iterator, cast, Union, AnyStr, IO

from coinmetrics._typing import DATA_RETRIEVAL_FUNC_TYPE, URL_PARAMS_TYPES
from coinmetrics._utils import get_file_path_or_buffer

logger = getLogger('cm_client_data_collection')


class CsvExportError(Exception):
    pass


class DataCollection:
    def __init__(
            self,
            data_retrieval_function: DATA_RETRIEVAL_FUNC_TYPE,
            endpoint: str,
            url_params: Dict[str, URL_PARAMS_TYPES],
            csv_export_supported: bool = True,
    ) -> None:
        self._csv_export_supported = csv_export_supported
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

    def export_to_csv(
            self,
            path_or_bufstr: Union[str, pathlib.Path, IO[AnyStr], None] = None,
            columns_to_store: List[str] = None
    ):
        if not self._csv_export_supported:
            raise CsvExportError('Sorry, csv export is not supported for this data type.')
        if path_or_bufstr is None:
            path_or_bufstr = StringIO()

        path_or_bufstr = get_file_path_or_buffer(path_or_bufstr)

        if hasattr(path_or_bufstr, "write"):
            f = path_or_bufstr
            close = False
        else:
            f = open(path_or_bufstr, 'w')
            close = True
        try:
            first_data_el = None
            if columns_to_store is None:
                try:
                    first_data_el = next(self)
                except StopIteration:
                    logger.info('no data to export')
                    return
                columns_to_store = list(first_data_el.keys())

            f.write(','.join(columns_to_store) + '\n')
            if first_data_el is not None:
                f.write(','.join(first_data_el[column] for column in columns_to_store) + '\n')

            for data_el in self:
                f.write(','.join(data_el[column] for column in columns_to_store) + '\n')
        finally:
            if close:
                f.close()
