import os
import pprint

import typer
from datetime import datetime
from coinmetrics.data_exporter import CoinMetricsDataExporter
from typing import Union

coinmetrics_app = typer.Typer()
export_app = typer.Typer()

STRING_LIST_HELP_MSG = (
    "Pass in arguments as a list of strings separated by by commas i.e. {}"
)
HELP_MSG_EXCHANGES = STRING_LIST_HELP_MSG.format("binance,coinbase,bitmex")
HELP_MSG_ASSET_PAIRS = STRING_LIST_HELP_MSG.format("1INCHUSDT,BTCUSDT")
DATE_ARGUMENT = typer.Argument(str(datetime.now()).split(" ")[0])


@export_app.command()
def market_candles_spot(
    frequency: str,
    exchanges: str = typer.Argument(..., help=HELP_MSG_EXCHANGES),
    start_date: datetime = DATE_ARGUMENT,
    end_date: datetime = DATE_ARGUMENT,
    output_format: str = "json.gz",
    threaded: bool = False,
    api_key: Union[str, None] = None,
) -> None:
    """
    Used to export data related to spot market candles.
    Format: coinmetrics export market-candles-spot <exchanges> <start_date> <end_date>
    Example: coinmetrics export market-candles-spot coinbase,binance 2022-01-01 2022-01-03.
    """
    list_exchanges = exchanges.split(",")
    api_key = api_key or os.environ["CM_API_KEY"]
    data_exporter = CoinMetricsDataExporter(api_key=api_key)
    data_exporter.export_market_candles_spot_data(
        frequency=frequency,
        start_date=start_date,
        end_date=end_date,
        exchanges=list_exchanges,
        output_format=output_format,
        threaded=threaded,
    )


@export_app.command()
def market_candles_future(
    frequency: str,
    exchanges: str = typer.Argument(..., help=HELP_MSG_EXCHANGES),
    start_date: datetime = DATE_ARGUMENT,
    end_date: datetime = DATE_ARGUMENT,
    output_format: str = "json.gz",
    threaded: bool = False,
    api_key: Union[str, None] = None,
) -> None:
    """
    Used to export data related to future market candles.
    Format: coinmetrics export market-candles-future <exchanges> <start_date> <end_date>
    Example: coinmetrics export market-candles-future coinbase,binance 2022-01-01 2022-01-03.
    """
    list_exchanges = exchanges.split(",")
    api_key = api_key or os.environ["CM_API_KEY"]
    data_exporter = CoinMetricsDataExporter(api_key=api_key)
    data_exporter.export_market_candles_future_data(
        frequency=frequency,
        start_date=start_date,
        end_date=end_date,
        exchanges=list_exchanges,
        output_format=output_format,
        threaded=threaded,
    )


@export_app.command()
def market_trades_spot(
    exchanges: str = typer.Argument(..., help=HELP_MSG_EXCHANGES),
    start_date: datetime = DATE_ARGUMENT,
    end_date: datetime = DATE_ARGUMENT,
    output_format: str = "json.gz",
    threaded: bool = False,
    api_key: Union[str, None] = None,
) -> None:
    """
    Used to export data related to spot market trades.
    Format: coinmetrics export market-trades-spot <exchanges> <start_date> <end_date>
    Example: coinmetrics export market-trades-spot coinbase,binance 2022-01-01 2022-01-03.
    """
    list_exchanges = exchanges.split(",")
    api_key = api_key or os.environ["CM_API_KEY"]
    data_exporter = CoinMetricsDataExporter(api_key=api_key)
    data_exporter.export_market_trades_spot_data(
        start_date=start_date,
        end_date=end_date,
        exchanges=list_exchanges,
        output_format=output_format,
        threaded=threaded,
    )


@export_app.command()
def market_trades_future(
    exchanges: str = typer.Argument(..., help=HELP_MSG_EXCHANGES),
    start_date: datetime = DATE_ARGUMENT,
    end_date: datetime = DATE_ARGUMENT,
    output_format: str = "json.gz",
    threaded: bool = False,
    api_key: Union[str, None] = None,
) -> None:
    """
    Used to export data related to future market trades.
    Format: coinmetrics export market-trades-future <exchanges> <start_date> <end_date>
    Example: coinmetrics export market-trades-future coinbase,binance 2022-01-01 2022-01-03.
    """
    list_exchanges = exchanges.split(",")
    api_key = api_key or os.environ["CM_API_KEY"]
    data_exporter = CoinMetricsDataExporter(api_key=api_key)
    data_exporter.export_market_trades_future_data(
        start_date=start_date,
        end_date=end_date,
        exchanges=list_exchanges,
        output_format=output_format,
        threaded=threaded,
    )


