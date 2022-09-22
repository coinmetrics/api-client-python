from coinmetrics.data_exporter import CoinMetricsDataExporter
from datetime import datetime

CM_API_KEY = "<YOUR_API_KEY>"
data_exporter = CoinMetricsDataExporter(api_key=CM_API_KEY)

if __name__ == "__main__":
    """
    This script will export all the daily market-candles-spot-5m files for all exchanges on the first day of the year in
    2020. It is using the threaded option so there is many files being downloaded at once  
    """
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2020, 1, 1)
    all_exchanges = data_exporter.get_exchanges("market-candles-spot-5m")
    frequency = "5m"
    data_exporter.export_market_candles_spot_data(frequency=frequency,
                                                  start_date=start_date,
                                                  end_date=end_date,
                                                  exchanges=all_exchanges,
                                                  threaded=True)