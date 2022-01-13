from typing import Any
from unittest.mock import Mock

from coinmetrics.api_client import CoinMetricsClient, requests
from coinmetrics._catalogs import (
    CatalogAssetsData,
    CatalogAssetAlertsData,
    CatalogAssetPairsData,
    CatalogExchangeAssetsData,
    CatalogExchangesData,
    CatalogIndexesData,
    CatalogInstitutionsData,
    CatalogMarketsData,
    CatalogMetricsData,
)
from coinmetrics._data_collection import DataCollection
from coinmetrics._typing import (
    DataRetrievalFuncType,
    UrlParamTypes,
    Dict,
    DataReturnType,
    DataFrameType,
)

try:
    import pandas as pd  # type: ignore

    DataFrameType = pd.core.frame.DataFrame
except ImportError:
    pd = None
    DataFrameType = Any

catalog_assets_test_data = [
    {
        "asset": "btc",
        "full_name": "Bitcoin",
        "metrics": [
            {
                "metric": "TestMetric",
                "frequencies": [
                    {
                        "frequency": "1b",
                        "min_time": "2009-01-03T18:15:05.000000000Z",
                        "max_time": "2020-06-08T20:22:17.000000000Z",
                        "min_height": "0",
                        "max_height": "10",
                        "min_hash": "0abc",
                        "max_hash": "0xyz",
                    },
                    {
                        "frequency": "1d",
                        "min_time": "2009-01-03T00:00:00.000000000Z",
                        "max_time": "2020-06-07T00:00:00.000000000Z",
                        "community": True,
                    },
                ],
            }
        ],
        "exchanges": ["binance", "coinbase", "kraken"],
        "markets": [
            "binance-btc-usdt-spot",
            "binance-eth-btc-spot",
            "coinbase-btc-usd-spot",
            "coinbase-eth-btc-spot",
            "kraken-btc-usd-spot",
        ],
    }
]

catalog_metrics_test_data = [
    {
        "metric": "AdrActCnt",
        "full_name": "Addresses, active, count",
        "description": "The sum count of unique addresses that were active in the network (either as a recipient or originator of a ledger change) that interval. All parties in a ledger change action (recipients and originators) are counted. Individual addresses are not double-counted if previously active.",
        "category": "Addresses",
        "subcategory": "Active",
        "unit": "Addresses",
        "data_type": "bigint",
        "frequencies": [
            {"frequency": "1b", "assets": ["btc", "eth"]},
            {"frequency": "1d", "assets": ["ada", "btc", "eth"]},
        ],
    },
    {
        "metric": "FlowInBFXNtv",
        "full_name": "Flow, in, to Bitfinex, native units",
        "description": "The sum in native units sent to Bitfinex that interval.",
        "category": "Exchange",
        "subcategory": "Deposits",
        "unit": "Native units",
        "data_type": "decimal",
        "frequencies": [
            {"frequency": "1b", "assets": ["btc", "eth"]},
            {"frequency": "1d", "assets": ["btc", "eth"]},
        ],
        "reviewable": "True",
    },
]

catalog_markets_test_data = [
    {
        "market": "bitmex-XBTF15-future",
        "min_time": "2014-11-24T13:05:32.850000000Z",
        "max_time": "2015-01-30T12:00:00.000000000Z",
        "trades": {
            "min_time": "2014-11-24T13:05:32.850000000Z",
            "max_time": "2015-01-30T12:00:00.000000000Z",
        },
        "exchange": "bitmex",
        "type": "future",
        "symbol": "XBTF15",
        "base": "btc",
        "quote": "usd",
        "size_asset": "XBT",
        "margin_asset": "USD",
        "contract_size": "1",
        "tick_size": "0.1",
        "listing": "2014-11-24T13:05:32.850000000Z",
        "expiration": "2015-01-30T12:00:00.000000000Z",
    },
    {
        "market": "bitfinex-agi-btc-spot",
        "min_time": "2018-04-07T16:25:55.000000000Z",
        "max_time": "2020-03-25T20:12:09.639000000Z",
        "trades": {
            "min_time": "2018-04-07T16:25:55.000000000Z",
            "max_time": "2020-03-25T20:12:09.639000000Z",
        },
        "exchange": "bitfinex",
        "type": "spot",
        "base": "agi",
        "quote": "btc",
    },
]

