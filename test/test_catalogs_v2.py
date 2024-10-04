
import pytest

from coinmetrics.api_client import CoinMetricsClient
from coinmetrics._utils import get_keys_from_catalog
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
    df_market_trades = client.catalog_market_trades_v2(markets="coinbase-btc-usd-spot").to_dataframe()
    list_market_trades = client.catalog_market_trades_v2(markets="coinbase-btc-usd-spot").to_list()
    catalog_fields = get_keys_from_catalog(list_market_trades[0])
    assert set(df_market_trades.columns) == catalog_fields


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_full_market_trades() -> None:
    catalog_market_trades = client.catalog_full_market_trades_v2(page_size=10).first_page()
    assert len(catalog_market_trades) == 10
    assert all(['market' in catalog for catalog in catalog_market_trades])
    df_market_trades = client.catalog_full_market_trades_v2(markets="coinbase-btc-usd-spot").to_dataframe()
    list_market_trades = client.catalog_full_market_trades_v2(markets="coinbase-btc-usd-spot").to_list()
    catalog_fields = get_keys_from_catalog(list_market_trades[0])
    assert set(df_market_trades.columns) == catalog_fields


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_full_market_candles() -> None:
    catalog_market_candles = client.catalog_full_market_candles_v2(page_size=10).first_page()
    assert len(catalog_market_candles) == 10
    assert all(['market' in catalog for catalog in catalog_market_candles])
    assert all(['frequencies' in catalog for catalog in catalog_market_candles])
    df_market_candles = client.catalog_full_market_candles_v2(markets="coinbase-btc-usd-spot").to_dataframe()
    list_market_candles = client.catalog_full_market_candles_v2(markets="coinbase-btc-usd-spot").to_list()
    catalog_fields = get_keys_from_catalog(list_market_candles[0])
    assert set(df_market_candles.columns) == catalog_fields


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_market_candles() -> None:
    catalog_market_candles = client.catalog_market_candles_v2(page_size=10).first_page()
    assert len(catalog_market_candles) == 10
    assert all(['market' in catalog for catalog in catalog_market_candles])
    assert all(['frequencies' in catalog for catalog in catalog_market_candles])
    df_market_candles = client.catalog_market_candles_v2(markets="coinbase-btc-usd-spot").to_dataframe()
    list_market_candles = client.catalog_market_candles_v2(markets="coinbase-btc-usd-spot").to_list()
    catalog_fields = get_keys_from_catalog(list_market_candles[0])
    assert set(df_market_candles.columns) == catalog_fields


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_contract_prices() -> None:
    catalog_contract_prices = client.catalog_market_contract_prices_v2(page_size=10).first_page()
    assert len(catalog_contract_prices) == 10
    assert all(['market' in catalog for catalog in catalog_contract_prices])
    assert all(['min_time' in catalog for catalog in catalog_contract_prices])
    assert all(['max_time' in catalog for catalog in catalog_contract_prices])
    df_market_contract_prices = client.catalog_market_contract_prices_v2(markets="deribit-BTC-15OCT21-60000-C-option").to_dataframe()
    list_market_contract_prices = client.catalog_market_contract_prices_v2(markets="deribit-BTC-15OCT21-60000-C-option").to_list()
    catalog_fields = get_keys_from_catalog(list_market_contract_prices[0])
    assert set(df_market_contract_prices.columns) == catalog_fields


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_full_contract_prices() -> None:
    catalog_contract_prices = client.catalog_full_market_contract_prices_v2(page_size=10).first_page()
    assert len(catalog_contract_prices) == 10
    assert all(['market' in catalog for catalog in catalog_contract_prices])
    assert all(['min_time' in catalog for catalog in catalog_contract_prices])
    assert all(['max_time' in catalog for catalog in catalog_contract_prices])
    df_market_contract_prices = client.catalog_full_market_contract_prices_v2(markets="deribit-BTC-15OCT21-60000-C-option").to_dataframe()
    list_market_contract_prices = client.catalog_full_market_contract_prices_v2(markets="deribit-BTC-15OCT21-60000-C-option").to_list()
    catalog_fields = get_keys_from_catalog(list_market_contract_prices[0])
    assert set(df_market_contract_prices.columns) == catalog_fields


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_full_market_funding_rates() -> None:
    catalog_funding_rates = client.catalog_full_market_funding_rates_v2(page_size=10).first_page()
    assert len(catalog_funding_rates) == 10
    assert all(['market' in catalog for catalog in catalog_funding_rates])
    assert all(['min_time' in catalog for catalog in catalog_funding_rates])
    assert all(['max_time' in catalog for catalog in catalog_funding_rates])
    df_market_funding_rates = client.catalog_full_market_funding_rates_v2(
        markets='binance-1000BONKUSDC-future'
    ).to_dataframe()
    list_market_funding_rates = client.catalog_full_market_funding_rates_v2(
        markets='binance-1000BONKUSDC-future'
    ).to_list()
    catalog_fields = get_keys_from_catalog(list_market_funding_rates[0])
    assert set(df_market_funding_rates.columns) == catalog_fields


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_full_market_funding_rates_predicted() -> None:
    catalog_funding_rates = client.catalog_full_market_funding_rates_predicted_v2(page_size=10).first_page()
    assert len(catalog_funding_rates) == 10
    assert all(['market' in catalog for catalog in catalog_funding_rates])
    assert all(['min_time' in catalog for catalog in catalog_funding_rates])
    assert all(['max_time' in catalog for catalog in catalog_funding_rates])
    df_market_funding_rates_predicted = client.catalog_full_market_funding_rates_predicted_v2(
        markets='bybit-10000000AIDOGEUSDT-future'
    ).to_dataframe()
    list_market_funding_rates_predicted = client.catalog_full_market_funding_rates_predicted_v2(
        markets='bybit-10000000AIDOGEUSDT-future'
    ).to_list()
    catalog_fields = get_keys_from_catalog(list_market_funding_rates_predicted[0])
    assert set(df_market_funding_rates_predicted.columns) == catalog_fields


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_market_funding_rates() -> None:
    catalog_funding_rates = client.catalog_market_funding_rates_v2(page_size=10).first_page()
    assert len(catalog_funding_rates) == 10
    assert all(['market' in catalog for catalog in catalog_funding_rates])
    assert all(['min_time' in catalog for catalog in catalog_funding_rates])
    assert all(['max_time' in catalog for catalog in catalog_funding_rates])
    df_market_funding_rates = client.catalog_market_funding_rates_v2(
        markets='binance-1000BONKUSDC-future'
    ).to_dataframe()
    list_market_funding_rates = client.catalog_market_funding_rates_v2(
        markets='binance-1000BONKUSDC-future'
    ).to_list()
    catalog_fields = get_keys_from_catalog(list_market_funding_rates[0])
    assert set(df_market_funding_rates.columns) == catalog_fields


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_market_funding_rates_predicted() -> None:
    catalog_funding_rates = client.catalog_market_funding_rates_predicted_v2(page_size=10).first_page()
    assert len(catalog_funding_rates) == 10
    assert all(['market' in catalog for catalog in catalog_funding_rates])
    assert all(['min_time' in catalog for catalog in catalog_funding_rates])
    assert all(['max_time' in catalog for catalog in catalog_funding_rates])
    df_market_funding_rates_predicted = client.catalog_market_funding_rates_predicted_v2(
        markets='bybit-10000000AIDOGEUSDT-future'
    ).to_dataframe()
    list_market_funding_rates_predicted = client.catalog_market_funding_rates_predicted_v2(
        markets='bybit-10000000AIDOGEUSDT-future'
    ).to_list()
    catalog_fields = get_keys_from_catalog(list_market_funding_rates_predicted[0])
    assert set(df_market_funding_rates_predicted.columns) == catalog_fields


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_market_greeks() -> None:
    catalog_greeks = client.catalog_market_greeks_v2(page_size=10).first_page()
    assert len(catalog_greeks) == 10
    assert all(['market' in catalog for catalog in catalog_greeks])
    assert all(['min_time' in catalog for catalog in catalog_greeks])
    assert all(['max_time' in catalog for catalog in catalog_greeks])
    df_market_greeks = client.catalog_market_greeks_v2(markets="deribit-BTC-15OCT21-60000-C-option").to_dataframe()
    list_market_greeks = client.catalog_market_greeks_v2(markets="deribit-BTC-15OCT21-60000-C-option").to_list()
    catalog_fields = get_keys_from_catalog(list_market_greeks[0])
    assert set(df_market_greeks.columns) == catalog_fields


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_full_market_greeks() -> None:
    catalog_greeks = client.catalog_full_market_greeks_v2(page_size=10).first_page()
    assert len(catalog_greeks) == 10
    assert all(['market' in catalog for catalog in catalog_greeks])
    assert all(['min_time' in catalog for catalog in catalog_greeks])
    assert all(['max_time' in catalog for catalog in catalog_greeks])
    df_market_greeks = client.catalog_full_market_greeks_v2(markets="deribit-BTC-15OCT21-60000-C-option").to_dataframe()
    list_market_greeks = client.catalog_full_market_greeks_v2(markets="deribit-BTC-15OCT21-60000-C-option").to_list()
    catalog_fields = get_keys_from_catalog(list_market_greeks[0])
    assert set(df_market_greeks.columns) == catalog_fields


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_full_market_implied_volatility() -> None:
    catalog_market_implied_vol = client.catalog_full_market_implied_volatility_v2(page_size=10).first_page()
    assert len(catalog_market_implied_vol) == 10
    assert all(['market' in catalog for catalog in catalog_market_implied_vol])
    assert all(['min_time' in catalog for catalog in catalog_market_implied_vol])
    assert all(['max_time' in catalog for catalog in catalog_market_implied_vol])
    df_market_implied_volatility = client.catalog_full_market_implied_volatility_v2(
        markets='binance-BNB-240620-550-C-option', page_size=10000).to_dataframe()
    list_market_implied_volatility = client.catalog_full_market_implied_volatility_v2(
        markets='binance-BNB-240620-550-C-option', page_size=10000).to_list()
    catalog_fields = get_keys_from_catalog(list_market_implied_volatility[0])
    assert set(df_market_implied_volatility.columns) == catalog_fields


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_market_implied_volatility() -> None:
    catalog_market_implied_vol = client.catalog_market_implied_volatility_v2(page_size=10).first_page()
    assert len(catalog_market_implied_vol) == 10
    assert all(['market' in catalog for catalog in catalog_market_implied_vol])
    assert all(['min_time' in catalog for catalog in catalog_market_implied_vol])
    assert all(['max_time' in catalog for catalog in catalog_market_implied_vol])
    df_market_implied_volatility = client.catalog_market_implied_volatility_v2(
        markets='binance-BNB-240620-550-C-option', page_size=10000).to_dataframe()
    list_market_implied_volatility = client.catalog_market_implied_volatility_v2(
        markets='binance-BNB-240620-550-C-option', page_size=10000).to_list()
    catalog_fields = get_keys_from_catalog(list_market_implied_volatility[0])
    assert set(df_market_implied_volatility.columns) == catalog_fields


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_market_liquidations() -> None:
    catalog_market_liquidations = client.catalog_market_liquidations_v2(page_size=10).first_page()
    assert len(catalog_market_liquidations) == 10
    assert all(['market' in catalog for catalog in catalog_market_liquidations])
    assert all(['min_time' in catalog for catalog in catalog_market_liquidations])
    assert all(['max_time' in catalog for catalog in catalog_market_liquidations])
    df_market_liquidations = client.catalog_market_liquidations_v2(markets="binance-BTCUSDT-future").to_dataframe()
    list_market_liquidations = client.catalog_market_liquidations_v2(markets="binance-BTCUSDT-future").to_list()
    catalog_fields = get_keys_from_catalog(list_market_liquidations[0])
    assert set(df_market_liquidations.columns) == catalog_fields


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_full_market_liquidations() -> None:
    catalog_market_liquidations = client.catalog_full_market_liquidations_v2(page_size=10).first_page()
    assert len(catalog_market_liquidations) == 10
    assert all(['market' in catalog for catalog in catalog_market_liquidations])
    assert all(['min_time' in catalog for catalog in catalog_market_liquidations])
    assert all(['max_time' in catalog for catalog in catalog_market_liquidations])
    df_market_liquidations = client.catalog_full_market_liquidations_v2(markets="binance-BTCUSDT-future").to_dataframe()
    list_market_liquidations = client.catalog_full_market_liquidations_v2(markets="binance-BTCUSDT-future").to_list()
    catalog_fields = get_keys_from_catalog(list_market_liquidations[0])
    assert set(df_market_liquidations.columns) == catalog_fields


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_full_market_openinterest() -> None:
    catalog_market_openinterest = client.catalog_full_market_open_interest_v2(page_size=10).first_page()
    assert len(catalog_market_openinterest) == 10
    assert all(['market' in catalog for catalog in catalog_market_openinterest])
    assert all(['min_time' in catalog for catalog in catalog_market_openinterest])
    assert all(['max_time' in catalog for catalog in catalog_market_openinterest])
    df_market_open_interest = client.catalog_full_market_open_interest_v2(markets="binance-BTCUSDT-future").to_dataframe()
    list_market_open_interest = client.catalog_full_market_open_interest_v2(markets="binance-BTCUSDT-future").to_list()
    catalog_fields = get_keys_from_catalog(list_market_open_interest[0])
    assert set(df_market_open_interest.columns) == catalog_fields


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_market_openinterest() -> None:
    catalog_market_openinterest = client.catalog_market_open_interest_v2(page_size=10).first_page()
    assert len(catalog_market_openinterest) == 10
    assert all(['market' in catalog for catalog in catalog_market_openinterest])
    assert all(['min_time' in catalog for catalog in catalog_market_openinterest])
    assert all(['max_time' in catalog for catalog in catalog_market_openinterest])
    df_market_open_interest = client.catalog_market_open_interest_v2(markets="binance-BTCUSDT-future").to_dataframe()
    list_market_open_interest = client.catalog_market_open_interest_v2(markets="binance-BTCUSDT-future").to_list()
    catalog_fields = get_keys_from_catalog(list_market_open_interest[0])
    assert set(df_market_open_interest.columns) == catalog_fields


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_market_orderbooks() -> None:
    catalog_market_orderbooks = client.catalog_market_orderbooks_v2(page_size=10).first_page()
    assert len(catalog_market_orderbooks) == 10
    assert all(['market' in catalog for catalog in catalog_market_orderbooks])
    assert all(['depths' in catalog for catalog in catalog_market_orderbooks])
    df_market_orderbooks = client.catalog_market_orderbooks_v2(markets="coinbase-btc-usd-spot").to_dataframe()
    list_market_orderbooks = client.catalog_market_orderbooks_v2(markets="coinbase-btc-usd-spot").to_list()
    catalog_fields = get_keys_from_catalog(list_market_orderbooks[0])
    assert set(df_market_orderbooks.columns) == catalog_fields


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_market_quotes() -> None:
    catalog_market_quotes = client.catalog_market_quotes_v2(page_size=10).first_page()
    assert len(catalog_market_quotes) == 10
    assert all(['market' in catalog for catalog in catalog_market_quotes])
    assert all(['min_time' in catalog for catalog in catalog_market_quotes])
    assert all(['max_time' in catalog for catalog in catalog_market_quotes])
    df_market_quotes = client.catalog_market_quotes_v2(markets="coinbase-btc-usd-spot").to_dataframe()
    list_market_quotes = client.catalog_market_quotes_v2(markets="coinbase-btc-usd-spot").to_list()
    catalog_fields = get_keys_from_catalog(list_market_quotes[0])
    assert set(df_market_quotes.columns) == catalog_fields


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_full_market_quotes() -> None:
    catalog_market_quotes = client.catalog_full_market_quotes_v2(page_size=10).first_page()
    assert len(catalog_market_quotes) == 10
    assert all(['market' in catalog for catalog in catalog_market_quotes])
    assert all(['min_time' in catalog for catalog in catalog_market_quotes])
    assert all(['max_time' in catalog for catalog in catalog_market_quotes])
    df_market_quotes = client.catalog_full_market_quotes_v2(markets="coinbase-btc-usd-spot").to_dataframe()
    list_market_quotes = client.catalog_full_market_quotes_v2(markets="coinbase-btc-usd-spot").to_list()
    catalog_fields = get_keys_from_catalog(list_market_quotes[0])
    assert set(df_market_quotes.columns) == catalog_fields


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_full_market_orderbooks() -> None:
    catalog_market_orderbooks = client.catalog_full_market_orderbooks_v2(page_size=10).first_page()
    assert len(catalog_market_orderbooks) == 10
    assert all(['market' in catalog for catalog in catalog_market_orderbooks])
    assert all(['depths' in catalog for catalog in catalog_market_orderbooks])
    list_market_orderbooks = client.catalog_full_market_orderbooks_v2(markets="coinbase-btc-usd-spot").to_list()
    df_market_orderbooks = client.catalog_full_market_orderbooks_v2(markets="coinbase-btc-usd-spot").to_dataframe()
    catalog_fields = get_keys_from_catalog(list_market_orderbooks[0])
    assert set(df_market_orderbooks.columns) == catalog_fields


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_full_market_metrics() -> None:
    catalog_market_metrics = client.catalog_full_market_metrics_v2(page_size=10).first_page()
    assert len(catalog_market_metrics) == 10
    assert all(['market' in catalog for catalog in catalog_market_metrics])
    assert all(['metrics' in catalog for catalog in catalog_market_metrics])
    list_market_metrics = client.catalog_full_market_metrics_v2(
        markets='coinbase-btc-usd-spot', metrics='liquidity_slippage_10K_ask_percent'
    ).to_list()
    df_market_metrics = client.catalog_full_market_metrics_v2(
        markets='coinbase-btc-usd-spot', metrics='liquidity_slippage_10K_ask_percent'
    ).to_dataframe()
    catalog_fields = get_keys_from_catalog(list_market_metrics[0])
    assert set(df_market_metrics.columns) == catalog_fields


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_market_metrics() -> None:
    catalog_market_metrics = client.catalog_market_metrics_v2(page_size=10).first_page()
    assert len(catalog_market_metrics) == 10
    assert all(['market' in catalog for catalog in catalog_market_metrics])
    assert all(['metrics' in catalog for catalog in catalog_market_metrics])
    list_market_metrics = client.catalog_market_metrics_v2(
        markets='coinbase-btc-usd-spot', metrics='liquidity_slippage_10K_ask_percent'
    ).to_list()
    df_market_metrics = client.catalog_market_metrics_v2(
        markets='coinbase-btc-usd-spot', metrics='liquidity_slippage_10K_ask_percent'
    ).to_dataframe()
    catalog_fields = get_keys_from_catalog(list_market_metrics[0])
    assert set(df_market_metrics.columns) == catalog_fields


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_asset_metrics() -> None:
    catalog_asset_metrics = client.catalog_asset_metrics_v2(page_size=10).first_page()
    assert len(catalog_asset_metrics) == 10
    assert all(['asset' in catalog for catalog in catalog_asset_metrics])
    assert all(['metrics' in catalog for catalog in catalog_asset_metrics])
    list_asset_metrics = client.catalog_asset_metrics_v2(assets='btc', metrics='PriceUSD').to_list()
    df_asset_metrics = client.catalog_asset_metrics_v2(assets='btc', metrics='PriceUSD').to_dataframe()
    catalog_fields = get_keys_from_catalog(list_asset_metrics[0])
    assert set(df_asset_metrics.columns) == catalog_fields


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_full_asset_metrics() -> None:
    catalog_asset_metrics = client.catalog_full_asset_metrics_v2(page_size=10).first_page()
    assert len(catalog_asset_metrics) == 10
    assert all(['asset' in catalog for catalog in catalog_asset_metrics])
    assert all(['metrics' in catalog for catalog in catalog_asset_metrics])
    list_asset_metrics = client.catalog_full_asset_metrics_v2(assets='btc', metrics='PriceUSD').to_list()
    df_asset_metrics = client.catalog_full_asset_metrics_v2(assets='btc', metrics='PriceUSD').to_dataframe()
    catalog_fields = get_keys_from_catalog(list_asset_metrics[0])
    assert set(df_asset_metrics.columns) == catalog_fields


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_exchange_metrics() -> None:
    catalog_exchange_metrics = client.catalog_exchange_metrics_v2(page_size=10).first_page()
    assert len(catalog_exchange_metrics) == 10
    assert all(['exchange' in catalog for catalog in catalog_exchange_metrics])
    assert all(['metrics' in catalog for catalog in catalog_exchange_metrics])
    list_exchange_metrics = client.catalog_exchange_metrics_v2(
        exchanges='binance', metrics='volume_reported_spot_usd_1h'
    ).to_list()
    df_exchange_metrics = client.catalog_exchange_metrics_v2(
        exchanges='binance',
        metrics='volume_reported_spot_usd_1h'
    ).to_dataframe()
    catalog_fields = get_keys_from_catalog(list_exchange_metrics[0])
    assert set(df_exchange_metrics.columns) == catalog_fields


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_full_exchange_metrics() -> None:
    catalog_exchange_metrics = client.catalog_full_exchange_metrics_v2(page_size=10).first_page()
    assert len(catalog_exchange_metrics) == 10
    assert all(['exchange' in catalog for catalog in catalog_exchange_metrics])
    assert all(['metrics' in catalog for catalog in catalog_exchange_metrics])
    list_exchange_metrics = client.catalog_full_exchange_metrics_v2(
        exchanges='binance', metrics='volume_reported_spot_usd_1h'
    ).to_list()
    df_exchange_metrics = client.catalog_full_exchange_metrics_v2(
        exchanges='binance',
        metrics='volume_reported_spot_usd_1h'
    ).to_dataframe()
    catalog_fields = get_keys_from_catalog(list_exchange_metrics[0])
    assert set(df_exchange_metrics.columns) == catalog_fields

