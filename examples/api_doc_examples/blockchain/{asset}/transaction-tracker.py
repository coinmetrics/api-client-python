
from coinmetrics.api_client import CoinMetricsClient

api_key = "<API_KEY>"
client = CoinMetricsClient(api_key)

data = client.get_transaction_tracker(asset='<arg values>').first_page()
print(data)
