import os
from coinmetrics.api_client import CoinMetricsClient

client = CoinMetricsClient(os.environ["CM_API_KEY"])

if __name__ == "__main__":
    markets = [market["market"] for market in client.catalog_markets()]
    intentional_414 = client.catalog_markets(markets=markets)
    print("test")
