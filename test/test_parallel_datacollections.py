# type: ignore
import datetime
from datetime import timedelta
import dateutil.relativedelta
import pandas as pd
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
def test_parallel_market_trades() -> None:
    """
    Basic test to make sure that parallel market trades works over a short horizon
    """
    markets = ['coinbase-eth-usdc-spot', 'coinbase-eth-btc-spot']
    start = datetime.datetime(year=2022, day=1, month=6, hour=0, minute=0, second=0).strftime("%Y-%m-%dT%H:%M:%SZ")
    end = datetime.datetime(year=2022, day=1, month=6, hour=0, minute=1, second=0).strftime("%Y-%m-%dT%H:%M:%SZ")
    parallel_trades = client.get_market_trades(markets=markets, start_time=start, end_time=end).parallel().to_list()
    normal_trades = client.get_market_trades(markets=markets, start_time=start, end_time=end).to_list()
    unique_markets = set([trade['market'] for trade in parallel_trades])
    assert len(parallel_trades) > 1
    assert len(parallel_trades) == len(normal_trades)
    for market in markets:
        assert market in unique_markets


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_parallel_market_trades_to_df() -> None:
    """
    Basic test to make sure to_dataframe renders right
    """
    markets = ['coinbase-eth-usdc-spot', 'coinbase-eth-btc-spot']
    start = datetime.datetime(year=2022, day=1, month=6, hour=0, minute=0, second=0).strftime("%Y-%m-%dT%H:%M:%SZ")
    end = datetime.datetime(year=2022, day=1, month=6, hour=0, minute=1, second=0).strftime("%Y-%m-%dT%H:%M:%SZ")
    parallel_trades = client.get_market_trades(markets=markets, start_time=start, end_time=end).parallel().to_dataframe()
    normal_trades = client.get_market_trades(markets=markets, start_time=start, end_time=end).to_dataframe()
    assert len(parallel_trades) > 1
    assert len(normal_trades) == len(parallel_trades)
    assert all([market in set(normal_trades['market']) for market in markets])


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_asset_metrics_to_single_csv() -> None:
    metrics = ["volume_reported_spot_usd_1d", "volume_trusted_spot_usd_1d"]
    start = datetime.datetime(year=2022, day=1, month=6, hour=0, minute=0, second=0).strftime("%Y-%m-%dT%H:%M:%SZ")
    end = datetime.datetime(year=2022, day=4, month=6, hour=3, minute=20, second=0).strftime("%Y-%m-%dT%H:%M:%SZ")
    normal_data = client.get_asset_metrics(assets="btc", metrics=metrics, start_time=start, end_time=end).to_list()
    _export = client.get_asset_metrics(assets="btc", metrics=metrics, start_time=start, end_time=end).parallel(parallelize_on="metrics").export_to_csv("metrics.csv")
    parallel_data = pd.read_csv("metrics.csv")
    assert len(normal_data) == len(parallel_data)
    assert len(parallel_data) == 4


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_parallel_export_to_csvs() -> None:
    """
    Tests that creates the expected
    """
    expected_files = ["btc_asset-metrics.csv", "eth_asset-metrics.csv", "algo_asset-metrics.csv"]
    start = datetime.datetime(year=2022, day=1, month=6, hour=0, minute=0, second=0).strftime("%Y-%m-%dT%H:%M:%SZ")
    end = datetime.datetime(year=2022, day=1, month=6, hour=0, minute=20, second=0).strftime("%Y-%m-%dT%H:%M:%SZ")
    try:
        _export_asset_metrics_csvs = client.get_asset_metrics(assets=["btc", "eth", "algo"],
                                                             metrics="ReferenceRateUSD",
                                                             frequency="1m",
                                                             start_time=start,
                                                             end_time=end).parallel().export_to_csv_files()
        assert all([os.path.exists(file) for file in expected_files])
        assert ([len(pd.read_csv(file)) > 5 for file in expected_files])

    finally:
        for file in expected_files:
            if os.path.exists(file):
                os.remove(file)


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_parallel_export_to_single_csv() -> None:
    """
    Tests that creates the expected
    """
    start = datetime.datetime(year=2022, day=1, month=6, hour=0, minute=0, second=0).strftime("%Y-%m-%dT%H:%M:%SZ")
    end = datetime.datetime(year=2022, day=1, month=6, hour=0, minute=20, second=0).strftime("%Y-%m-%dT%H:%M:%SZ")
    expected_file = "asset_metrics.csv"
    try:
        export_to_csv = client.get_asset_metrics(assets=["btc", "eth", "algo"],
                                                             metrics="ReferenceRateUSD",
                                                             frequency="1m",
                                                             start_time=start,
                                                             end_time=end).parallel().export_to_csv("asset_metrics.csv")
        normal_data = client.get_asset_metrics(assets=["btc", "eth", "algo"],
                                                             metrics="ReferenceRateUSD",
                                                             frequency="1m",
                                                             start_time=start,
                                                             end_time=end).to_list()
        df_from_csv = pd.read_csv(expected_file)
        assert os.path.exists(expected_file)
        assert len(df_from_csv) > 5
        assert len(normal_data) == len(df_from_csv)
    finally:
        os.remove(expected_file)


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_parallel_export_to_json_files() -> None:
    expected_files = ["btc_asset-metrics.json", "eth_asset-metrics.json", "algo_asset-metrics.json"]
    start = datetime.datetime(year=2022, day=1, month=6, hour=0, minute=0, second=0).strftime("%Y-%m-%dT%H:%M:%SZ")
    end = datetime.datetime(year=2022, day=1, month=6, hour=0, minute=20, second=0).strftime("%Y-%m-%dT%H:%M:%SZ")
    try:
        _export_asset_metrics_json = client.get_asset_metrics(assets=["btc", "eth", "algo"],
                                                              metrics="ReferenceRateUSD",
                                                              frequency="1m",
                                                              start_time=start,
                                                              end_time=end).parallel().export_to_json_files()
        assert all([os.path.exists(file) for file in expected_files])
        assert ([len(pd.read_json(file, lines=True)) > 5 for file in expected_files])

    finally:
        for file in expected_files:
            if os.path.exists(file):
                os.remove(file)


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_parallel_export_to_single_json() -> None:
    start = datetime.datetime(year=2022, day=1, month=6, hour=0, minute=0, second=0).strftime("%Y-%m-%dT%H:%M:%SZ")
    end = datetime.datetime(year=2022, day=1, month=6, hour=0, minute=20, second=0).strftime("%Y-%m-%dT%H:%M:%SZ")
    expected_file = "asset_metrics.json"
    try:
        _export_to_json = client.get_asset_metrics(assets=["btc", "eth", "algo"],
                                                 metrics="ReferenceRateUSD",
                                                 frequency="1m",
                                                 start_time=start,
                                                 end_time=end).parallel().export_to_json(expected_file)
        normal_data = client.get_asset_metrics(assets=["btc", "eth", "algo"],
                                               metrics="ReferenceRateUSD",
                                               frequency="1m",
                                               start_time=start,
                                               end_time=end).to_list()
        _df_from_csv = pd.read_json(expected_file, lines=True)
        assert os.path.exists(expected_file)
        assert len(pd.read_json(expected_file, lines=True)) > 5
        assert len(normal_data) == len(pd.read_json(expected_file, lines=True))
    finally:
        os.remove(expected_file)


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_parallelize_on_metrics() -> None:
    metrics = ["volume_reported_spot_usd_1d", "volume_trusted_spot_usd_1d"]
    start = datetime.datetime(year=2022, day=1, month=6, hour=0, minute=0, second=0).strftime("%Y-%m-%dT%H:%M:%SZ")
    end = datetime.datetime(year=2022, day=4, month=6, hour=0, minute=20, second=0).strftime("%Y-%m-%dT%H:%M:%SZ")
    normal_data = client.get_asset_metrics(assets="btc", metrics=metrics, start_time=start, end_time=end).to_dataframe()
    parallel_data = client.get_asset_metrics(assets="btc", metrics=metrics, start_time=start, end_time=end).parallel(parallelize_on="metrics").to_dataframe()
    assert len(normal_data) == len(parallel_data)
    assert len(parallel_data) == 4


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_parallelize_on_metrics_export_to_csvs() -> None:
    metrics = ["volume_reported_spot_usd_1d", "volume_trusted_spot_usd_1d"]
    expected_files = ["volume_reported_spot_usd_1d_asset-metrics.csv", "volume_trusted_spot_usd_1d_asset-metrics.csv"]
    start = datetime.datetime(year=2022, day=1, month=6, hour=0, minute=0, second=0).strftime("%Y-%m-%dT%H:%M:%SZ")
    end = datetime.datetime(year=2022, day=4, month=6, hour=0, minute=20, second=0).strftime("%Y-%m-%dT%H:%M:%SZ")
    try:
        client.get_asset_metrics(assets="btc", metrics=metrics, start_time=start, end_time=end).parallel(
            parallelize_on="metrics").export_to_csv_files()
        for file in expected_files:
            assert os.path.exists(file)
            assert len(pd.read_csv(file)) == 4
    finally:
        for file in expected_files:
            if os.path.exists(file):
                os.remove(file)

