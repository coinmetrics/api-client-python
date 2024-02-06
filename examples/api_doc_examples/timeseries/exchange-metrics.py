
from coinmetrics.api_client import CoinMetricsClient

api_key = "<API_KEY>"
client = CoinMetricsClient(api_key)

data = client.get_exchange_metrics(exchanges='<arg values>', metrics='<arg values>').first_page()
print(data)
