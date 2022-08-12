from coinmetrics.data_exporter import CoinMetricsDataExporter
from datetime import datetime

CM_API_KEY = "<YOUR_API_KEY>>"
data_exporter = CoinMetricsDataExporter(api_key=CM_API_KEY)

if __name__ == "__main__":
    """
    This script will export all the daily market-quotes-future for the supplied assets files for ByBit for the month
     of June 2022, as csv files.
     
     Note when writing these scripts it may be helpful to use the CLI commands in order to quickly find the valid values
     for asset pairs and exchanges:
     coinmetrics export get-exchanges market-quotes-future 
     coinmetrics export get-asset-pairs market-quotes-future bybit 
     
    """
    start_date = datetime(2022, 5, 1)
    end_date = datetime(2022, 5, 30)
    asset_pairs = ["ADAUSD", "ALGOUSDT", "1INCHUSDT"]
    exchanges = ["Bybit"]
    data_exporter.export_market_quotes_future_data(start_date=start_date,
                                                   end_date=end_date,
                                                   asset_pairs=asset_pairs,
                                                   exchanges=exchanges,
                                                   threaded=True,
                                                   output_format="csv")