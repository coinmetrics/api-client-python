
from coinmetrics.api_client import CoinMetricsClient

api_key = "<API_KEY>"
client = CoinMetricsClient(api_key)

data = client.get_stream_market_candles(markets='<arg values>').first_page()
print(data)
