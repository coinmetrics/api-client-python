import os
from coinmetrics.api_client import CoinMetricsClient
from concurrent.futures import ThreadPoolExecutor


if __name__ == '__main__':
    """
    This script shows how to paralellize a request for BTC 1m minute metrics. First it will export them all to separate 
    CSV files, then it will also make a single CSV file
    """
    client = CoinMetricsClient(os.environ['CM_API_KEY'])
    ASSET = "btc"
    start_time = "2023-03-01"
    btc_1m_metrics = [metric['metric'] for metric in client.catalog_asset_metrics_v2(assets=ASSET).to_list()[0]['metrics'] if
     "1m" in [freq['frequency'] for freq in metric['frequencies']]]
    print("Exporting to single csv...")
    client.get_asset_metrics(assets="btc", metrics=btc_1m_metrics, frequency="1m", start_time=start_time, page_size=1000).parallel(parallelize_on=["metrics"]).export_to_csv("./data_export/btc_1m_asset_metrics.csv")
    if not os.path.exists("./data_export"):
        os.mkdir("./data_export")
    print("Exporting to many csv files")
    client.get_asset_metrics(assets="btc", metrics=btc_1m_metrics, frequency="1m", start_time=start_time, page_size=1000).parallel(parallelize_on=["metrics"]).export_to_csv_files("./data_export")
