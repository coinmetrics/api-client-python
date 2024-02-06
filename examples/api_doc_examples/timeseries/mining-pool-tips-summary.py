
from coinmetrics.api_client import CoinMetricsClient

api_key = "<API_KEY>"
client = CoinMetricsClient(api_key)

data = client.get_mining_pool_tips_summary(assets='<arg values>').first_page()
print(data)
