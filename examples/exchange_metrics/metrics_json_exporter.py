import logging
import sys
from datetime import datetime, timedelta
from multiprocessing import Pool
from os import environ, makedirs
from os.path import abspath, join
from typing import Optional

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

# binance-btc, kraken-eth, ...
EXCHANGE_ASSETS_TO_EXPORT = {
    "binance-btc",
}


# basis_annualized_90d_exp, liquidations_reported_future_buy_units_1h, volume_reported_future_tether_margined_usd_1d ...
# use catalog to get more data
METRICS = {
    "basis_annualized_90d_exp",
}

# 1h, 1d
FREQUENCY = "1d"

EXPORT_START_DATE = datetime.today() - timedelta(days=7)

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
        if EXCHANGE_ASSETS_TO_EXPORT:
            exchange_assets_to_export = EXCHANGE_ASSETS_TO_EXPORT
        else:
            exchange_assets_to_export = []
            catalog_response = client.catalog_exchange_asset_metrics_v2().to_list()
            for asset_data in catalog_response:
                metric_names = [
                    metric_info["metric"]
                    for metric_info in asset_data.get("metrics", [])
                    if any(
                        frequency_info["frequency"] == FREQUENCY
                        for frequency_info in metric_info["frequencies"]
                    )
                ]
                if metric_names:
                    exchange_assets_to_export.append(asset_data['exchange_asset'])
        for exchange_asset in exchange_assets_to_export:
            tasks.append(pool.apply_async(export_exchange_asset_data, (exchange_asset,)))

        start_time = datetime.utcnow()
        for i, task in enumerate(tasks, 1):
            try:
                task.get()
            except Exception:
                logger.warning('failed to get data for task %s', i)
            time_since_start = datetime.utcnow() - start_time
            logger.info("processed task: %s/%s, time since start: %s, completion ETA:: %s",
                        i, len(tasks), time_since_start, time_since_start / i * (len(tasks) - i))

def export_exchange_asset_data(exchange_asset: str) -> None:
    logger.info("retrieving metric names for asset: %s", exchange_asset)
    catalog_response = client.catalog_exchange_assets(exchange_assets=exchange_asset)
    metric_names = [
        metric_info["metric"]
        for metric_info in catalog_response[0]["metrics"]
        if any(
            frequency_info["frequency"] == FREQUENCY
            for frequency_info in metric_info["frequencies"]
        )
    ]
    dst_file = join(DST_ROOT, "{}_exchange_asset.json".format(exchange_asset))
    makedirs(DST_ROOT, exist_ok=True)
    logger.info(
        "exporting metrics for exchange asset `%s` into a json file "
        "(this might take up to 30sec): %s",
        exchange_asset, abspath(dst_file),
    )
    # only pick metrics that are available for that asset
    available_metrics = list(set(metric_names) & METRICS)
    with open(dst_file, "wb") as dst_file_buffer:
        exchange_asset_metrics = client.get_exchange_asset_metrics(
            exchange_assets=exchange_asset,
            metrics=available_metrics,
            frequency=FREQUENCY,
            paging_from=PagingFrom.START,
            start_time=EXPORT_START_DATE,
            end_time=EXPORT_END_DATE,
            page_size=1000
        )
        exchange_asset_metrics.export_to_json(dst_file_buffer)


if __name__ == "__main__":
    export_start_time = datetime.now()
    try:
        export_data()
    finally:
        logger.info("export took: %s", datetime.now() - export_start_time)
