import pytest
import requests
from datetime import datetime
from coinmetrics._exceptions import (
    CoinMetricsClientQueryParamsException,
    CoinMetricsUnauthorizedException,
)
from coinmetrics.api_client import CoinMetricsClient
from coinmetrics.data_exporter import CoinMetricsDataExporter
import os

client = CoinMetricsClient(str(os.environ.get("CM_API_KEY")))
cm_api_key_set = os.environ.get("CM_API_KEY") is not None
REASON_TO_SKIP = "Need to set CM_API_KEY as an env var in order to run this test"

print("CM_API_KEY is set - tests will run") if cm_api_key_set else print(
    "CM_API_KEY not set, tests will not run"
)


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_custom_414_error() -> None:
    """
    This tests that the
    """
    markets = [market["market"] for market in client.catalog_markets()]
    try:
        intentional_414 = client.catalog_markets(markets=markets)
    except Exception as e:
        assert type(e) == CoinMetricsClientQueryParamsException
        print(e)


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_custom_exception_not_raised_for_403() -> None:
    """
    Tests that custom exceptions are not raised for unauthorized - just a normal HTTPError, If a different error is
    is raised it asserts false
    """
    unauthorized_client = CoinMetricsClient(api_key="Invalid API Key")
    try:
        intentional_401 = unauthorized_client.catalog_markets()
    except requests.HTTPError as e:
        assert e.response.status_code == 401
    except Exception as e:
        assert False


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_403_error_message() -> None:
    invalid_api_key = "invalid_key"
    data_exporter = CoinMetricsDataExporter(api_key=invalid_api_key)
    try:
        start_date = datetime(2019, 1, 1)
        end_date = datetime(2019, 1, 31)
        exchanges = ["coinbase", "gemini"]
        data_exporter.export_market_trades_spot_data(
            start_date=start_date, end_date=end_date, exchanges=exchanges, threaded=True
        )
    except CoinMetricsUnauthorizedException as e:
        assert e.response.status_code == 403 or e.response.status_code == 401
        print(e)


if __name__ == "__main__":
    pytest.main()
