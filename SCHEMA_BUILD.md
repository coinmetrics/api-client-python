# Schema Build Process

This document explains the optimized OpenAPI schema build process implemented to improve startup performance.

## Overview

Instead of parsing the full 787KB `openapi.yaml` file at runtime, the build process extracts only the minimal schema components needed by the application and pre-generates them as Python constants. This reduces:

- **File size**: From 787KB to 27KB (96.6% reduction)  
- **Schema count**: From 649 to 116 schemas (82% reduction)
- **Startup time**: No runtime YAML parsing required

## How It Works

1. **Build-time extraction**: `coinmetrics/build.py` analyzes which schemas are actually used by the application
2. **Dependency resolution**: Recursively finds all schemas referenced by the required schemas  
3. **Minimal generation**: Creates `_schema_constants.py` with only the needed components
4. **Runtime loading**: Schema resolver imports pre-built constants instead of parsing YAML

## Usage

### Manual Build
```bash
# Generate schema constants
make build-schema
# or
python coinmetrics/build.py
```

### Clean Generated Files
```bash
make clean
```

## Integration

- **Docker builds**: Schema generation runs automatically during `docker build`
- **GitLab CI/CD**: Included in both Docker build and documentation stages  
- **Development**: Use `make build-schema` or run manually
- **Fallback**: If generated file missing, automatically falls back to runtime YAML parsing

## Required Schemas

The build process extracts these schemas and their dependencies:

- MarketTrade, MarketCandle, MarketLiquidation
- MarketOrderBook, MarketQuote, MarketFundingRate  
- MarketFundingRatePredicted, MarketOpenInterest
- MarketContractPrices, MarketImpliedVolatility, MarketGreeks
- PairCandle, IndexCandle
- BlockchainBalanceUpdateV2, BlockchainBlockInfoV2
- BlockchainFullSingleTransactionResponseV2, BlockchainFullBlockResponseV2

## Files

- `coinmetrics/build.py` - Build script that extracts minimal schemas
- `coinmetrics/_schema_constants.py` - Generated constants (git-ignored) 
- `coinmetrics/schema_resolver.py` - Modified to use build-time constants
- `.gitignore` - Excludes generated file from version control