
from coinmetrics.api_client import CoinMetricsClient

api_key = "<API_KEY>"
client = CoinMetricsClient(api_key)

data = client.get_asset_metrics(assets='<arg values>', metrics='<arg values>').first_page()
print(data)
