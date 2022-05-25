import logging
import sys
from datetime import datetime
from os import environ, makedirs
from os.path import abspath, join

from coinmetrics.api_client import CoinMetricsClient

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

DST_ROOT = "./data"


def export_data(asset: str):
    logger.info("retrieving metric names")
    client = CoinMetricsClient(api_key)

    catalog_response = client.catalog_assets(assets=asset)
    metric_names = [
        metric_info["metric"]
        for metric_info in catalog_response[0]["metrics"]
        if any(
            frequency_info["frequency"] == "1d"
            for frequency_info in metric_info["frequencies"]
        )
    ]

    dst_file = join(DST_ROOT, "{}_eod_metrics.csv".format(asset))
    makedirs(DST_ROOT, exist_ok=True)
    logger.info(
        "exporting metrics into a csv file (this might take 30sec - 1min): %s",
        abspath(dst_file),
    )
    asset_metrics = client.get_asset_metrics(
        assets=asset, metrics=metric_names, frequency="1d", paging_from="start",
        page_size=1000
    )
    asset_metrics.export_to_csv(dst_file)


if __name__ == "__main__":
    export_start_time = datetime.now()
    try:
        export_data("btc")
    finally:
        logger.info("export took: %s", datetime.now() - export_start_time)
