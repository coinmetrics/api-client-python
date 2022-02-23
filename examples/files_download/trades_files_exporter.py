import sys
from os import makedirs

import requests
from requests.auth import HTTPBasicAuth

base_url = 'https://files.coinmetrics.io/api/'

api_key = sys.argv[1]
auth = HTTPBasicAuth(api_key, '')


def get_exchange_markets_data_files(exchange_name):
    root_dir = requests.get(base_url, auth=auth).json()
    for directory in root_dir:
        if 'trades' in directory['name']:
            yield from list_markets_data_files(directory, exchange_name)


def list_markets_data_files(root_dir, exchange_name):
    trades_root_dir = base_url + root_dir['name']
    trades_directory_list = requests.get(trades_root_dir, auth=auth).json()
    for market_dir in trades_directory_list:
        if exchange_name in market_dir['name']:
            market_root = trades_root_dir + '/' + market_dir['name']
            market_files = requests.get(market_root, auth=auth).json()
            for market_day_file in market_files:
                yield market_dir['name'], market_day_file['name'], market_root + '/' + market_day_file['name']


for market, date_file, data_file in get_exchange_markets_data_files('binance'):
    print(market, date_file, data_file)
    resp = requests.get(data_file, auth=auth)
    makedirs(market, exist_ok=True)
    with open(f'{market}/{date_file}', 'wb') as f:
        f.write(resp.content)
