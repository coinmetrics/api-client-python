## Exporting flat files 
Along with the API client we provide a data exporting tool which allow downloading large amount of data as flat files
rather than from the API itself. The tool allows users to download daily files over our entire provided history for 
market trades, market quotes, and market candles.  

## Authorization for flat files download
This program was set up to easily access a flat files server provided to Coin Metrics commercial clients. If you are a 
community API user or a client without access to this server, a 403 error will be returned. If you are a community API 
user and looking to get historical asset prices, Coin Metrics does offer [historical asset prices for download](https://coinmetrics.io/community-network-data/).  
The `CoinMetricsDataExporter` class will return a `CoinMetricsClientFlatFilesUnauthorizedException` if your API key is not authorized
to access this server. The flat files export is considered a separate product from the Coin Metrics API, if you would
like to gain access or believe you should have access but do not, please contact coinmetrics support. 

### Installation and set up
The tool is installed a long with the `coinmetrics-api-client`, it's recommended to create a new Python [virtual environment] 
for your project and install the package:  

```commandline
python -m venv .venv 
source .venv/bin/activate 
pip install coinmetrics-api-client
```

The export tool requires access to a CoinMetrics API key, and is accessed with the environment variable `CM_API_KEY`,
the easiest way to set this is to run `export CM_API_KEY=<API_KEY>` in your terminal on MacOS/Linux or just `set CM_API_KEY=<API_KEY>` 
on Windows. Additionally, you have the option of passing it in which each command instead.

To confirm the tool is installed correct execute the command `coinmetrics export --help` which brings up relevant 
documentation. At the bottom of the help message all the available commands are shown:  
```commandline
Commands:
  get-asset-pairs
  get-exchanges
  market-candles-future  Used to export data related to future market...
  market-candles-spot    Used to export data related to spot market candles.
  market-quotes-future   Used to export data related to future market...
  market-quotes-spot     Used to export data related to spot market quotes...
  market-trades-future   Used to export data related to future market...
  market-trades-spot     Used to export data related to spot market trades.
```

### Exporting Market Trades Files 
Further documentation is available on any of the commands by running `coinmetrics export <command> --help`, for example
running `coinmetrics export market-trades-spot --help` prints: 
```commandline
Usage: coinmetrics export market-trades-spot [OPTIONS] EXCHANGES [START_DATE]:
                                             [%Y-%m-%d|%Y-%m-%dT%H:%M:%S|%Y-%m
                                             -%d %H:%M:%S] [END_DATE]:[%Y-%m-%
                                             d|%Y-%m-%dT%H:%M:%S|%Y-%m-%d
                                             %H:%M:%S]

  Used to export data related to spot market trades. Format: coinmetrics
  export market-trades-spot <exchanges> <start_date> <end_date> Example:
  coinmetrics export market-trades-spot coinbase,binance 2022-01-01
  2022-01-03.

Arguments:
  EXCHANGES                       Pass in arguments as a list of strings
                                  separated by by commas i.e.
                                  binance,coinbase,bitmex  [required]

  [START_DATE]:[%Y-%m-%d|%Y-%m-%dT%H:%M:%S|%Y-%m-%d %H:%M:%S]
                                  [default: 2022-08-10]
  [END_DATE]:[%Y-%m-%d|%Y-%m-%dT%H:%M:%S|%Y-%m-%d %H:%M:%S]
                                  [default: 2022-08-10]

Options:
  --output-format TEXT        [default: json.gz]
  --threaded / --no-threaded  [default: False]
  --api-key TEXT
  --help                      Show this message and exit.

```

#### Example:
If you want to get the flat files for spot-market-trades from coinbase and binance for the first 5 days of June 2022:
`coinmetrics export market-trades-spot binance,coinbase 2022-06-01 2022-06-05`  

In your current directory you will see:  
```commandline
market-trades-spot
├── binance
│   ├── 2022-06-01.json.gz
│   ├── 2022-06-02.json.gz
│   ├── 2022-06-03.json.gz
│   ├── 2022-06-04.json.gz
│   └── 2022-06-05.json.gz
└── coinbase
    ├── 2022-06-01.json.gz
    ├── 2022-06-02.json.gz
    ├── 2022-06-03.json.gz
    ├── 2022-06-04.json.gz
    └── 2022-06-05.json.gz
```
By default the files are downloaded as [gzipped json files](https://fileinfo.com/extension/gz) - they are compressed in 
order to take up less space. If you instead wish to download the data as a csv or json you can use:  
`coinmetrics export market-trades-spot binance,coinbase 2022-06-01 2022-06-05 --output-format csv`

The functionality for getting future, rather than spot market trades is the exact same, just replace `market-trades-spot`
with `market-trades-future`

In order to figure out what exchanges are supported for a flat file type you can run `coinmetrics export get-exchanges <command>`, 
so in this case running `coinmetrics export get-exchanges market-trades-spot`

### Exporting market quotes
Market quotes are similar to market trades, except data is separated by exchange and by asset-pair. So you must provide
both what exchanges you are querying as well the specific asset pairs.

Example if you wanted to export files to market quotes for ETHUSDT and BTCUSDT over a certain timeframe as json files:  
`coinmetrics export market-quotes-spot binance ETHUSDT,BTCUSDT 2022-03-03 2022-03-05 --output-format json`  

In order to find what asset pairs are availible you can query this information with `coinmetrics export get-asset-pairs <command> <exchange>`
so in this case, for Binance you would run `coinmetrics export get-asset-pairs market-quotes-spot binance`. If you are comfortable 
with command line tools it may be helpful to string this with unix command line tools like `grep`. For example, to find all the BTC related pairs 
for binance you might run `coinmetrics export get-asset-pairs market-quotes-spot binance | grep BTC`.

The functionality is the same for `market-qutoes-futures`.

### Exporting market candles
Exporting market candles also functions similar to market trades, however you must specify a frequency in addition to
an exchange and date range. The frequency denominates the range which the market candles cover. These frequencies are 
currently `"1m", "5m", "10m", "15m", "30m", "1h", and "1d"`. 

Example to download 5m spot market candles for coinbase and binance for a date range:  
`coinmetrics export market-candles-spot 5m coinbase,binance 2022-01-01 2022-01-05`  
Which creates these files:  
```commandline
market-candles-spot-5m
├── binance
│   ├── 2022-01-01.json.gz
│   ├── 2022-01-02.json.gz
│   ├── 2022-01-03.json.gz
│   ├── 2022-01-04.json.gz
│   └── 2022-01-05.json.gz
└── coinbase
    ├── 2022-01-01.json.gz
    ├── 2022-01-02.json.gz
    ├── 2022-01-03.json.gz
    ├── 2022-01-04.json.gz
    └── 2022-01-05.json.gz
```

The functionality is the same for `market-candles-future`

### Using API Key without setting an environment variable
If you don't wish to put your CoinMetrics API key in your environment, you may also pass it in with any command with the
flag `--api-key`. Example:  
`coinmetrics export market-candles-spot 5m coinbase,binance 2022-01-01 2022-01-05 --api-key <API_KEY>`

### Downloading files in parallel
If you are downloading many files and want to speed the process up there is an option to concurrently download multiple 
rather than one at a time, using the `--threaded` flag. Example:  
`coinmetrics export market-candles-spot 5m coinbase,binance 2022-01-01 2022-01-05 --threaded`  
Note that using this option will consume more system resources and network bandwith, and the download speed will still
be limited by egress from the files server as well as the specs of your machine. 

### Using the CoinMetricsDataExporter in Python instead of CLI
Depending on the use case it might be more convenient to use the CoinMetricsDataExporter directly in Python rather than
from the CLI. There is several examples [here](examples/files_download) as well as one below:
```python
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
```