catalog_exchanges_test_data = [
    {
        "exchange": "bibox",
        "markets": ["bibox-abt-btc-spot", "bibox-etc-usdt-spot"],
        "min_time": "2019-04-24T11:09:59.000000000Z",
        "max_time": "2019-05-18T16:06:10.927000000Z",
        "metrics": [
            {
                "metric": "volume_reported_spot_usd_1d",
                "frequencies": [
                    {
                        "frequency": "1d",
                        "min_time": "2019-04-30T00:00:00.000000000Z",
                        "max_time": "2019-06-16T00:00:00.000000000Z",
                    }
                ],
            },
            {
                "metric": "volume_reported_spot_usd_1h",
                "frequencies": [
                    {
                        "frequency": "1h",
                        "min_time": "2019-04-29T21:00:00.000000000Z",
                        "max_time": "2019-06-17T15:00:00.000000000Z",
                    }
                ],
            },
        ],
    },
    {
        "exchange": "binance",
        "markets": [
            "binance-BTCUSDT-future",
            "binance-LTCUSDT-future",
            "binance-ada-bnb-spot",
            "binance-btc-usdt-spot",
            "binance-bcpt-btc-spot",
            "binance-bcd-eth-spot",
        ],
        "min_time": "2017-07-14T04:00:00.510000000Z",
        "max_time": "2020-06-08T20:33:28.868000000Z",
        "metrics": [
            {
                "metric": "volume_reported_spot_usd_1d",
                "frequencies": [
                    {
                        "frequency": "1d",
                        "min_time": "2019-04-30T00:00:00.000000000Z",
                        "max_time": "2019-06-16T00:00:00.000000000Z",
                    }
                ],
            },
            {
                "metric": "volume_reported_spot_usd_1h",
                "frequencies": [
                    {
                        "frequency": "1h",
                        "min_time": "2019-04-29T21:00:00.000000000Z",
                        "max_time": "2019-06-17T15:00:00.000000000Z",
                    }
                ],
            },
        ],
    },
]

catalog_exchange_assets_test_data = [
    {
        "exchange_asset": "binance-btc",
        "metrics": [
            {
                "metric": "volume_trusted_spot_usd_1d",
                "frequencies": [
                    {
                        "frequency": "1d",
                        "min_time": "2020-10-16T00:00:00.000000000Z",
                        "max_time": "2021-01-05T00:00:00.000000000Z",
                    }
                ],
            },
            {
                "metric": "volume_trusted_spot_usd_1h",
                "frequencies": [
                    {
                        "frequency": "1h",
                        "min_time": "2020-10-15T03:00:00.000000000Z",
                        "max_time": "2021-01-06T12:00:00.000000000Z",
                    }
                ],
            },
        ],
    },
    {
        "exchange_asset": "coinbase-eth",
        "metrics": [
            {
                "metric": "volume_trusted_spot_usd_1d",
                "frequencies": [
                    {
                        "frequency": "1d",
                        "min_time": "2020-10-11T00:00:00.000000000Z",
                        "max_time": "2021-01-05T00:00:00.000000000Z",
                    }
                ],
            },
            {
                "metric": "volume_trusted_spot_usd_1h",
                "frequencies": [
                    {
                        "frequency": "1h",
                        "min_time": "2020-10-10T19:00:00.000000000Z",
                        "max_time": "2021-01-06T12:00:00.000000000Z",
                    }
                ],
            },
        ],
    },
]

catalog_asset_pairs_test_data = [
    {
        "pair": "aave-bnb",
        "metrics": [
            {
                "metric": "volume_trusted_spot_usd_1d",
                "frequencies": [
                    {
                        "frequency": "1d",
                        "min_time": "2020-10-16T00:00:00.000000000Z",
                        "max_time": "2021-01-05T00:00:00.000000000Z",
                    }
                ],
            },
            {
                "metric": "volume_trusted_spot_usd_1h",
                "frequencies": [
                    {
                        "frequency": "1h",
                        "min_time": "2020-10-15T03:00:00.000000000Z",
                        "max_time": "2021-01-06T12:00:00.000000000Z",
                    }
                ],
            },
        ],
    },
    {
        "pair": "aave-btc",
        "metrics": [
            {
                "metric": "volume_trusted_spot_usd_1d",
                "frequencies": [
                    {
                        "frequency": "1d",
                        "min_time": "2020-10-11T00:00:00.000000000Z",
                        "max_time": "2021-01-05T00:00:00.000000000Z",
                    }
                ],
            },
            {
                "metric": "volume_trusted_spot_usd_1h",
                "frequencies": [
                    {
                        "frequency": "1h",
                        "min_time": "2020-10-10T19:00:00.000000000Z",
                        "max_time": "2021-01-06T12:00:00.000000000Z",
                    }
                ],
            },
        ],
    },
]