@export_app.command()
def market_quotes_spot(
    exchanges: str = typer.Argument(..., help=HELP_MSG_EXCHANGES),
    asset_pairs: str = typer.Argument(..., help=HELP_MSG_ASSET_PAIRS),
    start_date: datetime = DATE_ARGUMENT,
    end_date: datetime = DATE_ARGUMENT,
    output_format: str = "json.gz",
    threaded: bool = False,
    api_key: Union[str, None] = None,
) -> None:
    """
    Used to export data related to spot market quotes
    Format: coinmetrics export market-quotes-spot <exchanges> <asset_pairs> <start_date> <end_date>
    Example: coinmetrics export market-quotes-spot binance 1INCHUSDT 2022-03-01 2022-03-03.
    """
    list_exchanges, list_asset_pairs = exchanges.split(","), asset_pairs.split(",")
    list_exchanges = [exchange.capitalize() for exchange in exchanges]
    api_key = api_key or os.environ["CM_API_KEY"]
    data_exporter = CoinMetricsDataExporter(api_key=api_key)
    data_exporter.export_market_quotes_spot_data(
        start_date=start_date,
        end_date=end_date,
        exchanges=list_exchanges,
        asset_pairs=list_asset_pairs,
        output_format=output_format,
        threaded=threaded,
    )


@export_app.command()
def market_quotes_future(
    exchanges: str = typer.Argument(..., help=HELP_MSG_EXCHANGES),
    asset_pairs: str = typer.Argument(..., help=HELP_MSG_ASSET_PAIRS),
    start_date: datetime = DATE_ARGUMENT,
    end_date: datetime = DATE_ARGUMENT,
    output_format: str = "json.gz",
    threaded: bool = False,
    api_key: Union[str, None] = None,
) -> None:
    """
    Used to export data related to future market quotes.
    Format: coinmetrics export market-quotes-future <exchanges> <asset_pairs> <start_date> <end_date>
    Example: coinmetrics export market-quotes-future binance 1INCHUSDT 2022-03-01 2022-03-03.
    """
    list_exchanges, list_asset_pairs = exchanges.split(","), asset_pairs.split(",")
    list_exchanges = [exchange.capitalize() for exchange in exchanges]
    api_key = api_key or os.environ["CM_API_KEY"]
    data_exporter = CoinMetricsDataExporter(api_key=api_key)
    data_exporter.export_market_quotes_future_data(
        start_date=start_date,
        end_date=end_date,
        exchanges=list_exchanges,
        asset_pairs=list_asset_pairs,
        output_format=output_format,
        threaded=threaded,
    )


@export_app.command()
def get_exchanges(
    command: str = typer.Argument(...), api_key: Union[str, None] = None
) -> None:
    api_key = api_key or os.environ["CM_API_KEY"]
    data_exporter = CoinMetricsDataExporter(api_key=api_key)
    pprint.pprint(data_exporter.get_exchanges(command))


@export_app.command()
def get_asset_pairs(
    file_type: str = typer.Argument(...),
    exchange: str = typer.Argument(...),
    api_key: Union[str, None] = None,
) -> None:
    exchange = exchange.capitalize()
    api_key = api_key or os.environ["CM_API_KEY"]
    data_exporter = CoinMetricsDataExporter(api_key=api_key)
    pprint.pprint(data_exporter.get_asset_pairs(file_type=file_type, exchange=exchange))


EXPORT_APP_HELP_MSG = """
This app is used to programatically download files from the CoinMetrics flat files server. It supports exporting
daily data files related to market-trades, market-quotes, and market candles in json.gz, csv, or json formats.
To specify multiple exchanges or multiple asset_pairs use comma seperation in order to pass in a list.
Examples:

To download binance spot trade files for month of June 2019:
coinmetrics export market-trades-spot binance 2019-06-01 2019-06-30 --output-format csv

To download binance and coinbase market-trade-spot files for 10 days:
 coinmetrics export market-trades-spot binance,coinbase 2018-01-01 2018-01-10

To download market-quotes-futures file for binance 1INCHUSDT pair for only one day:
 coinmetrics export market-quotes-future binance 1INCHUSDT 2022-02-19 2022-02-19

To run any of the commands "threaded" or concurrently add the flag --threaded i.e.
 coinmetrics export market-trades-spot binance 2019-06-01 2019-06-30 --output-format csv --threaded
Note this may increase the speed of download but will use more system resources and bandwith.
"""


def main() -> None:
    coinmetrics_app.add_typer(export_app, name="export", help=EXPORT_APP_HELP_MSG)
    coinmetrics_app()


if __name__ == "__main__":
    main()
