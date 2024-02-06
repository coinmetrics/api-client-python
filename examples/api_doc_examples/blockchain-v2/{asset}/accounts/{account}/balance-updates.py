
from coinmetrics.api_client import CoinMetricsClient

api_key = "<API_KEY>"
client = CoinMetricsClient(api_key)

data = client.get_list_of_balance_updates_for_account_v2(asset='<arg values>', account='<arg values>').first_page()
print(data)
