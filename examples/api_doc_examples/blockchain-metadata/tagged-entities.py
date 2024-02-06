
from coinmetrics.api_client import CoinMetricsClient

api_key = "<API_KEY>"
client = CoinMetricsClient(api_key)

data = client.blockchain_metadata_tagged_entities().first_page()
print(data)
