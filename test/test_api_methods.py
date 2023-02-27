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
def test_catalog_metrics() -> None:
    """
    Tests the catalog/market-metrics endpoint works as expected - some data is returned and when converted to dataframe
    it has the expected amount of rows (5)
    """
    data = client.catalog_metrics()
    assert len(data) != 0
    data_df = data.to_dataframe()
    assert len(data_df != 0)
    assert len(data_df.columns == 5)


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalog_asset_metrics() -> None:
    """
    Tests the catalog/market-metrics endpoint works as expected - some data is returned and when converted to dataframe
    it has the expected amount of rows (5)
    """
    data = client.catalog_asset_metrics()
    assert len(data) != 0
    data_df = data.to_dataframe()
    assert len(data_df != 0)
    assert len(data_df.columns == 5)


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalog_exchange_asset_metrics() -> None:
    """
    Tests the catalog/market-metrics endpoint works as expected - some data is returned and when converted to dataframe
    it has the expected amount of rows (5)
    """
    data = client.catalog_exchange_asset_metrics()
    assert len(data) != 0
    data_df = data.to_dataframe()
    assert len(data_df != 0)
    assert len(data_df.columns == 5)


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalog_pair_metrics() -> None:
    """
    Tests the catalog/market-metrics endpoint works as expected - some data is returned and when converted to dataframe
    it has the expected amount of rows (5)
    """
    data = client.catalog_pair_metrics()
    assert len(data) != 0
    data_df = data.to_dataframe()
    assert len(data_df != 0)
    assert len(data_df.columns == 5)


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalog_exchange_metrics() -> None:
    """
    Tests the catalog/market-metrics endpoint works as expected - some data is returned and when converted to dataframe
    it has the expected amount of rows (5)
    """
    data = client.catalog_exchange_metrics()
    assert len(data) != 0
    data_df = data.to_dataframe()
    assert len(data_df != 0)
    assert len(data_df.columns == 5)


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalog_institution_metrics() -> None:
    """
    Tests the catalog/market-metrics endpoint works as expected - some data is returned and when converted to dataframe
    it has the expected amount of rows (5)
    """
    data = client.catalog_institution_metrics()
    assert len(data) != 0
    data_df = data.to_dataframe()
    assert len(data_df != 0)
    assert len(data_df.columns == 5)


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalog_market_metrics() -> None:
    """
    Tests the catalog/market-metrics endpoint works as expected - some data is returned and when converted to dataframe
    it has the expected amount of rows (5)
    """
    data = client.catalog_market_metrics()
    assert len(data) != 0
    data_df = data.to_dataframe()
    assert len(data_df != 0)
    assert len(data_df.columns == 5)


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalog_full_asset_pair_candles() -> None:
    """
    Tests the catalog-full/pair-candles endpoints works as expected - data is returned and when converted to dataframe
    it has the expected number of columns (4)
    """
    data = client.catalog_full_asset_pair_candles()
    assert len(data) != 0
    data_df = data.to_dataframe()
    assert len(data_df != 0)
    assert len(data_df.columns) == 4


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalog_full_market_trades() -> None:
    """
    Tests the catalog-full/market-trades endpoints works as expected - data is returned and when converted to dataframe
    it has the expected number of columns (3)
    """
    data = client.catalog_full_market_trades()
    assert len(data) != 0
    data_df = data.to_dataframe()
    assert len(data_df) != 0
    assert len(data_df.columns) == 3
    expected_cols = ["market", "max_time", "min_time"]
    assert all(col in expected_cols for col in data_df.columns)


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalog_full_market_orderbooks() -> None:
    """
    Tests the catalog-full/market-orderbooks endpoints works as expected - data is returned and when converted to dataframe
    it has the expected number of columns (3)
    """
    data = client.catalog_full_market_orderbooks()
    assert len(data) != 0
    data_df = data.to_dataframe()
    assert len(data_df) != 0
    assert len(data_df.columns) == 4
    expected_cols = ["market", "max_time", "min_time", "depths"]
    assert all(col in expected_cols for col in data_df.columns)


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalog_full_market_quotes() -> None:
    """
    Tests the catalog-full/market-quotes endpoints works as expected - data is returned and when converted to dataframe
    it has the expected number of columns (3)
    """
    data = client.catalog_full_market_quotes()
    assert len(data) != 0
    data_df = data.to_dataframe()
    assert len(data_df) != 0
    assert len(data_df.columns) == 3
    expected_cols = ["market", "max_time", "min_time"]
    assert all(col in expected_cols for col in data_df.columns)


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalog_market_greeks() -> None:
    """
    Tests the catalog-full/market-quotes endpoints works as expected - data is returned and when converted to dataframe
    it has the expected number of columns (3)
    """
    data = client.catalog_market_greeks()
    assert len(data) != 0
    data_df = data.to_dataframe()
    assert len(data_df) != 0
    assert len(data_df.columns) == 3
    expected_cols = ["market", "max_time", "min_time"]
    assert all(col in expected_cols for col in data_df.columns)


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalog_full_market_funding_rates() -> None:
    """
    Tests the catalog-full/market-funding-rates endpoints works as expected - data is returned and when converted to dataframe
    it has the expected number of columns (3)
    """
    data = client.catalog_full_market_funding_rates()
    assert len(data) != 0
    data_df = data.to_dataframe()
    assert len(data_df) != 0
    assert len(data_df.columns) == 3
    expected_cols = ["market", "max_time", "min_time"]
    assert all(col in expected_cols for col in data_df.columns)


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalog_full_market_openinterest() -> None:
    """
    Tests the catalog-full/market-openinterest endpoints works as expected - data is returned and when converted to dataframe
    it has the expected number of columns (3)
    """
    data = client.catalog_full_market_open_interest()
    assert len(data) != 0
    data_df = data.to_dataframe()
    assert len(data_df) != 0
    assert len(data_df.columns) == 3
    expected_cols = ["market", "max_time", "min_time"]
    assert all(col in expected_cols for col in data_df.columns)


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalog_full_market_liquidations() -> None:
    """
    Tests the catalog-full/market-openinterest endpoints works as expected - data is returned and when converted to dataframe
    it has the expected number of columns (3)
    """
    data = client.catalog_full_market_liquidations()
    assert len(data) != 0
    data_df = data.to_dataframe()
    assert len(data_df) != 0
    assert len(data_df.columns) == 3
    expected_cols = ["market", "max_time", "min_time"]
    assert all(col in expected_cols for col in data_df.columns)


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


if __name__ == "__main__":
    for data in client.get_list_of_transactions_v2(
        asset="eth", start_time="2023-02-17", end_time="2023-02-17"
    ):
        print(data)
    pytest.main()
