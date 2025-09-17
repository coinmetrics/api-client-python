# %%
import time
import os
import pandas as pd
import pytest
from coinmetrics.api_client import CoinMetricsClient
from coinmetrics._utils import get_keys_from_catalog
from typing import Tuple, Any, Callable, Dict, List, no_type_check
import argparse

client = CoinMetricsClient(str(os.environ.get("CM_API_KEY")))
cm_api_key_set = os.environ.get("CM_API_KEY") is not None
REASON_TO_SKIP = "Need to set CM_API_KEY as an env var in order to run this test"

print("CM_API_KEY is set - tests will run") if cm_api_key_set else print(
    "CM_API_KEY not set, tests will not run"
)

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Run API benchmark tests')
    parser.add_argument('--ignore-catalog', action='store_true', help='Skip catalog benchmark tests')
    parser.add_argument('--ignore-timeseries', action='store_true', help='Skip timeseries benchmark tests')
    return parser.parse_args()

@no_type_check
def benchmark_endpoint(
        endpoint_method: Any, output_method: str, **endpoint_method_kwargs: Dict[Any, Any]
) -> Tuple[Any, float, int]:
    start_time = time.time()

    if output_method == "to_dataframe":
        response = endpoint_method(**endpoint_method_kwargs).to_dataframe()
    elif output_method == "to_list":
        response = endpoint_method(**endpoint_method_kwargs).to_list()
    elif output_method == "export_to_csv":
        response = endpoint_method(**endpoint_method_kwargs).export_to_csv()
    elif output_method == "export_to_json":
        response = endpoint_method(**endpoint_method_kwargs).export_to_csv()

    end_time = time.time()
    response_time = end_time - start_time
    row_count = len(response)
    return response, response_time, row_count


