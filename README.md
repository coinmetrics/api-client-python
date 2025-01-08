<h1 align="center"><b>Coin Metrics Python API Client</b></h1>

<p align="center">
  <img src="assets/images/cm-dark-combination.png">
</p>

The **Coin Metrics Python API Client** is the official Python wrapper for the [Coin Metrics API](https://docs.coinmetrics.io/api/v4), allowing you to access [Coin Metrics data](https://docs.coinmetrics.io/) using Python. In just a few lines of code, anyone can access clean cryptocurrency data in a familiar form, such as a pandas dataframe.

This tool offers the following convenient features over simply using `requests` to query the Coin Metrics API:

- **Automatic Pagination**. The Coin Metrics API limits most endpoints to no more than 10,000 entries, requiring users to handle pagination. The Python API Client handles this automatically.
- **DataFrames**. Users may access Coin Metrics data using pandas DataFrames and potentially other data structures, such as polars.
- **Data Exports**. Users may export API outputs to CSV and JSON files.
- **Typing**. DataFrames are automatically converted to the appropriate data types.
- **Parallelization**. Users may submit many requests at once to extract data much more quickly than sending one request at a time.


# Getting Started

## Installation and Updates
To install the client you can run the following command:
```
pip install coinmetrics-api-client
```

Note that the client is updated regularly to reflect the changes made in [API v4](https://docs.coinmetrics.io/api/v4). Ensure that your latest version matches with what's in [pyPI](https://pypi.org/project/coinmetrics-api-client/) 

To update your version, run the following command:
```
pip install coinmetrics-api-client -U
```

## Initialization

To initialize the client you should use your API key, and the CoinMetricsClient class like the following.
```python
from coinmetrics.api_client import CoinMetricsClient
import os

# we recommend storing your Coin Metrics API key in an environment variable
api_key = os.environ.get("CM_API_KEY")
client = CoinMetricsClient(api_key)

# or to use community API:
client = CoinMetricsClient()
```