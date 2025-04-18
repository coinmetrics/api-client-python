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

# btc, eth, ...
ASSETS_TO_EXPORT = {
    # "btc",
}


# ReferenceRateUSD, ReferenceRateEUR, ReferenceRateBTC, ETH
REFERENCE_RATES = {
    "ReferenceRateUSD",
}

# 1s, 1m, 1h, 1d
FREQUENCY = "1h"

EXPORT_START_DATE = datetime.today() - timedelta(days=7)

# if you set EXPORT_END_DATE to None, then `today - 1 day` will be used as the end date
EXPORT_END_DATE: Optional[str] = None


FILTER_METRIC = 'CapMrktEstUSD'
FILTER_METRIC_VALUE = 10_000_000_000


def export_data():
    processes_count = 2

    if processes_count > 2:
        logger.warning(
            "Using more than two parallel processes will likely not result into faster export."
        )

    with Pool(processes_count) as pool:
        tasks = []
        if ASSETS_TO_EXPORT:
            assets_to_export = ASSETS_TO_EXPORT
        else:
            assets_to_export = []
            catalog_response = client.catalog_asset_metrics_v2().to_list()
            for i, asset_data in enumerate(catalog_response):
                metric_names = [
                    catalog_response[i]['metrics'][j]['metric'] for j in
                    range(len(catalog_response[i]['metrics']))
                ]
                if metric_names and FILTER_METRIC in metric_names:
                    metric_values = client.get_asset_metrics(
                        assets=asset_data['asset'],
                        metrics=FILTER_METRIC,
                        start_time=EXPORT_START_DATE,
                        end_time=EXPORT_END_DATE,
                        frequency='1d',
                        page_size=10000
                    ).to_list()
                    if metric_values:
                        max_val = max(*[float(v[FILTER_METRIC]) for v in metric_values])
                        print(asset_data['asset'], max_val)
                        if max_val > FILTER_METRIC_VALUE:
                            assets_to_export.append(asset_data['asset'])

        for asset in assets_to_export:
            tasks.append(pool.apply_async(export_asset_data, (asset,)))

        start_time = datetime.utcnow()
        for i, task in enumerate(tasks, 1):
            try:
                task.get()
            except Exception:
                logger.warning('failed to get data for task %s', i)
            time_since_start = datetime.utcnow() - start_time
            logger.info("processed task: %s/%s, time since start: %s, completion ETA:: %s",
                        i, len(tasks), time_since_start, time_since_start / i * (len(tasks) - i))


def export_asset_data(asset: str) -> None:
    logger.info("retrieving metric names for asset: %s", asset)
    catalog_response = client.catalog_asset_metrics_v2(asset).to_list()
    metric_names = [catalog_response[0]['metrics'][i]['metric'] for i in range(len(catalog_response[0]['metrics']))]
    dst_file = join(DST_ROOT, "{}_reference_rates.json".format(asset))
    makedirs(DST_ROOT, exist_ok=True)
    logger.info(
        "exporting rates for asset `%s` into a json file "
        "(this might take 5-10+ minutes for %s frequency and a 1-30sec for 1h and 1d frequencies): %s",
        asset, FREQUENCY, abspath(dst_file),
    )
    # only pick metrics that are available for that asset
    available_metrics = list(set(metric_names) & REFERENCE_RATES)
    with open(dst_file, "wb") as dst_file_buffer:
        asset_metrics = client.get_asset_metrics(
            assets=asset,
            metrics=available_metrics,
            frequency=FREQUENCY,
            paging_from=PagingFrom.START,
            start_time=EXPORT_START_DATE,
            end_time=EXPORT_END_DATE,
            page_size=10000
        )
        asset_metrics.export_to_json(dst_file_buffer)


if __name__ == "__main__":
    export_start_time = datetime.now()
    try:
        export_data()
    finally:
        logger.info("export took: %s", datetime.now() - export_start_time)
