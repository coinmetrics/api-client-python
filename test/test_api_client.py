import logging
import os
from typing import Any, Type
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
    CatalogAssetPairCandlesData,
    CatalogMarketTradesData,
)
from coinmetrics._data_collection import DataCollection
from coinmetrics._typing import (
    DataRetrievalFuncType,
    UrlParamTypes,
    Dict,
    DataReturnType
)

try:
    import pandas as pd

    DataFrameType: Type[pd.core.frame.DataFrame] = pd.core.frame.DataFrame
except ImportError:
    logging.info("Pandas not imported")

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

catalog_candles_test_data = [
    {
        "frequencies": [
            {
                "frequency": "1m",
                "max_time": "2022-07-12T17:50:00.000000000Z",
                "min_time": "2020-12-26T01:00:00.000000000Z",
            },
            {
                "frequency": "5m",
                "max_time": "2022-07-12T17:45:00.000000000Z",
                "min_time": "2020-12-26T01:00:00.000000000Z",
            },
            {
                "frequency": "10m",
                "max_time": "2022-07-12T17:40:00.000000000Z",
                "min_time": "2020-12-26T01:00:00.000000000Z",
            },
            {
                "frequency": "15m",
                "max_time": "2022-07-12T17:30:00.000000000Z",
                "min_time": "2020-12-26T01:00:00.000000000Z",
            },
            {
                "frequency": "30m",
                "max_time": "2022-07-12T17:00:00.000000000Z",
                "min_time": "2020-12-26T01:00:00.000000000Z",
            },
            {
                "frequency": "1h",
                "max_time": "2022-07-12T16:00:00.000000000Z",
                "min_time": "2020-12-26T01:00:00.000000000Z",
            },
            {
                "frequency": "4h",
                "max_time": "2022-07-12T12:00:00.000000000Z",
                "min_time": "2020-12-26T00:00:00.000000000Z",
            },
            {
                "frequency": "1d",
                "max_time": "2022-07-11T00:00:00.000000000Z",
                "min_time": "2020-12-26T00:00:00.000000000Z",
            },
        ],
        "pair": "1inch-usd",
    },
    {
        "frequencies": [
            {
                "frequency": "1m",
                "max_time": "2022-07-12T17:50:00.000000000Z",
                "min_time": "2020-10-10T08:13:00.000000000Z",
            },
            {
                "frequency": "5m",
                "max_time": "2022-07-12T17:45:00.000000000Z",
                "min_time": "2020-10-10T08:10:00.000000000Z",
            },
            {
                "frequency": "10m",
                "max_time": "2022-07-12T17:40:00.000000000Z",
                "min_time": "2020-10-10T08:10:00.000000000Z",
            },
            {
                "frequency": "15m",
                "max_time": "2022-07-12T17:30:00.000000000Z",
                "min_time": "2020-10-10T08:00:00.000000000Z",
            },
            {
                "frequency": "30m",
                "max_time": "2022-07-12T17:00:00.000000000Z",
                "min_time": "2020-10-10T08:00:00.000000000Z",
            },
            {
                "frequency": "1h",
                "max_time": "2022-07-12T16:00:00.000000000Z",
                "min_time": "2020-10-10T08:00:00.000000000Z",
            },
            {
                "frequency": "4h",
                "max_time": "2022-07-12T12:00:00.000000000Z",
                "min_time": "2020-10-10T08:00:00.000000000Z",
            },
            {
                "frequency": "1d",
                "max_time": "2022-07-11T00:00:00.000000000Z",
                "min_time": "2020-10-10T00:00:00.000000000Z",
            },
        ],
        "pair": "aave-usd",
    },
    {
        "frequencies": [
            {
                "frequency": "1m",
                "max_time": "2022-07-12T17:50:00.000000000Z",
                "min_time": "2018-02-26T00:00:00.000000000Z",
            },
            {
                "frequency": "5m",
                "max_time": "2022-07-12T17:45:00.000000000Z",
                "min_time": "2018-02-26T00:00:00.000000000Z",
            },
            {
                "frequency": "10m",
                "max_time": "2022-07-12T17:40:00.000000000Z",
                "min_time": "2018-02-26T00:00:00.000000000Z",
            },
            {
                "frequency": "15m",
                "max_time": "2022-07-12T17:30:00.000000000Z",
                "min_time": "2018-02-26T00:00:00.000000000Z",
            },
            {
                "frequency": "30m",
                "max_time": "2022-07-12T17:00:00.000000000Z",
                "min_time": "2018-02-26T00:00:00.000000000Z",
            },
            {
                "frequency": "1h",
                "max_time": "2022-07-12T16:00:00.000000000Z",
                "min_time": "2018-02-26T00:00:00.000000000Z",
            },
            {
                "frequency": "4h",
                "max_time": "2022-07-12T12:00:00.000000000Z",
                "min_time": "2018-02-26T00:00:00.000000000Z",
            },
            {
                "frequency": "1d",
                "max_time": "2022-07-11T00:00:00.000000000Z",
                "min_time": "2018-02-26T00:00:00.000000000Z",
            },
        ],
        "pair": "abt-usd",
    },
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

catalog_market_trades_data = [
    {
        "market": "binance-aave-btc-spot",
        "min_time": "2020-10-15T03:00:01.286000000Z",
        "max_time": "2022-07-12T21:00:39.933000000Z",
    },
    {
        "market": "binance-algo-usdc-spot",
        "min_time": "2019-06-22T00:00:07.600000000Z",
        "max_time": "2020-01-07T07:06:19.943000000Z",
    },
    {
        "market": "binance-atom-usdc-spot",
        "min_time": "2019-05-07T12:05:42.347000000Z",
        "max_time": "2022-07-12T21:01:25.281000000Z",
    },
]

catalog_market_quotes_data = [
    {
        "market": "coinbase-btc-usd-spot",
        "min_time": "2019-03-25T18:46:25.000000000Z",
        "max_time": "2022-07-12T21:01:40.000000000Z",
    },
    {
        "market": "coinbase-btc-usdt-spot",
        "min_time": "2021-08-20T13:00:00.000000000Z",
        "max_time": "2022-07-12T21:00:00.000000000Z",
    },
    {
        "market": "coinbase-eth-usd-spot",
        "min_time": "2019-03-25T18:46:25.000000000Z",
        "max_time": "2022-07-12T21:01:40.000000000Z",
    },
]

catalog_market_orderbook_data = [
    {
        "market": "binance-aave-btc-spot",
        "min_time": "2021-09-14T16:00:00.000000000Z",
        "max_time": "2022-07-12T20:00:00.000000000Z",
    },
    {
        "market": "binance-atom-usdc-spot",
        "min_time": "2021-09-14T16:00:00.000000000Z",
        "max_time": "2022-07-12T21:00:00.000000000Z",
    },
]


def get_empty_data(x: Any, y: Any) -> DataReturnType:
    return {"data": []}


def test_catalog_assets_request(mocker: Any) -> None:
    client = CoinMetricsClient("xxx")
    mock = Mock()
    mock.content = '{"data": [{"asset": "btc", "markets": ["coinbase-btc-usd-spot"]}]}'
    mocked_obj = mocker.patch.object(requests.Session, "get", return_value=mock)
    response = client.catalog_assets(assets="btc")
    mocked_obj.assert_called_once_with(
        "https://api.coinmetrics.io/v4/catalog/assets?api_key=xxx&assets=btc",
        verify=True,
        headers=client._session.headers,
        proxies={"http": None, "https": None},
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
    test_df: pd.DataFrame = test_data_collection.to_dataframe()
    assert test_df.shape == (2, 2)
    assert list(test_param_dict.keys()) == list(test_df.columns)
    assert (test_df["asset"] == "btc").all()

    test_data_collection_header = DataCollection(
        data_retrieval_function=test_data_retrieval_function,
        endpoint="",
        url_params=test_param_dict,
    )
    test_df_header: pd.DataFrame = test_data_collection_header.to_dataframe(
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
    print(os.getcwd())
    df_test = pd.read_csv("test/data/catalog_institutions.csv", dtype=str).fillna("")
    assert (df.values == df_test.values).all()


def test_catalog_asset_pairs_dataframe() -> None:
    data = CatalogAssetPairsData(catalog_asset_pairs_test_data)
    df = data.to_dataframe().fillna("").astype(str)
    df_test = pd.read_csv("test/data/catalog_asset_pairs.csv", dtype=str).fillna("")
    assert (df.values == df_test.values).all()


def test_catalog_asset_pairs_candles_dataframe() -> None:
    data = CatalogAssetPairCandlesData(catalog_candles_test_data)
    df = data.to_dataframe().fillna("").astype(str)
    df_test = pd.read_csv("test/data/catalog_asset_pair_candles.csv", dtype=str).fillna(
        ""
    )
    assert (df.values == df_test.values).all()


def test_catalog_market_trades_dataframe() -> None:
    data = CatalogMarketTradesData(catalog_market_trades_data)
    df = data.to_dataframe().fillna("").astype(str)
    df_test = pd.read_csv("test/data/catalog_market_trades.csv", dtype=str).fillna("")
    assert (df.values == df_test.values).all()


def test_catalog_market_orderbook_dataframe() -> None:
    data = CatalogMarketTradesData(catalog_market_orderbook_data)
    df = data.to_dataframe().fillna("").astype(str)
    df_test = pd.read_csv("test/data/catalog_market_orderbooks.csv", dtype=str).fillna(
        ""
    )
    assert (df.values == df_test.values).all()


def test_catalog_market_quotes() -> None:
    data = CatalogMarketTradesData(catalog_market_quotes_data)
    df = data.to_dataframe().fillna("").astype(str)
    df_test = pd.read_csv("test/data/catalog_market_quotes.csv", dtype=str).fillna("")
    assert (df.values == df_test.values).all()


def test_empty_dataframe() -> None:
    """Test client behavior when query results in no data"""
    empty_response = DataCollection(get_empty_data, "", {})
    assert empty_response
    assert empty_response.first_page() == []
    df = empty_response.to_dataframe()
    assert df.empty


def test_nested_dataframe() -> None:
    """Test the output for a dataframe with nested values"""
    nested_data: Dict[str, Any] = {
        "data": [
            {
                "time": "2020-05-01T22:00:00.000000000Z",
                "constituents": [
                    {"asset": "btc", "weight": "0.6"},
                    {"asset": "eth", "weight": "0.4"},
                ],
            }
        ]
    }

    def _get_test_data(x: Any, y: Any) -> DataReturnType:
        return nested_data

    test_data_collection = DataCollection(_get_test_data, "", {})
    df_nested = test_data_collection.to_dataframe()
    assert pd.api.types.is_datetime64tz_dtype(df_nested["time"])
    assert pd.api.types.is_string_dtype(df_nested["constituents"])
    assert pd.api.types.is_dict_like(df_nested["constituents"])
    assert pd.api.types.is_list_like(df_nested["constituents"])


def test_timeseries_dataframe() -> None:
    """Test the output dataframe of a timeseries response"""
    test_data: Dict[str, Any] = {
        "data": [
            {
                "time": "2022-01-01T00:00:00.000000000Z",
                "str_column": "str_value_1",
                "int_column": "1",
                "float_column": "1.5",
            },
            {
                "time": "2022-01-01T01:00:00.000000000Z",
                "str_column": "str_value_2",
                "int_column": "2",
                "float_column": "3.0",
            },
        ]
    }

    def _get_test_data(x: Any, y: Any) -> DataReturnType:
        return test_data

    test_data_collection = DataCollection(_get_test_data, "", {})
    df_test = test_data_collection.to_dataframe()
    assert pd.api.types.is_datetime64tz_dtype(df_test["time"])
    assert pd.api.types.is_integer_dtype(df_test["int_column"])
    assert pd.api.types.is_float_dtype(df_test["float_column"])
    assert pd.api.types.is_string_dtype(df_test["str_column"])


def test_export_to_csv() -> None:
    """Test the export_to_csv function"""
    test_data: Dict[str, Any] = {
        "data": [
            {
                "time": "2022-01-01T00:00:00.000000000Z",
                "test_column": "test_value1",
                "test_nested": [
                    {"asset": "btc", "weight": "0.6"},
                    {"asset": "eth", "weight": "0.4"},
                ],
            },
            {
                "time": "2022-01-01T01:00:00.000000000Z",
                "test_column": "test_value2",
                "test_nested": [
                    {"asset": "btc", "weight": "0.5"},
                    {"asset": "eth", "weight": "0.5"},
                ],
            },
        ]
    }

    def _get_test_data(x: Any, y: Any) -> DataReturnType:
        return test_data

    test_data_collection = DataCollection(_get_test_data, "", {})
    test_csv_str = test_data_collection.export_to_csv()
    if test_csv_str is not None:
        assert test_csv_str.split("\n")[0] == "time,test_column,test_nested"
        row1_str = test_csv_str.split("\n")[1]
        row1_value = row1_str.strip('"').split('","')
        assert len(row1_value) == len(test_data["data"][0].keys())
        assert row1_value[0] == test_data["data"][0]["time"]
        assert row1_value[1] == test_data["data"][0]["test_column"]
        assert row1_value[2] == str(test_data["data"][0]["test_nested"])
    else:
        raise
