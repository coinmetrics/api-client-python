import datetime

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
    assert all(['min_time' in catalog for catalog in catalog_market_orderbooks])
    assert all(['max_time' in catalog for catalog in catalog_market_orderbooks])


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
    assert all(['min_time' in catalog for catalog in catalog_market_orderbooks])
    assert all(['max_time' in catalog for catalog in catalog_market_orderbooks])

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


if __name__ == '__main__':
    pytest.main()