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


def test_as_list_works_like_first_page_short_query() -> None:
    """
    In theory, on a small query that works on a small number of results should have equivalent results for .first_page()
    and also _to_list()
    """
    test_time = datetime.datetime(year=2022, month=2, day=1)
    assets = ["eth", "algo", "btc"]
    data_first_page = client.get_asset_metrics(
        assets=assets,
        metrics="SplyFF",
        limit_per_asset=1,
        start_time=test_time,
        end_time=test_time,
    ).first_page()
    data_list = client.get_asset_metrics(
        assets=assets,
        metrics="SplyFF",
        limit_per_asset=1,
        start_time=test_time,
        end_time=test_time,
    ).to_list()
    assert data_list == data_first_page


def test_as_list_doesnt_work_like_first_page_long_query() -> None:
    """
    In theory, on a long query, that will have multiple pages of response data should have very different results
    as first page
    """
    start_time = datetime.datetime(year=2021, month=1, day=1)
    end_time = datetime.datetime(year=2022, month=2, day=1)
    assets = ["eth", "algo", "btc"]
    data_first_page = client.get_asset_metrics(
        assets=assets,
        metrics="SplyFF",
        limit_per_asset=100,
        start_time=start_time,
        end_time=end_time,
    ).first_page()
    data_list = client.get_asset_metrics(
        assets=assets,
        metrics="SplyFF",
        limit_per_asset=100,
        start_time=start_time,
        end_time=end_time,
    ).to_list()
    assert data_list != data_first_page


def test_as_list_gets_all_data() -> None:
    """
    This tests that .to_list() gets the same amount and the same data as _to_dataframe()
    """
    start_time = datetime.datetime(year=2021, month=1, day=1)
    end_time = datetime.datetime(year=2022, month=2, day=1)
    assets = ["eth"]
    data_df = client.get_asset_metrics(
        assets=assets,
        metrics="ReferenceRateUSD",
        start_time=start_time,
        end_time=end_time,
    ).to_dataframe()
    data_list = client.get_asset_metrics(
        assets=assets,
        metrics="ReferenceRateUSD",
        start_time=start_time,
        end_time=end_time,
    ).to_list()
    assert len(data_df) == len(data_list)


if __name__ == "__main__":
    pytest.main()
