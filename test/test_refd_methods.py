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

COMMON_REFD_COLS = ["metric",
                    "full_name",
                    "description",
                    "product",
                    "category",
                    "subcategory",
                    "unit",
                    "data_type",
                    "type",
                    "display_name"]

@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_refd_asset_pairs() -> None:
    expected_cols = COMMON_REFD_COLS
    asset_pairs = client.reference_data_pair_metrics().first_page()[0]
    assert all([col in asset_pairs for col in expected_cols])


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_refd_institution_metrics() -> None:
    expected_cols = COMMON_REFD_COLS
    institution_data = client.reference_data_institution_metrics().first_page()[0]
    assert all([col in institution_data for col in expected_cols])


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_refd_exchange_asset_metrics() -> None:
    expected_cols = COMMON_REFD_COLS
    exchange_asset_metrics = client.reference_data_exchange_asset_metrics().first_page()[0]
    assert all([col in exchange_asset_metrics for col in expected_cols])


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_refd_exchange_metrics() -> None:
    expected_cols = COMMON_REFD_COLS
    exchange_asset_metrics = client.reference_data_exchange_metrics().first_page()[0]
    assert all([col in exchange_asset_metrics for col in expected_cols])


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_refd_asset_metrics() -> None:
    expected_cols = COMMON_REFD_COLS
    asset_metrics = client.reference_data_exchange_asset_metrics().first_page()[0]
    assert all([col in asset_metrics for col in expected_cols])


if __name__ == '__main__':
    pytest.main()
