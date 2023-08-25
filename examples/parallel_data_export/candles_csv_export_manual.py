import datetime
import os
from coinmetrics.api_client import CoinMetricsClient
from concurrent.futures import ProcessPoolExecutor
from typing import Optional, List


def download_all_market_candles_for_assets(assets: List[str], start_date: str, end_date: str, data_dir: str = ".") -> None:
    """
    This function will download all the market candles for an asset over the given time period
    :param assets: List of assets i.e. ["btc", "eth", "busd", ...]
    :param start_date: Start date in YYYY-MM-DD format
    :param end_date: End Date in YYYY-MM-DD format
    :param data_dir: directory to dump files
    """
    client = CoinMetricsClient(os.environ["CM_API_KEY"])
    set_markets = set()
    for asset in assets:
        markets_for_asset = [market['market'] for market in client.catalog_market_candles(asset=asset, market_type="spot")]
        set_markets.update(markets_for_asset)

    with ProcessPoolExecutor(max_workers=10) as processor:
        for i, market in enumerate(set_markets):
            processor.submit(download_csv_of_market_candles, market=market, start_time=start_date, end_time=end_date, data_dir=data_dir, counter=i)



def download_csv_of_market_candles(market: str, start_time: str, end_time: str, data_dir: str = ".", counter: Optional[int] = None) -> None:
    client = CoinMetricsClient(os.environ["CM_API_KEY"])
    process_start_time = datetime.datetime.now()
    full_file_path = os.path.join(data_dir, f"{market}_{start_time}_{end_time}.csv")
    data = client.get_market_candles(markets=market, frequency="1m", start_time=start_time, end_time=end_time, page_size=1000).export_to_csv(full_file_path, compress=True)  # type: ignore
    print(f"market: {market} downloaded at: {full_file_path}. Took: {datetime.datetime.now() - process_start_time}. Market #: {counter}")


if __name__ == '__main__':
    """
    This example exists as an explanation for how the parallel feature is working under the hood - it is spliting a 
    single query into many queries based on the first parameter usually, and then either combining the results at the 
    end or exporting them separately.
    
    In this specific cases it exports all BUSD market candles for spot markets 
    """
    list_assets = ["busd"]
    start_time = "2022-07-01"
    end_time = "2022-12-31"
    download_all_market_candles_for_assets(assets=list_assets, start_date=start_time, end_date=end_time)
