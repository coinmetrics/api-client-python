
import pytest

from coinmetrics.api_client import CoinMetricsClient
import os

client = CoinMetricsClient(str(os.environ.get("CM_API_KEY")), verbose=True)
cm_api_key_set = os.environ.get("CM_API_KEY") is not None
REASON_TO_SKIP = "Need to set CM_API_KEY as an env var in order to run this test"

print("CM_API_KEY is set - tests will run") if cm_api_key_set else print(
    "CM_API_KEY not set, tests will not run"
)

@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_market_trades() -> None:
    catalog_market_trades = client.catalog_market_trades_v2(page_size=10).first_page()
    assert len(catalog_market_trades) == 10
    assert all(['market' in catalog for catalog in catalog_market_trades])


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_full_market_trades() -> None:
    catalog_market_trades = client.catalog_full_market_trades_v2(page_size=10).first_page()
    assert len(catalog_market_trades) == 10
    assert all(['market' in catalog for catalog in catalog_market_trades])


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_full_market_candles() -> None:
    catalog_market_candles = client.catalog_full_market_candles_v2(page_size=10).first_page()
    assert len(catalog_market_candles) == 10
    assert all(['market' in catalog for catalog in catalog_market_candles])
    assert all(['frequencies' in catalog for catalog in catalog_market_candles])


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_market_candles() -> None:
    catalog_market_candles = client.catalog_market_candles_v2(page_size=10).first_page()
    assert len(catalog_market_candles) == 10
    assert all(['market' in catalog for catalog in catalog_market_candles])
    assert all(['frequencies' in catalog for catalog in catalog_market_candles])


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_contract_prices() -> None:
    catalog_contract_prices = client.catalog_market_contract_prices_v2(page_size=10).first_page()
    assert len(catalog_contract_prices) == 10
    assert all(['market' in catalog for catalog in catalog_contract_prices])
    assert all(['min_time' in catalog for catalog in catalog_contract_prices])
    assert all(['max_time' in catalog for catalog in catalog_contract_prices])


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_full_contract_prices() -> None:
    catalog_contract_prices = client.catalog_full_market_contract_prices_v2(page_size=10).first_page()
    assert len(catalog_contract_prices) == 10
    assert all(['market' in catalog for catalog in catalog_contract_prices])
    assert all(['min_time' in catalog for catalog in catalog_contract_prices])
    assert all(['max_time' in catalog for catalog in catalog_contract_prices])


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_full_market_funding_rates() -> None:
    catalog_funding_rates = client.catalog_full_market_funding_rates_v2(page_size=10).first_page()
    assert len(catalog_funding_rates) == 10
    assert all(['market' in catalog for catalog in catalog_funding_rates])
    assert all(['min_time' in catalog for catalog in catalog_funding_rates])
    assert all(['max_time' in catalog for catalog in catalog_funding_rates])


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_market_funding_rates() -> None:
    catalog_funding_rates = client.catalog_market_funding_rates_v2(page_size=10).first_page()
    assert len(catalog_funding_rates) == 10
    assert all(['market' in catalog for catalog in catalog_funding_rates])
    assert all(['min_time' in catalog for catalog in catalog_funding_rates])
    assert all(['max_time' in catalog for catalog in catalog_funding_rates])


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_market_greeks() -> None:
    catalog_greeks = client.catalog_market_greeks_v2(page_size=10).first_page()
    assert len(catalog_greeks) == 10
    assert all(['market' in catalog for catalog in catalog_greeks])
    assert all(['min_time' in catalog for catalog in catalog_greeks])
    assert all(['max_time' in catalog for catalog in catalog_greeks])


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_full_market_greeks() -> None:
    catalog_greeks = client.catalog_full_market_greeks_v2(page_size=10).first_page()
    assert len(catalog_greeks) == 10
    assert all(['market' in catalog for catalog in catalog_greeks])
    assert all(['min_time' in catalog for catalog in catalog_greeks])
    assert all(['max_time' in catalog for catalog in catalog_greeks])


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_full_market_implied_volatility() -> None:
    catalog_market_implied_vol = client.catalog_full_market_implied_volatility_v2(page_size=10).first_page()
    assert len(catalog_market_implied_vol) == 10
    assert all(['market' in catalog for catalog in catalog_market_implied_vol])
    assert all(['min_time' in catalog for catalog in catalog_market_implied_vol])
    assert all(['max_time' in catalog for catalog in catalog_market_implied_vol])


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_market_implied_volatility() -> None:
    catalog_market_implied_vol = client.catalog_market_implied_volatility_v2(page_size=10).first_page()
    assert len(catalog_market_implied_vol) == 10
    assert all(['market' in catalog for catalog in catalog_market_implied_vol])
    assert all(['min_time' in catalog for catalog in catalog_market_implied_vol])
    assert all(['max_time' in catalog for catalog in catalog_market_implied_vol])


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_market_liquidations() -> None:
    catalog_market_liquidations = client.catalog_market_liquidations_v2(page_size=10).first_page()
    assert len(catalog_market_liquidations) == 10
    assert all(['market' in catalog for catalog in catalog_market_liquidations])
    assert all(['min_time' in catalog for catalog in catalog_market_liquidations])
    assert all(['max_time' in catalog for catalog in catalog_market_liquidations])


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_full_market_liquidations() -> None:
    catalog_market_liquidations = client.catalog_full_market_liquidations_v2(page_size=10).first_page()
    assert len(catalog_market_liquidations) == 10
    assert all(['market' in catalog for catalog in catalog_market_liquidations])
    assert all(['min_time' in catalog for catalog in catalog_market_liquidations])
    assert all(['max_time' in catalog for catalog in catalog_market_liquidations])


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_full_market_openinterest() -> None:
    catalog_market_openinterest = client.catalog_full_market_open_interest_v2(page_size=10).first_page()
    assert len(catalog_market_openinterest) == 10
    assert all(['market' in catalog for catalog in catalog_market_openinterest])
    assert all(['min_time' in catalog for catalog in catalog_market_openinterest])
    assert all(['max_time' in catalog for catalog in catalog_market_openinterest])


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_market_openinterest() -> None:
    catalog_market_openinterest = client.catalog_market_open_interest_v2(page_size=10).first_page()
    assert len(catalog_market_openinterest) == 10
    assert all(['market' in catalog for catalog in catalog_market_openinterest])
    assert all(['min_time' in catalog for catalog in catalog_market_openinterest])
    assert all(['max_time' in catalog for catalog in catalog_market_openinterest])


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_market_orderbooks() -> None:
    catalog_market_orderbooks = client.catalog_market_orderbooks_v2(page_size=10).first_page()
    assert len(catalog_market_orderbooks) == 10
    assert all(['market' in catalog for catalog in catalog_market_orderbooks])
    assert all(['depths' in catalog for catalog in catalog_market_orderbooks])


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_market_quotes() -> None:
    catalog_market_quotes = client.catalog_market_quotes_v2(page_size=10).first_page()
    assert len(catalog_market_quotes) == 10
    assert all(['market' in catalog for catalog in catalog_market_quotes])
    assert all(['min_time' in catalog for catalog in catalog_market_quotes])
    assert all(['max_time' in catalog for catalog in catalog_market_quotes])


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_full_market_quotes() -> None:
    catalog_market_quotes = client.catalog_full_market_quotes_v2(page_size=10).first_page()
    assert len(catalog_market_quotes) == 10
    assert all(['market' in catalog for catalog in catalog_market_quotes])
    assert all(['min_time' in catalog for catalog in catalog_market_quotes])
    assert all(['max_time' in catalog for catalog in catalog_market_quotes])


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_full_market_orderbooks() -> None:
    catalog_market_orderbooks = client.catalog_full_market_orderbooks_v2(page_size=10).first_page()
    assert len(catalog_market_orderbooks) == 10
    assert all(['market' in catalog for catalog in catalog_market_orderbooks])
    assert all(['depths' in catalog for catalog in catalog_market_orderbooks])

