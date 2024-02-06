
from coinmetrics.api_client import CoinMetricsClient

api_key = "<API_KEY>"
client = CoinMetricsClient(api_key)

data = client.get_predicted_market_funding_rates(markets='<params>').first_page()
print(data)
