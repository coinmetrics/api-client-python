# type: ignore
import datetime
from datetime import timedelta
import os

import dateutil.relativedelta
import pandas as pd
from coinmetrics.api_client import CoinMetricsClient
from coinmetrics._data_collection import DataCollection, ParallelDataCollection
from copy import deepcopy
from enum import Enum
from typing import Tuple



client = CoinMetricsClient(os.environ.get("CM_API_KEY"))

def compare_performance_data_collections(data_collection: DataCollection, max_workers: int = 10) -> None:
    """
    This function will compare
    """
    compare_export_to_csv(data_collection)
    compare_export_to_df(data_collection)
    compare_export_to_csv_normal_parallel_multiple_csvs(data_collection)
    compare_export_to_json_normal_parallel_multiple_jsons(data_collection)


def compare_export_to_csv(data_collection: DataCollection, max_workers: int = 10) -> None:
    start_time_normal = datetime.datetime.now()
    _normal_trades = deepcopy(data_collection).export_to_csv("test.csv")
    print(f"normal export to csv took: {datetime.datetime.now() - start_time_normal}")
    start_time_parallel = datetime.datetime.now()
    _parallel_trades = deepcopy(data_collection).parallel(max_workers=max_workers).export_to_csv("test_parallel.csv")
    print(f"parallel export to csv took: {datetime.datetime.now() - start_time_parallel}")


def compare_export_to_df(data_collection: DataCollection, max_workers: int = 10) -> Tuple[pd.DataFrame, pd.DataFrame]:
    start_time_normal = datetime.datetime.now()
    normal_df = deepcopy(data_collection).to_dataframe()
    print(f"normal export to dataframe took: {datetime.datetime.now() - start_time_normal}")
    start_time_parallel = datetime.datetime.now()
    parallel_df = deepcopy(data_collection).parallel(max_workers=max_workers).to_dataframe()
    print(f"parallel export to dataframe took: {datetime.datetime.now() - start_time_parallel}")
    return normal_df, parallel_df


def compare_export_to_list(data_collection: DataCollection, max_workers: int = 10):
    start_time_normal = datetime.datetime.now()
    normal_df = deepcopy(data_collection).to_list()
    print(f"normal export to list took: {datetime.datetime.now() - start_time_normal}")
    start_time_parallel = datetime.datetime.now()
    parallel_df = deepcopy(data_collection).parallel(max_workers=max_workers).to_list()
    print(f"parallel export to list took: {datetime.datetime.now() - start_time_parallel}")

def compare_export_to_csv_normal_parallel_multiple_csvs(data_collection: DataCollection):
    start_time_normal = datetime.datetime.now()
    normal_df = deepcopy(data_collection).export_to_csv("testsingle.csv")
    print(f"normal export to single csv file took: {datetime.datetime.now() - start_time_normal}")
    start_time_parallel = datetime.datetime.now()
    parallel_df = deepcopy(data_collection).parallel().export_to_csv_files()
    print(f"parallel export to many csv files took: {datetime.datetime.now() - start_time_parallel}")
    return normal_df, parallel_df

def compare_export_to_json_normal_parallel_multiple_jsons(data_collection: DataCollection, max_workers: int = 10):
    start_time_normal = datetime.datetime.now()
    normal_df = deepcopy(data_collection).export_to_csv("testsingle.json")
    print(f"normal export to single json file took: {datetime.datetime.now() - start_time_normal}")
    start_time_parallel = datetime.datetime.now()
    parallel_df = deepcopy(data_collection).parallel(max_workers=max_workers).export_to_json_files()
    print(f"parallel export to many json files took: {datetime.datetime.now() - start_time_parallel}")
    return normal_df, parallel_df

def parallel_time_analysis(data_collection: DataCollection) -> None:
    if not os.path.exists("data"):
        os.mkdir("data")
    start_time = datetime.datetime.now()
    deepcopy(data_collection).parallel().export_to_csv("examplecsv.csv")
    print(f"Parallel export to csv took: {datetime.datetime.now() - start_time}")
    start_time = datetime.datetime.now()
    deepcopy(data_collection).parallel().export_to_csv_files("./data")
    print(f"Parallel export to many csv took: {datetime.datetime.now() - start_time}")
    start_time = datetime.datetime.now()
    deepcopy(data_collection).parallel().export_to_json()
    print(f"Parallel export to json: took {datetime.datetime.now() - start_time}")
    start_time = datetime.datetime.now()
    deepcopy(data_collection).parallel().export_to_json_files("./data")
    print(f"Parallel export to many json files took: {datetime.datetime.now() - start_time}")
    start_time = datetime.datetime.now()
    deepcopy(data_collection).parallel().to_list()
    print(f"Parallel export to list took: {datetime.datetime.now() - start_time}")
    start_time = datetime.datetime.now()
    deepcopy(data_collection).parallel().to_dataframe()
    print(f"Parallel export to dataframe took: {datetime.datetime.now() - start_time}")


def normal_time_analysis(data_collection: DataCollection) -> None:
    if not os.path.exists("data"):
        os.mkdir("data")
    start_time = datetime.datetime.now()
    deepcopy(data_collection).export_to_csv("examplecsv.csv")
    print(f"Normal export to csv took: {datetime.datetime.now() - start_time}")
    start_time = datetime.datetime.now()
    deepcopy(data_collection).export_to_json()
    print(f"Normal export to json: took {datetime.datetime.now() - start_time}")
    start_time = datetime.datetime.now()
    deepcopy(data_collection).to_list()
    print(f"Normal export to list took: {datetime.datetime.now() - start_time}")
    start_time = datetime.datetime.now()
    deepcopy(data_collection).to_dataframe()
    print(f"Normal export to dataframe took: {datetime.datetime.now() - start_time}")


if __name__ == '__main__':
    client = CoinMetricsClient(os.environ.get("CM_API_KEY"))
    start_time = datetime.datetime.now()
    assets = ["btc", "eth", "algo"]
    client.get_asset_metrics(
        assets=assets,
        metrics="ReferenceRateUSD",
        frequency="1m",
        start_time="2022-03-01",
        end_time="2023-03-01",
        page_size=1000,
        end_inclusive=False).parallel(
        time_increment=dateutil.relativedelta.relativedelta(months=1)).export_to_csv("btcRRs.csv")
    print(f"Time taken parallel: {datetime.datetime.now() - start_time}")
    start_time = datetime.datetime.now()
    client.get_asset_metrics(
        assets=assets,
        metrics="ReferenceRateUSD",
        frequency="1m",
        start_time="2022-03-01",
        end_time="2023-03-01",
        page_size=1000,
        end_inclusive=False).export_to_csv("btcRRsNormal.csv")
    print(f"Time taken normal: {datetime.datetime.now() - start_time}")