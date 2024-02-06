
from coinmetrics.api_client import CoinMetricsClient

api_key = "<API_KEY>"
client = CoinMetricsClient(api_key)

data = client.get_asset_alerts(assets='<arg values>', alerts='<arg values>').first_page()
print(data)
