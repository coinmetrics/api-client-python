
from coinmetrics.api_client import CoinMetricsClient

api_key = "<API_KEY>"
client = CoinMetricsClient(api_key)

data = client.get_institution_metrics(institutions='<arg values>', metrics='<arg values>').first_page()
print(data)
