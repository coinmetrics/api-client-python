
from coinmetrics.api_client import CoinMetricsClient

api_key = "<API_KEY>"
client = CoinMetricsClient(api_key)

data = client.get_timeframes_of_asset_metric_constituents(metric='<arg values>').first_page()
print(data)
