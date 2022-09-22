import logging
import sys
from datetime import datetime
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

INSTITUTIONS_TO_EXPORT = [
    "grayscale"
]


FREQUENCY = "1d"

EXPORT_START_DATE = datetime(year=2021, month=4 , day=1)

EXPORT_END_DATE = datetime.today()


def export_data(institutions: List[str], frequency: str,
                start_time: datetime, end_time: datetime) -> None:
    processes_count = 2

    if processes_count > 2:
        logger.warning(
            "Using more than two parallel processes will likely not result into faster export."
        )

    with Pool(processes_count) as pool:
        tasks = []
        for institution in institutions:
            institution_specific_metrics = [metric['metric'] for metric
                                            in client.catalog_institutions(institutions=institution)[0]['metrics']]
            tasks.append(pool.apply_async(export_institution_metric_data,
                                          (institution, institution_specific_metrics, frequency, start_time, end_time)))

        start_time = datetime.utcnow()
        for i, task in enumerate(tasks, 1):
            try:
                task.get()
            except Exception:
                logger.warning('failed to get data for task %s', i)
            time_since_start = datetime.utcnow() - start_time
            logger.info("processed task: %s/%s, time since start: %s, completion ETA:: %s",
                        i, len(tasks), time_since_start, time_since_start / i * (len(tasks) - i))


def export_institution_metric_data(institution: str, metrics: List[str], frequency: str, start_time: datetime, end_time: datetime) -> None:
    logger.info("retrieving institution metrics for institution: %s", institution)
    dst_file = join(DST_ROOT, "{}_institution_metrics.json".format(institution))
    makedirs(DST_ROOT, exist_ok=True)
    logger.info(
        f"exporting institution metrics {institution} into a json file ")
    with open(dst_file, "wb") as dst_file_buffer:
        asset_metrics = client.get_institution_metrics(
            institutions=institution,
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
        export_data(institutions=INSTITUTIONS_TO_EXPORT, frequency=FREQUENCY,
                    start_time=EXPORT_START_DATE, end_time=EXPORT_END_DATE)
    finally:
        logger.info("export took: %s", datetime.now() - export_start_time)
