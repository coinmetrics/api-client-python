from copy import deepcopy
from gzip import GzipFile
from io import BytesIO
from logging import getLogger
from time import sleep
from typing import Any, Dict, Iterable, Iterator, List, Optional, cast
from dateutil.parser import isoparse

import requests

from coinmetrics._typing import (
    DataRetrievalFuncType,
    DataReturnType,
    FilePathOrBuffer,
    UrlParamTypes,
    DataFrameType,
)
from coinmetrics._utils import get_file_path_or_buffer

try:
    import orjson as json
except ImportError:
    import json  # type: ignore


logger = getLogger("cm_client_data_collection")

try:
    import pandas as pd  # type: ignore
except ImportError:
    pd = None
    logger.info(
        "Pandas export is unavailable. Install pandas to unlock dataframe functions."
    )


class CsvExportError(Exception):
    pass


class DataFetchError(Exception):
    pass


NUMBER_OF_RETRIES = 3


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
            self._fetch_data_with_retries(self._url_params)["data"],
        )

    def to_list(self) -> List[Dict[str, Any]]:
        return [data for data in self]

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

    def _fetch_data_with_retries(
        self, url_params: Dict[str, UrlParamTypes]
    ) -> DataReturnType:
        for i in range(1, NUMBER_OF_RETRIES + 1):
            try:
                return self._data_retrieval_function(self._endpoint, url_params)
            except requests.exceptions.ProxyError as e:
                if i == NUMBER_OF_RETRIES:
                    raise
                logger.warning(
                    "failed to fetch data with error: %s, retrying in 1 second, try (%s/%s)",
                    e,
                    i,
                    NUMBER_OF_RETRIES,
                )
                sleep(1)

        raise DataFetchError("Failed to fetch data")

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
                ",".join(
                    f'"{first_data_el.get(column)}"' or ""
                    for column in columns_to_store
                )
                + "\n"
            ).encode()
        for data_el in self:
            yield (
                ",".join(
                    f'"{data_el.get(column)}"' or "" for column in columns_to_store
                )
                + "\n"
            ).encode()

    def export_to_json(
        self,
        path_or_bufstr: FilePathOrBuffer = None,
        compress: bool = False,
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

    def to_dataframe(
        self,
        header: Optional[List[str]] = None,
        dtype_mapper: Optional[Dict[str, Any]] = None,
        optimize_pandas_types: Optional[bool] = True,
    ) -> DataFrameType:
        """
        Outputs a pandas dataframe.

        :param header: Optional column names for outputted dataframe. List length must match the output.
        :type header: list(str)
        :param dtype_mapper: Dictionary for converting columns to types, where keys are columns and values are types that pandas accepts in an `as_type()` call. This mapping is prioritized over the pandas dtype conversions.
        :type dtype_mapper: dict
        :param optimize_pandas_types: Boolean flag for using pandas typing for dataframes. If True and dtype_mapper is not specified, then the output will result in all columns with string dtype. If True and dtype_mapper is specified, then the output will convert the dataframe columns with the user-specified dtyoes.
        :type optimize_pandas_types: Bool
        :return: Data in a pandas dataframe
        :rtype: DataFrameType
        """
        if pd is None:
            logger.info("Pandas not found; Returning None")
            return None
        else:
            if optimize_pandas_types:
                f = BytesIO()
                self.export_to_csv(f)
                if f.getbuffer().nbytes == 0:
                    logger.warning("Response is empty.")
                    return pd.DataFrame()
                else:
                    f.seek(0)
                    columns = (
                        BytesIO(f.getvalue())
                        .readlines(1)[0]
                        .decode()
                        .strip()
                        .split(",")
                    )
                    datetime_cols = [
                        c for c in columns if c.endswith("_time") or c == "time"
                    ]
                    df = pd.read_csv(
                        f,
                        parse_dates=datetime_cols,
                        dtype=dtype_mapper,
                        date_parser=isoparse,
                    )
                    if dtype_mapper is None:
                        df = df.convert_dtypes()
                    if header is not None:
                        assert len(df.columns) == len(
                            header
                        ), "header length does not match output values"
                        df.columns = header
                    return df
            else:
                if dtype_mapper is None:
                    return pd.DataFrame(self)
                else:
                    return pd.DataFrame(self).astype(dtype=dtype_mapper)
