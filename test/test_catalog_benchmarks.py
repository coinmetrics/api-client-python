# %%
import time
import os
import pandas as pd
import pytest
from coinmetrics.api_client import CoinMetricsClient
from coinmetrics._utils import get_keys_from_catalog
from typing import Tuple, Any, Callable, Dict, no_type_check

client = CoinMetricsClient(str(os.environ.get("CM_API_KEY")), verbose=True)
cm_api_key_set = os.environ.get("CM_API_KEY") is not None
REASON_TO_SKIP = "Need to set CM_API_KEY as an env var in order to run this test"

print("CM_API_KEY is set - tests will run") if cm_api_key_set else print(
    "CM_API_KEY not set, tests will not run"
)


@no_type_check
def benchmark_endpoint(
        endpoint_method: Any, output_method: str, **endpoint_method_kwargs: Dict[Any, Any]
) -> Tuple[Any, float, int]:
    start_time = time.time()

    if output_method == "to_dataframe":
        response = endpoint_method(**endpoint_method_kwargs).to_dataframe()
    elif output_method == "to_list":
        response = endpoint_method(**endpoint_method_kwargs).to_list()

    end_time = time.time()
    response_time = end_time - start_time
    row_count = len(response)
    return response, response_time, row_count


test_cases = [
    # ("/catalog-v2/asset-metrics", client.catalog_asset_metrics_v2, "to_dataframe", "json", {"page_size": 10000, format: "json"}),
    # ("/catalog-v2/exchange-metrics", client.catalog_exchange_metrics_v2, "to_dataframe", "json", {"page_size": 10000, format: "json"}),
    # ("/catalog-v2/exchange-asset-metrics", client.catalog_exchange_asset_metrics_v2, "to_dataframe", "json", {"page_size": 10000, format: "json"}),
    # ("/catalog-v2/pair-metrics", client.catalog_pair_metrics_v2, "to_dataframe", "json", {"page_size": 10000, format: "json"}),
    # ("/catalog-v2/institution-metrics", client.catalog_institution_metrics_v2, "to_dataframe", "json", {"page_size": 10000, format: "json"}),
    # ("/catalog-v2/market-trades", client.catalog_market_trades_v2, "to_dataframe", "json", {"page_size": 10000, format: "json"}),
    # ("/catalog-v2/market-candles", client.catalog_market_candles_v2, "to_dataframe", "json", {"page_size": 10000, format: "json"}),
    # ("/catalog-v2/market-orderbooks", client.catalog_market_orderbooks_v2, "to_dataframe", "json", {"page_size": 10000, format: "json"}),
    # ("/catalog-v2/market-quotes", client.catalog_market_quotes_v2, "to_dataframe", "json", {"page_size": 10000, format: "json"}),
    # ("/catalog-v2/market-funding-rates", client.catalog_market_funding_rates_v2, "to_dataframe", "json", {"page_size": 10000, format: "json"}),
    # ("/catalog-v2/market-funding-rates-predicted", client.catalog_full_market_funding_rates_predicted_v2, "to_dataframe", "json", {"page_size": 10000, format: "json"}),
    # ("/catalog-v2/market-contract-prices", client.catalog_market_contract_prices_v2, "to_dataframe", "json", {"page_size": 10000, format: "json"}),
    # ("/catalog-v2/market-implied-volatility", client.catalog_market_implied_volatility_v2, "to_dataframe", "json", {"page_size": 10000, format: "json"}),
    # ("/catalog-v2/market-openinterest", client.catalog_market_open_interest_v2, "to_dataframe", "json", {"page_size": 10000, format: "json"}),
    # ("/catalog-v2/market-liquidtations", client.catalog_market_liquidations_v2, "to_dataframe", "json", {"page_size": 10000, format: "json"}),
    # ("/catalog-v2/market-metrics", client.catalog_market_metrics_v2, "to_dataframe", "json", {"page_size": 10000, format: "json"}),
    # ("/catalog-v2/pair-candles", client.catalog_pair_candles_v2, "to_dataframe", "json", {"page_size": 10000, format: "json"}),
    # ("/catalog-v2/index-levels", client.catalog_index_levels_v2, "to_dataframe", "json", {"page_size": 10000, format: "json"}),
    # ("/catalog-v2/index-candles", client.catalog_index_candles_v2, "to_dataframe", "json", {"page_size": 10000, format: "json"}),
    # ("/catalog-v2/asset-chains", client.catalog_asset_chains_v2, "to_dataframe", "json", {"page_size": 10000, format: "json"}),
    # ("/catalog-v2/mempool-feerates", client.catalog_mempool_feerates_v2, "to_dataframe", "json", {"page_size": 10000, format: "json"}),
    # ("/catalog-v2/mining-pool-tips-summary", client.catalog_mining_pool_tips_summaries_v2, "to_dataframe", "json", {"page_size": 10000, format: "json"}),
    # ("/catalog-v2/transaction-tracker", client.catalog_transaction_tracker_assets_v2, "to_dataframe", "json", {"page_size": 10000, format: "json"}),
    ("/catalog-v2/asset-metrics", client.catalog_asset_metrics_v2, "to_list", "json", {"page_size": 10000, "format": "json"}),
    ("/catalog-v2/exchange-metrics", client.catalog_exchange_metrics_v2, "to_list", "json", {"page_size": 10000, "format": "json"}),
    ("/catalog-v2/exchange-asset-metrics", client.catalog_exchange_asset_metrics_v2, "to_list", "json", {"page_size": 10000, "format": "json"}),
    ("/catalog-v2/pair-metrics", client.catalog_pair_metrics_v2, "to_list", "json", {"page_size": 10000, "format": "json"}),
    ("/catalog-v2/institution-metrics", client.catalog_institution_metrics_v2, "to_list", "json", {"page_size": 10000, "format": "json"}),
    ("/catalog-v2/market-trades", client.catalog_market_trades_v2, "to_list", "json", {"page_size": 10000, "format": "json"}),
    ("/catalog-v2/market-candles", client.catalog_market_candles_v2, "to_list", "json", {"page_size": 10000, "format": "json"}),
    ("/catalog-v2/market-orderbooks", client.catalog_market_orderbooks_v2, "to_list", "json", {"page_size": 10000, "format": "json"}),
    ("/catalog-v2/market-quotes", client.catalog_market_quotes_v2, "to_list", "json", {"page_size": 10000, "format": "json"}),
    ("/catalog-v2/market-funding-rates", client.catalog_market_funding_rates_v2, "to_list", "json", {"page_size": 10000, "format": "json"}),
    ("/catalog-v2/market-funding-rates-predicted", client.catalog_full_market_funding_rates_predicted_v2, "to_list", "json", {"page_size": 10000, "format": "json"}),
    ("/catalog-v2/market-contract-prices", client.catalog_market_contract_prices_v2, "to_list", "json", {"page_size": 10000, "format": "json"}),
    ("/catalog-v2/market-implied-volatility", client.catalog_market_implied_volatility_v2, "to_list", "json", {"page_size": 10000, "format": "json"}),
    ("/catalog-v2/market-openinterest", client.catalog_market_open_interest_v2, "to_list", "json", {"page_size": 10000, "format": "json"}),
    ("/catalog-v2/market-liquidtations", client.catalog_market_liquidations_v2, "to_list", "json", {"page_size": 10000, "format": "json"}),
    ("/catalog-v2/market-metrics", client.catalog_market_metrics_v2, "to_list", "json", {"page_size": 10000, "format": "json"}),
    ("/catalog-v2/pair-candles", client.catalog_pair_candles_v2, "to_list", "json", {"page_size": 10000, "format": "json"}),
    ("/catalog-v2/index-levels", client.catalog_index_levels_v2, "to_list", "json", {"page_size": 10000, "format": "json"}),
    ("/catalog-v2/index-candles", client.catalog_index_candles_v2, "to_list", "json", {"page_size": 10000, "format": "json"}),
    ("/catalog-v2/asset-chains", client.catalog_asset_chains_v2, "to_list", "json", {"page_size": 10000, "format": "json"}),
    ("/catalog-v2/mempool-feerates", client.catalog_mempool_feerates_v2, "to_list", "json", {"page_size": 10000, "format": "json"}),
    ("/reference-data/assets", client.reference_data_assets, "to_list", "json",
     {"page_size": 10000, "format": "json"}),
    ("/reference-data/exchanges", client.reference_data_exchanges, "to_list", "json",
     {"page_size": 10000, "format": "json"}),
    ("/reference-data/markets", client.reference_data_markets, "to_list", "json",
     {"page_size": 10000, "format": "json"}),
    ("/reference-data/indexes", client.reference_data_indexes, "to_list", "json",
     {"page_size": 10000, "format": "json"}),
    ("/reference-data/pairs", client.reference_data_pairs, "to_list", "json",
     {"page_size": 10000, "format": "json"}),
    ("/reference-data/asset-metrics", client.reference_data_asset_metrics, "to_list", "json",
     {"page_size": 10000, "format": "json"}),
    ("/reference-data/exchange-metrics", client.reference_data_exchange_metrics, "to_list", "json",
     {"page_size": 10000, "format": "json"}),
    ("/reference-data/exchange-asset-metrics", client.reference_data_exchange_asset_metrics, "to_list", "json",
     {"page_size": 10000, "format": "json"}),
    ("/reference-data/pair-metrics", client.reference_data_pair_metrics, "to_list", "json",
     {"page_size": 10000, "format": "json"}),
    ("/reference-data/institution-metrics", client.reference_data_institution_metrics, "to_list", "json",
     {"page_size": 10000, "format": "json"}),
    ("/reference-data/market-metrics", client.reference_data_market_metrics, "to_list", "json",
     {"page_size": 10000, "format": "json"}),
    # ("/catalog-v2/mining-pool-tips-summary", client.catalog_mining_pool_tips_summaries_v2, "to_list", "json", {"page_size": 10000, "format": "json"}),
    # ("/catalog-v2/transaction-tracker", client.catalog_transaction_tracker_assets_v2, "to_list", "json", {"page_size": 10000, "format": "json"}),
    ("/catalog-v2/asset-metrics", client.catalog_asset_metrics_v2, "to_list", "json_stream",
     {}),
    ("/catalog-v2/exchange-metrics", client.catalog_exchange_metrics_v2, "to_list", "json_stream",
     {}),
    ("/catalog-v2/exchange-asset-metrics", client.catalog_exchange_asset_metrics_v2, "to_list", "json_stream",
     {}),
    ("/catalog-v2/pair-metrics", client.catalog_pair_metrics_v2, "to_list", "json_stream",
     {}),
    ("/catalog-v2/institution-metrics", client.catalog_institution_metrics_v2, "to_list", "json_stream",
     {}),
    ("/catalog-v2/market-trades", client.catalog_market_trades_v2, "to_list", "json_stream",
     {}),
    ("/catalog-v2/market-candles", client.catalog_market_candles_v2, "to_list", "json_stream",
     {}),
    ("/catalog-v2/market-orderbooks", client.catalog_market_orderbooks_v2, "to_list", "json_stream",
     {}),
    ("/catalog-v2/market-quotes", client.catalog_market_quotes_v2, "to_list", "json_stream",
     {}),
    ("/catalog-v2/market-funding-rates", client.catalog_market_funding_rates_v2, "to_list", "json_stream",
     {}),
    ("/catalog-v2/market-funding-rates-predicted", client.catalog_full_market_funding_rates_predicted_v2, "to_list",
     "json_stream", {}),
    ("/catalog-v2/market-contract-prices", client.catalog_market_contract_prices_v2, "to_list", "json_stream",
     {}),
    ("/catalog-v2/market-implied-volatility", client.catalog_market_implied_volatility_v2, "to_list", "json_stream",
     {}),
    ("/catalog-v2/market-openinterest", client.catalog_market_open_interest_v2, "to_list", "json_stream",
     {}),
    ("/catalog-v2/market-liquidtations", client.catalog_market_liquidations_v2, "to_list", "json_stream",
     {}),
    ("/catalog-v2/market-metrics", client.catalog_market_metrics_v2, "to_list", "json_stream",
     {}),
    ("/catalog-v2/pair-candles", client.catalog_pair_candles_v2, "to_list", "json_stream",
     {}),
    ("/catalog-v2/index-levels", client.catalog_index_levels_v2, "to_list", "json_stream",
     {}),
    ("/catalog-v2/index-candles", client.catalog_index_candles_v2, "to_list", "json_stream",
     {}),
    ("/catalog-v2/asset-chains", client.catalog_asset_chains_v2, "to_list", "json_stream",
     {}),
    ("/catalog-v2/mempool-feerates", client.catalog_mempool_feerates_v2, "to_list", "json_stream",
     {}),
    ("/reference-data/assets", client.reference_data_assets, "to_list", "json_stream",
     {}),
    ("/reference-data/exchanges", client.reference_data_exchanges, "to_list", "json_stream",
     {}),
    ("/reference-data/markets", client.reference_data_markets, "to_list", "json_stream",
     {}),
    ("/reference-data/indexes", client.reference_data_indexes, "to_list", "json_stream",
     {}),
    ("/reference-data/pairs", client.reference_data_pairs, "to_list", "json_stream",
     {}),
    ("/reference-data/asset-metrics", client.reference_data_asset_metrics, "to_list", "json_stream",
     {}),
    ("/reference-data/exchange-metrics", client.reference_data_exchange_metrics, "to_list", "json_stream",
     {}),
    ("/reference-data/exchange-asset-metrics", client.reference_data_exchange_asset_metrics, "to_list", "json_stream",
     {}),
    ("/reference-data/pair-metrics", client.reference_data_pair_metrics, "to_list", "json_stream",
     {}),
    ("/reference-data/institution-metrics", client.reference_data_institution_metrics, "to_list", "json_stream",
     {}),
    ("/reference-data/market-metrics", client.reference_data_market_metrics, "to_list", "json_stream",
     {}),
    # ("/catalog-v2/mining-pool-tips-summary", client.catalog_mining_pool_tips_summaries_v2, "to_list", "json_stream",
    #  {}),
    # ("/catalog-v2/transaction-tracker", client.catalog_transaction_tracker_assets_v2, "to_list", "json_stream",
    #  {})
]


@no_type_check
@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def benchmark_results() -> None:
    benchmark_results = []

    for name, endpoint_method, output_method, fmt, endpoint_method_kwargs in test_cases:
        print(f"Requesting {name} output method {output_method} and format {fmt}.")
        response, response_time, row_count = benchmark_endpoint(
            endpoint_method, output_method, **endpoint_method_kwargs
        )
        benchmark_results.append((name, output_method, fmt, response_time, row_count))

    # %%
    print(f"{'Endpoint':<60} {'Output Method':<20} {'Response Time':>23} {'Rows':>10}")
    print("-" * 95)
    for name, output_method, fmt, response_time, row_count in benchmark_results:
        print(f"{name:<60} {fmt:<20} {response_time:>15.2f} seconds {row_count:>10}")

    # %%
    results_df = pd.DataFrame(benchmark_results, columns=["Endpoint", "Output Method", "Format", "Response Time", "Rows"])
    print(results_df)
    # results_df.to_csv("benchmark_results.csv", index=False)
