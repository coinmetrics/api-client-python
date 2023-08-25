import datetime
import os
from coinmetrics.api_client import CoinMetricsClient
from concurrent.futures import ThreadPoolExecutor

if __name__ == '__main__':
    """
    This example will take a very large orderbook - binance-eth-btc-spot and split the export into 31 daily files, 
    this will make exporting this data much faster. It is commented out but it could even be split int 745 hourly files
    each of which will end up at ~3mb as an example. In general time increments of less than a month can use 
    datetime.timedelta to specify, larget time increments can use dateutil.relativedelta.relativedelta to specify months
    or years
    """
    MARKET_ORDERBOOKS = [
                         "binance-eth-btc-spot",
    ]
    # TIME_INCREMENT = datetime.timedelta(hours=1)
    TIME_INCREMENT = datetime.timedelta(days=1)
    client = CoinMetricsClient(os.environ['CM_API_KEY'])
    start_date = "2023-03-01"
    end_date = "2023-04-01"
    if not os.path.exists("./data_export"):
        os.mkdir("./data_export")
    client.get_market_orderbooks(markets=MARKET_ORDERBOOKS,
                                 start_time=start_date,
                                 end_time=end_date,
                                 page_size=1000).parallel(time_increment=TIME_INCREMENT, executor=ThreadPoolExecutor).export_to_csv_files("./data_export")
