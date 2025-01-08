import os
from coinmetrics.api_client import CoinMetricsClient

if __name__ == '__main__':
    """
    This will split the normal single request into one request per binance eth market, and then create a json file 
    for each query
    """
    client = CoinMetricsClient(os.environ['CM_API_KEY'])
    binance_eth_markets = [market['market'] for market in client.catalog_market_candles(exchange="binance", base="eth")]
    start_time = "2023-03-01"
    end_time = "2023-05-01"
    if not os.path.exists("./data_export"):
        os.mkdir("./data_export")
    client.get_market_candles(markets=binance_eth_markets, start_time=start_time, end_time=end_time,
                              page_size=1000).parallel().export_to_json_files("./data_export")
