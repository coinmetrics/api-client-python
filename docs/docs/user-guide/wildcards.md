# Wildcards

All endpoints for time series support a single wildcard for the first parameter that accepts a list. For example, let's
say you want market candles for BTC trading against any quote currency. The first list parameter is `markets`.

You have two choices: 

* You use `catalog_market_candles_v2()` to obtain a list of available candles, filter it according to your needs, and pass 
an explicit list to the `get_market_candles()` function. 
* You use a single wildcard, like so: `get_market_candles(markets='binance-btc-*-spot')`. In the backend, 
your wildcarded string is mapped against all possible market strings and all matches are used as argument.

## Performance

If you have a choice of passing a specific list of 100 markets or a wildcard that resolves to 100 markets, we recommend the former. The API client will parallelize the requests across the list of markets resulting in a performance boost.


