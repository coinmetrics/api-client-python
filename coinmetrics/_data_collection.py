from __future__ import annotations

import os
import warnings

import requests
import itertools
from dateutil.relativedelta import relativedelta
from copy import deepcopy
from gzip import GzipFile
from io import BytesIO
from logging import getLogger
from time import sleep
from datetime import datetime, timedelta, date, timezone
from typing import Any, Dict, Iterable, Iterator, List, Optional, cast, Type, Callable, Union, Generator, Tuple, TYPE_CHECKING
from dateutil.parser import isoparse
from coinmetrics._typing import (
    DataRetrievalFuncType,
    DataReturnType,
    FilePathOrBuffer,
    UrlParamTypes,
    DataFrameType,
)
from coinmetrics._utils import (
    convert_pandas_dtype_to_polars,
    deprecated_optimize_pandas_types,
    get_file_path_or_buffer,
)
from coinmetrics._models import AssetChainsData, CoinMetricsAPIModel, TransactionTrackerData
from coinmetrics._catalogs import convert_catalog_dtypes, _expand_df
from importlib import import_module
from concurrent.futures import ThreadPoolExecutor, Executor
from tqdm import tqdm
from collections import defaultdict
from coinmetrics._exceptions import CoinMetricsClientNotFoundError
if TYPE_CHECKING:
    from coinmetrics.api_client import CoinMetricsClient
import numpy as np
import polars as pl

orjson_found = True
try:
    json = import_module("orjson")
except ModuleNotFoundError:
    orjson_found = False

if not orjson_found:
    import json

isoparse_typed: Callable[[Union[str, bytes]], datetime] = isoparse


logger = getLogger("cm_client_data_collection")

try:
    import pandas as pd
    from pandas import DateOffset
except ImportError:
    logger.info(
        "Pandas export is unavailable. Install pandas to unlock dataframe functions."
    )
    if TYPE_CHECKING:
        import pandas as pd
        from pandas import DateOffset


class CsvExportError(Exception):
    pass


class DataFetchError(Exception):
    pass


NUMBER_OF_RETRIES = 3


