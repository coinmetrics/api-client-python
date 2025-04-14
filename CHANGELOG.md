# Changelog

## __version__
### Added
- Allow `optimize_pandas_types` argument as an alias for `optimize_dtypes` in `DataCollection.to_dataframe()` calls but issue a deprecated warning.  Prevents exception for code using the old name.

## 2025.3.12.17
### Changed
- Made Pandas and Polars mandatory packages.

## 2025.3.3.16
### Added
- `get_network_profiles`, missing `format` param to `get_market_orderbooks`, `ignore_*_errors` to `get_stream_asset_metrics`,

## 2025.2.26.22
### Added
- Enhanced documentation for API flows

## 2025.2.12.22
### Fixed
- Polars dependency issues.

## 2025.2.11.16
**Note: This release may be unstable if you do not have polars installed. Please update to 2025.2.12.22 for a patched version.**
### Added
- Added Polars dataframes and LazyFrames. They can be accessed using `DataCollection.to_dataframe(dataframe_type='polars')` and `DataCollection.to_lazyframe()` respectively.

### Changed
- `DataCollection` attribute `optimize_pandas_types` changed to `optimize_dtypes`.

## 2025.2.4.18
### Fixed
- Type annotations in docstrings

## 2024.12.23.19
### Added
- CHANGELOG.md

## 2024.12.20.17
### Added
- pd.DateOffset as a valid data type for `time_increment` in `parallel()`

### Changed
- Update pandas dependency to >= 2.0 and websocket-client >= 1.6.0

## 2024.12.16.21
### Added
- Allowed pandas Timestamp data type to be passed in `client` API calls
- Added "deprecated" flag to catalog v1 endpoints

## 2024.12.11.19 
### Added
- Catalog-v2/blockchain endpoints

## 2024.12.10.20
### Changed
- Removed unused columns for `reference_data_*().to_dataframe()` return
- Improved casting for return data types

## 2024.11.21.20
### Changed
- Upgraded the typer dependency to >= 0.6.1

## 2024.11.18.19
### Changed
- Set `format=json_stream` for `catalog` and `reference_data` functions by default, drastically improving speed

## 2024.10.31.17
### Fixed
- Bug where requests have double '/' in URL

## 2024.10.15.19
### Changed
- Updated the request header to denote User-Agent as a Python API Client user

## 2024.10.9.20 
### Added
- `txids` as a valid `parallelize_on` variable

## 2024.10.4.15
### Added
- Transformation logic for `catalog_*_v2().to_dataframe()` that flattens these dataframes
### Fixed
- Type casting for `coin_metrics_id` field from pandas dataframes for very large integers

## 2024.9.18.17
### Added
- Auto-retry logic for Websockets
### Removed
- Redundant tests

## 2024.9.18.16
### Fixed
- Bug on parallelization where `end_time` uses user's timezone instead of UTC
### Added
- `base_native` and `quote_native` fields to `reference_data_markets()`

## 2024.8.20.13
### Changed
- Removed JSON parsing on `on_error` for `CmStream` default

## 2024.8.16.10
### Removed
- Atlas V1 (`get_blockchain_()`) endpoints
### Added
- Warnings for upcoming `catalog` deprecation

## 2024.8.14.17
### Added
- `txid`, `accounts`, `block_hashes`, `heights`, and `sub_accounts` as valid `parallel` variables
- `height_increment` as a valid `parallel` parameter

## 2024.8.5.13
### Added
- Temporary patch for returning all columns for `to_dataframe()` call for `reference_data_*` and `security_master_*` functions

## 2024.7.12.14
### Added
- Allowed timezone aware datetimes to be passed to client API calls

## 2024.2.6.16
### Added
- Functions `get_market_funding_rates_predicted`, `catalog_{full}_market_funding_rates_predicted_v2`
- Generic examples for Python API Client functions

## 2024.1.17.17
### Fixed
- Bug where `blockchain_metadata` functions were not being called properly

## 2023.11.27.17
### Added
- `blockchain_metadata_tags()` and `blockchain_metadata_tagged_entities` functions
### Changed
- Updated README to shorten example code and remove catalog v1

## 2023.11.13.14
### Added
- Functions `get_snapshots_of_asset_metric_constituents` and `get_timeframes_of_asset_metric_constituents`

## 2023.10.30.13
### Added
- Function `get_stream_market_open_interest`

