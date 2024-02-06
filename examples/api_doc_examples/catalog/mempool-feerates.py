
from coinmetrics.api_client import CoinMetricsClient

api_key = "<API_KEY>"
client = CoinMetricsClient(api_key)

data = client.catalog_mempool_feerates().first_page()
print(data)
