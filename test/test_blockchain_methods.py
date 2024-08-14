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
def test_get_blockchain_list_of_account_balance_updates() -> None:
    asset = "btc"
    account = "112jmDkNGHSbhhY17JGpxU3sMA9ZExG7b2"
    updates = client.get_list_of_balance_updates_for_account_v2(asset=asset, account=account).to_list()
    assert updates[0]['block_hash'] == "0000000000000000002c7505ef2272e0677fa53d68d633f8e076ed42dd3380e6"


if __name__ == "__main__":
    pytest.main()
