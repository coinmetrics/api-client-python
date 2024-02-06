
from coinmetrics.api_client import CoinMetricsClient

api_key = "<API_KEY>"
client = CoinMetricsClient(api_key)

data = client.catalog_full_market_open_interest_v2().first_page()
print(data)