test_cases_catalog = [
    # ("/catalog-v2/asset-metrics", client.catalog_asset_metrics_v2, "to_dataframe", "format=json", {"page_size": 10000, format: "json"}),
    # ("/catalog-v2/exchange-metrics", client.catalog_exchange_metrics_v2, "to_dataframe", "format=json", {"page_size": 10000, format: "json"}),
    # ("/catalog-v2/exchange-asset-metrics", client.catalog_exchange_asset_metrics_v2, "to_dataframe", "format=json", {"page_size": 10000, format: "json"}),
    # ("/catalog-v2/pair-metrics", client.catalog_pair_metrics_v2, "to_dataframe", "format=json", {"page_size": 10000, format: "json"}),
    # ("/catalog-v2/institution-metrics", client.catalog_institution_metrics_v2, "to_dataframe", "format=json", {"page_size": 10000, format: "json"}),
    # ("/catalog-v2/market-trades", client.catalog_market_trades_v2, "to_dataframe", "format=json", {"page_size": 10000, format: "json"}),
    # ("/catalog-v2/market-candles", client.catalog_market_candles_v2, "to_dataframe", "format=json", {"page_size": 10000, format: "json"}),
    # ("/catalog-v2/market-orderbooks", client.catalog_market_orderbooks_v2, "to_dataframe", "format=json", {"page_size": 10000, format: "json"}),
    # ("/catalog-v2/market-quotes", client.catalog_market_quotes_v2, "to_dataframe", "format=json", {"page_size": 10000, format: "json"}),
    # ("/catalog-v2/market-funding-rates", client.catalog_market_funding_rates_v2, "to_dataframe", "format=json", {"page_size": 10000, format: "json"}),
    # ("/catalog-v2/market-funding-rates-predicted", client.catalog_full_market_funding_rates_predicted_v2, "to_dataframe", "format=json", {"page_size": 10000, format: "json"}),
    # ("/catalog-v2/market-contract-prices", client.catalog_market_contract_prices_v2, "to_dataframe", "format=json", {"page_size": 10000, format: "json"}),
    # ("/catalog-v2/market-implied-volatility", client.catalog_market_implied_volatility_v2, "to_dataframe", "format=json", {"page_size": 10000, format: "json"}),
    # ("/catalog-v2/market-openinterest", client.catalog_market_open_interest_v2, "to_dataframe", "format=json", {"page_size": 10000, format: "json"}),
    # ("/catalog-v2/market-liquidtations", client.catalog_market_liquidations_v2, "to_dataframe", "format=json", {"page_size": 10000, format: "json"}),
    # ("/catalog-v2/market-metrics", client.catalog_market_metrics_v2, "to_dataframe", "format=json", {"page_size": 10000, format: "json"}),
    # ("/catalog-v2/pair-candles", client.catalog_pair_candles_v2, "to_dataframe", "format=json", {"page_size": 10000, format: "json"}),
    # ("/catalog-v2/index-levels", client.catalog_index_levels_v2, "to_dataframe", "format=json", {"page_size": 10000, format: "json"}),
    # ("/catalog-v2/index-candles", client.catalog_index_candles_v2, "to_dataframe", "format=json", {"page_size": 10000, format: "json"}),
    # ("/catalog-v2/asset-chains", client.catalog_asset_chains_v2, "to_dataframe", "format=json", {"page_size": 10000, format: "json"}),
    # ("/catalog-v2/mempool-feerates", client.catalog_mempool_feerates_v2, "to_dataframe", "format=json", {"page_size": 10000, format: "json"}),
    # ("/catalog-v2/mining-pool-tips-summary", client.catalog_mining_pool_tips_summaries_v2, "to_dataframe", "format=json", {"page_size": 10000, format: "json"}),
    # ("/catalog-v2/transaction-tracker", client.catalog_transaction_tracker_assets_v2, "to_dataframe", "format=json", {"page_size": 10000, format: "json"}),
    ("/catalog-v2/asset-metrics", client.catalog_asset_metrics_v2, "to_list", "format=json", {"page_size": 10000, "format": "json"}),
    ("/catalog-v2/exchange-metrics", client.catalog_exchange_metrics_v2, "to_list", "format=json", {"page_size": 10000, "format": "json"}),
    ("/catalog-v2/exchange-asset-metrics", client.catalog_exchange_asset_metrics_v2, "to_list", "format=json", {"page_size": 10000, "format": "json"}),
    ("/catalog-v2/pair-metrics", client.catalog_pair_metrics_v2, "to_list", "format=json", {"page_size": 10000, "format": "json"}),
    ("/catalog-v2/institution-metrics", client.catalog_institution_metrics_v2, "to_list", "format=json", {"page_size": 10000, "format": "json"}),
    ("/catalog-v2/market-trades", client.catalog_market_trades_v2, "to_list", "format=json", {"page_size": 10000, "format": "json"}),
    ("/catalog-v2/market-candles", client.catalog_market_candles_v2, "to_list", "format=json", {"page_size": 10000, "format": "json"}),
    ("/catalog-v2/market-orderbooks", client.catalog_market_orderbooks_v2, "to_list", "format=json", {"page_size": 10000, "format": "json"}),
    ("/catalog-v2/market-quotes", client.catalog_market_quotes_v2, "to_list", "format=json", {"page_size": 10000, "format": "json"}),
    ("/catalog-v2/market-funding-rates", client.catalog_market_funding_rates_v2, "to_list", "format=json", {"page_size": 10000, "format": "json"}),
    ("/catalog-v2/market-funding-rates-predicted", client.catalog_full_market_funding_rates_predicted_v2, "to_list", "format=json", {"page_size": 10000, "format": "json"}),
    ("/catalog-v2/market-contract-prices", client.catalog_market_contract_prices_v2, "to_list", "format=json", {"page_size": 10000, "format": "json"}),
    ("/catalog-v2/market-implied-volatility", client.catalog_market_implied_volatility_v2, "to_list", "format=json", {"page_size": 10000, "format": "json"}),
    ("/catalog-v2/market-openinterest", client.catalog_market_open_interest_v2, "to_list", "format=json", {"page_size": 10000, "format": "json"}),
    ("/catalog-v2/market-liquidations", client.catalog_market_liquidations_v2, "to_list", "format=json", {"page_size": 10000, "format": "json"}),
    ("/catalog-v2/market-metrics", client.catalog_market_metrics_v2, "to_list", "format=json", {"page_size": 10000, "format": "json"}),
    ("/catalog-v2/pair-candles", client.catalog_pair_candles_v2, "to_list", "format=json", {"page_size": 10000, "format": "json"}),
    ("/catalog-v2/index-levels", client.catalog_index_levels_v2, "to_list", "format=json", {"page_size": 10000, "format": "json"}),
    ("/catalog-v2/index-candles", client.catalog_index_candles_v2, "to_list", "format=json", {"page_size": 10000, "format": "json"}),
    ("/catalog-v2/asset-chains", client.catalog_asset_chains_v2, "to_list", "format=json", {"page_size": 10000, "format": "json"}),
    ("/catalog-v2/mempool-feerates", client.catalog_mempool_feerates_v2, "to_list", "format=json", {"page_size": 10000, "format": "json"}),
    ("/reference-data/assets", client.reference_data_assets, "to_list", "format=json",
     {"page_size": 10000, "format": "json"}),
    ("/reference-data/exchanges", client.reference_data_exchanges, "to_list", "format=json",
     {"page_size": 10000, "format": "json"}),
    ("/reference-data/markets", client.reference_data_markets, "to_list", "format=json",
     {"page_size": 10000, "format": "json"}),
    ("/reference-data/indexes", client.reference_data_indexes, "to_list", "format=json",
     {"page_size": 10000, "format": "json"}),
    ("/reference-data/pairs", client.reference_data_pairs, "to_list", "format=json",
     {"page_size": 10000, "format": "json"}),
    ("/reference-data/asset-metrics", client.reference_data_asset_metrics, "to_list", "format=json",
     {"page_size": 10000, "format": "json"}),
    ("/reference-data/exchange-metrics", client.reference_data_exchange_metrics, "to_list", "format=json",
     {"page_size": 10000, "format": "json"}),
    ("/reference-data/exchange-asset-metrics", client.reference_data_exchange_asset_metrics, "to_list", "format=json",
     {"page_size": 10000, "format": "json"}),
    ("/reference-data/pair-metrics", client.reference_data_pair_metrics, "to_list", "format=json",
     {"page_size": 10000, "format": "json"}),
    ("/reference-data/institution-metrics", client.reference_data_institution_metrics, "to_list", "format=json",
     {"page_size": 10000, "format": "json"}),
    ("/reference-data/market-metrics", client.reference_data_market_metrics, "to_list", "format=json",
     {"page_size": 10000, "format": "json"}),
    # ("/catalog-v2/mining-pool-tips-summary", client.catalog_mining_pool_tips_summaries_v2, "to_list", "format=json", {"page_size": 10000, "format": "json"}),
    # ("/catalog-v2/transaction-tracker", client.catalog_transaction_tracker_assets_v2, "to_list", "format=json", {"page_size": 10000, "format": "json"}),
    ("/catalog-v2/asset-metrics", client.catalog_asset_metrics_v2, "to_list", "format=json_stream",
     {}),
    ("/catalog-v2/exchange-metrics", client.catalog_exchange_metrics_v2, "to_list", "format=json_stream",
     {}),
    ("/catalog-v2/exchange-asset-metrics", client.catalog_exchange_asset_metrics_v2, "to_list", "format=json_stream",
     {}),
    ("/catalog-v2/pair-metrics", client.catalog_pair_metrics_v2, "to_list", "format=json_stream",
     {}),
    ("/catalog-v2/institution-metrics", client.catalog_institution_metrics_v2, "to_list", "format=json_stream",
     {}),
    ("/catalog-v2/market-trades", client.catalog_market_trades_v2, "to_list", "format=json_stream",
     {}),
    ("/catalog-v2/market-candles", client.catalog_market_candles_v2, "to_list", "format=json_stream",
     {}),
    ("/catalog-v2/market-orderbooks", client.catalog_market_orderbooks_v2, "to_list", "format=json_stream",
     {}),
    ("/catalog-v2/market-quotes", client.catalog_market_quotes_v2, "to_list", "format=json_stream",
     {}),
    ("/catalog-v2/market-funding-rates", client.catalog_market_funding_rates_v2, "to_list", "format=json_stream",
     {}),
    ("/catalog-v2/market-funding-rates-predicted", client.catalog_full_market_funding_rates_predicted_v2, "to_list",
     "format=json_stream", {}),
    ("/catalog-v2/market-contract-prices", client.catalog_market_contract_prices_v2, "to_list", "format=json_stream",
     {}),
    ("/catalog-v2/market-implied-volatility", client.catalog_market_implied_volatility_v2, "to_list", "format=json_stream",
     {}),
    ("/catalog-v2/market-openinterest", client.catalog_market_open_interest_v2, "to_list", "format=json_stream",
     {}),
    ("/catalog-v2/market-liquidations", client.catalog_market_liquidations_v2, "to_list", "format=json_stream",
     {}),
    ("/catalog-v2/market-metrics", client.catalog_market_metrics_v2, "to_list", "format=json_stream",
     {}),
    ("/catalog-v2/pair-candles", client.catalog_pair_candles_v2, "to_list", "format=json_stream",
     {}),
    ("/catalog-v2/index-levels", client.catalog_index_levels_v2, "to_list", "format=json_stream",
     {}),
    ("/catalog-v2/index-candles", client.catalog_index_candles_v2, "to_list", "format=json_stream",
     {}),
    ("/catalog-v2/asset-chains", client.catalog_asset_chains_v2, "to_list", "format=json_stream",
     {}),
    ("/catalog-v2/mempool-feerates", client.catalog_mempool_feerates_v2, "to_list", "format=json_stream",
     {}),
    ("/reference-data/assets", client.reference_data_assets, "to_list", "format=json_stream",
     {}),
    ("/reference-data/exchanges", client.reference_data_exchanges, "to_list", "format=json_stream",
     {}),
    ("/reference-data/markets", client.reference_data_markets, "to_list", "format=json_stream",
     {}),
    ("/reference-data/indexes", client.reference_data_indexes, "to_list", "format=json_stream",
     {}),
    ("/reference-data/pairs", client.reference_data_pairs, "to_list", "format=json_stream",
     {}),
    ("/reference-data/asset-metrics", client.reference_data_asset_metrics, "to_list", "format=json_stream",
     {}),
    ("/reference-data/exchange-metrics", client.reference_data_exchange_metrics, "to_list", "format=json_stream",
     {}),
    ("/reference-data/exchange-asset-metrics", client.reference_data_exchange_asset_metrics, "to_list", "format=json_stream",
     {}),
    ("/reference-data/pair-metrics", client.reference_data_pair_metrics, "to_list", "format=json_stream",
     {}),
    ("/reference-data/institution-metrics", client.reference_data_institution_metrics, "to_list", "format=json_stream",
     {}),
    ("/reference-data/market-metrics", client.reference_data_market_metrics, "to_list", "format=json_stream",
     {}),
    # ("/catalog-v2/mining-pool-tips-summary", client.catalog_mining_pool_tips_summaries_v2, "to_list", "format=json_stream",
    #  {}),
    # ("/catalog-v2/transaction-tracker", client.catalog_transaction_tracker_assets_v2, "to_list", "format=json_stream",
    #  {})
]

