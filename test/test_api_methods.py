import pytest

from coinmetrics.api_client import CoinMetricsClient
import os

client = CoinMetricsClient(str(os.environ.get("CM_API_KEY")))
cm_api_key_set = os.environ.get("CM_API_KEY") is not None
REASON_TO_SKIP = "Need to set CM_API_KEY as an env var in order to run this test"

print("CM_API_KEY is set - tests will run") if cm_api_key_set else print(
    "CM_API_KEY not set, tests will not run"
)


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_timeseries_pair_candles() -> None:
    """
    Tests the timeseries/pair-candles endpoints works as expected - data is returned and the date is in the right format
    """
    data = client.get_pair_candles(pairs=["btc-usd", "eth-usd", "sol-usd"])
    assert len(data.first_page()) != 0
    expected_cols = [
        "pair",
        "time",
        "price_open",
        "price_close",
        "price_high",
        "price_low",
    ]
    assert all(col in expected_cols for col in data.first_page()[0])


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_get_list_of_transactions_v2_eth() -> None:
    """
    Tests the timeseries get list of transactions v2 for eth
    """
    transactions = client.get_list_of_transactions_v2(
        asset="eth", start_height=16644700, end_height=16644767
    ).to_list()
    assert len(transactions) >= 9800
    transactions_called_by_id = client.get_list_of_transactions_v2(
        asset="eth",
        txids="1ec9982bee6cd96049b0ac7745df4374bcd37dce996bae46d09c3d25c5cfd413",
    ).first_page()[0]
    assert (
        transactions_called_by_id["height"] == "16644767"
        and transactions_called_by_id["n_balance_updates"] == "9"
    )


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_get_list_of_balance_updates_v2() -> None:
    asset = "usdc"
    accounts = [
        "4a30ff596cc84c630b2998012b0586ff36113cba",
        "4dd384f41f3e91f2e204fd462dc0fa73aef029d4",
    ]
    updates = client.get_list_of_balance_updates_v2(
        asset=asset, accounts=accounts, limit_per_account=1
    ).to_list()
    assert len(updates) == 2


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_get_asset_profiles() -> None:
    data = client.get_asset_profiles().first_page()
    print(data)
    assert len(data) > 10
    one_inch = client.get_asset_profiles(assets="1inch").first_page()[0]
    assert one_inch["asset"] == "1inch"

@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_get_predicted_market_funding_rates() -> None:
    data = client.get_predicted_market_funding_rates(
        markets="bybit-1000000VINUUSDT-future"
    ).first_page()
    print(data)
    assert len(data) > 1
    predicted_funding_rate = data[0]
    assert predicted_funding_rate["market"] == "bybit-1000000VINUUSDT-future"


if __name__ == "__main__":
    pytest.main()
