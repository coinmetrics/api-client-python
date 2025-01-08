## Debugging the API Client
There are two additional options for the API Client - `debug_mode` and `verbose`. These two options log network calls 
to the console, and in the case of `debug_mode` it will generate a log file of all the network requests and the time
it takes to call them. These tools can be used to diagnose issues in your code and also to get a better understanding 
of request times so that users can write more performant code. For example, running the below code:
```python
import os

from coinmetrics.api_client import CoinMetricsClient

api_key = os.environ['CM_API_KEY']

if __name__ == '__main__':
    client = CoinMetricsClient(api_key=api_key, debug_mode=True)
    reference_rates_example = client.get_asset_metrics(assets=['btc', 'algo', 'eth'], metrics=['ReferenceRateUSD'])
    for data in reference_rates_example:
        continue
```

The console output will look like:
```commandline
[DEBUG] 2023-01-09 11:01:02,044 - Starting API Client debugging session. logging to stdout and cm_api_client_debug_2023_01_09_11_01_02.txt
[DEBUG] 2023-01-09 11:01:02,044 - Using coinmetrics version 2022.11.14.16
[DEBUG] 2023-01-09 11:01:02,044 - Current state of API Client, excluding API KEY: {'_verify_ssl_certs': True, '_api_base_url': 'https://api.coinmetrics.io/v4', '_ws_api_base_url': 'wss://api.coinmetrics.io/v4', '_http_header': {'Api-Client-Version': '2022.11.14.16'}, '_proxies': {'http': None, 'https': None}, 'debug_mode': True, 'verbose': False}
[DEBUG] 2023-01-09 11:01:02,044 - Attempting to call url: timeseries/asset-metrics with params: {'assets': ['btc', 'algo', 'eth'], 'metrics': ['ReferenceRateUSD'], 'frequency': None, 'page_size': None, 'paging_from': 'start', 'start_time': None, 'end_time': None, 'start_height': None, 'end_height': None, 'start_inclusive': None, 'end_inclusive': None, 'timezone': None, 'sort': None, 'limit_per_asset': None}
[DEBUG] 2023-01-09 11:01:02,387 - Response status code: 200 for url: https://api.coinmetrics.io/v4/timeseries/asset-metrics?api_key=[REDACTED]&assets=btc%2Calgo%2Ceth&metrics=ReferenceRateUSD&paging_from=start took: 0:00:00.342874 response body size (bytes): 9832
[DEBUG] 2023-01-09 11:01:02,388 - Attempting to call url: timeseries/asset-metrics with params: {'assets': ['btc', 'algo', 'eth'], 'metrics': ['ReferenceRateUSD'], 'frequency': None, 'page_size': None, 'paging_from': 'start', 'start_time': None, 'end_time': None, 'start_height': None, 'end_height': None, 'start_inclusive': None, 'end_inclusive': None, 'timezone': None, 'sort': None, 'limit_per_asset': None, 'next_page_token': '0.MjAxOS0wOS0zMFQwMDowMDowMFo'}
[DEBUG] 2023-01-09 11:01:02,559 - Response status code: 200 for url: https://api.coinmetrics.io/v4/timeseries/asset-metrics?api_key=[REDACTED]&assets=btc%2Calgo%2Ceth&metrics=ReferenceRateUSD&paging_from=start&next_page_token=0.MjAxOS0wOS0zMFQwMDowMDowMFo took: 0:00:00.171487 response body size (bytes): 9857
```
Then it can be easier to understand what network calls the API Client is making, and where any issues may exist. If you
wish to dig even deeper, you may consider modifying the `_send_request()` method of the API Client to log additional 
data about the state of your environment, or anything else that would help diagnose issues. You will notice a log file
generated in the format `cm_api_client_debug_2023_01_09_11_01_02.txt`. This log file might be helpful for your own use
or to give more context if you are working with Coin Metrics customer success. 

### SSL Certs Verification

Sometimes your organization network have special rules on SSL certs verification and in this case you might face the
following error when running the script:
```text
SSLError: HTTPSConnectionPool(host='api.coinmetrics.io', port=443): Max retries exceeded with url: <some_url_path> (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self signed certificate in certificate chain (_ssl.c:1123)')))
```

In this case, you can pass an option during client initialization to disable ssl verification for requests like this:

```python

client = CoinMetricsClient(verify_ssl_certs=False)
```

We don't recommend setting it to False by default and you should make sure you understand the security risks of disabling SSL certs verification.

Additionally, you may choose to specify the path to the SSL certificates on your machine. This may cause errors where 
Python is unable to locate the certificates on your machine, particularly when using Python virtual environments. 

```python
from coinmetrics.api_client import CoinMetricsClient
SSL_CERT_LOCATION = '/Users/<USER_NAME>/Library/Python/3.8/lib/python/site-packages/certifi/cacert.pem'
client = CoinMetricsClient(verify_ssl_certs=SSL_CERT_LOCATION)
```

A quick way to find the certs on your machine is:  
`python3 -c "import requests; print(requests.certs.where())"`  
And note that this will change based on whether or not you are using a [Python virtual environment or not](https://realpython.com/python-virtual-environments-a-primer/)

## Installation Issues

### Installing Behind a Private Network
Related to SSL Certs verification, you may have trouble installing and updating PyPi packages to your local environment.
So you may need to choose the best solution for your company and environment - either using package managers or
installing offline.

### Installing using package managers
Full instructions for setting up your environment to use conda, pip, yarn, npm, etc. can be [found here](https://medium.com/@iffi33/dealing-with-ssl-authentication-on-a-secure-corporate-network-pip-conda-git-npm-yarn-bower-73e5b93fd4b2).
Additionally, a workaround to disable SSL verification when installing a trusted Python package is this:  
```commandline
pip install --trusted-host pypi.python.org <packagename>
```  
Although it is important to make sure you understand the risks associated with disabling SSL verification and ensure 
compliance with company policies.


### Installing Python Packages Locally
It may be easier to download and install the package locally. Steps:  

1. Download the files for the [Coin Metrics API Client from PyPi](https://pypi.org/project/coinmetrics-api-client/#files)
2. [Install it locally](https://packaging.python.org/en/latest/tutorials/installing-packages/#installing-from-local-archives)

## Requests Proxy
Sometimes your organization has special rules on making requests to third parties and you have to use proxies in order to comply with the rules.

For proxies that don't require auth you can specify them similar to this example:
```python

client = CoinMetricsClient(proxy_url=f'http://<hostname>:<port>')
```

For proxies that require auth, you should be able to specify username and password similar to this example:
```python

client = CoinMetricsClient(proxy_url=f'http://<username>:<password>@<hostname>:<port>')
```
