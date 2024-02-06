
from coinmetrics.api_client import CoinMetricsClient

api_key = "<API_KEY>"
client = CoinMetricsClient(api_key)

data = client.get_market_implied_volatility(markets='<arg values>').first_page()
print(data)