catalog_institutions_test_data = [
    {
        "institution": "grayscale",
        "metrics": [
            {
                "metric": "gbtc_total_assets",
                "frequencies": [
                    {
                        "frequency": "1d",
                        "min_time": "2020-10-16T00:00:00.000000000Z",
                        "max_time": "2021-01-05T00:00:00.000000000Z",
                    }
                ],
            },
            {
                "metric": "gbtc_shares_outstanding",
                "frequencies": [
                    {
                        "frequency": "1h",
                        "min_time": "2020-10-15T03:00:00.000000000Z",
                        "max_time": "2021-01-06T12:00:00.000000000Z",
                    }
                ],
            },
        ],
    }
]

catalog_indexes_test_data = [
    {
        "index": "CMBI10",
        "description": "'CMBI10' index.",
        "frequencies": [
            {
                "frequency": "15s",
                "min_time": "2020-06-08T20:12:40.000000000Z",
                "max_time": "2020-06-08T20:29:30.000000000Z",
            }
        ],
    },
    {
        "index": "CMBIBTC",
        "description": "'CMBIBTC' index.",
        "frequencies": [
            {
                "frequency": "15s",
                "min_time": "2010-07-18T20:00:00.000000000Z",
                "max_time": "2020-06-08T20:29:45.000000000Z",
            },
            {
                "frequency": "1d",
                "min_time": "2010-07-19T00:00:00.000000000Z",
                "max_time": "2020-06-08T00:00:00.000000000Z",
            },
            {
                "frequency": "1d-ny-close",
                "min_time": "2010-07-18T20:00:00.000000000Z",
                "max_time": "2020-06-08T20:00:00.000000000Z",
            },
            {
                "frequency": "1d-sg-close",
                "min_time": "2010-07-19T08:00:00.000000000Z",
                "max_time": "2020-06-08T08:00:00.000000000Z",
            },
            {
                "frequency": "1h",
                "min_time": "2010-07-18T20:00:00.000000000Z",
                "max_time": "2020-06-08T20:00:00.000000000Z",
            },
        ],
    },
]

catalog_asset_alerts_test_data = [
    {
        "asset": "btc",
        "name": "block_count_empty_6b_hi",
        "description": "description",
        "threshold": "4",
        "constituents": ["block_count_empty_6b"],
    }
]
def get_empty_data(x: Any, y: Any) -> DataReturnType:
    return {"data": []}


def test_catalog_assets_request(mocker: Any) -> None:
    client = CoinMetricsClient("xxx")
    mock = Mock()
    mock.content = '{"data": [{"asset": "btc", "markets": ["coinbase-btc-usd-spot"]}]}'
    mocked_obj = mocker.patch.object(requests, "get", return_value=mock)
    response = client.catalog_assets(assets="btc")
    mocked_obj.assert_called_once_with(
        "https://api.coinmetrics.io/v4/catalog/assets?api_key=xxx&assets=btc",
        verify=True,
        headers=client._http_header,
    )
    assert response == [{"asset": "btc", "markets": ["coinbase-btc-usd-spot"]}]


def test_base_url() -> None:
    assert CoinMetricsClient("xxx")._api_base_url == "https://api.coinmetrics.io/v4"
    assert CoinMetricsClient("xxx")._api_key_url_str == "api_key=xxx"
    assert (
        CoinMetricsClient()._api_base_url == "https://community-api.coinmetrics.io/v4"
    )
    assert CoinMetricsClient()._api_key_url_str == ""


def test_to_dataframe() -> None:
    test_param_dict: Dict[str, UrlParamTypes] = {"asset": "btc", "metric": "1"}
    test_data_dict: DataReturnType = {"data": [test_param_dict for i in range(2)]}
    test_header = ["col1", "col2"]

    test_data_retrieval_function: DataRetrievalFuncType = lambda x, y: test_data_dict

    test_data_collection: DataCollection = DataCollection(
        data_retrieval_function=test_data_retrieval_function,
        endpoint="",
        url_params=test_param_dict,
    )
    test_df: DataFrameType = test_data_collection.to_dataframe()
    assert test_df.shape == (2, 2)
    assert list(test_param_dict.keys()) == list(test_df.columns)
    assert (test_df["asset"] == "btc").all()

    test_data_collection_header = DataCollection(
        data_retrieval_function=test_data_retrieval_function,
        endpoint="",
        url_params=test_param_dict,
    )
    test_df_header: DataFrameType = test_data_collection_header.to_dataframe(
        header=test_header
    )
    assert list(test_df_header.columns) == test_header