class DataCollection:

    API_RETURN_MODEL: Optional[Type[CoinMetricsAPIModel]] = None

    def __init__(
        self,
        data_retrieval_function: DataRetrievalFuncType,
        endpoint: str,
        url_params: Dict[str, UrlParamTypes],
        csv_export_supported: bool = True,
        columns_to_store: List[str] = [],
        client: Optional[CoinMetricsClient] = None,
        optimize_dtypes: Optional[bool] = True,
        dtype_mapper: Optional[Dict[str, Any]] = None,
        paginated: bool = True
    ) -> None:
        self._csv_export_supported = csv_export_supported
        self._data_retrieval_function = data_retrieval_function
        self._endpoint = endpoint
        self._url_params = url_params
        self._next_page_token: Optional[str] = ""
        self._current_data_iterator: Optional[Iterator[Any]] = None
        self._columns_to_store = columns_to_store
        self._client = client
        self._optimize_dtypes = optimize_dtypes
        self._dtype_mapper = dtype_mapper
        self._paginated = paginated
        if url_params.get("format") == "json_stream":
            self._paginated = False

    def first_page(self) -> List[Dict[str, Any]]:
        return cast(
            List[Dict[str, Any]],
            self._fetch_data_with_retries(self._url_params)["data"],
        )

    def to_list(self) -> List[Dict[str, Any]]:
        return list(self)

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
        if (
            isinstance(api_response, dict)
        ):
            data = api_response.get("data")
            # API responses that are paginated with "data" key
            if "data" in api_response and isinstance(data, list):
                self._next_page_token = cast(Optional[str], api_response.get("next_page_token"))
                self._current_data_iterator = iter(cast(List[Any], data))
            # API responses that return a single object
            else:
                self._next_page_token = None
                self._current_data_iterator = iter([api_response])
        # API responses that are not paginated, such as json_stream
        elif isinstance(api_response, list):
            self._next_page_token = None
            self._current_data_iterator = iter(list(api_response))
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
            if self.API_RETURN_MODEL:
                columns_to_store = self.API_RETURN_MODEL.get_dataframe_cols()
            elif (
                # for timeseries/{*-metrics}
                self._endpoint.split("/")[0] == "timeseries"
                and self._endpoint.split("/")[1].split("-")[-1] == "metrics"
                and self._url_params.get("metrics") is not None
            ):
                entity = ["_".join(self._endpoint.split("/")[1].split("-")[:-1])]
                metrics = self._url_params.get("metrics")
                if isinstance(metrics, str):
                    metrics = metrics.split(",")
                else:
                    metrics = list(metrics)  # type: ignore
                if (
                    any(m.startswith(("Sply", "Flow")) for m in metrics)
                ):
                    metrics_copy = metrics[:]
                    for metric in metrics_copy:
                        if (
                            metric.startswith("Sply")
                            or metric.startswith("Flow")
                            or metric.startswith("TxEx")
                        ):
                            metrics.append(f"{metric}-status-time")
                            metrics.append(f"{metric}-status")
                if self._url_params.get("frequency") == "1b":
                    time = ["time", "block_hash", "parent_block_hash", "height"]
                else:
                    time = ["time"]
                columns_to_store = time + entity + metrics
            elif self._columns_to_store:
                columns_to_store = self._columns_to_store
            else:
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
            dirname = os.path.dirname(path_or_bufstr_obj)  # type: ignore
            if dirname != '':
                if not os.path.exists(path_or_bufstr_obj):  # type: ignore
                    os.makedirs(dirname, exist_ok=True)
                elif not os.path.isdir(dirname):
                    return None
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

    @deprecated_optimize_pandas_types
    def to_dataframe(
        self,
        header: Optional[List[str]] = None,
        dtype_mapper: Optional[Dict[str, Any]] = None,
        optimize_dtypes: Optional[bool] = None,
        dataframe_type: str = "pandas"
    ) -> DataFrameType:
        """
        Outputs a pandas or polars dataframe.

        :param header: Optional column names for outputted dataframe. List length must match the output.
        :type header: list(str)
        :param dtype_mapper: Dictionary for converting columns to types, where keys are columns and values are types that pandas accepts in an `as_type()` call. This mapping is prioritized over the pandas dtype conversions.
        :type dtype_mapper: dict
        :param optimize_dtypes: Boolean flag for using pandas typing for dataframes. If True and dtype_mapper is not specified, then the output will result in all columns with string dtype. If True and dtype_mapper is specified, then the output will convert the dataframe columns with the user-specified dtyoes.
        :type optimize_dtypes: Bool
        :param dataframe_type: Type of dataframe outputted, either "pandas" (default) or "polars".
        :type dataframe_type: str
        :return: Data in a pandas dataframe
        :rtype: DataFrameType
        """
        if optimize_dtypes is None:
            optimize_dtypes = self._optimize_dtypes
        if dtype_mapper is None:
            dtype_mapper = self._dtype_mapper
        if pd is None:
            logger.info("Pandas not found; Returning None")
            return None
        else:
            if optimize_dtypes:
                f = BytesIO()
                self.export_to_csv(f)
                if f.getbuffer().nbytes == 0:
                    return pd.DataFrame()
                else:
                    f.seek(0)
                    # if self.API_RETURN_MODEL:
                    #     columns = self.API_RETURN_MODEL.get_dataframe_cols()
                    # else:
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
                    buffer: BytesIO = f
                    cols: List[str] = datetime_cols
                    dtype_map: Optional[Dict[str, Any]] = dtype_mapper
                    if dataframe_type == 'pandas':
                        df = pd.read_csv(
                            buffer,
                            parse_dates=cols,
                            dtype=dtype_map,
                        )
                        if dtype_mapper is None:
                            df = df.convert_dtypes()
                        if df.dtypes.get("coin_metrics_id") == np.dtype("object"):
                            df["coin_metrics_id"] = df["coin_metrics_id"].astype(np.float128)
                        if header is not None:
                            assert len(df.columns) == len(
                                header
                            ), "header length does not match output values"
                            df.columns = pd.Index(header)
                        return df
                    elif dataframe_type == 'polars':
                        df = pl.read_csv(
                            buffer,
                            try_parse_dates=True,
                            null_values=["None"]
                        )
                        return df
                    else:
                        raise ValueError("Invalid dataframe_type. Choose one of 'polars' or 'pandas'")
            else:
                if dataframe_type == 'pandas':
                    if dtype_mapper is None:
                        return pd.DataFrame(self)
                    else:
                        df = pd.DataFrame(self)
                        dtype_mapper = {key: value for key, value in dtype_mapper.items() if key in df.columns}
                        return df.astype(dtype_mapper)

                elif dataframe_type == 'polars':
                    if dtype_mapper is None:
                        return pl.DataFrame(self)
                    else:
                        df = pl.DataFrame(self)
                        list_casting_expressions = []
                        for col_name in df.columns:
                            if col_name in dtype_mapper:
                                pandas_dtype = dtype_mapper[col_name]
                                polars_dtype = convert_pandas_dtype_to_polars(pandas_dtype)
                                list_casting_expressions.append(pl.col(col_name).cast(polars_dtype, strict=False))
                            else:
                                list_casting_expressions.append(pl.col(col_name))

                        return df.select(list_casting_expressions)

                else:
                    raise ValueError("Invalid dataframe_type. Choose one of 'polars' or 'pandas'")

    def to_lazyframe(self, **kwargs: Any) -> pl.LazyFrame:
        return pl.LazyFrame(self, **kwargs)

    def parallel(
            self,
            parallelize_on: Optional[Union[str, List[str]]] = None,
            executor: Optional[Callable[[Any], Executor]] = None,
            max_workers: Optional[int] = None,
            progress_bar: Optional[bool] = None,
            time_increment: Optional[Union[relativedelta, timedelta, DateOffset]] = None,
            height_increment: Optional[int] = None
    ) -> "ParallelDataCollection":
        """
        This method will convert the DataCollection into a ParallelDataCollection - enabling the ability to split
        one http request into many HTTP requests for faster data export. By default this will be split based on the
        primary query parameter. For example if you query get_asset_metrics(assets=....) it will split into many requests
        based on the assets.
        :param parallelize_on: parameter(s) to parallelize on. Can be any list type parameters
        :type parallelize_on: List[str], str
        :param executor: By defualt the ParallelDataCollection will use a ProcessPoolExecutor, but this can be changed
        :type executor: Executor
        :param max_workers: Specify the number of parallel threads. By default this is 10 and cannot be increased beyond 10
        :type: int
        :param progress_bar: flag to show a progress bar for data export or not, by default is true
        :type progress_bar: bool
        :param time_increment: option to parallelize by a time. Can use timedelta for time periods in weeks and relativedelta for longer time periods like a month or year
        :type time_increment: timedelta, relativedelta
        :param height_increment: Optionally, can split the data collections by height_increment. This feature splits
        data collections further by block height increment. If there is no "start_height" in the request it will raise a ValueError
        :type height_increment: int
        :return: ParallelDataCollection that matches the existing one
        """
        return ParallelDataCollection(self,
                                      parallelize_on=parallelize_on,
                                      executor=executor,
                                      max_workers=max_workers,
                                      progress_bar=progress_bar,
                                      time_increment=time_increment,
                                      height_increment=height_increment
                                      )


