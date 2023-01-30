import logging
import sys
from datetime import date, datetime, timedelta
from multiprocessing import Pool
from os import environ, makedirs, remove
from os.path import exists
from pathlib import Path
from typing import Iterable, Optional

from coinmetrics.api_client import CoinMetricsClient
from coinmetrics.constants import PagingFrom

try:
    import orjson as json
except ImportError:
    import json  # type: ignore

logger = logging.getLogger()
stream_handler = logging.StreamHandler()
level = logging.getLevelName("INFO")
stream_handler.level = level
formatter = logging.Formatter(
    datefmt="[%Y-%m-%d %H:%M:%S]", fmt="%(asctime)-15s %(levelname)s %(message)s"
)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
logger.level = level

# use it if you want to get specific exchanges or leave it empty if you want to get all exchanges data
# examples of echanges names:
# "binance.us",
# "binance",
# "coinbase",
# "okex",
# "kraken",
# "huobi",
# "bitmex",
# "bitfinex",
# "deribit",
# "cme",
EXCHANGES_TO_EXPORT = {"binance"}

# use it if you want to get specific markets or leave it empty if you want to get all markets
# example of market name to be used in this filter: "binance-BTCUSDT-future",
# note that if you specified exchanges filter, it will act as selecting intersection with the markets to export
# not as union.
MARKETS_TO_EXPORT = {}


# example values: "spot", "future"
# you can use all 3 if you want or just a subset
MARKET_TYPES_TO_COLLECT = {
    "spot",
    "future",
}

# leave it empty to catch all
BASE_MARKETS = {
    "btc",
}

# leave it empty to catch all
QUOTE_MARKETS = {
    "usd",
}

# 1 - 30000, or None for full_book
DEPTH_LIMIT = 100

# DST_ROOT is the path where you want the data to be saved to
# start the path with 's3://' prefix to make the script save to AWS S3, example
# or omit the s3:// prefix to save to local storage
# examples:
# DST_ROOT = './data'
# DST_ROOT = 's3://<bucket_name>/data'
DST_ROOT = "./data"

EXPORT_START_DATE = "2021-11-01"

# if you set EXPORT_END_DATE to None, then `today - 1 day` will be used as the end date
EXPORT_END_DATE: Optional[str] = None

COMPRESS_DATA = False  # False - for raw json files; True - for gzipped json files

# path to local file that is used to not reexport data if it was already exported
PROCESSED_DAYS_REGISTRY_FILE_PATH = "books_processed_days_registry.txt"


api_key = (
    environ.get("CM_API_KEY") or sys.argv[1]
)  # sys.argv[1] is executed only if CM_API_KEY is not found
client = CoinMetricsClient(api_key)

s3 = None
if DST_ROOT.startswith("s3://"):
    import s3fs

    s3 = s3fs.S3FileSystem(
        key=environ.get("AWS_ACCESS_KEY_ID"),
        secret=environ.get("AWS_SECRET_ACCESS_KEY"),
    )


def export_data():
    min_export_date = date.fromisoformat(EXPORT_START_DATE)
    max_export_date = (
        date.fromisoformat(EXPORT_END_DATE)
        if EXPORT_END_DATE is not None
        else date.today() - timedelta(days=1)
    )
    processed_dates_and_markets = read_already_processed_files()

    markets = get_markets_to_process()

    logger.info("getting markets: %s", [market["market"] for market in markets])
    processes_count = 2

    if processes_count > 2:
        logger.warning(
            "Using more than two parallel processes will likely not result into faster export."
        )

    with Pool(processes_count) as pool:
        tasks = []
        for market in markets:
            market_data_root = "/".join(
                (
                    DST_ROOT.rstrip("/"),
                    market["market"].split("-")[0],
                    get_instrument_root(market),
                )
            )

            # creating all the directories upfront to not to call this function in export function for each day
            # otherwise it can fail in the multiproc environment even with exist_ok=True.
            if s3 is not None:
                s3.makedirs(market_data_root, exist_ok=True)
            else:
                makedirs(market_data_root, exist_ok=True)

            for target_date in get_days_to_export(
                market, min_export_date, max_export_date
            ):
                if (
                    get_registry_key(market, target_date)
                    not in processed_dates_and_markets
                ):
                    tasks.append(
                        pool.apply_async(
                            export_data_for_a_market,
                            (market, market_data_root, target_date),
                        )
                    )

        start_time = datetime.utcnow()
        for i, task in enumerate(tasks, 1):
            try:
                task.get()
            except Exception:
                logger.warning('failed to get data for task %s', i)
            time_since_start = datetime.utcnow() - start_time
            logger.info("processed task: %s/%s, time since start: %s, completion ETA:: %s",
                        i, len(tasks), time_since_start, time_since_start / i * (len(tasks) - i))

