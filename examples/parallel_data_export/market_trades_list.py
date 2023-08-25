import os
from coinmetrics.api_client import CoinMetricsClient

if __name__ == '__main__':
    """
    This script will create a list of market trades, running the different markets in different queries and combining them 
    at the end in order to improve performance
    """
    client = CoinMetricsClient(os.environ['CM_API_KEY'])
    MARKETS = [
        'coinbase-1inch-btc-spot',
        'coinbase-aave-btc-spot',
        'coinbase-ada-btc-spot',
        'coinbase-algo-btc-spot',
        'coinbase-ankr-btc-spot',
        'coinbase-atom-btc-spot',
        'coinbase-avax-btc-spot',
        'coinbase-axs-btc-spot',
        'coinbase-bal-btc-spot',
        'coinbase-band-btc-spot',
        'coinbase-bat-btc-spot',
        'coinbase-bch-btc-spot'
    ]
    START_DATE = "2023-03-01"
    END_DATE = "2023-03-30"
    fast_list_of_data = client.get_market_trades(markets=MARKETS, start_time=START_DATE, end_time=END_DATE, page_size=1000).parallel().to_list()