class AssetChainsDataCollection(DataCollection):

    API_RETURN_MODEL = AssetChainsData

    @deprecated_optimize_pandas_types
    def to_dataframe(
        self,
        header: Optional[List[str]] = None,
        dtype_mapper: Optional[Dict[str, Any]] = None,
        optimize_dtypes: Optional[bool] = True,
        dataframe_type: str = "pandas"
    ) -> DataFrameType:
        if dataframe_type == "pandas":
            df = super().to_dataframe(
                header=header, dtype_mapper=dtype_mapper, optimize_dtypes=optimize_dtypes, dataframe_type=dataframe_type
            )
            if 'reorg' in df.columns:
                if isinstance(df, pd.DataFrame):
                    df['reorg'] = df['reorg'].astype(str).apply(lambda x: x == 'True').fillna(False)
                elif isinstance(df, pl.DataFrame):
                    df = df.with_columns(
                        pl.col('reorg').cast(pl.Utf8).eq('True').fill_null(False).alias('reorg')
                    )
            return df
        else:
            raise ValueError(f"dataframe_type '{dataframe_type}' not supported for AssetChains")


class TransactionTrackerDataCollection(DataCollection):
    API_RETURN_MODEL = TransactionTrackerData


class ParallelDataCollection(DataCollection):
    """
    This class will be used as an extension of the normal data collection, but all functions will run in parallel,
    utilizing Python's concurrent.futures features. The main purpose of this class is for historical export of
    data.
    """

    TIME = "time"
    _VALID_PARALLELIZATION_PARAMS = {
        'exchanges', 'assets', 'indexes', 'metrics', 'markets', 'institutions',
        'defi_protocols', 'exchange_assets', 'pairs', 'txid', 'accounts',
        'block_hashes', 'heights', 'sub_accounts', 'txids'
    }
    _ENDPOINT_FIRST_PARAM_DICT = {
        'blockchain-metadata/tags': 'type',
        'blockchain-v2/{asset}/accounts': 'asset',
        'blockchain-v2/{asset}/accounts/{account}/balance-updates': 'asset',
        'blockchain-v2/{asset}/balance-updates': 'asset',
        'blockchain-v2/{asset}/blocks': 'asset',
        'blockchain-v2/{asset}/blocks/{block_hash}': 'asset',
        'blockchain-v2/{asset}/blocks/{block_hash}/transactions/{txid}': 'asset',
        'blockchain-v2/{asset}/sub-accounts': 'asset',
        'blockchain-v2/{asset}/transactions': 'asset',
        'blockchain-v2/{asset}/transactions/{txid}': 'asset',
        'blockchain/{asset}/accounts': 'asset',
        'blockchain/{asset}/balance-updates': 'asset',
        'blockchain/{asset}/blocks': 'asset',
        'blockchain/{asset}/blocks/{block_hash}': 'asset',
        'blockchain/{asset}/blocks/{block_hash}/transactions/{txid}': 'asset',
        'blockchain/{asset}/settlement': 'asset',
        'blockchain/{asset}/transaction-tracker': 'asset',
        'blockchain/{asset}/transactions': 'asset',
        'blockchain/{asset}/transactions/{txid}': 'asset',
        'catalog-v2/asset-metrics': 'assets',
        'catalog-v2/exchange-asset-metrics': 'exchange_assets',
        'catalog-v2/exchange-metrics': 'exchanges',
        'catalog-v2/institution-metrics': 'institutions',
        'catalog-v2/market-candles': 'markets',
        'catalog-v2/market-contract-prices': 'markets',
        'catalog-v2/market-funding-rates': 'markets',
        'catalog-v2/market-greeks': 'markets',
        'catalog-v2/market-implied-volatility': 'markets',
        'catalog-v2/market-liquidations': 'markets',
        'catalog-v2/market-metrics': 'markets',
        'catalog-v2/market-openinterest': 'markets',
        'catalog-v2/market-orderbooks': 'markets',
        'catalog-v2/market-quotes': 'markets',
        'catalog-v2/market-trades': 'markets',
        'catalog-v2/index-candles': 'indexes',
        'catalog-v2/index-levels': 'indexes',
        'catalog-v2/pair-metrics': 'pairs',
        'profile/assets': 'assets',
        'taxonomy-metadata/assets': 'version',
        'taxonomy/assets': 'assets',
        'timeseries/asset-alerts': 'assets',
        'timeseries/asset-chains': 'assets',
        'timeseries/asset-metrics': 'assets',
        'timeseries/defi-balance-sheets': 'defi_protocols',
        'timeseries/exchange-asset-metrics': 'exchange_assets',
        'timeseries/exchange-metrics': 'exchanges',
        'timeseries/index-candles': 'indexes',
        'timeseries/index-constituents': 'indexes',
        'timeseries/index-levels': 'indexes',
        'timeseries/institution-metrics': 'institutions',
        'timeseries/market-candles': 'markets',
        'timeseries/market-contract-prices': 'markets',
        'timeseries/market-funding-rates': 'markets',
        'timeseries/market-funding-rates-predicted': 'markets',
        'timeseries/market-greeks': 'markets',
        'timeseries/market-implied-volatility': 'markets',
        'timeseries/market-liquidations': 'markets',
        'timeseries/market-metrics': 'markets',
        'timeseries/market-openinterest': 'markets',
        'timeseries/market-orderbooks': 'markets',
        'timeseries/market-quotes': 'markets',
        'timeseries/market-trades': 'markets',
        'timeseries/mempool-feerates': 'assets',
        'timeseries/mining-pool-tips-summary': 'assets',
        'timeseries/pair-candles': 'pairs',
        'timeseries/pair-metrics': 'pairs',
        'reference-data/markets': "markets",
        'reference-data/asset-metrics': 'metrics',
        'reference-data/exchange-metrics': 'metrics',
        'reference-data/exchange-asset-metrics': 'metrics',
        'reference-data/pair-metrics': 'metrics',
        'reference-data/institution-metrics': 'metrics'}

    def __init__(
        self,
        parent_data_collection: DataCollection,
        parallelize_on: Optional[Union[str, List[str]]] = None,
        executor: Optional[Callable[..., Executor]] = None,
        max_workers: Optional[int] = None,
        progress_bar: Optional[bool] = None,
        time_increment: Optional[Union[relativedelta, timedelta, DateOffset]] = None,
        height_increment: Optional[int] = None
    ):
        """
        :param parallelize_on: What parameter to parallelize on. By default will use the primary query parameter in the
        endpoint the user is calling. For example - if the user is calling `.get_market_candles(assets="...") it will
        split their request into many separate requests, one for each asset
        :param executor: by default this class uses ProcessPoolExecutor for concurrency, this could be swapped out for
        ThreadPoolExecutor or something else custom, based on User needs
        :param max_workers: The default max_workers number is 10 - so up to 10 processes or threads will be running at
        once. Increasing this can make the code run faster, but users may run into issues with resources, or start to hit
        rate limits.
        :param progress_bar: By default this class uses a tqdm progress bar to show the progress of the threads finishing
        so it is clear what is happening during long running intervals. Can be set to false to disable
        :param time_increment: Optionally, can split the data collections by time_increment. This feature splits
        data collections further by time increment. So if you split by MONTH this will split a year long request into
        12 smaller requests. If there is no "start_time" in the request it will raise a ValueError
        :param height_increment: Optionally, can split the data collections by height_increment. This feature splits
        data collections further by block height increment. If there is no "start_height" in the request it will raise a ValueError
        """
        super().__init__(parent_data_collection._data_retrieval_function, parent_data_collection._endpoint,
                         parent_data_collection._url_params, parent_data_collection._csv_export_supported,
                         client=parent_data_collection._client)
        self._parallelize_on = self._get_parallelize_on(parallelize_on)
        self._executor: Callable[..., Executor] = executor or ThreadPoolExecutor
        self._max_workers = max_workers if max_workers else 10
        if self._max_workers > 10:
            warnings.warn("Max workers greater than 10 are not permitted due to rate limits restrictions")
            self._max_workers = 10
        self._progress_bar = progress_bar if progress_bar is not None else True
        self._time_increment = time_increment
        self._height_increment = height_increment
        if self._time_increment is not None and self._height_increment is not None:
            raise ValueError("time_increment and height_increment are mutually exclusive")

        elif (self._time_increment is not None) or (self._height_increment is not None):
            self._url_params.update({"end_inclusive": False})

    def get_parallel_datacollections(self) -> List[DataCollection]:
        """
        This method creates a list of data collections all possible combinations of all the url parameters that are
        parallelized on, as well as all over all date incremnts as specified in time_increment. For example, if a user
        is calls client.get_asset_metrics(assets="btc,eth,algo", ...).parallel.get_parallel_datacollections() this will
        return three data collections split by asset. If they instead called
        client.get_asset_metrics(assets="btc,eth,algo", metrics="volume_reported_spot_usd_1d", "volume_trusted_spot_usd_1d").parallel(paralellize_on=["metrics", "assets"]).get_parallel_datacollections()
        this would instead create 6 data collections combinations. There is also a possible time increment, so if the
        user did client.get_asset_metrics(assets="btc,eth,algo", metrics="volume_reported_spot_usd_1d", "volume_trusted_spot_usd_1d", start_time="2023-01-01", end_time="2023-02-01).parallel(paralellize_on=["metrics", "assets'], time_increment=timedelta(weeks=2)).get_parallel_datacollections()
        it would create 12 data collections total, since it would split it by the 2 week increment as well.
        :return: List[DataCollection] all combinations of DataCollections based on the parallelized parameters and
        time increment.
        """
        query_items = {}
        for param in self._parallelize_on:
            val = self._url_params.get(param)
            if isinstance(val, str):
                val = val.split(",")  # Always convert to a list
            assert isinstance(val, Iterable)
            query_items[param] = val

        combinations = [dict(zip(query_items, vals)) for vals in itertools.product(*query_items.values())]

        data_collections = []
        for combo in combinations:
            new_params = self._url_params.copy()
            new_params.update(combo)
            new_data_collection = DataCollection(
                data_retrieval_function=self._data_retrieval_function,
                endpoint=self._endpoint,
                url_params=new_params,
                csv_export_supported=True
            )
            data_collections.append(new_data_collection)

        data_collections = self._add_time_dimension_to_data_collections(data_collections=data_collections)
        return data_collections

    def _get_asset_end_height(self, asset: str) -> int:
        block_data = None
        if self._client is not None:
            block_data = self._client.get_list_of_blocks_v2(asset=asset, paging_from='end', page_size=1).first_page()
        if block_data:
            end_height = int(block_data[0]['height'])
        else:
            raise Exception(f"End height for asset {asset} not found.")
        return end_height

    def _add_time_dimension_to_data_collections(
            self,
            data_collections: List[DataCollection]
    ) -> List[DataCollection]:
        """
        Helper function to help create all possible combinations of time or height + parallelized parameters. Takes a list of
        of data collections and returns a larger a list of dataframe over the time or height range.
        :param data_collections: List[DataCollection] list of data collections to be expanded
        :return: List[DataCollections] All combinations of the original data collections, over the specified time_increment
        """
        def generate_ranges(
            start: Union[datetime, int],
            end: Union[datetime, int],
            increment: Union[timedelta, relativedelta, DateOffset, int]
        ) -> Generator[Tuple[Union[datetime, int], Union[datetime, int]]]:
            current = start
            if (
                isinstance(current, datetime)
                and isinstance(end, datetime)
                and isinstance(increment, (timedelta, relativedelta, DateOffset))
            ):
                while current < end:
                    next_ = current + increment
                    if next_ > end:
                        next_ = end
                    yield (current, next_)
                    current = next_
            elif (
                isinstance(current, int)
                and isinstance(end, int)
                and isinstance(increment, int)
            ):
                while current < end:
                    next_ = current + increment
                    if next_ > end:
                        next_ = end
                    yield (current, next_)
                    current = next_
            else:
                raise ValueError("Unsupported combination of types for start, end, or increment")

        if not self._time_increment and not self._height_increment:
            return data_collections

        full_data_collections = []
        if self._height_increment and isinstance(self._height_increment, int):
            if self._url_params.get("start_height") and isinstance(self._url_params.get("start_height"), (int, str)):
                start_height = int(self._url_params.get("start_height"))  # type: ignore
            else:
                start_height = 0
            if self._url_params.get("end_height") and isinstance(self._url_params.get("end_height"), (int, str)):
                end_height = int(self._url_params.get("end_height"))  # type: ignore
            else:
                if self._url_params.get("asset"):
                    asset = str(self._url_params.get("asset"))
                else:
                    raise ValueError(
                        """
                        Parameter "asset" not found in request.
                        Note: Parallel height increment only works on a single asset.
                        Consider breaking query into asset-by-asset chunks (e.g. .parallel('assets').parallel(height_increment=height_increment))
                        """
                    )
                if self._client is not None:
                    end_height = self._get_asset_end_height(asset)
                else:
                    raise CoinMetricsClientNotFoundError

            for start, end in generate_ranges(
                start_height,
                end_height,
                increment=self._height_increment
            ):
                for data_collection in data_collections:
                    new_data_collection = deepcopy(data_collection)
                    new_data_collection._url_params.update(
                        {"start_height": start, "end_height": end}
                    )
                    full_data_collections.append(new_data_collection)
        elif self._time_increment and isinstance(self._time_increment, (timedelta, relativedelta, DateOffset)):
            if not self._url_params.get("start_time"):
                raise ValueError("No start_time specified, cannot use time_increment feature")
            else:
                start_time = self.parse_date(
                    cast(datetime, self._url_params.get("start_time"))
                )
                end_time = self.parse_date(
                    cast(datetime, self._url_params.get("end_time"))
                ) if self._url_params.get(
                    "end_time") else datetime.now(timezone.utc).replace(microsecond=0, tzinfo=None)
                for start, end in generate_ranges(
                    start_time,
                    end_time,
                    increment=self._time_increment
                ):
                    for data_collection in data_collections:
                        new_data_collection = deepcopy(data_collection)
                        new_data_collection._url_params.update({"start_time": start, "end_time": end})
                        full_data_collections.append(new_data_collection)
        return full_data_collections

    def to_list(self) -> List[Dict[str, Any]]:
        data_collections = self.get_parallel_datacollections()
        total_tasks = len(data_collections)
        with self._executor(max_workers=self._max_workers) as processor:
            combined_data = processor.map(self._helper_to_list, data_collections)
            if self._progress_bar:
                combined_data = tqdm(combined_data, total=total_tasks, desc="Converting to List")
        combined_list = list(itertools.chain.from_iterable(combined_data))
        return combined_list

    @deprecated_optimize_pandas_types
    def to_dataframe(
        self,
        header: Optional[List[str]] = None,
        dtype_mapper: Optional[Dict[str, Any]] = None,
        optimize_dtypes: Optional[bool] = True,
        dataframe_type: str = "pandas"
    ) -> DataFrameType:

        if dataframe_type == "pandas":
            def group_and_merge(dfs: List[pd.DataFrame]) -> pd.DataFrame:
                """
                This function is a helper to merge the kind of dataframes we are dealing with. All the dataframes with
                common columns are merged first, then they are all merged
                :param dfs: List of dataframes
                :return: DataFrame that combines the full list into one
                """
                grouped_dfs = defaultdict(list)

                for df in dfs:
                    key = tuple(df.columns)
                    grouped_dfs[key].append(df)

                concatenated_dfs = [pd.concat(group, axis=0) for group in grouped_dfs.values()]

                result = concatenated_dfs[0]
                for df in concatenated_dfs[1:]:
                    result = pd.merge(result, df, on=['time', self._get_first_param_from_endpoint().rstrip("s")], how='outer')
                return result

            data_collections = self.get_parallel_datacollections()
            with self._executor(max_workers=self._max_workers) as processor:
                if self._progress_bar:
                    combined_dataframes = list(tqdm(processor.map(ParallelDataCollection._helper_to_dataframe, data_collections), total=len(data_collections), desc="Exporting to dataframe type"))
                else:
                    combined_dataframes = list(processor.map(ParallelDataCollection._helper_to_dataframe, data_collections))

            if len(self._parallelize_on) > 1 or (len(self._parallelize_on) == 1 and self._get_first_param_from_endpoint() != self._parallelize_on[0]):
                combined_df = group_and_merge(combined_dataframes)
            else:
                combined_df = pd.concat(combined_dataframes, axis=0)
            combined_df.reset_index(drop=True, inplace=True)
            return combined_df
        else:
            raise ValueError(f"dataframe_type '{dataframe_type}' not supported for parallelization.")

    def export_to_csv_files(
        self,
        data_directory: Optional[str] = None,
        columns_to_store: Optional[List[str]] = None,
        compress: bool = False,
    ) -> None:
        """
        This function will export the data requested to several csvs, based on the `parallize_on` attribute of the
        parent class, for example:
        client.get_market_trades("coinbase-eth-btc-spot,coinbase-eth-usdc-spot").parallel(["markets"]) will create a
        file each like ./market-trades/coinbase-eth-btc-spot.csv, ./market-trades/coinbase-eth-usdc-spot.csv
        client.get_asset_metrics('btc,eth', 'ReferenceRateUSD', start_time='2024-01-01', limit_per_asset=1).parallel(
        "assets,metrics", time_increment=timedelta(days=1))
        will create a file each like ./asset-metrics/btc/ReferenceRateUSD/start_time=2024-01-01T00-00-00Z.csv,
        ./asset-metrics/eth/ReferenceRateUSD/start_time=2024-01-01T00-00-00Z.csv
        :param data_directory: str path to directory where files should be dropped
        :param columns_to_store: List[str] columns to store
        :param compress: bool whether or not to compress to tar files
        """
        if data_directory is None:
            data_directory = "."
        data_collections = self.get_parallel_datacollections()
        data_directorys = [data_directory] * len(data_collections)
        columns_to_store_args = [columns_to_store] * len(data_collections)
        compress_args = [compress] * len(data_collections)
        total_tasks = len(data_collections)
        with self._executor(max_workers=self._max_workers) as processor:
            if self._progress_bar:
                list(
                    tqdm(
                        processor.map(
                            self._helper_to_csv,
                            data_collections,
                            data_directorys,
                            columns_to_store_args,
                            compress_args
                        ), total=total_tasks,
                        desc="Exporting to CSV"
                    )
                )
            else:
                processor.map(
                    self._helper_to_csv,
                    data_collections,
                    data_directorys,
                    columns_to_store_args,
                    compress_args
                )
        file_directories = '\n'.join(
            sorted(
                list(
                    set(
                        f"{data_directory}/{os.path.dirname(self._get_export_file_name(dc, 'csv'))}/*.csv"
                        for dc in data_collections
                    )
                )
            )
        )
        logger.info(f"Files saved in: \n{file_directories}")

    def export_to_csv(
        self,
        path_or_bufstr: FilePathOrBuffer = None,
        columns_to_store: Optional[List[str]] = None,
        compress: bool = False,
        dataframe_type: str = "pandas"
    ) -> None:
        if dataframe_type == "pandas":
            self.to_dataframe(dataframe_type="pandas").to_csv(path_or_bufstr)
        elif dataframe_type == "polars":
            self.to_dataframe(dataframe_type="polars").write_csv(path_or_bufstr)

    def export_to_json(
        self,
        path_or_bufstr: FilePathOrBuffer = None,
        compress: bool = False,
    ) -> Optional[str]:
        data_collections = self.get_parallel_datacollections()
        compress_args = [compress] * len(data_collections)
        with self._executor(max_workers=self._max_workers) as processor:
            if self._progress_bar:
                json_data = list(
                    tqdm(
                        processor.map(
                            ParallelDataCollection._helper_to_json,
                            data_collections,
                            compress_args
                        ), total=len(data_collections),
                        desc="Exporting to Json"
                    )
                )
            else:
                json_data = list(
                    processor.map(
                        ParallelDataCollection._helper_to_json,
                        data_collections,
                        compress_args
                    )
                )
        if path_or_bufstr:
            with open(path_or_bufstr, 'w') as file:  # type: ignore
                file.writelines(json_data)
                return None
        else:
            return "".join(json_data)

    def export_to_json_files(
            self,
            data_directory: Optional[str] = None,
            compress: bool = False,
    ) -> None:
        """
        This function will export the data requested to several json, based on the `parallelize_on` attribute of the
        parent class, for example:
        client.get_market_trades("coinbase-eth-btc-spot,coinbase-eth-usdc-spot").parallel("markets") will create a
        file each like ./market-trades/coinbase-eth-btc-spot.json, ./market-trades/coinbase-eth-usdc-spot.json
        client.get_asset_metrics('btc,eth', 'ReferenceRateUSD', start_time='2024-01-01', limit_per_asset=1).parallel(
        "assets,metrics", time_increment=timedelta(days=1))
        will create a file each like ./asset-metrics/btc/ReferenceRateUSD/start_time=2024-01-01T00-00-00Z.json,
        ./asset-metrics/eth/ReferenceRateUSD/start_time=2024-01-01T00-00-00Z.json
        :param data_directory: str path to directory where files should be dropped
        :param columns_to_store: List[str] columns to store
        :param compress: bool whether or not to compress to tar files
        """
        if data_directory is None:
            data_directory = "."
        data_collections = self.get_parallel_datacollections()
        data_directorys = [data_directory] * len(data_collections)
        compress_args = [compress] * len(data_collections)
        with self._executor(max_workers=self._max_workers) as processor:
            if self._progress_bar:
                list(
                    tqdm(
                        processor.map(
                            self._helper_to_json_file,
                            data_collections,
                            data_directorys,
                            compress_args
                        ),
                        total=len(data_collections),
                        desc="Exporting to Json Files"
                    )
                )
            else:
                processor.map(
                    self._helper_to_json_file,
                    data_collections,
                    data_directorys,
                    compress_args
                )
        file_directories = '\n'.join(
            sorted(
                list(
                    set(
                        f"{data_directory}/{os.path.dirname(self._get_export_file_name(dc, 'json'))}/*.json"
                        for dc in data_collections
                    )
                )
            )
        )
        logger.info(f"Files saved in {file_directories}")

    def _get_parallelize_on(self, parallelize_on: Optional[Union[List[str], str]]) -> List[str]:
        if parallelize_on is None:
            return [self._get_first_param_from_endpoint()]
        if isinstance(parallelize_on, str):
            self._validate_parallelization_param(parallelize_on)
            return [parallelize_on]
        elif isinstance(parallelize_on, list) and all([isinstance(item, str) for item in parallelize_on]):
            [self._validate_parallelization_param(param) for param in parallelize_on]  # type: ignore
            return parallelize_on
        else:
            raise ValueError(f"Parallelize on must be either either a string or a list of strings, instead: {parallelize_on}")

    def _validate_parallelization_param(self, param: str) -> None:
        if param not in self._VALID_PARALLELIZATION_PARAMS:
            raise ValueError(
                f"Invalid parallelization param: {param}, only these values are supported: {self._VALID_PARALLELIZATION_PARAMS}")
        if param not in self._url_params:
            raise ValueError(
                f"Invalid parallelization param: {param}, parallelization param must be in {self._url_params.keys()}")
        if self._url_params.get(param) is None:
            raise ValueError(
                f"Invalid parallelization param: {param}, parallelization param is None, must be a non default value")
        if not isinstance(self._url_params.get(param), list) and len(self._url_params.get(param).split(",")) < 2:  # type: ignore
            raise ValueError(f"Invalid parallelization param: {param} - values must be a list, instead: {self._url_params.get(param)}")

    def _get_export_file_name(
            self,
            data_collection: DataCollection,
            file_type: str
    ) -> str:
        arg_values = []
        for param in self._parallelize_on:
            values = data_collection._url_params.get(param)
            if values:
                if isinstance(values, str) and len(values.split(",")) > 1:
                    arg_values.extend(values.split(","))
                else:
                    arg_values.append(values)  # type: ignore

        arg_value = "/".join(arg_values)
        friendly_endpoint_name = data_collection._endpoint.split("/")[-1]
        if self._time_increment and data_collection._url_params.get("start_time"):
            start_time = cast(datetime, data_collection._url_params.get("start_time")).strftime("%Y-%m-%dT%H-%M-%SZ")
            file_name = f"{friendly_endpoint_name}/{arg_value}/start_time={start_time}.{file_type}"
        elif self._height_increment and data_collection._url_params.get("start_height"):
            start_height = cast(int, data_collection._url_params.get("start_height"))
            file_name = f"{friendly_endpoint_name}/{arg_value}/start_height={start_height}.{file_type}"
        else:
            file_name = f"{friendly_endpoint_name}/{arg_value}.{file_type}"
        return file_name

    def _helper_to_csv(
            self,
            data_collection: DataCollection,
            data_directory: str,
            *args: Any
    ) -> None:
        file_name = self._get_export_file_name(data_collection, file_type="csv")
        full_file_path = os.path.join(data_directory, file_name)
        data_collection.export_to_csv(full_file_path, *args)

    def _helper_to_json_file(
        self,
        data_collection: DataCollection,
        data_directory: str,
        compress: bool = False
    ) -> Optional[str]:
        file_name = self._get_export_file_name(data_collection, file_type="json")
        full_file_path = os.path.join(data_directory, file_name)
        return data_collection.export_to_json(full_file_path, compress)

    def _get_first_param_from_endpoint(self) -> str:
        try:
            if self._endpoint.startswith("blockchain"):
                blockchain_endpoints_split = list(map(lambda e: e.split("/"), [endpoint for endpoint in self._ENDPOINT_FIRST_PARAM_DICT.keys() if endpoint.startswith("blockchain")]))
                self_endpoint_split = self._endpoint.split("/")
                for blockchain_split in blockchain_endpoints_split:
                    if all([keyword in self_endpoint_split or keyword.startswith("{") for keyword in blockchain_split]):
                        endpoint = "/".join(blockchain_split)
                        return self._ENDPOINT_FIRST_PARAM_DICT[endpoint]
                raise ValueError(f"Endpoint: {self._endpoint} not supported for parallel requests")
            else:
                return self._ENDPOINT_FIRST_PARAM_DICT[self._endpoint]
        except KeyError:
            raise ValueError(f"Endpoint: {self._endpoint} not supported for parallel requests")

    @staticmethod
    def _helper_to_json(data_collection: DataCollection, compress: bool = False) -> Optional[str]:
        data = data_collection.export_to_json(compress=compress)
        return data

    @staticmethod
    def _helper_to_dataframe(data_collection: DataCollection) -> pd.DataFrame:
        return data_collection.to_dataframe()

    @staticmethod
    def _helper_to_list(data_collection: DataCollection) -> List[Dict[str, Any]]:
        return data_collection.to_list()

    @staticmethod
    def parse_date(date_input: Union[datetime, date, str, pd.Timestamp]) -> datetime:
        """
        Parses a datetime object or datetime string into a datetime object. Datetime string must be a valid
        ISO 8601 format. Timezone aware objects are converted to UTC
        :param date_input: Union[datetime, date, str] date to parse into datetime
        :return: datetime
        """
        # pd.Timestamp is a subset of datetime
        if isinstance(date_input, pd.Timestamp):
            date_input = date_input.to_pydatetime()

        if isinstance(date_input, datetime):
            if date_input.tzname() is None:
                return date_input
            else:
                return date_input.astimezone(timezone.utc).replace(tzinfo=None)

        if isinstance(date_input, date):
            return datetime(date_input.year, date_input.month, date_input.day)

        formats = [
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%dT%H%M%S",
            "%Y-%m-%dT%H:%M:%S.%f",
            "%Y-%m-%dT%H%M%S.%f",
            "%Y-%m-%d",
            "%Y%m%d",
        ]
        # -Z => UTC time
        if date_input.endswith('Z'):
            date_input = date_input[:-1]
        for fmt in formats:
            try:
                return datetime.strptime(date_input, fmt)
            except ValueError:
                continue
        raise ValueError(f"Unrecognized date format for string: {date_input}")


