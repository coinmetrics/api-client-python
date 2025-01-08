import os
from coinmetrics.api_client import CoinMetricsClient

if __name__ == '__main__':
    # This script will create a csv file for each market orderbook listed, running them in parallel so that it is faster
    MARKET_ORDERBOOKS = [
        'binance-btc-ars-spot',
        'binance-btc-aud-spot',
        'binance-btc-bidr-spot',
        'binance-btc-brl-spot',
        'binance-btc-busd-spot',
        'binance-btc-dai-spot',
        'binance-btc-eur-spot',
        'binance-btc-fdusd-spot'
    ]
    client = CoinMetricsClient(os.environ['CM_API_KEY'])
    start_date = "2023-03-01"
    end_date = "2023-03-01"
    client.get_market_orderbooks(
        markets=MARKET_ORDERBOOKS,
        start_time=start_date,
        end_time=end_date,
        page_size=1000
    ).parallel().export_to_csv_files()
