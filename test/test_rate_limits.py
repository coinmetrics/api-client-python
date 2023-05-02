import os
import threading
import pytest

from coinmetrics.api_client import CoinMetricsClient

client = CoinMetricsClient()
cm_api_key_set = os.environ.get("CM_API_KEY") is not None
REASON_TO_SKIP = "Need to set CM_API_KEY as an env var in order to run this test"

print("CM_API_KEY is set - tests will run") if cm_api_key_set else print(
    "CM_API_KEY not set, tests will not run"
)


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_rate_limiter_works_as_expected() -> None:
    """
    This function tests if a community user can run a 20 second query against our API without tripping the 429 error
    """
    def target() -> None:
        try:
            client.get_asset_metrics(assets="btc,algo,eth,usdc", metrics="ReferenceRateUSD", frequency="1m").to_list()
        except Exception as e:
            pytest.fail(f"Function failed with exception: {e}")

    test_thread = threading.Thread(target=target)
    test_thread.daemon = True
    test_thread.start()

    test_thread.join(20)

    if not test_thread.is_alive():
        pytest.fail("Function failed to run for 20 seconds without throwing an exception")


if __name__ == '__main__':
    pytest.main()