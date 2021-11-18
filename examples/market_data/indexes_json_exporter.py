import logging
import sys
from datetime import datetime
from multiprocessing import Pool
from os import environ, makedirs
from os.path import abspath, join
from typing import Optional

import requests

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

# CMBIBTC, CMBIETH, ...
INDEXES_TO_EXPORT = {
    "CMBIBTC",
    "CMBIETH",
}

# 15s, 1h, 1d
FREQUENCY = "1h"

EXPORT_START_DATE = "2019-01-01"

# if you set EXPORT_END_DATE to None, then `today - 1 day` will be used as the end date
EXPORT_END_DATE: Optional[str] = None


def export_data():
    processes_count = 2

    if processes_count > 2:
        logger.warning(
            "Using more than two parallel processes will likely not result into faster export."
        )

    with Pool(processes_count) as pool:
        tasks = []
        for asset in INDEXES_TO_EXPORT:
            tasks.append(pool.apply_async(export_asset_data, (asset,)))

        for i, task in enumerate(tasks, 1):
            task.get()
            logger.info("processed task: %s/%s", i, len(tasks))


def export_asset_data(index: str) -> None:
    logger.info("retrieving indexes values for index: %s", index)
    dst_file = join(DST_ROOT, "{}_index.json".format(index))
    makedirs(DST_ROOT, exist_ok=True)
    logger.info(
        "exporting indexes for index `%s` into a json file "
        "(this might take 5-10+ minutes for %s frequency and a 1-30sec for 1h and 1d frequencies): %s",
        index, FREQUENCY, abspath(dst_file),
    )
    # only pick metrics that are available for that asset
    with open(dst_file, "wb") as dst_file_buffer:
        asset_metrics = client.get_index_levels(
            indexes=index,
            frequency=FREQUENCY,
            paging_from=PagingFrom.START,
            start_time=EXPORT_START_DATE,
            end_time=EXPORT_END_DATE,
        )
        asset_metrics.export_to_json(dst_file_buffer)


if __name__ == "__main__":
    export_start_time = datetime.now()
    try:
        export_data()
    finally:
        logger.info("export took: %s", datetime.now() - export_start_time)
