import pandas as pd
import polars as pl
import pytest
from coinmetrics.api_client import CoinMetricsClient
from coinmetrics.schema_resolver import get_schema_fields
import os
import numpy as np
from typing import Any

CM_API_KEY = os.environ.get("CM_API_KEY")
client = CoinMetricsClient(str(CM_API_KEY))
cm_api_key_set = CM_API_KEY is not None
REASON_TO_SKIP = "Need to set CM_API_KEY as an env var in order to run this test"


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_defi_balance_sheets() -> None:
    """
    Testing this works for aave
    """
    aave_balance_sheets: pd.DataFrame = client.get_defi_balance_sheets(
        defi_protocols="aave_v2_eth",
        start_time="2025-01-01",
        end_time="2025-01-01"
    ).to_dataframe(dataframe_type='pandas')
    assert not aave_balance_sheets.empty


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_pandas_timestamp() -> None:
    list_timestamp_objects = [
        pd.Timestamp(2024, 1, 1),
        pd.Timestamp(2024, 1, 1, 12, 0, 0),
        pd.Timestamp(2024, 1, 1, 12, 0, 0).tz_localize('US/Eastern'),
        pd.Timestamp(2024, 1, 1, 0, 0, 0).tz_localize('UTC')
    ]
    for ts in list_timestamp_objects:
        data = client.get_asset_metrics(
            'btc',
            'ReferenceRateUSD',
            start_time=ts,
            limit_per_asset=1
        ).to_dataframe()
        assert isinstance(data, pd.DataFrame)


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_to_dataframe_polars() -> None:
    _ = client.get_asset_metrics(
        'btc',
        'ReferenceRateUSD',
        limit_per_asset=1
    ).to_dataframe(
        optimize_dtypes=True, dataframe_type="polars"
    )

    _ = client.get_asset_metrics(
        'btc',
        'ReferenceRateUSD',
        limit_per_asset=1
    ).to_dataframe(
        optimize_dtypes=True,
        dataframe_type="polars",
        dtype_mapper={"time": pl.Time, "ReferenceRateUSD": pl.Float64}
    )

    _ = client.catalog_asset_metrics_v2('btc', 'ReferenceRateUSD').to_dataframe(dataframe_type='polars')

    _ = client.catalog_market_contract_prices_v2(
        'deribit-ETH-25MAR22-1200-P-option'
    ).to_dataframe(dataframe_type='polars')

    _ = client.catalog_market_orderbooks_v2("coinbase-btc-usd-spot").to_dataframe(dataframe_type="polars")

    _ = client.reference_data_markets(
        markets=["coinbase-btc-usd-spot", "deribit-ETH-25MAR22-1200-P-option", "binance-BTCUSDT-future"]
    ).to_dataframe(dataframe_type="polars")


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_optimize_pandas_types_deprecated(caplog: pytest.LogCaptureFixture) -> None:
    with caplog.at_level("WARNING"):
        df = client.get_asset_metrics(
            "btc", "ReferenceRateUSD", limit_per_asset=1
        ).to_dataframe(dataframe_type="pandas", optimize_pandas_types=True)
    assert isinstance(df, pd.DataFrame)
    assert "'optimize_pandas_types' is deprecated." in caplog.text
    assert pd.api.types.is_datetime64_ns_dtype(df["time"])

    caplog.clear()
    with caplog.at_level("WARNING"):
        df = client.get_asset_metrics(
            "btc", "ReferenceRateUSD", limit_per_asset=1
        ).to_dataframe(dataframe_type="pandas", optimize_pandas_types=False)
    assert isinstance(df, pd.DataFrame)
    assert "'optimize_pandas_types' is deprecated." in caplog.text
    assert not pd.api.types.is_datetime64_ns_dtype(df["time"])

    caplog.clear()
    with caplog.at_level("WARNING"):
        df = client.get_asset_metrics(
            "btc", "ReferenceRateUSD", limit_per_asset=1
        ).to_dataframe(dataframe_type="pandas", optimize_dtypes=True)
    assert isinstance(df, pd.DataFrame)
    assert "'optimize_pandas_types' is deprecated." not in caplog.text
    assert pd.api.types.is_datetime64_ns_dtype(df["time"])
    
