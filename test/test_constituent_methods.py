
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
def test_constituent_snapshots() -> None:
    data = client.get_snapshots_of_asset_metric_constituents(metric="volume_trusted_spot_usd_1d").to_list()
    assert all(["time" in item for item in data])
    assert all(["exchange" in item for item in data])


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_constituent_timeframes() -> None:
    data = client.get_timeframes_of_asset_metric_constituents(metric="volume_trusted_spot_usd_1d").to_list()
    assert all(["exchange" in item for item in data])
    assert all(["start_time" in item for item in data])
    assert all(["end_time" in item for item in data])