@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_exchange_asset_metrics() -> None:
    catalog_exchange_metrics = client.catalog_exchange_asset_metrics_v2(page_size=10).first_page()
    assert len(catalog_exchange_metrics) == 10
    assert all(['exchange_asset' in catalog for catalog in catalog_exchange_metrics])
    assert all(['metrics' in catalog for catalog in catalog_exchange_metrics])
    list_exchange_asset_metrics = client.catalog_exchange_asset_metrics_v2(
        exchange_assets='binance-btc',
        metrics='volume_reported_spot_usd_1h'
    ).to_list()
    df_exchange_asset_metrics = client.catalog_exchange_asset_metrics_v2(
        exchange_assets='binance-btc',
        metrics='volume_reported_spot_usd_1h'
    ).to_dataframe()
    catalog_fields = get_keys_from_catalog(list_exchange_asset_metrics[0])
    assert set(df_exchange_asset_metrics.columns) == catalog_fields


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_full_exchange_asset_metrics() -> None:
    catalog_exchange_metrics = client.catalog_full_exchange_asset_metrics_v2(page_size=10).first_page()
    assert len(catalog_exchange_metrics) == 10
    assert all(['exchange_asset' in catalog for catalog in catalog_exchange_metrics])
    assert all(['metrics' in catalog for catalog in catalog_exchange_metrics])
    list_exchange_asset_metrics = client.catalog_full_exchange_asset_metrics_v2(
        exchange_assets='binance-btc',
        metrics='volume_reported_spot_usd_1h'
    ).to_list()
    df_exchange_asset_metrics = client.catalog_full_exchange_asset_metrics_v2(
        exchange_assets='binance-btc',
        metrics='volume_reported_spot_usd_1h'
    ).to_dataframe()
    catalog_fields = get_keys_from_catalog(list_exchange_asset_metrics[0])
    assert set(df_exchange_asset_metrics.columns) == catalog_fields


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_pair_metrics() -> None:
    catalog_pair_metrics = client.catalog_pair_metrics_v2(page_size=10).first_page()
    assert len(catalog_pair_metrics) == 10
    assert all(['pair' in catalog for catalog in catalog_pair_metrics])
    assert all(['metrics' in catalog for catalog in catalog_pair_metrics])
    list_pair_metrics = client.catalog_pair_metrics_v2(pairs='btc-usd', metrics='volume_reported_spot_usd_1h').to_list()
    df_pair_metrics = client.catalog_pair_metrics_v2(pairs='btc-usd', metrics='volume_reported_spot_usd_1h').to_dataframe()
    catalog_fields = get_keys_from_catalog(list_pair_metrics[0])
    assert set(df_pair_metrics.columns) == catalog_fields


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_exchange_full_pair_metrics() -> None:
    catalog_pair_metrics = client.catalog_full_pair_metrics_v2(page_size=10).first_page()
    assert len(catalog_pair_metrics) == 10
    assert all(['pair' in catalog for catalog in catalog_pair_metrics])
    assert all(['metrics' in catalog for catalog in catalog_pair_metrics])
    list_pair_metrics = client.catalog_full_pair_metrics_v2(pairs='btc-usd', metrics='volume_reported_spot_usd_1h').to_list()
    df_pair_metrics = client.catalog_full_pair_metrics_v2(pairs='btc-usd', metrics='volume_reported_spot_usd_1h').to_dataframe()
    catalog_fields = get_keys_from_catalog(list_pair_metrics[0])
    assert set(df_pair_metrics.columns) == catalog_fields


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_institution_pair_metrics() -> None:
    catalog_institution_metrics = client.catalog_institution_metrics_v2(page_size=10).first_page()
    assert all(['institution' in catalog for catalog in catalog_institution_metrics])
    assert all(['metrics' in catalog for catalog in catalog_institution_metrics])
    list_institution_metrics = client.catalog_institution_metrics_v2(institutions='grayscale').to_list()
    df_institution_metrics = client.catalog_institution_metrics_v2(institutions='grayscale').to_dataframe()
    catalog_fields = get_keys_from_catalog(list_institution_metrics[0])
    assert set(df_institution_metrics.columns) == catalog_fields


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_full_institution_pair_metrics() -> None:
    catalog_institution_metrics = client.catalog_full_institution_metrics_v2(page_size=10).first_page()
    assert all(['institution' in catalog for catalog in catalog_institution_metrics])
    assert all(['metrics' in catalog for catalog in catalog_institution_metrics])
    list_institution_metrics = client.catalog_full_institution_metrics_v2(institutions='grayscale').to_list()
    df_institution_metrics = client.catalog_full_institution_metrics_v2(institutions='grayscale').to_dataframe()
    catalog_fields = get_keys_from_catalog(list_institution_metrics[0])
    assert set(df_institution_metrics.columns) == catalog_fields


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_pair_candles() -> None:
    catalog_pair_candles = client.catalog_pair_candles_v2(page_size=10).first_page()
    catalog_full_pair_candles = client.catalog_full_pair_candles_v2(page_size=10).first_page()
    assert all(['pair' in catalog for catalog in catalog_pair_candles])
    assert all(['pair' in catalog for catalog in catalog_full_pair_candles])
    assert all(['frequencies' in catalog for catalog in catalog_pair_candles])
    assert all(['frequencies' in catalog for catalog in catalog_full_pair_candles])
    df_candles = client.catalog_pair_candles_v2(pairs="btc-usd").to_dataframe()
    list_candles = client.catalog_pair_candles_v2(pairs="btc-usd").to_list()
    catalog_fields = get_keys_from_catalog(list_candles[0])
    assert set(df_candles.columns) == catalog_fields


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_catalogv2_index_candles() -> None:
    catalog_index_candles = client.catalog_index_candles_v2(page_size=10).first_page()
    catalog_full_index_candles = client.catalog_full_index_candles_v2(page_size=10).first_page()
    assert all(['index' in catalog for catalog in catalog_index_candles])
    assert all(['index' in catalog for catalog in catalog_full_index_candles])
    assert all(['frequencies' in catalog for catalog in catalog_index_candles])
    assert all(['frequencies' in catalog for catalog in catalog_full_index_candles])
    df_candles = client.catalog_index_candles_v2(indexes="CMBI10").to_dataframe()
    list_candles = client.catalog_index_candles_v2(indexes="CMBI10").to_list()
    catalog_fields = get_keys_from_catalog(list_candles[0])
    assert set(df_candles.columns) == catalog_fields


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