class CatalogV2DataCollection(DataCollection):
    """
    This class is used to implement functionality specific to catalog-v2 endpoints.
    """

    def __init__(
        self,
        data_retrieval_function: DataRetrievalFuncType,
        endpoint: str,
        url_params: Dict[str, UrlParamTypes],
        csv_export_supported: bool = True,
        columns_to_store: List[str] = [],
        client: Optional[CoinMetricsClient] = None,
        metric_type: Optional[str] = None,
        iterable_col: Optional[str] = None,
        iterable_key: Optional[str] = None,
        explode_on: Optional[str] = None,
        assign_to: Optional[str] = None,
        nested_catalog_columns: List[str] = ["min_time", "max_time"],
        dataframe_type: str = "pandas"
    ):
        super().__init__(
            data_retrieval_function=data_retrieval_function,
            endpoint=endpoint,
            url_params=url_params,
            csv_export_supported=csv_export_supported,
            columns_to_store=columns_to_store,
            client=client
        )
        # *-metrics data
        self.metric_type = metric_type
        # column where nested catalog fields live e.g. "frequencies"
        self.iterable_col = iterable_col
        # grain for each value in iterable_col e.g. "frequency"
        self.iterable_key = iterable_key
        self.explode_on = explode_on
        self.assign_to = assign_to
        # fields in nested dicts in catalog response
        self.nested_catalog_columns = nested_catalog_columns
        self.dataframe_type = dataframe_type

    @deprecated_optimize_pandas_types
    def to_dataframe(
        self,
        header: Optional[List[str]] = None,
        dtype_mapper: Optional[Dict[str, Any]] = None,
        optimize_dtypes: Optional[bool] = True,
        dataframe_type: str = "pandas"
    ) -> DataFrameType:
        """
        Transforms catalog data in list form into a dataframe
        :return: DataFrame
        """
        if dataframe_type == "pandas":
            df = pd.DataFrame(self)

            # catalog data with no nested data
            if self.iterable_col is None or not isinstance(self.iterable_col, str) or not isinstance(self.iterable_key, str):
                return convert_catalog_dtypes(df)

            # for *-metrics and market-* types, add frequency (depth if orderbook)
            if isinstance(self.iterable_key, str):
                self.nested_catalog_columns = [self.iterable_key] + self.nested_catalog_columns

            def _assign_column(df_: pd.DataFrame, col_name: str, values: Iterable[Any]) -> DataFrameType:
                return df_.assign(**{col_name: values})

            if self.metric_type is not None:
                # for *-metrics datatypes
                mapper = df[self.metric_type].to_dict()

                def _assign_metric(x: pd.DataFrame) -> Any:
                    try:
                        return x[self.assign_to]
                    except TypeError:
                        return None

                df = df.explode(self.explode_on).assign(
                    metrics=lambda x: pd.Series(x[self.explode_on])
                )
                df[self.assign_to] = df[self.explode_on].apply(_assign_metric)
                df_metrics = df.dropna(subset=[self.explode_on]).metrics.apply(
                    pd.Series
                )
                df_metrics[self.metric_type] = df_metrics.index.map(mapper)
                df_metrics = df_metrics.explode(self.iterable_col)

                # expand min/max time, heights, hash
                for column in self.nested_catalog_columns:
                    df_metrics = _assign_column(
                        df_metrics,
                        column,
                        _expand_df(
                            key=column, iterable=df_metrics[self.iterable_col]
                        )
                    )
                df_metrics = df_metrics.drop([self.iterable_col], axis=1)

                df = (
                    df.drop(["metrics"], axis=1).merge(
                        df_metrics, on=["metric", self.metric_type], how="left"
                    ).reset_index(drop=True)
                )
                df = convert_catalog_dtypes(df)
                return df
            else:
                # for market-* data types
                df = df.explode(self.iterable_col)

                # expand metadata (min/max time)
                for column in self.nested_catalog_columns:
                    df = _assign_column(
                        df,
                        column,
                        _expand_df(
                            key=column, iterable=df[self.iterable_col]
                        )
                    )
                df = df.drop([self.iterable_col], axis=1)

                return convert_catalog_dtypes(df)
        elif dataframe_type == "polars":
            df = pl.DataFrame(self)

            # catalog data with no nested data
            if self.iterable_col is None or not isinstance(self.iterable_col, str) or not isinstance(self.iterable_key, str):
                return convert_catalog_dtypes(df)

            # *-metrics
            if self.metric_type is not None:
                df = df.explode('metrics')

                # Get fields from the first struct level
                first_row_dict = df['metrics'][0]
                metrics_fields = first_row_dict.keys()
                df = df.with_columns([
                    pl.col('metrics').struct.field(field).alias(field)
                    for field in metrics_fields
                ])

                # Find any list columns that contain structs and explode them
                for col in df.schema.items():
                    col_name, dtype = col
                    if isinstance(dtype, pl.List):
                        df = df.explode(col_name)
                        # Get fields from first row of the exploded column
                        first_nested_row = df[col_name][0]
                        nested_fields = first_nested_row.keys()
                        df = df.with_columns([
                            pl.col(col_name).struct.field(field).alias(field)
                            for field in nested_fields
                        ])

                # Drop the original nested columns
                df = df.drop(
                    ['metrics'] + [col for col in metrics_fields if isinstance(df.schema[col], (pl.List, pl.Struct))]
                )

            # for *-metrics and market-* types, add frequency (depth if orderbook)
            else:
                df = df.explode(self.iterable_col)

                # Get the struct field names from the first row
                first_row_dict = df[self.iterable_col][0]
                struct_fields = first_row_dict.keys()

                # Create expressions to extract each struct field
                df = df.with_columns([
                    pl.col(self.iterable_col).struct.field(field).alias(field)
                    for field in struct_fields
                ])

                # Drop the original struct column
                df = df.drop(self.iterable_col)

            return convert_catalog_dtypes(df)
        else:
            raise ValueError(f"dataframe_type {dataframe_type} not supported.")
