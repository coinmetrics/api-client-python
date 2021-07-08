from copy import deepcopy
from gzip import GzipFile
from io import BytesIO
from logging import getLogger
from typing import Any, Dict, Iterable, Iterator, List, Optional, cast

from coinmetrics._typing import DataRetrievalFuncType, FilePathOrBuffer, UrlParamTypes
from coinmetrics._utils import get_file_path_or_buffer

try:
    import orjson as json
except ImportError:
    import json  # type: ignore


logger = getLogger("cm_client_data_collection")


class CsvExportError(Exception):
    pass


class DataCollection:
    def __init__(
        self,
        data_retrieval_function: DataRetrievalFuncType,
        endpoint: str,
        url_params: Dict[str, UrlParamTypes],
        csv_export_supported: bool = True,
    ) -> None:
        self._csv_export_supported = csv_export_supported
        self._data_retrieval_function = data_retrieval_function
        self._endpoint = endpoint
        self._url_params = url_params
        self._next_page_token: Optional[str] = ""
        self._current_data_iterator: Optional[Iterator[Any]] = None

    def first_page(self) -> List[Dict[str, Any]]:
        return cast(
            List[Dict[str, Any]],
            self._data_retrieval_function(self._endpoint, self._url_params)["data"],
        )

    def __next__(self) -> Any:
        try:
            if self._current_data_iterator is not None:
                return next(self._current_data_iterator)
        except StopIteration:
            if self._next_page_token is None:
                raise StopIteration

        url_params = deepcopy(self._url_params)
        if self._next_page_token:
            url_params["next_page_token"] = self._next_page_token
        api_response = self._data_retrieval_function(self._endpoint, url_params)
        self._next_page_token = cast(Optional[str], api_response.get("next_page_token"))
        self._current_data_iterator = iter(api_response["data"])
        return next(self._current_data_iterator)

    def __iter__(self) -> "DataCollection":
        return self

    def export_to_csv(
        self,
        path_or_bufstr: FilePathOrBuffer = None,
        columns_to_store: Optional[List[str]] = None,
        compress: bool = False,
    ) -> Optional[str]:
        if not self._csv_export_supported:
            raise CsvExportError(
                "Sorry, csv export is not supported for this data type."
            )

        return self._export_to_file(
            self._get_csv_data_lines(columns_to_store), path_or_bufstr, compress
        )

    def _get_csv_data_lines(
        self, columns_to_store: Optional[List[str]]
    ) -> Iterable[bytes]:
        first_data_el = None
        if columns_to_store is None:
            try:
                first_data_el = next(self)
            except StopIteration:
                logger.info("no data to export")
                return
            columns_to_store = list(first_data_el.keys())

        yield (",".join(columns_to_store) + "\n").encode()

        if first_data_el is not None:
            yield (
                ",".join(first_data_el.get(column) or "" for column in columns_to_store)
                + "\n"
            ).encode()
        for data_el in self:
            yield (
                ",".join(data_el.get(column) or "" for column in columns_to_store)
                + "\n"
            ).encode()

    def export_to_json(
        self, path_or_bufstr: FilePathOrBuffer = None, compress: bool = False,
    ) -> Optional[str]:
        def _gen_json_lines() -> Iterable[bytes]:
            for data_row in self:
                yield json.dumps(data_row) + b"\n"

        return self._export_to_file(_gen_json_lines(), path_or_bufstr, compress)

    def _export_to_file(
        self,
        data_generator: Iterable[bytes],
        path_or_bufstr: FilePathOrBuffer = None,
        compress: bool = False,
    ) -> Optional[str]:

        if path_or_bufstr is None:
            path_or_bufstr_obj: FilePathOrBuffer = BytesIO()
        else:
            path_or_bufstr_obj = path_or_bufstr

        path_or_bufstr_obj = get_file_path_or_buffer(path_or_bufstr_obj)
        if hasattr(path_or_bufstr_obj, "write"):
            f = path_or_bufstr_obj
            close = False
        else:
            f = open(path_or_bufstr_obj, "wb")  # type: ignore
            close = True
        if compress:
            output_file = GzipFile(fileobj=f)  # type: ignore
        else:
            output_file = f  # type: ignore
        try:
            for line in data_generator:
                output_file.write(line)
        finally:
            if compress:
                output_file.close()
            if close:
                f.close()  # type: ignore

        if path_or_bufstr is None:
            return path_or_bufstr_obj.getvalue().decode()  # type: ignore

        return None
