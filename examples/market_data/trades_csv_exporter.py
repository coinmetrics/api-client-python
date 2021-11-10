import logging
import sys
from datetime import date, timedelta, datetime
from multiprocessing import Pool, cpu_count
from os import makedirs, environ
from os.path import exists

from coinmetrics.api_client import CoinMetricsClient
from coinmetrics.constants import PagingFrom

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


EXCHANGES_TO_EXPORT = [
    "binance.us",
    "binance",
    "coinbase",
    "okex",
    "kraken",
    "huobi",
    "bitmex",
    "bitfinex",
    "deribit",
]

FUTURES_MARKETS_TO_EXPORT = [
    "binance-BTCUSDT-future",
    "bitmex-XBTUSD-future",
    "bitfinex-tBTCF0:USTF0-future",
    "deribit-BTC-PERPETUAL-future",
]

# DST_ROOT is the path where you want the data to be saved to
# start the path with 's3://' prefix to make the script save to AWS S3, example
# or omit the s3:// prefix to save to local storage
# examples:
# DST_ROOT = './data'
# DST_ROOT = 's3://<bucket_name>/data'
DST_ROOT = "./data"

EXPORT_START_DATE = "2017-01-01"
EXPORT_END_DATE = "2020-05-31"  # if you set this to None, then `today - 1 day` will be used as the end date
COMPRESS_DATA = True  # False - for raw csv files; True - for gzipped csv files

# path to local file that is used to not reexport data if it was already exported
PROCESSED_DAYS_REGISTRY_FILE_PATH = "processed_days_registry.txt"


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
        if EXPORT_END_DATE
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

        for i, task in enumerate(tasks, 1):
            task.get()
            logger.info("processed task: %s/%s", i, len(tasks))


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
    for exchange in EXCHANGES_TO_EXPORT:
        for market in client.catalog_markets(exchange=exchange):
            if market["market"] in FUTURES_MARKETS_TO_EXPORT or (
                market["type"] == "spot"
                and (
                    (market["base"] == "btc" and market["quote"] in ["usd", "usdt"])
                    or (market["quote"] == "btc" and market["base"] in ["usd", "usdt"])
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
    market_trades = client.get_market_trades(
        market["market"],
        start_time=target_date,
        end_time=target_date,
        page_size=10000,
        paging_from=PagingFrom.START,
    )
    dst_csv_file_path = "/".join((market_data_root, target_date.isoformat())) + ".csv"
    if COMPRESS_DATA:
        dst_csv_file_path = dst_csv_file_path + ".gz"
    logger.info("downloading data to: %s", dst_csv_file_path)
    if s3 is not None:
        with s3.open(dst_csv_file_path.split("s3://")[1], "wb") as data_file:
            market_trades.export_to_csv(data_file, compress=COMPRESS_DATA)
    else:
        market_trades.export_to_csv(dst_csv_file_path, compress=COMPRESS_DATA)
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
