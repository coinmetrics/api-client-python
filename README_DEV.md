# Contributing guidelines


## Setting up env
Run these commands to set up your conda environment. We use `poetry` to manage dependencies as we make changes.
```
conda create -n api-client-python python=3.8

activate api-client-python

curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
poetry install
```
_Install is taken from poetry documentation. For more information on poetry, see [their docs](https://python-poetry.org/docs/#updating-poetry)_



Alternatively, you may install poetry via `pip` and lock in dependencies from there:

```
pip install poetry
poetry install
```

But this is not recommended as you may run into dependency issues from doing so.

Commands you should run before merging your changes into master
```
python -m mypy -p coinmetrics
python -m black coinmetrics test
python -m flake8 coinmetrics
python -m pytest test

poetry export --without-hashes --format=requirements.txt > requirements.txt
```

Additionally, when updating the package to a new version, run this command:
```
sh update_version.sh <new_version>
```

## Publishing package to pypi
**NOTE: Run this only when you merge your changes into master and actually want to release the updates**
```
poetry build
poetry publish
```


## GENERATING DOCUMENTATION
#### Windows
```
pydoc-markdown -m coinmetrics.api_client > docs\docs\api_client.md

cp -f README.md docs\docs\index.md
cp -f FlatFilesExport.md docs\docs\FlatFilesExport.md
mkdocs build 
cd ..
```

#### Mac
```
pydoc-markdown -m coinmetrics.api_client > docs/docs/api_client.md

cp -f README.md docs/docs/index.md
cp -f FlatFilesExport.md docs/docs/FlatFilesExport.md

cd docs && mkdocs build && cd ..
```

## Codebase overview/ explanation
If you're adding methods to the client or generally contributing to the codebase it may be useful to have an overview of what exists.  
The main code for the API client is in [api_client.py](coinmetrics/api_client.py) which contains the main `CoinMetricsClient` class,
where all the API endpoints are implemented as methods. The methods in the API are fully typed to be in compliance with 
[mypy](http://mypy-lang.org/) a type checker for Python. You'll notice that there are three main return types for the 
methods in the client - `Catalog-`, `DataCollection`, and `CmStream`.  

#### Catalog data types
The `Catalog` data types are an extension of the Python List type and add the method `.to_dataframe()` in order to allow
the data from the catalog API methods to be easily converted to flat files. So this converts a list of dictionaries that 
might look something like this:  
```python
[
    {
        "market": "binance-aave-btc-spot",
        "min_time": "2020-10-15T03:00:01.286000000Z",
        "max_time": "2022-07-12T21:00:39.933000000Z",
    },
    {
        "market": "binance-algo-usdc-spot",
        "min_time": "2019-06-22T00:00:07.600000000Z",
        "max_time": "2020-01-07T07:06:19.943000000Z",
    },
    {
        "market": "binance-atom-usdc-spot",
        "min_time": "2019-05-07T12:05:42.347000000Z",
        "max_time": "2022-07-12T21:01:25.281000000Z",
    },
]
```  
to a flat file that looks like: 
```
market,min_time,max_time
0,binance-aave-btc-spot,2020-10-15 03:00:01.286000+00:00,2022-07-12 21:00:39.933000+00:00
1,binance-algo-usdc-spot,2019-06-22 00:00:07.600000+00:00,2020-01-07 07:06:19.943000+00:00
2,binance-atom-usdc-spot,2019-05-07 12:05:42.347000+00:00,2022-07-12 21:01:25.281000+00:00
```  
This is useful for the catalog endpoints because they are meant to show the breadth and depth of data available from 
the API for different topics from market trades to supported exchanges, but they don't conform to a standardized format.
If you are implementing a new API method you may need to define a new return type in [_catalogs.py](coinmetrics/_catalogs.py)
that matches the response schema of the endpoint. 

#### DataCollection 
The `DataCollection` class is defined in the [_data_collection.py](coinmetrics/_data_collection.py) file and is used as 
a general purpose return type for our non-stream timeseries data. It adds some utility function to the time series 
data like pagination and easy export options, but shouldn't need to be developed further unless you wanted to add 
more export options or functionality that doesn't currently exist. 


#### CmStream
The `CmStream` class is defined in the [api_client.py](coinmetrics/api_client.py) and facilitates connecting to the 
websocket endpoints and reading the data. Again, no reason to develop this further unless to add functionality, fix bugs, logging, etc. 