@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_parallelize_on_metrics_and_assets_export_to_csvs() -> None:
    metrics = ["volume_reported_spot_usd_1d", "volume_trusted_spot_usd_1d"]
    expected_files = ["btc_volume_reported_spot_usd_1d_asset-metrics.csv",
                      "eth_volume_trusted_spot_usd_1d_asset-metrics.csv",
                      "eth_volume_reported_spot_usd_1d_asset-metrics.csv",
                      "btc_volume_trusted_spot_usd_1d_asset-metrics.csv"]
    start = datetime.datetime(year=2022, day=1, month=6, hour=0, minute=0, second=0).strftime("%Y-%m-%dT%H:%M:%SZ")
    end = datetime.datetime(year=2022, day=4, month=6, hour=0, minute=20, second=0).strftime("%Y-%m-%dT%H:%M:%SZ")
    try:
        client.get_asset_metrics(assets="btc,eth", metrics=metrics, start_time=start, end_time=end).parallel(
            parallelize_on=["assets", "metrics"]).export_to_csv_files()
        for file in expected_files:
            assert os.path.exists(file)
            assert len(pd.read_csv(file)) == 4
    finally:
        for file in expected_files:
            if os.path.exists(file):
                os.remove(file)


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_parallel_to_dataframe_time_increment_month() -> None:
    markets = ['coinbase-eth-usdc-spot']
    test_df_parallel = client.get_market_candles(markets=markets, page_size=1000, start_time="2022-01-01", end_time="2022-03-01", end_inclusive=False).parallel(time_increment=dateutil.relativedelta.relativedelta(months=1)).to_dataframe()
    test_df_normal = client.get_market_candles(markets=markets, page_size=1000, start_time="2022-01-01", end_time="2022-03-01", end_inclusive=False).to_dataframe()
    assert len(test_df_parallel) > 10
    assert len(test_df_normal) == len(test_df_parallel)
    assert set(test_df_parallel.columns) == set(test_df_normal.columns)


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_parallel_to_dataframe_time_increment_week() -> None:
    markets = ['coinbase-eth-usdc-spot']
    test_df_parallel = client.get_market_candles(markets=markets, page_size=1000, start_time="2022-01-01", end_time="2022-03-01", end_inclusive=False).parallel(progress_bar=False, time_increment=dateutil.relativedelta.relativedelta(weeks=1)).to_dataframe()
    test_df_normal = client.get_market_candles(markets=markets, page_size=1000, start_time="2022-01-01", end_time="2022-03-01", end_inclusive=False).to_dataframe()
    assert len(test_df_parallel) > 10
    assert len(test_df_normal) == len(test_df_parallel)
    assert set(test_df_parallel.columns) == set(test_df_normal.columns)


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_parallel_to_dataframe_time_increment_week_multiple_markets() -> None:
    markets = ['coinbase-eth-usdc-spot', 'coinbase-eth-btc-spot']
    test_df_parallel = client.get_market_candles(markets=markets, page_size=1000, start_time="2022-01-01", end_time="2022-03-01", end_inclusive=False).parallel(progress_bar=False, time_increment=dateutil.relativedelta.relativedelta(weeks=1)).to_dataframe()
    test_df_normal = client.get_market_candles(markets=markets, page_size=1000, start_time="2022-01-01", end_time="2022-03-01", end_inclusive=False).to_dataframe()
    assert len(test_df_parallel) > 10
    assert len(test_df_normal) == len(test_df_parallel)
    assert set(test_df_parallel.columns) == set(test_df_normal.columns)


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_parallel_asset_metrics_using_time_increment_enum() -> None:
    metrics = ["ReferenceRateUSD", "AdrAct30dCnt",  "AdrAct7dCnt", "AdrActCnt"]
    test_df_parallel = client.get_asset_metrics(assets="btc", metrics=metrics, page_size=1000, start_time="2022-01-01", end_time="2022-03-01", end_inclusive=False, frequency="1d").parallel(parallelize_on=["metrics"], time_increment=dateutil.relativedelta.relativedelta(months=1)).to_dataframe()
    test_df_normal = client.get_asset_metrics(assets="btc", metrics=metrics, page_size=1000, start_time="2022-01-01", end_time="2022-03-01", end_inclusive=False, frequency="1d").to_dataframe()
    assert len(test_df_parallel) > 10
    assert len(test_df_normal) == len(test_df_parallel)
    assert set(test_df_parallel.columns) == set(test_df_normal.columns)


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_export_to_csvs_time_increment_files() -> None:
    assets = ["btc"]
    client.get_asset_metrics(
        assets=assets,
        metrics="ReferenceRateUSD",
        frequency="1m",
        start_time="2023-03-01",
        end_time="2023-05-01",
        page_size=1000,
        end_inclusive=False).parallel(
        time_increment=timedelta(days=1)).export_to_csv("btcRRs.csv")

@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_blockchain_parallel_export() -> None:
    df_temp = client.get_list_of_blocks_v2(
        asset="btc",
        start_time='2023-09-07',
        end_time='2023-09-22',
        page_size=10000,
        end_inclusive=False
    ).parallel(time_increment=timedelta(days=1)).to_dataframe()
    assert len(df_temp) > 2000


if __name__ == '__main__':
    pytest.main()


