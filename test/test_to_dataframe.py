import pandas as pd  # type: ignore
import pytest
from coinmetrics.api_client import CoinMetricsClient
import os

CM_API_KEY = os.environ.get("CM_API_KEY")
client = CoinMetricsClient(str(CM_API_KEY))
cm_api_key_set = CM_API_KEY is not None
REASON_TO_SKIP = "Need to set CM_API_KEY as an env var in order to run this test"


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_secondary_level_catalog_assets() -> None:
    """
    Tests that the secondary expansion functions works as expected - there is one row created for each secondary level
    expansion
    """
    catalog_assets: pd.DataFrame = client.catalog_assets().to_dataframe()
    catalog_assets_metrics_expansion: pd.DataFrame = (
        client.catalog_assets().to_dataframe(secondary_level="metrics")
    )
    catalog_assets_usdc_metrics = catalog_assets[
        catalog_assets["asset"] == "usdc"
    ].iloc[0]["metrics"]
    usdc_metrics = catalog_assets_metrics_expansion[
        catalog_assets_metrics_expansion["asset"] == "usdc"
    ]["metric"]
    usdc_metrics_unique = set(usdc_metrics)
    assert len(usdc_metrics_unique) == len(catalog_assets_usdc_metrics)
    assert len(usdc_metrics_unique) > 100

    catalog_assets_markets_expansion: pd.DataFrame = (
        client.catalog_assets().to_dataframe(secondary_level="markets")
    )
    catalog_assets_usdc_markets = catalog_assets[
        catalog_assets["asset"] == "usdc"
    ].iloc[0]["markets"]
    usdc_markets = catalog_assets_markets_expansion[
        catalog_assets_markets_expansion["asset"] == "usdc"
    ]["market"]
    usdc_markets_unqiue = set(usdc_markets)
    assert len(usdc_markets_unqiue) == len(catalog_assets_usdc_markets)


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_secondary_level_catalog_morderbooks() -> None:
    """
    Tests that the binance-BTCUSDT-future expands into multiple rows as expected
    """
    market_to_test = "binance-BTCUSDT-future"
    catalog_orderbooks = client.catalog_market_orderbooks().to_dataframe()
    catalog_orderbooks_depths_expansion = (
        client.catalog_market_orderbooks().to_dataframe(secondary_level="depths")
    )
    catalog_orderbooks_market_depths = catalog_orderbooks[
        catalog_orderbooks["market"] == market_to_test
    ].iloc[0]["depths"]
    catalog_orderbooks_depths_expansion_market = catalog_orderbooks_depths_expansion[
        catalog_orderbooks_depths_expansion["market"] == market_to_test
    ]
    assert len(catalog_orderbooks_market_depths) == len(
        catalog_orderbooks_depths_expansion_market
    )
    assert len(catalog_orderbooks_market_depths) > 1


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_secondary_level_catalog_asset_alerts() -> None:
    """
    Probably not worth implementing secondary level in this case - this test just confirms this doesn't break, it
    previously was broken due to changes in data model
    """
    catalog_asset_alerts = client.catalog_asset_alerts().to_dataframe()
    conditions = list(catalog_asset_alerts["conditions"])
    for item in conditions:
        print(item)
    print("test!")


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalog_asset_pairs_to_df() -> None:
    """
    Just a sanity test, no relevant secondary level here
    """
    catalog_asset_pairs: pd.DataFrame = client.catalog_asset_pairs().to_dataframe()
    assert len(catalog_asset_pairs) > 5


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalog_exchanges_secondary_level() -> None:
    """
    Checks that the binance exchange is expanded the expected way - for metrics same amount of rows as there are unique
    metric and same amount of rows as there are markets
    """
    exchange_to_test = "binance"
    catalog_exchanges = client.catalog_exchanges().to_dataframe()
    catalog_exchanges_metrics_expansion = client.catalog_exchanges().to_dataframe(
        secondary_level="metrics"
    )
    catalog_exchanges_metrics = catalog_exchanges[
        catalog_exchanges["exchange"] == exchange_to_test
    ].iloc[0]["metrics"]
    metrics_expansion_metrics = set(
        catalog_exchanges_metrics_expansion[
            catalog_exchanges_metrics_expansion["exchange"] == exchange_to_test
        ]["metric"]
    )
    assert len(catalog_exchanges_metrics) == len(metrics_expansion_metrics)
    assert len(metrics_expansion_metrics) > 1

    catalog_exchange_markets = catalog_exchanges[
        catalog_exchanges["exchange"] == exchange_to_test
    ].iloc[0]["markets"]
    catalog_exchange_markets_expansion = client.catalog_exchanges().to_dataframe(
        secondary_level="markets"
    )
    markets_expansion_markets = catalog_exchange_markets_expansion[
        catalog_exchange_markets_expansion["exchange"] == exchange_to_test
    ]["market"]
    assert len(catalog_exchange_markets) == len(markets_expansion_markets)


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalog_asset_metrics() -> None:
    """
    No extensive testing needed, just checks that a dataframe is created
    """
    asset_metrics = client.catalog_asset_metrics().to_dataframe()
    assert len(asset_metrics) > 100


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalog_exchange_metrics() -> None:
    """
    No extensive testing is needed, just checks dataframe is created
    """
    exchange_metrics = client.catalog_exchange_metrics().to_dataframe()
    assert len(exchange_metrics) > 10


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalog_exchange_asset_metrics() -> None:
    """
    No extensive testing needed, just checks dataframe is created
    """
    exchange_asset_metrics = client.catalog_exchange_asset_metrics().to_dataframe()
    assert len(exchange_asset_metrics) > 20


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalog_pair_metrics() -> None:
    """
    No extensive testing needed, just checks dataframe is created
    """
    pair_metrics = client.catalog_pair_metrics().to_dataframe()
    assert len(pair_metrics) > 100
    print("test!")


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalog_institution_metrics() -> None:
    """
    No extensive testing needed, just checks dataframe is created
    """
    inst_metrics = client.catalog_institution_metrics().to_dataframe()
    assert len(inst_metrics) > 20


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalog_asset_pair_candles() -> None:
    """
    No extensive testing needed, just checks dataframe is created
    """
    pair_candles = client.catalog_asset_pair_candles().to_dataframe()
    assert len(pair_candles) > 10


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalog_indexes() -> None:
    """
    No extensive testing needed, just checks dataframe is created
    """
    indexes = client.catalog_indexes().to_dataframe()
    assert len(indexes) > 10


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalog_index_candles() -> None:
    """
    No extensive testing needed, just checks dataframe is created
    """
    indexes = client.catalog_index_candles().to_dataframe()
    assert len(indexes) > 10


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalog_institutions() -> None:
    """
    No extensive testing needed, just checks dataframe is created
    """
    institutions = client.catalog_institutions().to_dataframe()
    assert len(institutions) > 10


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalog_markets() -> None:
    """
    No extensive testing needed, just checks dataframe is created
    """
    catalog_markets = client.catalog_markets(exchange="coinbase").to_dataframe()
    assert len(catalog_markets) > 10


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalog_market_trades() -> None:
    """
    No extensive testing needed, just checks dataframe is created
    """
    catalog_market_trades = client.catalog_market_trades().to_dataframe()
    assert len(catalog_market_trades) > 20


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalog_metrics() -> None:
    """
    No extensive testing needed, just checks dataframe is created
    """
    catalog_metrics = client.catalog_metrics().to_dataframe()
    assert len(catalog_metrics) > 100


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalog_market_metrics() -> None:
    """
    No extensive testing needed, just checks dataframe is created
    """
    catalog_market_metrics = client.catalog_market_metrics(
        exchange="coinbase"
    ).to_dataframe()
    assert len(catalog_market_metrics) > 20


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalog_market_candles() -> None:
    """
    No extensive testing needed, just checks dataframe is created
    """
    catalog_market_candles = client.catalog_market_candles(
        exchange="coinbase"
    ).to_dataframe()
    assert len(catalog_market_candles) > 50


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalog_market_quotes() -> None:
    """
    No extensive testing needed, just checks dataframe is created
    """
    catalog_market_quotes = client.catalog_market_quotes().to_dataframe()
    assert len(catalog_market_quotes) > 100


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalog_market_funding_rates() -> None:
    """
    No extensive testing needed, just checks dataframe is created
    """
    catalog_market_funding_rates = client.catalog_market_funding_rates().to_dataframe()
    assert len(catalog_market_funding_rates) > 100


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalog_market_greeks() -> None:
    """
    No extensive testing needed, just checks dataframe is created
    """
    catalog_market_greeks = client.catalog_market_greeks().to_dataframe()
    assert len(catalog_market_greeks) > 100


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalog_market_openinterest() -> None:
    """
    No extensive testing needed, just checks dataframe is created
    """
    catalog_open_interest = client.catalog_market_open_interest().to_dataframe()
    assert len(catalog_open_interest) > 100


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalog_market_liquidations() -> None:
    """
    No extensive testing needed, just checks dataframe is created
    """
    catalog_liquidations = client.catalog_market_liquidations().to_dataframe()
    assert len(catalog_liquidations) > 100


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_defi_balance_sheets() -> None:
    """
    Testing this works for aave
    """
    aave_balance_sheets = client.get_defi_balance_sheets(
        defi_protocols="aave_v2_eth"
    ).to_dataframe()
    assert len(aave_balance_sheets) > 100
    assert aave_balance_sheets.iloc[:1]["defi_protocol"][0] == "aave_v2_eth"


if __name__ == "__main__":
    pytest.main()
