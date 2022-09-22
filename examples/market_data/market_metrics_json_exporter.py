import logging
import sys
import datetime as dt
from typing import List, Union, Dict
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
FREQUENCY = "1d"
EXCHANGE = "binance"
BASE_ASSET = "btc"
START_TIME = dt.datetime(year=2020, month=1, day=1)
END_TIME = dt.datetime.today()


def get_markets_for_assets_and_exchange(asset: str, exchange: Union[str, None] = None, frequency: str = "1d") -> Dict[str, List[str]]:
    """
    Gets a list of markets related to specified assets and exchange
    :param assets: list of str of assets i.e. btc, eth
    :param exchange: optional param to specify an exchagne i.e. coinbase
    :return: list of str of markets
    """
    client = CoinMetricsClient(api_key)
    catalog_market_metrics = client.catalog_market_metrics(base=asset, exchange=exchange)
    result_markets_and_metrics: Dict[str, List[str]] = {}
    for item in catalog_market_metrics:
        for metric in item['metrics']:
            if any(frequency_info['frequency'] == frequency for frequency_info in metric['frequencies']):
                market_name = item['market']
                metric_name = metric['metric']
                if market_name in result_markets_and_metrics:
                    result_markets_and_metrics[market_name].append(metric_name)
                else:
                    result_markets_and_metrics[market_name] = [metric_name]
    return result_markets_and_metrics


def export_data(markets: Union[str, List[str]], metrics: Union[str, List[str], None], frequency: str = "1d",
                start_time: dt.datetime = START_TIME, end_time: dt.datetime = END_TIME):
    logger.info("retrieving metric names")
    client = CoinMetricsClient(api_key)

    dst_file = join(DST_ROOT, "{}_market_metrics.csv".format(frequency))
    makedirs(DST_ROOT, exist_ok=True)
    logger.info(
        "exporting metrics into a csv file (this might take 30sec - 1min): %s",
        abspath(dst_file),
    )
    market_metrics = client.get_market_metrics(
        markets=markets, metrics=metrics, frequency=frequency, start_time=start_time, end_time=end_time)
    market_metrics.export_to_csv(dst_file)


if __name__ == "__main__":
    market_and_metrics = get_markets_for_assets_and_exchange(BASE_ASSET, EXCHANGE, FREQUENCY)
    export_start_time = datetime.now()
    try:
        export_data(markets=list(market_and_metrics.keys()), metrics=list(market_and_metrics.values())[0],
                    start_time=START_TIME, end_time=END_TIME, frequency=FREQUENCY)
    finally:
        logger.info("export took: %s", datetime.now() - export_start_time)