## 2023.10.19.17
### Added
- Function `get_stream_market_liquidations`

## 2023.9.29.14
### Added
- `metrics` parameter to `catalog_{full}_markets_v2`
- `catalog_index_levels_v2` and `reference_data_markets`

## 2023.9.22.21
### Added
- Parallelization support for `blockchain` endpoints

## 2023.9.11.14
### Changed
- Replaced `frequency` parameter with `granularity` for `get_market_quotes` and `get_market_orderbooks`
### Added
- Functions `reference_data_assets`, `reference_data_indexes`, `reference_data_pairs`

## 2023.8.30.20
### Added
- Functions `security_master_assets`, `security_master_markets`

## 2023.8.28.16
### Added
- Functions `catalog_{full}_pair_candles_v2`, `catalog_{full}_index_candles_v2`, `catalog_{full}_asset_chains_v2`, `catalog_{full}_mempool_feerates_v2`, `catalog_{full}_mining_pool_tips_summaries_v2`, `catalog_{full}_transaction_tracker_assets_v2`

## 2023.8.25.15
### Added
- Ability to parallelize API request for significantly improved data pull speed

## 2023.8.24.13
### Added
- Functions `reference_data_asset_metrics`, `reference_data_institution_metrics`
### Fixed
- Added `frequency` parameter to `get_market_orderbooks` (fixed in 2023.9.11.14)

## 2023.8.22.14
### Added
- Functions `catalog_{full}_asset_metrics_v2`, `catalog_exchange_{full}_metrics_v2`, `catalog_{full}_exchange_asset_metrics_v2`, `catalog_{full}_pair_metrics_v2`, `catalog_{full}_institution_metrics_v2`

## 2023.8.10.19
### Added
- `on_close` handler to `CmStream`

## 2023.7.11.17
### Added
- Functions `catalog_{full}_contract_prices_v2`, `catalog_{full}_market_trades_v2`, `catalog_{full}_market_candles_v2`, `catalog_{full}_market_orderbooks_v2`, `catalog_{full}_market_quotes_v2`, `catalog_{full}_market_funding_rates_v2`, `catalog_{full}_market_contract_prices_v2`, `catalog_{full}_market_implied_volatility_v2`, `catalog_{full}_market_greeks_v2`, `catalog_{full}_market_open_interest`, `catalog_{full}_market_liquidations_v2`, `catalog_{full}_market_metrics_v2`.

## 2023.6.8.20
### Fixed
- Market metrics catalog implementation to prevent duplicate rows
- Added test to verify one row per frequency

## 2023.5.26.17
### Added
- Transaction tracker parameters
- Include heartbeats functionality

## 2023.5.17.19
### Changed
- Fixed catalog performance issues

### Added
- Walkthrough notebook for DS UA Workshop

## 2023.5.2.20
### Added
- Rate limiter for community users
- Multithreading to CI pipeline
- Sample script for exporting atlas balance updates

## 2023.4.26.13
### Fixed
- URL fixes

## 2023.4.24.14
### Added
- Missing catalog endpoints
- Support for optional columns in API data
- New endpoint and tests

## 2023.3.16.17
### Changed
- Updated Dockerfile and dependencies
- Updated poetry lock file
- Bug fixes in examples

### Added
- Missing timeseries stream endpoints

## 2023.2.27.22
### Added
- Missing functions and parameters

## 2023.2.23.0
### Added
- Missing functions parameters
- Improved documentation for DataCollections usage

## 2023.1.26.23
### Added
- Unauthorized error handling to FlatFilesExporter
- Updated CI pipeline

## 2023.1.10.21
### Added
- Debug mode to help figure out performance issues
- Documentation updates for to_dataframe() method for catalog
- Automated testing code coverage
- Error handling for large requests (URI too long)
- Support for secondary_level parameter in to_dataframe()
- Support for index levels via WS in the client

## 2022.11.14.16
### Changed
- Modified API Client to use python requests.Session for improved performance

## 2022.11.3.18
### Added
- Taxonomy endpoints
- Updated Atlas V2 balance endpoints

### Fixed
- Fixed broken examples using `type` parameter

## 2022.10.18.18
### Changed
- Updated build pipeline

## 2022.10.14.20
### Added
- New catalog endpoints for metrics
- Automated version updates on release
- Documentation generation
