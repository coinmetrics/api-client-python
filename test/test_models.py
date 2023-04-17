import datetime

import pytest

from coinmetrics.api_client import CoinMetricsClient
from coinmetrics._models import TransactionTrackerData
import os

client = CoinMetricsClient(str(os.environ.get("CM_API_KEY")))
cm_api_key_set = os.environ.get("CM_API_KEY") is not None
REASON_TO_SKIP = "Need to set CM_API_KEY as an env var in order to run this test"

print("CM_API_KEY is set - tests will run") if cm_api_key_set else print(
    "CM_API_KEY not set, tests will not run"
)


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_asset_chains_optional_returns() -> None:
    """
    In the old implementation, this test would fail since 'reorg' wouldn't be in the the df columns
    """
    r = client.get_asset_chains(
        assets='btc',
        start_time='2022-10-22T05:40:00',  # '2022-10-22T00:00:00',
        end_time='2022-10-22T06:40:00')

    print(r)
    df = r.to_dataframe()
    print(df.columns)
    print(df)
    assert 'reorg' in df.columns


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_normal_api_call_asset_chains() -> None:
    """
    Tests that when calling get asset chains, the to_dataframe() will contain those with and without reorgs
    """
    request = client.get_asset_chains(
        assets='btc',
        start_time='2022-10-22T05:40:00',  # '2022-10-22T00:00:00',
        end_time='2022-10-22T10:40:00')
    df = request.to_dataframe()
    assert df.iloc[4].reorg == False
    assert df.iloc[3].reorg == True


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_get_transaction_tracker_df() -> None:
    request = client.get_transaction_tracker(
        'btc',
        start_time='2023-03-30T00:00:00',
        end_time='2023-03-30T00:05:00',
        page_size=200
    )
    df = request.to_dataframe()
    assert all([col in df.columns for col in TransactionTrackerData.get_dataframe_cols()])



if __name__ == '__main__':
    request = client.get_transaction_tracker(
        "btc",
        start_time=datetime.datetime.now() - datetime.timedelta(seconds=10),
        page_size=100
    )
    df = request.to_dataframe()
    print("test!")