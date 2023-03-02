import csv
import logging
import orjson
import requests
import socket
import os
import zlib
import sys
from requests import Response, HTTPError
from requests.auth import HTTPBasicAuth

from coinmetrics._exceptions import CoinMetricsUnauthorizedException
from coinmetrics._utils import retry
from datetime import datetime
from typing import Union, Optional, List, Dict, Any, Iterable
from concurrent.futures import ThreadPoolExecutor

DEFAULT_OUTPUT_FORMAT = "json.gz"
Log_Format = "%(levelname)s %(asctime)s - %(message)s"

logging.basicConfig(
    stream=sys.stdout, filemode="w", format=Log_Format, level=logging.INFO
)

logger = logging.getLogger()


class CoinMetricsDataExporter:
    """
    Class to facilitate exporting flat files for coinmetrics market data to various data formats
    """

    _API_BASE_URL = "https://files.coinmetrics.io/api/"
    _SUPPORTED_FREQUENCIES = ["1m", "5m", "10m", "15m", "30m", "1h", "1d"]

    def __init__(
        self,
        api_key: str = "",
        verify_ssl_certs: Union[bool, str] = True,
        proxy_url: Optional[str] = None,
        session: Optional[requests.Session] = None,
    ):
        self._api_key = api_key
        self._verify_ssl_certs = verify_ssl_certs
        self._proxy_url = proxy_url
        self._auth = HTTPBasicAuth(self._api_key, "")
        self.proxies = {"http": proxy_url, "https": proxy_url}
        if session is None:
            self._session = requests.Session()
            self._session.verify = self._verify_ssl_certs
            self._session.proxies.update({"http": proxy_url, "https": proxy_url})  # type: ignore
        else:
            self._session = session

    def export_market_candles_future_data(
        self,
        frequency: str,
        start_date: datetime,
        end_date: datetime,
        exchanges: Union[str, List[str]],
        output_format: str = DEFAULT_OUTPUT_FORMAT,
        threaded: bool = False,
    ) -> None:
        if frequency not in self._SUPPORTED_FREQUENCIES:
            raise ValueError(
                f"This frequency is not supported for market-candles-futures,"
                f" supported frequencies: {self._SUPPORTED_FREQUENCIES}"
            )
        candles_future_route = f"market-candles-future-{frequency}"
        list_files_to_download = self._get_list_of_file_urls_to_download_market_trades(
            start_date=start_date,
            end_date=end_date,
            route_url=candles_future_route,
            exchanges=exchanges,
        )
        self._download_list_of_files(
            list_files_to_download, output_format=output_format, threaded=threaded
        )

    def export_market_candles_spot_data(
        self,
        frequency: str,
        start_date: datetime,
        end_date: datetime,
        exchanges: Union[str, List[str]],
        output_format: str = DEFAULT_OUTPUT_FORMAT,
        threaded: bool = False,
    ) -> None:
        if frequency not in self._SUPPORTED_FREQUENCIES:
            raise ValueError(
                f"This frequency is not supported for market-candles-spot,"
                f" supported frequencies: {self._SUPPORTED_FREQUENCIES}"
            )
        candles_future_route = f"market-candles-spot-{frequency}"
        list_files_to_download = self._get_list_of_file_urls_to_download_market_trades(
            start_date=start_date,
            end_date=end_date,
            route_url=candles_future_route,
            exchanges=exchanges,
        )
        self._download_list_of_files(
            list_files_to_download, output_format=output_format, threaded=threaded
        )

    def export_market_quotes_future_data(
        self,
        start_date: datetime,
        end_date: datetime,
        asset_pairs: List[str],
        exchanges: Union[str, List[str]],
        output_format: str = DEFAULT_OUTPUT_FORMAT,
        threaded: bool = False,
    ) -> None:
        """
        Exports market quotes futures data to flat files given the parameters
        :param asset_pairs: list of string of asset pairs to download
        :param exchanges: list of string of exchanges
        :param start_date: date to start querying files
        :param end_date: date to end querying
        :param output_format: str how the files should be saved, supported data types are "json.gz", "json", and "csv"
        :param threaded: if true will thread the download process
        """
        if isinstance(exchanges, str):
            exchanges = exchanges.capitalize()
        else:
            exchanges = [exchange.capitalize() for exchange in exchanges]
        quotes_route = "market-quotes-future"
        list_files_to_download = self._get_list_files_to_download_from_ff_server(
            assets_pairs=asset_pairs,
            route_url=quotes_route,
            start_date=start_date,
            end_date=end_date,
            exchanges=exchanges,
        )
        self._download_list_of_files(
            list_files_to_download, output_format=output_format, threaded=threaded
        )

    def export_market_quotes_spot_data(
        self,
        start_date: datetime,
        end_date: datetime,
        asset_pairs: List[str],
        exchanges: Union[str, List[str]],
        output_format: str = DEFAULT_OUTPUT_FORMAT,
        threaded: bool = False,
    ) -> None:
        """
        Exports market quotes data to flat files given the parameters
        :param asset_pairs: list of string of asset pairs to download
        :param exchanges: list of string of exchanges
        :param start_date: date to start querying files
        :param end_date: date to end querying
        :param output_format: str how the files should be saved, supported data types are "json.gz", "json", and "csv"
        :param threaded: if true will thread the download process
        """
        if isinstance(exchanges, str):
            exchanges = exchanges.capitalize()
        else:
            exchanges = [exchange.capitalize() for exchange in exchanges]
        quotes_route = "market-quotes-spot"
        list_files_to_download = self._get_list_files_to_download_from_ff_server(
            assets_pairs=asset_pairs,
            route_url=quotes_route,
            start_date=start_date,
            end_date=end_date,
            exchanges=exchanges,
        )
        self._download_list_of_files(
            list_files_to_download, output_format=output_format, threaded=threaded
        )

    def export_market_trades_spot_data(
        self,
        start_date: datetime,
        end_date: datetime,
        exchanges: Union[str, List[str]],
        output_format: str = DEFAULT_OUTPUT_FORMAT,
        threaded: bool = False,
    ) -> None:
        """
        Exports market trade data to flat files given the parameters
        :param exchanges: list of string of exchanges
        :param start_date: date to start querying files
        :param end_date: date to end querying
        :param output_format: str how the files should be saved, supported data types are "json.gz", "json", and "csv"
        """
        market_trades_url = "market-trades-spot"
        list_files_to_download = self._get_list_of_file_urls_to_download_market_trades(
            start_date=start_date,
            end_date=end_date,
            exchanges=exchanges,
            route_url=market_trades_url,
        )
        self._download_list_of_files(
            list_files_to_download, output_format=output_format, threaded=threaded
        )

    def export_market_trades_future_data(
        self,
        start_date: datetime,
        end_date: datetime,
        exchanges: Union[str, List[str]],
        output_format: str = DEFAULT_OUTPUT_FORMAT,
        threaded: bool = False,
    ) -> None:
        """
        Exports market trade data to flat files given the parameters
        :param exchanges: list of string of exchanges
        :param start_date: date to start querying files
        :param end_date: date to end querying
        :param output_format: str how the files should be saved, supported data types are "json.gz", "json", and "csv"
        """
        market_trades_url = "market-trades-future"
        list_files_to_download = self._get_list_of_file_urls_to_download_market_trades(
            start_date=start_date,
            end_date=end_date,
            exchanges=exchanges,
            route_url=market_trades_url,
        )
        self._download_list_of_files(
            list_of_files=list_files_to_download,
            output_format=output_format,
            threaded=threaded,
        )

    def get_exchanges(self, file_type: str) -> List[str]:
        """
        Get the exchanges available for a file type
        :param file_type: str one of the queryable file types, such as "market-trades-future/spot",
        "market-candles-future/spot-<frequency>", "market-quotes-future/spot"
        """
        request_data = self._send_request(self._API_BASE_URL + file_type).json()
        result = [directory["name"] for directory in request_data]
        return result

    def get_asset_pairs(self, file_type: str, exchange: str) -> List[str]:
        request_data = self._send_request(
            f"{self._API_BASE_URL}/{file_type}/{exchange}"
        ).json()
        result = [directory["name"] for directory in request_data]
        return result

    def _download_list_of_files(
        self, list_of_files: List[str], output_format: str, threaded: bool = False
    ) -> None:
        """
        Downloads a list of files from the CM API server, gives the option to thread it or not
        :param list_of_files: list of files to download from server
        :output_format: str supported formats are json.gz, csv, or json
        :param threaded: if true will run download processes concurrently, which can make long running tasks run quicker.
        Downloading is still limited by bandwith
        """
        if threaded:
            with ThreadPoolExecutor() as executor:
                for file in list_of_files:
                    executor.submit(
                        self._download_file_from_server,
                        url=file,
                        output_format=output_format,
                    )
        else:
            for file in list_of_files:
                self._download_file_from_server(url=file, output_format=output_format)

    def _download_file_from_server(
        self, url: str, output_format: str = DEFAULT_OUTPUT_FORMAT
    ) -> None:
        """
        Downloads file from flat files server, converts the data type if neccesary, and stores it locally
        :param url: url to the file to download i.e. 'market-trades-spot/binance/2019-09-09.json.gz'
        :param output_format: str output format supported formats are 'csv', 'json', and 'json.gz'
        """
        url_split = url.split("/")
        file_name = url_split[-1]
        rest_of_url = "/".join(url_split[:-1])
        os.makedirs(rest_of_url, exist_ok=True)

        if output_format == "json.gz":
            with self._send_request(self._API_BASE_URL + url, stream=True) as response:
                with open(url, "wb") as file:
                    for chunk in response.iter_content(chunk_size=1024):
                        file.write(chunk)
                    logger.info(f"Downloaded file {url}")
            return

        elif output_format == "csv":
            file_name = file_name.replace("json.gz", "csv")
            full_file_name = f"{rest_of_url}/{file_name}"
            self._download_and_stream_data_to_csv(
                self._API_BASE_URL + url, full_file_name
            )

        elif output_format == "json":
            file_name = file_name.replace("json.gz", "json")
            full_file_name = f"{rest_of_url}/{file_name}"
            self._download_and_stream_data_to_json(
                request_url=self._API_BASE_URL + url, file_name=full_file_name
            )

        else:
            raise ValueError(f"Unsupported output type: {output_format}")

    def _get_list_files_to_download_from_ff_server(
        self,
        assets_pairs: List[str],
        exchanges: Union[str, List[str]],
        route_url: str,
        start_date: datetime,
        end_date: datetime,
    ) -> List[str]:
        """
        Queries the CoinMetrics flat files server and figures out what files to download
        """
        if isinstance(exchanges, str):
            exchanges = [exchanges]

        market_quotes_spot = self._API_BASE_URL + route_url
        market_quotes_exchange_folders = self._send_request(market_quotes_spot).json()
        list_of_files_to_download = []
        list_supported_exchanges = set()
        for market_trade_dir in market_quotes_exchange_folders:
            exchange_name = market_trade_dir["name"]
            list_supported_exchanges.add(exchange_name)

        for exchange in exchanges:
            if exchange not in list_supported_exchanges:
                raise ValueError(
                    f"Provided exchange: {exchange} is not supported for flat files. Supported exchanges: {list_supported_exchanges}"
                )

        for exchange in exchanges:
            exchange_files_url = market_quotes_spot + f"/{exchange}"
            exchange_asset_pair_data = self._send_request(exchange_files_url).json()
            exchange_asset_pair_folders = {
                folder["name"] for folder in exchange_asset_pair_data
            }

            asset_pair_url_dict = {}
            for asset_pair in assets_pairs:
                if asset_pair not in exchange_asset_pair_folders:
                    logger.info(
                        f"Asset pair: {asset_pair} not supported for exchange: {exchange}, skipping"
                    )
                else:
                    exchange_asset_pair_url = f"{exchange_files_url}/{asset_pair}"
                    asset_pair_url_dict[asset_pair] = exchange_asset_pair_url

            for asset_pair, asset_pair_url in asset_pair_url_dict.items():
                date_files_exchange_asset_pair = self._send_request(
                    asset_pair_url
                ).json()
                filtered_date_files = self.filter_date_files(
                    date_files_exchange_asset_pair,
                    start_date,
                    end_date,
                    f"{route_url}/{exchange}/{asset_pair}",
                )
                list_of_files_to_download.extend(filtered_date_files)

        return list_of_files_to_download

    def _get_list_of_file_urls_to_download_market_trades(
        self,
        start_date: datetime,
        end_date: datetime,
        exchanges: Union[str, List[str]],
        route_url: str,
    ) -> List[str]:
        if type(exchanges) == str:
            exchanges = [str(exchanges)]

        market_trades_url = self._API_BASE_URL + route_url
        market_trades_exchanges = self._send_request(market_trades_url).json()
        list_of_files_to_download = []
        list_supported_exchanges = []
        for market_trade_dir in market_trades_exchanges:
            exchange_name = market_trade_dir["name"]
            list_supported_exchanges.append(exchange_name)

        for exchange in exchanges:
            if exchange not in list_supported_exchanges:
                raise ValueError(
                    f"Provided exchange: {exchange} is not supported for flat files. Supported exchanges: {list_supported_exchanges}"
                )

            exchange_files_url = market_trades_url + f"/{exchange}"
            files = self._send_request(exchange_files_url).json()
            filtered_exchange_files = self.filter_date_files(
                files, start_date, end_date, f"{route_url}/{exchange}"
            )
            list_of_files_to_download.extend(filtered_exchange_files)

        return list_of_files_to_download

    def _download_and_stream_data_to_json(
        self, request_url: str, file_name: str
    ) -> None:
        """
        Streams gzipped data from url and decodes it to a valid json file
        :param request_url: str request url where json.gz file is stored
        :param file_name: name of the file to store
        """
        with self._send_request(request_url, stream=True) as resp:
            decoded = stream_gzip_decompress(resp.iter_content(chunk_size=1024))
            with open(file_name, "w") as file:
                file.write("[")
                for line in decoded:
                    full_line = line.decode("UTF-8").replace("}", "},")
                    file.write(full_line)
                # This is done in order to remove trailing ',' and add a ']' to conform with JSON spec
                file.seek(file.tell() - 1, os.SEEK_SET)
                file.write("")
                file.seek(file.tell() - 1, os.SEEK_SET)
                file.write("")
                file.write("]")

    def _download_and_stream_data_to_csv(
        self, request_url: str, file_name: str
    ) -> None:
        """
        Streams gzipped data from url and decodes it into a valid csv file
        :param request_url: str request url where json.gz file is stored
        :param file_name: name of the file to store
        """
        with self._send_request(request_url, stream=True) as resp:
            decoded_dicts = stream_gzip_decompress_to_dicts(resp.iter_content(1024))
            with open(file_name, "w") as csvfile:
                first_iteration = True
                for data in decoded_dicts:
                    if first_iteration:
                        writer = csv.DictWriter(
                            csvfile,
                            fieldnames=list(data[0].keys()),
                            extrasaction="ignore",
                        )
                        writer.writeheader()
                        first_iteration = False
                    writer.writerows(data)
                logger.info(f"Downloaded file {file_name}")

    @staticmethod
    def filter_date_files(
        list_of_dated_file_names: List[Dict[str, str]],
        start_date: datetime,
        end_date: datetime,
        result_file_abbreviation: str,
    ) -> List[str]:
        """
        Filters file names formatted like YYYY-MM-DD.<file_format> so that only files with dates that fall in between
         the start and end dates are returned
         :param list_of_dated_file_names: list of files names formatted as YYYY-MM-DD.<file_format>
         :param start_date: datetime start date of filter
         :param end_date: datetime end date of filter
         :param result_file_abbreviation: str abbreviation to append to front of file names. I.e.
          market-trades-spot/binance     would be included with all results
         :return: list of str file names that fall in between the start and end dates
        """
        result_files = []
        for file in list_of_dated_file_names:
            file_name = file["name"]
            file_date_str = file_name.split(".")[0]
            file_date = datetime.strptime(file_date_str, "%Y-%m-%d")
            if start_date <= file_date <= end_date:
                full_file_name = f"{result_file_abbreviation}/{file_name}"
                result_files.append(full_file_name)
        return result_files

    @retry((socket.gaierror, HTTPError), retries=5, wait_time_between_retries=5)
    def _send_request(self, actual_url: str, stream: bool = False) -> Response:
        response = self._session.get(
            actual_url, verify=self._verify_ssl_certs, auth=self._auth, stream=stream, proxies=self.proxies
        )
        if response.status_code == 403 or response.status_code == 401:
            raise CoinMetricsUnauthorizedException(response=response)
        if response.status_code != 200:
            response.raise_for_status()
        return response


def stream_gzip_decompress_to_dicts(
    stream: Iterable[bytes],
) -> Iterable[Dict[Any, Any]]:
    dec = zlib.decompressobj(32 + zlib.MAX_WBITS)
    remainder = ""
    for chunk in stream:
        rv = dec.decompress(chunk)
        if rv:
            test_line = rv.decode("UTF-8")
            line_split = test_line.split("}")
            full_dict = remainder + "},".join(line_split[:-1]) + "}"
            remainder = line_split[-1:][0]
            yield orjson.loads("[" + full_dict + "]")


def stream_gzip_decompress(stream: Iterable[bytes]) -> Iterable[bytes]:
    dec = zlib.decompressobj(32 + zlib.MAX_WBITS)
    for chunk in stream:
        rv = dec.decompress(chunk)
        if rv:
            yield rv
