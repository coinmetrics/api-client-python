from coinmetrics.api_client import CoinMetricsClient
from os import environ
import sys
from datetime import date, datetime, timedelta
import logging
import pandas as pd
import ast
import numpy as np

logger = logging.getLogger()
formatter = logging.Formatter(
    datefmt="[%Y-%m-%d %H:%M:%S]", fmt="%(asctime)-15s %(levelname)s %(message)s"
)
level = logging.getLevelName("INFO")
logger.level = level

api_key = (
    environ.get("CM_API_KEY") or sys.argv[1]
)  # sys.argv[1] is executed only if CM_API_KEY is not found
client = CoinMetricsClient(api_key)

MARKETS = ["coinbase-btc-usd-spot"]
START_TIME = "2022-03-29T00:00:00"
END_TIME = "2022-03-29T00:01:00"
DEPTH_LIMIT = 'full_book'  # 1-30000 or 'full_book'


def _expand_df(key, iterable):
    def _assign_value(row):
        try:
            return row[key]
        except (KeyError, TypeError):
            return None

    return list(map(_assign_value, iterable))


def export_data():
    logging.info(f"Gathering orderbook data for {MARKETS} from {START_TIME} to {END_TIME}...")
    df_orderbooks = client.get_market_orderbooks(
        markets=MARKETS, start_time=START_TIME, end_time=END_TIME, depth_limit=DEPTH_LIMIT,
        page_size=1000
    ).to_dataframe()

    df_orderbooks.asks = df_orderbooks.asks.apply(lambda x: ast.literal_eval(x))
    df_orderbooks.bids = df_orderbooks.bids.apply(lambda x: ast.literal_eval(x))

    logging.info(f"Wrangling orderbook data for bids and asks...")
    df_asks = df_orderbooks.explode(
        'asks'
    ).assign(
        price=lambda df: _expand_df(key='price', iterable=df.asks)
    ).assign(
        volume=lambda df: _expand_df(key='size', iterable=df.asks)
    )
    df_asks['type'] = 'ask'
    df_asks = df_asks[['market', 'time', 'price', 'volume', 'type']]

    df_bids = df_orderbooks.drop('coin_metrics_id', axis=1).explode(
        'bids'
    ).assign(
        price=lambda df: _expand_df(key='price', iterable=df.bids)
    ).assign(
        volume=lambda df: _expand_df(key='size', iterable=df.bids)
    )
    df_bids['type'] = 'bid'
    df_bids = df_bids[['market', 'time', 'price', 'volume', 'type']]

    df_orderbooks_full = pd.concat([df_asks, df_bids])
    df_orderbooks_full['price'] = df_orderbooks_full['price'].astype(float)
    df_orderbooks_full['volume'] = df_orderbooks_full['volume'].astype(float)

    orderbooks_file_name = f'orderbooks_flattened.csv'
    logging.info(f"file saved under {orderbooks_file_name}")
    df_orderbooks_full.to_csv(orderbooks_file_name)


if __name__ == "__main__":
    export_start_time = datetime.now()
    try:
        export_data()
    finally:
        logger.info("export took: %s", datetime.now() - export_start_time)
