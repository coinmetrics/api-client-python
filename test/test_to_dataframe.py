import pandas as pd
import polars as pl
import pytest
from coinmetrics.api_client import CoinMetricsClient
import os
import numpy as np

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
        defi_protocols="aave_v2_eth"
    ).to_dataframe(dataframe_type='pandas')
    assert len(aave_balance_sheets) > 100
    assert aave_balance_sheets.iloc[:1]["defi_protocol"][0] == "aave_v2_eth"


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_transaction_tracker_catalog_full() -> None:
    data = client.catalog_full_transaction_tracker_assets().to_dataframe()
    assert len(data) >= 2


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_transaction_tracker_catalog() -> None:
    data = client.catalog_transaction_tracker_assets().to_dataframe()
    assert len(data) >= 2


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

if __name__ == "__main__":
    pytest.main()
