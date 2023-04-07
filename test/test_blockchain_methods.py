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


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_get_blockchain_list_of_account_balance_updates() -> None:
    asset = "btc"
    account = "112jmDkNGHSbhhY17JGpxU3sMA9ZExG7b2"
    updates = client.get_list_of_balance_updates_for_account_v2(asset=asset, account=account).to_list()
    assert updates[0]['block_hash'] == "0000000000000000002c7505ef2272e0677fa53d68d633f8e076ed42dd3380e6"


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_get_full_block_v1() -> None:
    asset = "eth"
    block_hash = "0x27a2bd0fd3b3298dd8004c18aaad83374bdc5dbd36eac46bfe00772d88dba7cf"
    full_block = client.get_full_block(asset=asset, block_hash=block_hash)
    assert full_block['block_hash'] == block_hash.strip("0x")
    assert full_block['height'] == '15442095'


if __name__ == "__main__":
    pytest.main()
