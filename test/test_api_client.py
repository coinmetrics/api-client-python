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
    client = CoinMetricsClient()

    df_blk_test = client.get_asset_metrics(
        assets='btc',
        metrics=['BlkCnt'],
        start_time='2019-10-19T00:00:00Z',
        end_time='2019-10-19T00:00:05Z',
        limit_per_asset=1
    ).to_dataframe()

    assert (df_blk_test['asset'] == 'btc').all()
    assert 'BlkCnt' in df_blk_test.columns
    assert df_blk_test.shape[0] == 1