def test_catalog_assets_dataframe() -> None:
    data = CatalogAssetsData(catalog_assets_test_data)
    df = data.to_dataframe()
    assert len(df) == df.asset.nunique()

    df_markets = data.to_dataframe(secondary_level="markets")
    df_markets["metrics"] = df_markets["metrics"].astype(str)
    df_markets_test = pd.read_csv("test/data/catalog_assets_markets.csv", dtype=str)
    assert (df_markets.values == df_markets_test.values).all()

    df_metrics = data.to_dataframe(secondary_level="metrics")
    df_metrics = df_metrics.fillna("").astype(str)
    df_metrics_test = pd.read_csv(
        "test/data/catalog_assets_metrics.csv", dtype=str
    ).fillna("")
    assert (df_metrics_test.values == df_metrics.values).all()


def test_catalog_metrics_dataframe() -> None:
    data = CatalogMetricsData(catalog_metrics_test_data)
    df = data.to_dataframe().fillna("")
    df_test = pd.read_csv("test/data/catalog_metrics.csv", dtype=str).fillna("")
    assert (df.values == df_test.values).all()


def test_catalog_markets_dataframe() -> None:
    data = CatalogMarketsData(catalog_markets_test_data)
    df = data.to_dataframe().fillna("").astype(str)
    df_test = pd.read_csv("test/data/catalog_markets.csv", dtype=str).fillna("")
    assert (df.values == df_test.values).all()


def test_catalog_exchanges_dataframe() -> None:
    data = CatalogExchangesData(catalog_exchanges_test_data)
    df = data.to_dataframe()
    assert len(df) == df.exchange.nunique()
    df_markets = data.to_dataframe(secondary_level="markets")
    df_markets = df_markets.fillna("").astype(str)
    df_markets_test = pd.read_csv(
        "test/data/catalog_exchanges_markets.csv", dtype=str
    ).fillna("")
    assert (df_markets.values == df_markets_test.values).all()

    df_metrics = data.to_dataframe(secondary_level="metrics")
    df_metrics = df_metrics.fillna("").astype(str)
    df_metrics_test = pd.read_csv(
        "test/data/catalog_exchanges_metrics.csv", dtype=str
    ).fillna("")
    assert (df_metrics_test.values == df_metrics.values).all()


def test_catalog_exchange_assets_dataframe() -> None:
    data = CatalogExchangeAssetsData(catalog_exchange_assets_test_data)
    df = data.to_dataframe().fillna("").astype(str)
    df.to_csv("test/data/catalog_exchange_assets.csv", index_label=False)
    df_test = pd.read_csv("test/data/catalog_exchange_assets.csv", dtype=str).fillna("")
    assert (df.values == df_test.values).all()


def test_catalog_indexes_dataframe() -> None:
    data = CatalogIndexesData(catalog_indexes_test_data)
    df = data.to_dataframe().fillna("").astype(str)
    df_test = pd.read_csv("test/data/catalog_indexes.csv", dtype=str).fillna("")
    assert (df.values == df_test.values).all()


def test_catalog_institutions_dataframe() -> None:
    data = CatalogInstitutionsData(catalog_institutions_test_data)
    df = data.to_dataframe().fillna("").astype(str)
    df_test = pd.read_csv("test/data/catalog_institutions.csv", dtype=str).fillna("")
    assert (df.values == df_test.values).all()


def test_catalog_asset_pairs_dataframe() -> None:
    data = CatalogAssetPairsData(catalog_asset_pairs_test_data)
    df = data.to_dataframe().fillna("").astype(str)
    df_test = pd.read_csv("test/data/catalog_asset_pairs.csv", dtype=str).fillna("")
    assert (df.values == df_test.values).all()


def test_empty_dataframe() -> None:
    """Test client behavior when query results in no data"""
    empty_response = DataCollection(get_empty_data, "", {})
    assert empty_response
    assert empty_response.first_page() == []
    df = empty_response.to_dataframe()
    assert df.empty
