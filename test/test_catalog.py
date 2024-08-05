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