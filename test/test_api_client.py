from unittest.mock import Mock

from coinmetrics.api_client import CoinMetricsClient, requests


def test_catalog_assets_request(mocker):
    client = CoinMetricsClient("xxx")
    mock = Mock()
    mock.content = '{"data": [{"asset": "btc", "markets": ["coinbase-btc-usd-spot"]}]}'
    mocked_obj = mocker.patch.object(requests, "get", return_value=mock)
    response = client.catalog_assets(assets="btc")
    mocked_obj.assert_called_once_with(
        "https://api.coinmetrics.io/v4/catalog/assets?api_key=xxx&assets=btc"
    )
    assert response == [{"asset": "btc", "markets": ["coinbase-btc-usd-spot"]}]


def test_base_url():
    assert CoinMetricsClient("xxx")._api_base_url == "https://api.coinmetrics.io/v4"
    assert CoinMetricsClient("xxx")._api_key_url_str == "api_key=xxx"
    assert (
        CoinMetricsClient()._api_base_url == "https://community-api.coinmetrics.io/v4"
    )
    assert CoinMetricsClient()._api_key_url_str == ""
