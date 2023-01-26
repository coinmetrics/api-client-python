import os
import json
import pytest
from datetime import datetime
from typing import List
from coinmetrics.data_exporter import CoinMetricsDataExporter


CM_API_KEY = os.environ.get("CM_API_KEY")
data_exporter = CoinMetricsDataExporter(api_key=str(CM_API_KEY))
cm_api_key_set = CM_API_KEY is not None
REASON_TO_SKIP = "Need to set CM_API_KEY as an env var in order to run this test"


@pytest.fixture()
def setup_function() -> None:
    folders_to_check_and_delete = [
        "data",
        "market-trades-spot",
        "market-trades-future",
        "market-candles-future",
        "market-candles-spot",
    ]
    print(
        f"Deleting any folders that test folders that exist before tests are run: {folders_to_check_and_delete}"
    )
    for dir in folders_to_check_and_delete:
        if os.path.exists(dir):
            os.rmdir(dir)


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def files_downloaded_test_helper_start(list_of_expected_files: List[str]) -> None:
    """
    This is a helper function that test that the provided files do not exist at the time the tests start
    """
    for file in list_of_expected_files:
        if os.path.exists(file):
            print(
                f"The file {file} is not supposed to exist before this test is run, failing"
            )
            assert not (os.path.exists(file))


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def files_downloaded_test_helper_end(list_of_file_locations: List[str]) -> None:
    """
    This is a helper function that tests that the expected files were created and then deletes them to clean up
    """
    try:
        for file in list_of_file_locations:
            assert os.path.exists(file)
    except Exception as e:
        print("Exceptions found, removing files then raising exceptions")
        for file in list_of_file_locations:
            if os.path.exists(file):
                os.remove(file)
        raise e


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_export_market_candles_5m() -> None:
    list_of_expected_files = [
        "market-candles-future-5m/binance/2019-10-10.json.gz",
        "market-candles-future-5m/binance/2019-10-11.json.gz",
        "market-candles-future-5m/binance/2019-10-12.json.gz",
    ]
    files_downloaded_test_helper_start(list_of_expected_files)
    start_date = datetime(2019, 10, 10)
    end_date = datetime(2019, 10, 12)
    exchange = "binance"
    data_exporter.export_market_candles_future_data(
        frequency="5m",
        start_date=start_date,
        end_date=end_date,
        exchanges=exchange,
        output_format="csv",
    )


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_export_market_quotes_future_one_asset() -> None:
    list_of_expected_files = [
        "market-quotes-future/Binance/1INCHUSDT/2022-02-19.json.gz",
        "market-quotes-future/Binance/1INCHUSDT/2022-02-20.json.gz",
        "market-quotes-future/Binance/1INCHUSDT/2022-02-21.json.gz",
    ]
    files_downloaded_test_helper_start(list_of_expected_files)
    start_date = datetime(2022, 2, 19)
    end_date = datetime(2022, 2, 21)
    exchanges = ["Binance"]
    asset_pairs = ["1INCHUSDT"]
    data_exporter.export_market_quotes_future_data(
        start_date=start_date,
        end_date=end_date,
        asset_pairs=asset_pairs,
        exchanges=exchanges,
        output_format="json.gz",
    )
    files_downloaded_test_helper_end(list_of_expected_files)


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_get_list_of_files_to_download_mquote() -> None:
    list_of_expected_files = [
        "market-quotes-spot/Binance/1INCHBTC/2022-02-19.json.gz",
        "market-quotes-spot/Binance/1INCHBTC/2022-02-20.json.gz",
        "market-quotes-spot/Binance/1INCHBTC/2022-02-21.json.gz",
    ]
    start_date = datetime(2022, 2, 19)
    end_date = datetime(2022, 2, 21)
    exchanges = ["Binance"]
    asset_pairs = ["1INCHBTC"]
    actual_files = data_exporter._get_list_files_to_download_from_ff_server(
        route_url="market-quotes-spot",
        assets_pairs=asset_pairs,
        exchanges=exchanges,
        start_date=start_date,
        end_date=end_date,
    )
    assert actual_files == list_of_expected_files


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_get_list_of_files_to_download_mquote_future() -> None:
    list_of_expected_files = [
        "market-quotes-future/Binance/1INCHUSDT/2022-02-19.json.gz",
        "market-quotes-future/Binance/1INCHUSDT/2022-02-20.json.gz",
        "market-quotes-future/Binance/1INCHUSDT/2022-02-21.json.gz",
    ]
    start_date = datetime(2022, 2, 19)
    end_date = datetime(2022, 2, 21)
    exchanges = ["Binance"]
    asset_pairs = ["1INCHUSDT"]
    actual_files = data_exporter._get_list_files_to_download_from_ff_server(
        route_url="market-quotes-future",
        assets_pairs=asset_pairs,
        exchanges=exchanges,
        start_date=start_date,
        end_date=end_date,
    )
    assert actual_files == list_of_expected_files


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_get_list_of_files_to_download_market() -> None:
    """
    Tests the data exporter get list of files function works as expected on a fixed dataframe. This can be
    considered an integration test because it will call the API, however our data schema and data file history
    should stay the same so the dependency is minimal
    """
    expected_file_names = [
        "market-trades-spot/binance/2017-07-15.json.gz",
        "market-trades-spot/binance/2017-07-16.json.gz",
        "market-trades-spot/binance/2017-07-17.json.gz",
    ]
    start_date = datetime(2017, 7, 15)
    end_date = datetime(2017, 7, 17)
    exchange = "binance"
    market_trades_url = "market-trades-spot"
    actual_file_names = data_exporter._get_list_of_file_urls_to_download_market_trades(
        start_date=start_date,
        end_date=end_date,
        exchanges=exchange,
        route_url=market_trades_url,
    )
    assert expected_file_names == actual_file_names


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_get_list_of_files_to_download_market_future() -> None:
    expected_file_names = [
        "market-trades-future/binance/2019-09-15.json.gz",
        "market-trades-future/binance/2019-09-16.json.gz",
        "market-trades-future/binance/2019-09-17.json.gz",
    ]
    start_date = datetime(2019, 9, 15)
    end_date = datetime(2019, 9, 17)
    exchange = "binance"
    market_trades_url = "market-trades-future"
    actual_file_names = data_exporter._get_list_of_file_urls_to_download_market_trades(
        start_date=start_date,
        end_date=end_date,
        exchanges=exchange,
        route_url=market_trades_url,
    )
    assert expected_file_names == actual_file_names


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_get_list_of_files_to_download_market_empty() -> None:
    expected_file_names: List[str] = []
    start_date = datetime(2015, 7, 15)
    end_date = datetime(2015, 7, 17)
    exchange = "binance"
    actual_file_names = data_exporter._get_list_of_file_urls_to_download_market_trades(
        route_url="market-trades-spot",
        start_date=start_date,
        end_date=end_date,
        exchanges=exchange,
    )
    assert expected_file_names == actual_file_names


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_get_list_of_files_market_quotes() -> None:
    expected_file_names: List[str] = []
    start_date = datetime(2015, 7, 15)
    end_date = datetime(2015, 7, 17)
    exchange = "Binance"
    quotes_route = "market-quotes-spot"
    assets = ["1INCHUSD"]
    actual_file_names = data_exporter._get_list_files_to_download_from_ff_server(
        assets_pairs=assets,
        route_url=quotes_route,
        start_date=start_date,
        end_date=end_date,
        exchanges=exchange,
    )
    assert expected_file_names == actual_file_names


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_download_jsongz_market_trades() -> None:
    """
    Tests downloading some market trades spot data
    """
    assert not (os.path.exists("market-trades-spot/binance/2017-07-15.json.gz"))
    assert not (os.path.exists("market-trades-spot/binance/2017-07-16.json.gz"))
    assert not (os.path.exists("market-trades-spot/binance/2017-07-17.json.gz"))
    start_date = datetime(2017, 7, 15)
    end_date = datetime(2017, 7, 17)
    data_exporter.export_market_trades_spot_data(
        start_date=start_date,
        end_date=end_date,
        exchanges="binance",
        output_format="json.gz",
    )
    assert os.path.exists("market-trades-spot/binance/2017-07-15.json.gz")
    assert os.path.exists("market-trades-spot/binance/2017-07-16.json.gz")
    assert os.path.exists("market-trades-spot/binance/2017-07-17.json.gz")


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_download_market_trades_futures() -> None:
    list_of_expected_files = [
        "market-trades-future/binance/2022-07-15.json.gz",
        "market-trades-future/binance/2022-07-16.json.gz",
        "market-trades-future/binance/2022-07-17.json.gz",
    ]
    files_downloaded_test_helper_start(list_of_expected_files)
    start_date = datetime(2022, 7, 15)
    end_date = datetime(2022, 7, 17)
    data_exporter.export_market_trades_future_data(
        start_date=start_date,
        end_date=end_date,
        exchanges="binance",
        output_format="json.gz",
    )
    files_downloaded_test_helper_end(list_of_expected_files)


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_download_json_market_trades_spot() -> None:
    list_of_expected_files = [
        "market-trades-spot/binance/2019-07-15.json",
        "market-trades-spot/binance/2019-07-16.json",
        "market-trades-spot/binance/2019-07-17.json",
    ]
    files_downloaded_test_helper_start(list_of_expected_files)
    start_date = datetime(2019, 7, 15)
    end_date = datetime(2019, 7, 17)
    data_exporter.export_market_trades_spot_data(
        start_date=start_date,
        end_date=end_date,
        exchanges="binance",
        output_format="json",
    )
    files_downloaded_test_helper_end(list_of_expected_files)


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_download_csv_market_trades() -> None:
    """
    Tests the same set of files are created fine using the csv output option
    """
    assert not (os.path.exists("market-trades-spot/binance/2017-07-15.csv"))
    assert not (os.path.exists("market-trades-spot/binance/2017-07-16.csv"))
    assert not (os.path.exists("market-trades-spot/binance/2017-07-17.csv"))
    start_date = datetime(2017, 7, 15)
    end_date = datetime(2017, 7, 17)
    data_exporter.export_market_trades_spot_data(
        start_date=start_date,
        end_date=end_date,
        exchanges="binance",
        output_format="csv",
    )
    assert os.path.exists("market-trades-spot/binance/2017-07-15.csv")
    assert os.path.exists("market-trades-spot/binance/2017-07-16.csv")
    assert os.path.exists("market-trades-spot/binance/2017-07-17.csv")


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_download_json_market_trades() -> None:
    """
    Tests the same set of files are created as json files
    """
    assert not (os.path.exists("market-trades-spot/binance/2017-07-15.json"))
    assert not (os.path.exists("market-trades-spot/binance/2017-07-16.json"))
    assert not (os.path.exists("market-trades-spot/binance/2017-07-17.json"))
    start_date = datetime(2017, 7, 15)
    end_date = datetime(2017, 7, 17)
    data_exporter.export_market_trades_spot_data(
        start_date=start_date,
        end_date=end_date,
        exchanges="binance",
        output_format="json",
    )
    assert os.path.exists("market-trades-spot/binance/2017-07-15.json")
    assert os.path.exists("market-trades-spot/binance/2017-07-16.json")
    assert os.path.exists("market-trades-spot/binance/2017-07-17.json")
    loaded_data = json.load(open("market-trades-spot/binance/2017-07-15.json"))
    assert (
        loaded_data[0]["market"] == "binance-bnb-btc-spot"
    )  # spot checking a known value in the data file


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_invalid_exchange_value_error() -> None:
    """
    Tests that ValueError is thrown when an invalid exchange is provided
    """
    start_date = datetime(2017, 7, 15)
    end_date = datetime(2017, 7, 17)
    with pytest.raises(ValueError) as excinfo:
        data_exporter.export_market_trades_spot_data(
            start_date=start_date,
            end_date=end_date,
            exchanges=["invalid_exchange", "binance"],
            output_format="csv",
        )


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_invalid_output_format_exchange_value_error() -> None:
    """
    Tests that ValueError is thrown when an invalid output format is provided
    """
    start_date = datetime(2017, 7, 15)
    end_date = datetime(2017, 7, 17)
    with pytest.raises(ValueError) as excinfo:
        data_exporter.export_market_trades_spot_data(
            start_date=start_date,
            end_date=end_date,
            exchanges=["binance"],
            output_format="invalid_format",
        )


if __name__ == "__main__":
    pytest.main()
