import logging
import sys
from typing import List
from datetime import date, datetime, timedelta
from multiprocessing import Pool
from os import environ, makedirs, remove
from os.path import exists
from pathlib import Path
from typing import Optional

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




# example values: "spot", "future", "option"
# you can use all 3 if you want or just a subset
MARKET_TYPES_TO_COLLECT = {
    "spot",
    "future",
}

# leave it empty to catch all
BASE_ASSETS = {
    "btc",
}


# 1m, 5m, 10m, 15m, 30m, 1h, 4h, 1d
FREQUENCY = "1h"

# DST_ROOT is the path where you want the data to be saved to
# start the path with 's3://' prefix to make the script save to AWS S3, example
# or omit the s3:// prefix to save to local storage
# examples:
# DST_ROOT = './data'
# DST_ROOT = 's3://<bucket_name>/data'
DST_ROOT = "./data"

EXPORT_START_DATE = datetime.today() - timedelta(days=7)

# if you set EXPORT_END_DATE to None, then `today - 1 day` will be used as the end date
EXPORT_END_DATE: Optional[str] = None

COMPRESS_DATA = False  # False - for raw json files; True - for gzipped json files

# path to local file that is used to not reexport data if it was already exported
REGISTRY_FILE_PATH = "asset_pair_candles_processed_days_registry.txt"


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


def export_data(base_assets: List[str]):
    min_export_date = EXPORT_START_DATE
    max_export_date = (
        date.fromisoformat(EXPORT_END_DATE)
        if EXPORT_END_DATE is not None
        else date.today() - timedelta(days=1)
    )

    asset_pairs = get_asset_pairs_to_process(base_assets=base_assets)

    logger.info("getting asset_pairs_candles: %s", asset_pairs)
    processes_count = 2

    if processes_count > 2:
        logger.warning(
            "Using more than two parallel processes will likely not result into faster export."
        )

    with Pool(processes_count) as pool:
        tasks = []
        for asset_pair in asset_pairs:
            market_data_root = "/".join(
                (
                    DST_ROOT.rstrip("/"),
                    asset_pair
                )
            )

            # creating all the directories upfront to not to call this function in export function for each day
            # otherwise it can fail in the multiproc environment even with exist_ok=True.
            if s3 is not None:
                s3.makedirs(market_data_root, exist_ok=True)
            else:
                makedirs(market_data_root, exist_ok=True)

            if FREQUENCY in {"1h", "4h", "1d"}:
                tasks.append(
                    pool.apply_async(
                        export_data_for_an_asset_pair,
                        (
                            asset_pair,
                            market_data_root,
                            min_export_date,
                            max_export_date,
                        ),
                    )
                )
            else:
                for target_date in get_days_to_export(
                    asset_pair, min_export_date, max_export_date
                ):
                    tasks.append(
                        pool.apply_async(
                            export_data_for_an_asset_pair,
                            (asset_pair, market_data_root, target_date, target_date),
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
    if exists(REGISTRY_FILE_PATH):
        with open(REGISTRY_FILE_PATH) as registry_file:
            exports_to_skip = set(registry_file.read().splitlines())
            logging.warning(
                f"Registry file: {registry_file} exists, this means that the following exports will be skipped."
                f"if this is not intended delete or modify file {registry_file}. \n {exports_to_skip}")
            return exports_to_skip
    return set()


def get_asset_pairs_to_process(base_assets: List[str]) -> List[str]:
    pairs = set()
    catalog_asset_pairs = client.catalog_pair_candles_v2()
    for item in catalog_asset_pairs:
        pair_split = item['pair'].split("-")
        if pair_split[0] in base_assets or pair_split[1] in base_assets:
            pairs.add(item['pair'])
    return list(pairs)


def get_days_to_export(market_info, min_export_date, max_export_date):
    min_date = max(
        date.fromisoformat(market_info["min_time"].split("T")[0]), min_export_date
    )
    max_date = min(
        date.fromisoformat(market_info["max_time"].split("T")[0]), max_export_date
    )
    for target_date_index in range((max_date - min_date).days + 1):
        yield min_date + timedelta(days=target_date_index)


def export_data_for_an_asset_pair(pair: str, market_data_root: str, start_date, end_date):
    market_candles = client.get_pair_candles(
        pair,
        start_time=start_date,
        end_time=end_date,
        page_size=10000,
        paging_from=PagingFrom.START,
        frequency=FREQUENCY,
    )
    if start_date != end_date:
        dst_json_file_path = "/".join((market_data_root, "candles")) + ".json"
    else:
        dst_json_file_path = (
            "/".join((market_data_root, "candles_" + start_date.isoformat())) + ".json"
        )

    if COMPRESS_DATA:
        dst_json_file_path = dst_json_file_path + ".gz"
    logger.info("downloading data to: %s", dst_json_file_path)
    if s3 is not None:
        with s3.open(dst_json_file_path.split("s3://")[1], "wb") as data_file:
            market_candles.export_to_json(data_file, compress=COMPRESS_DATA)
    else:
        market_candles.export_to_json(dst_json_file_path, compress=COMPRESS_DATA)
        # cleanup files without data
        if Path(dst_json_file_path).stat().st_size == 0:
            remove(dst_json_file_path)
    with open(REGISTRY_FILE_PATH, "a") as registry_file:
        registry_file.write(get_registry_key(pair, start_date) + "\n")


def get_registry_key(market, target_date):
    return "{},{}".format(market["market"], target_date.isoformat())


if __name__ == "__main__":
    test_pairs = get_asset_pairs_to_process(["btc", "eth"])
    print("test!")
    export_start_time = datetime.now()
    try:
        export_data(["btc", "eth"])
    finally:
        logger.info("export took: %s", datetime.now() - export_start_time)
