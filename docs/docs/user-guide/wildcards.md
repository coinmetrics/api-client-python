# Wildcards

All endpoints for time series support a single wildcard for the first parameter that accepts a list. For example, let's
say you want market candles for BTC trading against any quote currency. The first list parameter is `markets`.

You have two choices: 

* You use `catalog_market_candles_v2()` to obtain a list of available candles, filter it according to your needs, and pass 
an explicit list to the `get_market_candles()` function. This gives you full control, but you need to watch 
the length of the list. At approx. 25 chars per market, more than 180 markets or so risks exceeding the max. of
5k chars. The API client does not currently implement any safeguards, it will just fail.
* You use a single wildcard, like so: `get_market_candles(markets='binance-btc-*-spot')`. In the backend, 
your wildcarded string is mapped against all possible market strings and all matches are used as argument.

In our current implementation, a wildcarded selection will not benefit from parallelization across the list. For example,
passing a list of 100 markets could be fully parallelized, but a wildcard resolving to 100 markets would be executed
as a single thread.

