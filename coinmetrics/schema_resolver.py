from typing import Any, Dict
from ._schema_constants import OPENAPI_SCHEMA

# Map endpoints to their schema names
ENDPOINT_SCHEMA_MAP = {
    "timeseries/market-trades": "MarketTrade",
    "timeseries/market-candles": "MarketCandle",
    "timeseries/market-liquidations": "MarketLiquidation",
    "timeseries/market-orderbooks": "MarketOrderBook",
    "timeseries/market-quotes": "MarketQuote",
    "timeseries/market-funding-rates": "MarketFundingRate",
    "timeseries/market-funding-rates-predicted": "MarketFundingRatePredicted",
    "timeseries/market-openinterest": "MarketOpenInterest",
    "timeseries/market-contract-prices": "MarketContractPrices",
    "timeseries/market-implied-volatility": "MarketImpliedVolatility",
    "timeseries/market-greeks": "MarketGreeks",
    "timeseries/pair-candles": "PairCandle",
    "timeseries/index-candles": "IndexCandle",
    "blockchain-v2/{asset}/balance-updates": "BlockchainBalanceUpdateV2",
    "blockchain-v2/{asset}/blocks/{block_hash}": "BlockchainBlockInfoV2",
    "blockchain-v2/{asset}/blocks/{block_hash}/transactions/{txid}": "BlockchainFullSingleTransactionResponseV2",
    "blockchain-v2/{asset}/transactions/{txid}": "BlockchainFullSingleTransactionResponseV2"
}

# If mapping between field and type from schemas is suboptimal, override them here
FIELD_TYPE_EXCEPTIONS = {
    "bids": "object",
    "asks": "object",
    "transactions": "object",
    "balance_updates": "object",
    "sub_accounts": "object",
}


def get_schema_for_endpoint(endpoint: str) -> str:
    """
    Get the schema name to use for resolving fields based on the API endpoint.

    Args:
        endpoint: The API endpoint path

    Returns:
        The schema name to use for field resolution
    """
    # Get schema name from map, default to None if not found
    schema_name = ENDPOINT_SCHEMA_MAP.get(endpoint)

    if not schema_name:
        raise ValueError(f"No schema mapping found for endpoint: {endpoint}")

    return schema_name


def resolve_schema_field(
    prop: Dict[Any, Any],
    root: Dict[Any, Any] = OPENAPI_SCHEMA,
    prefix: str = ''
) -> Any:
    """Resolve $ref or inline type/description for a schema property."""
    if '$ref' in prop:
        ref_path = prop['$ref'].lstrip('#/').split('/')
        ref_obj = root
        for part in ref_path:
            ref_obj = ref_obj[part]

        # Handle allOf composition
        if 'allOf' in ref_obj:
            nested_fields = {}
            for part in ref_obj['allOf']:
                nested_fields.update(resolve_schema_field(part, root, prefix))
            return nested_fields

        # Handle nested properties if this is a referenced object
        if 'properties' in ref_obj:
            nested_fields = {}
            for name, nested_prop in ref_obj['properties'].items():
                nested_name = f"{prefix}_{name}" if prefix else name
                nested_fields[nested_name] = resolve_schema_field(nested_prop, root, nested_name)
            return nested_fields

        return resolve_schema_field(ref_obj, root, prefix)

    # Handle allOf composition directly in property
    if 'allOf' in prop:
        nested_fields = {}
        for part in prop['allOf']:
            nested_fields.update(resolve_schema_field(part, root, prefix))
        return nested_fields

    # For non-ref properties that might have nested properties
    if 'properties' in prop:
        nested_fields = {}
        for name, nested_prop in prop['properties'].items():
            nested_name = f"{prefix}_{name}" if prefix else name
            nested_fields[nested_name] = resolve_schema_field(nested_prop, root, nested_name)
        return nested_fields

    # For array types
    if 'items' in prop:
        if '$ref' in prop['items']:
            return resolve_schema_field(prop['items'], root, prefix)
        return resolve_schema_field(prop['items'], root, prefix)

    return prop.get('type', 'object')


def get_schema_fields(
    schema_name: str,
    openapi_schema: Dict[Any, Any] = OPENAPI_SCHEMA
) -> Dict[str, str]:
    """Get all fields from a schema with flattened field names."""
    schema = openapi_schema['components']['schemas'][schema_name]
    field_type_map = {}

    # Handle allOf at schema level
    if 'allOf' in schema:
        for part in schema['allOf']:
            fields = resolve_schema_field(part, openapi_schema)
            field_type_map.update(fields)
        return field_type_map

    # Handle properties at schema level
    if 'properties' in schema:
        for name, prop in schema['properties'].items():
            field_type_map[name] = resolve_schema_field(prop, openapi_schema, name)

    field_type_map.update(FIELD_TYPE_EXCEPTIONS)
    return field_type_map
