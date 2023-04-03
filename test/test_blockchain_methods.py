import datetime

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
def test_get_full_transaction_for_block() -> None:
    asset = "btc"
    block_hash = "0000000000000000000334e8637314d72d86a533c71f48da23e85e70a82cd38a"
    transaction_id = "29d401526b06d55749034c10c3ee7ffd9ecab942c9b6852c963fa61103552729"
    transaction = client.get_full_transaction_for_block(
        asset=asset, block_hash=block_hash, txid=transaction_id
    )
    as_list = transaction
    print(as_list)
    assert len(as_list) >= 1


if __name__ == "__main__":
    pytest.main()
