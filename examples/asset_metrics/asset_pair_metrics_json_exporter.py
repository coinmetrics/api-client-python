import logging
import sys
from datetime import datetime, timedelta
from multiprocessing import Pool
from os import environ, makedirs
from os.path import join
from typing import List

from coinmetrics.api_client import CoinMetricsClient
from coinmetrics.constants import PagingFrom

logger = logging.getLogger()
stream_handler = logging.StreamHandler()
level = logging.INFO
stream_handler.level = level
formatter = logging.Formatter(
    datefmt="[%Y-%m-%d %H:%M:%S]", fmt="%(asctime)-15s %(levelname)s %(message)s"
)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
logger.level = level


api_key = (
    environ.get("CM_API_KEY") or sys.argv[1]
)  # sys.argv[1] is executed only if CM_API_KEY is not found

client = CoinMetricsClient(api_key)

DST_ROOT = "./data"

ASSET_PAIRS_TO_EXPORT = [
    "btc-usd",
    "eth-usd",
    "ada-usd"
]

METRICS_TO_EXPORT = [
    "open_interest_reported_future_nonperpetual_usd",
    "volume_reported_spot_usd_1d",
    "volume_reported_spot_usd_1h",
    "open_interest_reported_future_tether_margined_usd",
    "volume_reported_future_usd_1h",
]

# 15s, 1h, 1d
FREQUENCY = "1h"

EXPORT_START_DATE = datetime.today() - timedelta(days=7)

EXPORT_END_DATE = datetime.today()


def export_data(asset_pairs: List[str], metrics_to_export: List[str], frequency: str,
                start_time: datetime, end_time: datetime) -> None:
    processes_count = 2

    if processes_count > 2:
        logger.warning(
            "Using more than two parallel processes will likely not result into faster export."
        )

    with Pool(processes_count) as pool:
        tasks = []
        for asset in asset_pairs:
            tasks.append(pool.apply_async(export_asset_pair_metric_data,
                                          (asset, metrics_to_export, frequency, start_time, end_time)))

        start_time = datetime.utcnow()
        for i, task in enumerate(tasks, 1):
            try:
                task.get()
            except Exception:
                logger.warning('failed to get data for task %s', i)
            time_since_start = datetime.utcnow() - start_time
            logger.info("processed task: %s/%s, time since start: %s, completion ETA:: %s",
                        i, len(tasks), time_since_start, time_since_start / i * (len(tasks) - i))


def export_asset_pair_metric_data(asset_pair: str, metrics: List[str], frequency: str, start_time: datetime, end_time: datetime) -> None:
    logger.info("retrieving asset pair metrics for pair: %s", asset_pair)
    dst_file = join(DST_ROOT, "{}_pair_metrics.json".format(asset_pair))
    makedirs(DST_ROOT, exist_ok=True)
    logger.info(
        f"exporting asset pair metrics {asset_pair} into a json file ")
    with open(dst_file, "wb") as dst_file_buffer:
        asset_metrics = client.get_pair_metrics(
            pairs=asset_pair,
            metrics=metrics,
            frequency=frequency,
            paging_from=PagingFrom.START,
            start_time=start_time,
            end_time=end_time,
            page_size=1000
        )
        asset_metrics.export_to_json(dst_file_buffer)


if __name__ == "__main__":
    export_start_time = datetime.now()
    try:
        export_data(asset_pairs=ASSET_PAIRS_TO_EXPORT, metrics_to_export=METRICS_TO_EXPORT, frequency=FREQUENCY,
                    start_time=EXPORT_START_DATE, end_time=EXPORT_END_DATE)
    finally:
        logger.info("export took: %s", datetime.now() - export_start_time)
