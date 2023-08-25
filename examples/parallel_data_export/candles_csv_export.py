import os
from coinmetrics.api_client import CoinMetricsClient


if __name__ == '__main__':
    client = CoinMetricsClient(os.environ['CM_API_KEY'])
    binance_eth_markets = [market['market'] for market in client.catalog_market_candles(exchange="binance", base="eth")]
    start_time = "2023-03-01"
    end_time = "2023-05-01"
    data_dir = "./data_export"
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)
    client.get_market_candles(markets=binance_eth_markets, start_time=start_time, end_time=end_time, page_size=1000).parallel().export_to_csv_files(data_directory=data_dir)
