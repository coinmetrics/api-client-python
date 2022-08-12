from coinmetrics.data_exporter import CoinMetricsDataExporter
from datetime import datetime

CM_API_KEY = "<YOUR_API_KEY>"
data_exporter = CoinMetricsDataExporter(api_key=CM_API_KEY)

if __name__ == "__main__":
    """
    This script will export all the daily market-quotes-spot for Binance BTC asset pairs files for the month
     of May 2022, as json.gz files. Note this may take a long time to run because the trade volumes for Binance is very 
     large, so the files are also very large. For this reason we are using the json.gz file type here, which is 
     a compressed data format

     Note when writing these scripts it may be helpful to use the CLI commands in order to quickly find the valid values
     for asset pairs and exchanges:
     coinmetrics export get-exchanges market-quotes-spot
     coinmetrics export get-asset-pairs market-quotes-future binance 

    """
    start_date = datetime(2022, 5, 1)
    end_date = datetime(2022, 5, 30)
    asset_pairs = data_exporter.get_asset_pairs("market-quotes-spot", "Binance")
    btc_binance_asset_pairs = [pair for pair in asset_pairs if "BTC" in pair]
    exchanges = ["Binance"]
    data_exporter.export_market_quotes_spot_data(start_date=start_date,
                                                   end_date=end_date,
                                                   asset_pairs=btc_binance_asset_pairs,
                                                   exchanges=exchanges,
                                                   threaded=True,
                                                   output_format="json.gz")