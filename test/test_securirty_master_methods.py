import os
import threading
import pytest

from coinmetrics.api_client import CoinMetricsClient

client = CoinMetricsClient(str(os.environ.get("CM_API_KEY")))
cm_api_key_set = os.environ.get("CM_API_KEY") is not None
REASON_TO_SKIP = "Need to set CM_API_KEY as an env var in order to run this test"

print("CM_API_KEY is set - tests will run") if cm_api_key_set else print(
    "CM_API_KEY not set, tests will not run"
)


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_security_master_markets() -> None:
    expected_cols = ["market", "exchange", "type"]
    markets = client.security_master_markets().first_page()[0]
    assert all([col in markets for col in expected_cols])


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_security_master_assets() -> None:
    expected_cols = ["asset"]
    assets = client.security_master_assets().first_page()[0]
    assert all([col in assets for col in expected_cols])


if __name__ == '__main__':
    pytest.main()