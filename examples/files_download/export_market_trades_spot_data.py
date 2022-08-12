from coinmetrics.data_exporter import CoinMetricsDataExporter
from datetime import datetime

CM_API_KEY = "<YOUR_API_KEY>"
data_exporter = CoinMetricsDataExporter(api_key=CM_API_KEY)

if __name__ == "__main__":
    """
    This script will export all the daily market-trades-spot files for Coinbase and Gemini for the month of January  
    """
    start_date = datetime(2019, 1, 1)
    end_date = datetime(2019, 1, 31)
    exchanges = ["coinbase","gemini"]
    data_exporter.export_market_trades_spot_data(start_date=start_date, end_date=end_date, exchanges=exchanges, threaded=True)