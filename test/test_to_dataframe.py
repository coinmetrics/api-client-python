import pandas as pd
import pytest
from coinmetrics.api_client import CoinMetricsClient
import os
import numpy as np

CM_API_KEY = os.environ.get("CM_API_KEY")
client = CoinMetricsClient(str(CM_API_KEY))
cm_api_key_set = CM_API_KEY is not None
REASON_TO_SKIP = "Need to set CM_API_KEY as an env var in order to run this test"


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_defi_balance_sheets() -> None:
    """
    Testing this works for aave
    """
    aave_balance_sheets = client.get_defi_balance_sheets(
        defi_protocols="aave_v2_eth"
    ).to_dataframe()
    assert len(aave_balance_sheets) > 100
    assert aave_balance_sheets.iloc[:1]["defi_protocol"][0] == "aave_v2_eth"


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_transaction_tracker_catalog_full() -> None:
    data = client.catalog_full_transaction_tracker_assets().to_dataframe()
    assert len(data) >= 2


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_transaction_tracker_catalog() -> None:
    data = client.catalog_transaction_tracker_assets().to_dataframe()
    assert len(data) >= 2


if __name__ == "__main__":
    pytest.main()
