
from coinmetrics.api_client import CoinMetricsClient

api_key = "<API_KEY>"
client = CoinMetricsClient(api_key)

data = client.get_pair_metrics(pairs='<arg values>', metrics='<arg values>').first_page()
print(data)