def get_instrument_root(market):
    if market["type"] == "spot":
        return "{}_{}_{}".format(market["base"], market["quote"], market["type"])
    return "{}_{}".format(market["symbol"].replace(":", "_"), market["type"])


def read_already_processed_files():
    if exists(PROCESSED_DAYS_REGISTRY_FILE_PATH):
        with open(PROCESSED_DAYS_REGISTRY_FILE_PATH) as registry_file:
            return set(registry_file.read().splitlines())
    return set()

def get_markets_to_process():
    markets = []

    for exchange in EXCHANGES_TO_EXPORT or [None]:
        for market in client.catalog_markets(exchange=exchange):
            if market["market"] in MARKETS_TO_EXPORT or (
                (market["type"] in MARKET_TYPES_TO_COLLECT)
                and (
                    (
                        ('base' in market and market["base"] in BASE_MARKETS or not BASE_MARKETS)
                        and (market["quote"] in QUOTE_MARKETS or not QUOTE_MARKETS)
                    )
                )
            ):
                markets.append(market)
    return markets


def get_days_to_export(market_info, min_export_date, max_export_date):
    min_date = max(
        date.fromisoformat(market_info["min_time"].split("T")[0]), min_export_date
    )
    max_date = min(
        date.fromisoformat(market_info["max_time"].split("T")[0]), max_export_date
    )
    for target_date_index in range((max_date - min_date).days + 1):
        yield min_date + timedelta(days=target_date_index)


def export_data_for_a_market(market, market_data_root, target_date):
    market_orderbooks = client.get_market_orderbooks(
        market["market"],
        start_time=target_date,
        end_time=target_date,
        page_size=10000,
        paging_from=PagingFrom.START,
        depth_limit="full_book" if DEPTH_LIMIT is None or DEPTH_LIMIT > 100 else 100,
    )
    dst_json_file_path = (
        "/".join((market_data_root, "books_" + target_date.isoformat())) + ".json"
    )
    if COMPRESS_DATA:
        dst_json_file_path = dst_json_file_path + ".gz"
    logger.info("downloading data to: %s", dst_json_file_path)

    def _gen_json_lines() -> Iterable[bytes]:
        if DEPTH_LIMIT in {None, 100, 30000}:
            for data_row in market_orderbooks:
                yield json.dumps(data_row) + b"\n"
        else:
            for data_row in market_orderbooks:
                data_row["asks"] = data_row["asks"][:DEPTH_LIMIT]
                data_row["bids"] = data_row["bids"][:DEPTH_LIMIT]
                yield json.dumps(data_row) + b"\n"

    if s3 is not None:
        with s3.open(dst_json_file_path.split("s3://")[1], "wb") as data_file:
            market_orderbooks._export_to_file(
                _gen_json_lines(), data_file, compress=COMPRESS_DATA
            )
    else:
        market_orderbooks._export_to_file(
            _gen_json_lines(), dst_json_file_path, compress=COMPRESS_DATA
        )
        # cleanup files without data
        if Path(dst_json_file_path).stat().st_size == 0:
            remove(dst_json_file_path)
    with open(PROCESSED_DAYS_REGISTRY_FILE_PATH, "a") as registry_file:
        registry_file.write(get_registry_key(market, target_date) + "\n")


def get_registry_key(market, target_date):
    return "{},{}".format(market["market"], target_date.isoformat())


if __name__ == "__main__":
    export_start_time = datetime.now()
    try:
        export_data()
    finally:
        logger.info("export took: %s", datetime.now() - export_start_time)