@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_nullable_columns_exchange() -> None:
    """
    Test that nullable columns are returned correctly when calling to_dataframe()
    """
    # Case 1: Exchange Metrcs
    # pick exchanges where metric coverage is spotty to force nullable columns
    exchanges = ["binance", "bibox", "bitmex"]
    metrics = [
        "open_interest_reported_future_usd",
        "volume_reported_spot_usd_1d",
        "volume_reported_future_usd_1d"
    ]
    df_exchanges_default = client.get_exchange_metrics(
        exchanges=exchanges,
        metrics=metrics,
        start_time="2024-01-01",
        end_time="2024-02-01",
        end_inclusive=False,
        limit_per_exchange=1
    ).to_dataframe()
    
    fields = set()
    for row in client.get_exchange_metrics(
        exchanges=exchanges,
        metrics=metrics,
        start_time="2024-01-01",
        end_time="2024-02-01",
        end_inclusive=False,
        limit_per_exchange=1
    ):
        fields.update(set(row.keys()))
        
    assert set(df_exchanges_default.columns) >= set(metrics)
    assert sorted(df_exchanges_default.columns) == sorted(fields)
    
    # Case 2: Exchange-Asset Metrics
    exchange_assets = ["binance-btc", "bibox-btc", "bitmex-btc"]
    df_exchange_assets_default = client.get_exchange_asset_metrics(
        exchange_assets=exchange_assets,
        metrics=metrics,
        start_time="2024-01-01",
        end_time="2024-02-01",
        end_inclusive=False,
        limit_per_exchange_asset=1
    ).to_dataframe()
    
    fields = set()
    for row in client.get_exchange_asset_metrics(
            exchange_assets=exchange_assets,
            metrics=metrics,
            start_time="2024-01-01",
            end_time="2024-02-01",
            end_inclusive=False,
            limit_per_exchange_asset=1
        ):
        fields.update(set(row.keys()))

    assert set(df_exchange_assets_default.columns) >= set(metrics)
    assert sorted(df_exchange_assets_default.columns) == sorted(fields)

    
@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_nullable_columns_asset_metrics() -> None:
    # Case 3: Asset Metrics
    # Case 3a: frequency=1b returns time columns beyond "time"
    assets = ["btc"]
    metrics_1b = ["TxCnt"]
    df_assets_default = client.get_asset_metrics(
        assets=assets,
        metrics=metrics_1b,
        frequency="1b",
        limit_per_asset=1
    ).to_dataframe()
    api_return_row = next(
        client.get_asset_metrics(
            assets=assets,
            metrics=metrics_1b,
            frequency="1b",
            limit_per_asset=1
        )
    )
    assert set(df_assets_default.columns) >= set(metrics_1b)
    assert sorted(df_assets_default.columns) == sorted(api_return_row.keys())
    
    # Case 3b: Exchange Flow metrics return <metric>-status and <metric>-status-time columns
    metrics_flow = ["SplyBMXNtv"]
    df_flow_metrics_default = client.get_asset_metrics(
        assets=assets,
        metrics=metrics_flow,
        limit_per_asset=1
    ).to_dataframe()
    api_return_row = next(
        client.get_asset_metrics(
            assets=assets,
            metrics=metrics_flow,
            limit_per_asset=1
        )
    )
    assert set(df_flow_metrics_default.columns) >= set(["SplyBMXNtv", "SplyBMXNtv-status", "SplyBMXNtv-status-time"])
    assert sorted(df_flow_metrics_default.columns) == sorted(api_return_row.keys())
    
    