test_cases_timeseries = [
    ("/timeseries/asset-metrics", client.get_asset_metrics, "to_list", "format=json",
     {"assets": "btc", "metrics": "ReferenceRateUSD", "frequency": "1s", "limit_per_asset": 100000, "page_size": 10000, "format": "json"}),
    ("/timeseries/market-trades", client.get_market_trades, "to_list", "format=json",
     {"markets": "coinbase-btc-usd-spot", "limit_per_market": 100000, "page_size": 10000, "format": "json"}),
    ("/timeseries/market-orderbooks", client.get_market_orderbooks, "to_list", "format=json",
     {"markets": "binance-BTCUSDT-future", "granularity": "1m", "limit_per_market": 10000, "page_size": 10000, "format": "json"}),
    ("/timeseries/asset-metrics", client.get_asset_metrics, "to_list", "format=json_stream",
     {"assets": "btc", "metrics": "ReferenceRateUSD", "frequency": "1s", "limit_per_asset": 100000, "format": "json_stream"}),
    ("/timeseries/market-trades", client.get_market_trades, "to_list", "format=json_stream",
     {"markets": "coinbase-btc-usd-spot", "limit_per_market": 100000, "format": "json_stream"}),
    ("/timeseries/market-orderbooks", client.get_market_orderbooks, "to_list", "format=json_stream",
     {"markets": "binance-BTCUSDT-future", "granularity": "1m", "limit_per_market": 10000, "format": "json_stream"}),
]


