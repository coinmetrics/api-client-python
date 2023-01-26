import pytest

from coinmetrics.api_client import CoinMetricsClient
import os

client = CoinMetricsClient(str(os.environ.get("CM_API_KEY")), debug_mode=True)
cm_api_key_set = os.environ.get("CM_API_KEY") is not None
REASON_TO_SKIP = "Need to set CM_API_KEY as an env var in order to run this test"

print("CM_API_KEY is set - tests will run") if cm_api_key_set else print(
    "CM_API_KEY not set, tests will not run"
)


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_debugging_get_rrs() -> None:
    """
    Checks that log file is created as expected
    """
    eth_reference_rates = client.get_asset_metrics(
        metrics="ReferenceRateUSD",
        assets="eth",
        start_time="2020-01-01",
        frequency="1d",
    )
    for data in eth_reference_rates:
        print(data)
    assert any(
        list(
            map(
                lambda file_name: file_name.startswith("cm_api_client_debug_"),
                os.listdir(os.getcwd()),
            )
        )
    )
