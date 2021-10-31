import logging
import sys
from datetime import datetime
from multiprocessing import Pool
from os import environ, makedirs
from os.path import abspath, join

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


def export_data(asset: str):
    logger.info("retrieving metric names")
    catalog_response = client.catalog_assets(assets="btc")
    metric_names = [
        metric_info["metric"]
        for metric_info in catalog_response[0]["metrics"]
        if any(
            frequency_info["frequency"] == "1b"
            for frequency_info in metric_info["frequencies"]
        )
    ]

    dst_file = join(DST_ROOT, "{}_bbb_metrics.json".format(asset))
    makedirs(DST_ROOT, exist_ok=True)
    logger.info(
        "exporting metrics into a json file (this might take 5-10+ minutes): %s",
        abspath(dst_file),
    )
    with open(dst_file, "wb") as dst_file_buffer:
        asset_metrics = client.get_asset_metrics(
            assets="btc",
            metrics=metric_names,
            frequency='1b',
            paging_from=PagingFrom.START,
        )
        asset_metrics.export_to_json(dst_file_buffer)


if __name__ == "__main__":
    export_start_time = datetime.now()
    try:
        export_data("btc")
    finally:
        logger.info("export took: %s", datetime.now() - export_start_time)
