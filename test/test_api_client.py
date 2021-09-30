from typing import Any
from unittest.mock import Mock

from coinmetrics.api_client import CoinMetricsClient, requests
from coinmetrics._data_collection import DataCollection


def test_catalog_assets_request(mocker: Any) -> None:
    client = CoinMetricsClient("xxx")
    mock = Mock()
    mock.content = '{"data": [{"asset": "btc", "markets": ["coinbase-btc-usd-spot"]}]}'
    mocked_obj = mocker.patch.object(requests, "get", return_value=mock)
    response = client.catalog_assets(assets="btc")
    mocked_obj.assert_called_once_with(
        "https://api.coinmetrics.io/v4/catalog/assets?api_key=xxx&assets=btc"
    )
    assert response == [{"asset": "btc", "markets": ["coinbase-btc-usd-spot"]}]


def test_base_url() -> None:
    assert CoinMetricsClient("xxx")._api_base_url == "https://api.coinmetrics.io/v4"
    assert CoinMetricsClient("xxx")._api_key_url_str == "api_key=xxx"
    assert (
        CoinMetricsClient()._api_base_url == "https://community-api.coinmetrics.io/v4"
    )
    assert CoinMetricsClient()._api_key_url_str == ""

def test_to_dataframe() -> None:
    test_param_dict = {'asset': 'btc', 'metric': '1'}
    test_data_dict = {'data': [test_param_dict for i in range(2)]}
    test_data_iter = iter([test_data_dict])
    test_header = ['col1', 'col2']

    def test_data_retrieval_function(p1, p2): return test_data_dict

    test_data_collection = DataCollection(
        data_retrieval_function=test_data_retrieval_function,
        endpoint="",
        url_params=test_param_dict
    )
    test_df = test_data_collection.to_dataframe()
    assert test_df.shape == (2, 2)
    assert list(test_param_dict.keys()) == list(test_df.columns)
    assert (test_df['asset'] == 'btc').all()

    test_data_collection_header = DataCollection(
        data_retrieval_function=test_data_retrieval_function,
        endpoint="",
        url_params=test_param_dict
    )
    test_df_header = test_data_collection_header.to_dataframe(header=test_header)
    assert list(test_df_header.columns) == test_header