@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_polars_dataframe() -> None:
    # Test: Check that Polars DataFrame with nullable columns doesn't error when loading and is equivalent
    df_accounts_btc_no_debit = client.get_list_of_accounts_v2(
        asset='btc', 
        page_size=10000,
        end_height=1,
    ).to_lazyframe().filter(pl.col("last_debit_height").is_null()).collect()

    df_accounts_btc_debited = client.get_list_of_accounts_v2(
        asset='btc', 
        page_size=10000,
        end_height=1,
    ).to_lazyframe().filter(pl.col("last_debit_height").is_not_null()).collect()
    
    df_concat = pl.concat([df_accounts_btc_debited, df_accounts_btc_no_debit]) 
    
    df_accounts_btc = client.get_list_of_accounts_v2(
        asset='btc', 
        page_size=10000,
        end_height=1,
    ).to_dataframe(dataframe_type="polars")
    
    assert df_concat.columns == df_accounts_btc.columns
    

@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_nullable_columns_blockchain_v2() -> None:
    # Case 4: Blockchain V2 with Sub-Accounts
    api_return_row = next(
        client.get_list_of_balance_updates_v2(
            asset="btc",
            accounts="112dvb4DogEpcp3yUR59HQuN1LFJbPErAT",
            include_sub_accounts=True,
            limit_per_account=1
        )
    )

    df_balance_updates = client.get_list_of_balance_updates_v2(
        asset="btc",
        accounts="112dvb4DogEpcp3yUR59HQuN1LFJbPErAT",
        include_sub_accounts=True,
        limit_per_account=1
    ).to_dataframe()
    assert set(df_balance_updates.columns) >= set(api_return_row.keys())
    
    api_return_row = next(
        client.get_list_of_balance_updates_for_account_v2(
            asset="btc",
            account="112dvb4DogEpcp3yUR59HQuN1LFJbPErAT",
            include_sub_accounts=True,
        )
    )

    df_balance_updates = client.get_list_of_balance_updates_for_account_v2(
        asset="btc",
        account="112dvb4DogEpcp3yUR59HQuN1LFJbPErAT",
        include_sub_accounts=True,
    ).to_dataframe()
    assert set(df_balance_updates.columns) >= set(api_return_row.keys())
    
    fields = set()
    for row in client.get_full_transaction_v2(
        asset="ltc",
        txid="16262dacdac04f41b50dd4174d3bd0d133916a325e5244b3febcb760a8d3975f",
        include_sub_accounts=True
    ):
        fields.update(set(row.keys()))
        
    df_transactions = client.get_full_transaction_v2(
        asset="ltc",
        txid="16262dacdac04f41b50dd4174d3bd0d133916a325e5244b3febcb760a8d3975f",
        include_sub_accounts=True
    ).to_dataframe()
    assert set(df_transactions.columns) >= set(fields)
    
    fields = set()
    for row in client.get_full_block_v2(
        asset="btc",
        block_hash="0000000000000000000079fca9c54dd7532d139ed258f02e3d1368e7006157d9",
        include_sub_accounts=True
    ):
        fields.update(set(row.keys()))
        
    df_blocks = client.get_full_block_v2(
        asset="btc",
        block_hash="0000000000000000000079fca9c54dd7532d139ed258f02e3d1368e7006157d9",
        include_sub_accounts=True
    ).to_dataframe()
    assert set(df_blocks.columns) >= set(fields)
    

@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_nullable_columns_market_trades() -> None:
    # Case 5: Market Trades
    markets = [
        "uniswap_v3_eth-1-usdc-weth-spot",
        "coinbase-btc-usd-spot",
        "deribit-BTC-10JAN25-93500-C-option"
    ]

    fields = set()
    for row in client.get_market_trades(
        markets=markets,
        limit_per_market=1
    ):
        fields.update(set(row.keys()))
        
    df_market_trades = client.get_market_trades(
        markets=markets,
        limit_per_market=1
    ).to_dataframe()

    assert set(df_market_trades.columns) >= set(fields)


if __name__ == "__main__":
    pytest.main()