@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_full_market_metrics() -> None:
    catalog_market_metrics = client.catalog_full_market_metrics_v2(page_size=10).first_page()
    assert len(catalog_market_metrics) == 10
    assert all(['market' in catalog for catalog in catalog_market_metrics])
    assert all(['metrics' in catalog for catalog in catalog_market_metrics])


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_market_metrics() -> None:
    catalog_market_metrics = client.catalog_market_metrics_v2(page_size=10).first_page()
    assert len(catalog_market_metrics) == 10
    assert all(['market' in catalog for catalog in catalog_market_metrics])
    assert all(['metrics' in catalog for catalog in catalog_market_metrics])


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_asset_metrics() -> None:
    catalog_asset_metrics = client.catalog_asset_metrics_v2(page_size=10).first_page()
    assert len(catalog_asset_metrics) == 10
    assert all(['asset' in catalog for catalog in catalog_asset_metrics])
    assert all(['metrics' in catalog for catalog in catalog_asset_metrics])


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_full_asset_metrics() -> None:
    catalog_asset_metrics = client.catalog_full_asset_metrics_v2(page_size=10).first_page()
    assert len(catalog_asset_metrics) == 10
    assert all(['asset' in catalog for catalog in catalog_asset_metrics])
    assert all(['metrics' in catalog for catalog in catalog_asset_metrics])


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_exchange_metrics() -> None:
    catalog_exchange_metrics = client.catalog_exchange_metrics_v2(page_size=10).first_page()
    assert len(catalog_exchange_metrics) == 10
    assert all(['exchange' in catalog for catalog in catalog_exchange_metrics])
    assert all(['metrics' in catalog for catalog in catalog_exchange_metrics])


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_full_exchange_metrics() -> None:
    catalog_exchange_metrics = client.catalog_full_exchange_metrics_v2(page_size=10).first_page()
    assert len(catalog_exchange_metrics) == 10
    assert all(['exchange' in catalog for catalog in catalog_exchange_metrics])
    assert all(['metrics' in catalog for catalog in catalog_exchange_metrics])


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_exchange_asset_metrics() -> None:
    catalog_exchange_metrics = client.catalog_exchange_asset_metrics_v2(page_size=10).first_page()
    assert len(catalog_exchange_metrics) == 10
    assert all(['exchange_asset' in catalog for catalog in catalog_exchange_metrics])
    assert all(['metrics' in catalog for catalog in catalog_exchange_metrics])


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_full_exchange_asset_metrics() -> None:
    catalog_exchange_metrics = client.catalog_full_exchange_asset_metrics_v2(page_size=10).first_page()
    assert len(catalog_exchange_metrics) == 10
    assert all(['exchange_asset' in catalog for catalog in catalog_exchange_metrics])
    assert all(['metrics' in catalog for catalog in catalog_exchange_metrics])


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_exchange_pair_metrics() -> None:
    catalog_pair_metrics = client.catalog_pair_metrics_v2(page_size=10).first_page()
    assert len(catalog_pair_metrics) == 10
    assert all(['pair' in catalog for catalog in catalog_pair_metrics])
    assert all(['metrics' in catalog for catalog in catalog_pair_metrics])


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_exchange_full_pair_metrics() -> None:
    catalog_pair_metrics = client.catalog_full_pair_metrics_v2(page_size=10).first_page()
    assert len(catalog_pair_metrics) == 10
    assert all(['pair' in catalog for catalog in catalog_pair_metrics])
    assert all(['metrics' in catalog for catalog in catalog_pair_metrics])


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_institution_pair_metrics() -> None:
    catalog_institution_metrics = client.catalog_institution_metrics_v2(page_size=10).first_page()
    assert all(['institution' in catalog for catalog in catalog_institution_metrics])
    assert all(['metrics' in catalog for catalog in catalog_institution_metrics])


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_full_institution_pair_metrics() -> None:
    catalog_institution_metrics = client.catalog_full_institution_metrics_v2(page_size=10).first_page()
    assert all(['institution' in catalog for catalog in catalog_institution_metrics])
    assert all(['metrics' in catalog for catalog in catalog_institution_metrics])


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_pair_candles() -> None:
    catalog_pair_candles = client.catalog_pair_candles_v2(page_size=10).first_page()
    catalog_full_pair_candles = client.catalog_full_pair_candles_v2(page_size=10).first_page()
    assert all(['pair' in catalog for catalog in catalog_pair_candles])
    assert all(['pair' in catalog for catalog in catalog_full_pair_candles])
    assert all(['frequencies' in catalog for catalog in catalog_pair_candles])
    assert all(['frequencies' in catalog for catalog in catalog_full_pair_candles])


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_index_candles() -> None:
    catalog_index_candles = client.catalog_index_candles_v2(page_size=10).first_page()
    catalog_full_index_candles = client.catalog_full_index_candles_v2(page_size=10).first_page()
    assert all(['index' in catalog for catalog in catalog_index_candles])
    assert all(['index' in catalog for catalog in catalog_full_index_candles])
    assert all(['frequencies' in catalog for catalog in catalog_index_candles])
    assert all(['frequencies' in catalog for catalog in catalog_full_index_candles])


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_asset_chains() -> None:
    catalog_asset_chains = client.catalog_asset_chains_v2(page_size=10).first_page()
    catalog_full_asset_chains = client.catalog_full_asset_chains_v2(page_size=10).first_page()
    assert all(['asset' in catalog for catalog in catalog_asset_chains])
    assert all(['asset' in catalog for catalog in catalog_full_asset_chains])
    assert all(['min_time' in catalog for catalog in catalog_asset_chains])
    assert all(['min_time' in catalog for catalog in catalog_full_asset_chains])
    assert all(['max_time' in catalog for catalog in catalog_asset_chains])
    assert all(['max_time' in catalog for catalog in catalog_full_asset_chains])


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_mempool_feerates() -> None:
    catalog_mempool_feerates = client.catalog_mempool_feerates_v2(page_size=10).first_page()
    catalog_full_mempool_feerates = client.catalog_full_mempool_feerates_v2(page_size=10).first_page()
    assert all(['asset' in catalog for catalog in catalog_mempool_feerates])
    assert all(['asset' in catalog for catalog in catalog_full_mempool_feerates])
    assert all(['min_time' in catalog for catalog in catalog_mempool_feerates])
    assert all(['min_time' in catalog for catalog in catalog_full_mempool_feerates])
    assert all(['max_time' in catalog for catalog in catalog_mempool_feerates])
    assert all(['max_time' in catalog for catalog in catalog_full_mempool_feerates])


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_mining_pool_tips() -> None:
    catalog_mining_pool_tips = client.catalog_asset_chains_v2(page_size=10).first_page()
    catalog_full_mining_pool_tips = client.catalog_full_asset_chains_v2(page_size=10).first_page()
    assert all(['asset' in catalog for catalog in catalog_mining_pool_tips])
    assert all(['asset' in catalog for catalog in catalog_full_mining_pool_tips])
    assert all(['min_time' in catalog for catalog in catalog_mining_pool_tips])
    assert all(['min_time' in catalog for catalog in catalog_full_mining_pool_tips])
    assert all(['max_time' in catalog for catalog in catalog_mining_pool_tips])
    assert all(['max_time' in catalog for catalog in catalog_full_mining_pool_tips])


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_transaction_tracker() -> None:
    catalog_transaction_tracker = client.catalog_transaction_tracker_assets_v2(page_size=10).first_page()
    catalog_full_transaction_tracker = client.catalog_full_transaction_tracker_assets_v2(page_size=10).first_page()
    assert all(['asset' in catalog for catalog in catalog_transaction_tracker])
    assert all(['asset' in catalog for catalog in catalog_full_transaction_tracker])
    assert all(['min_time' in catalog for catalog in catalog_transaction_tracker])
    assert all(['min_time' in catalog for catalog in catalog_full_transaction_tracker])
    assert all(['max_time' in catalog for catalog in catalog_transaction_tracker])
    assert all(['max_time' in catalog for catalog in catalog_full_transaction_tracker])


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_index_levels() -> None:
    catalog_index_levels = client.catalog_index_levels_v2(page_size=10).first_page()
    catalog_all_index_levels = client.catalog_index_levels_v2(page_size=10).first_page()
    assert all(['index' in catalog for catalog in catalog_all_index_levels])
    assert all(['index' in catalog for catalog in catalog_all_index_levels])
    assert all(['frequencies' in catalog for catalog in catalog_index_levels])
    assert all(['frequencies' in catalog for catalog in catalog_all_index_levels])


if __name__ == '__main__':
    pytest.main()