def benchmark_results(test_cases: List[Any]) -> None:
    benchmark_results = []

    for name, endpoint_method, output_method, param, endpoint_method_kwargs in test_cases:
        print(f"Requesting {name} Collection {output_method} and param {param}.")
        response, response_time, row_count = benchmark_endpoint(
            endpoint_method, output_method, **endpoint_method_kwargs
        )
        benchmark_results.append((name, output_method, param, response_time, row_count))

    # %%
    print(f"{'Endpoint':<60} {'Parameter':<20} {'Response Time':>23} {'Rows':>10}")
    print("-" * 95)
    for name, output_method, param, response_time, row_count in benchmark_results:
        print(f"{name:<60} {param:<20} {response_time:>15.2f} seconds {row_count:>10}")

    # %%
    results_df = pd.DataFrame(benchmark_results, columns=["Endpoint", "Collection", "Parameter", "Response Time", "Rows"])
    print(results_df)
    
@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def benchmark_catalog() -> None:
    benchmark_results(test_cases_catalog)
    
    
@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def benchmark_timeseries() -> None:
    benchmark_results(test_cases_timeseries)
    

if __name__ == "__main__":
    args = parse_args()
    if not args.ignore_catalog:
        print("\nRunning catalog benchmarks...")
        benchmark_catalog()
    else:
        print("\nSkipping catalog benchmarks")
        
    if not args.ignore_timeseries:
        print("\nRunning timeseries benchmarks...")
        benchmark_timeseries()
    else:
        print("\nSkipping timeseries benchmarks")