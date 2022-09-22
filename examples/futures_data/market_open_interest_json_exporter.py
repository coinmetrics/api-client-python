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

DST_ROOT = "./data/market_open_interest/"

# Will export all future markets with BTC as a base
MARKETS_TO_EXPORT = [data['market'] for data in client.catalog_markets(base="btc", type="future")]

EXPORT_START_DATE = datetime(year=2020, month=1, day=1)

EXPORT_END_DATE = datetime.today()


def export_data(markets: List[str], start_time: datetime, end_time: datetime) -> None:
    processes_count = 6

    with Pool(processes_count) as pool:
        tasks = []
        for market in markets:
            tasks.append(pool.apply_async(export_market_open_interest_data,
                                          (market, start_time, end_time)))

        start_time = datetime.utcnow()
        for i, task in enumerate(tasks, 1):
            try:
                task.get()
            except Exception:
                logger.warning('failed to get data for task %s', i)
            time_since_start = datetime.utcnow() - start_time
            logger.info("processed task: %s/%s, time since start: %s, completion ETA:: %s",
                        i, len(tasks), time_since_start, time_since_start / i * (len(tasks) - i))


def export_market_open_interest_data(market: str, start_time: datetime, end_time: datetime) -> None:
    logger.info("retrieving market open interest for market: %s", market)
    dst_file = join(DST_ROOT, "{}_market_open_interest.json".format(market))
    makedirs(DST_ROOT, exist_ok=True)
    logger.info(
        f"exporting market open interest for {market} into a json file, this may take several minutes large markets ")
    with open(dst_file, "wb") as dst_file_buffer:
        market_open_interest = client.get_market_open_interest(
            markets=market,
            paging_from=PagingFrom.START,
            start_time=start_time,
            end_time=end_time,
            page_size=1000
        )
        market_open_interest.export_to_json(dst_file_buffer)


if __name__ == "__main__":
    export_start_time = datetime.now()
    try:
        export_data(markets=MARKETS_TO_EXPORT, start_time=EXPORT_START_DATE, end_time=EXPORT_END_DATE)
    finally:
        logger.info("export took: %s", datetime.now() - export_start_time)
