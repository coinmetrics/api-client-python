# type: ignore
import pytest
import orjson
import os
import websocket
from coinmetrics.api_client import CoinMetricsClient, CmStream
import signal

client = CoinMetricsClient(str(os.environ.get("CM_API_KEY")))
cm_api_key_set = os.environ.get("CM_API_KEY") is not None
REASON_TO_SKIP = "Need to set CM_API_KEY as an env var in order to run this test"

print("CM_API_KEY is set - tests will run") if cm_api_key_set else print(
    "CM_API_KEY not set, tests will not run"
)


def on_message_index_levels_test(stream: websocket.WebSocketApp, message: str) -> None:
    """
    Tests that data with the expected keys can be loaded by orjson
    """
    data = orjson.loads(message)
    expected_cols_index_levels = ["index", "time", "level", "cm_sequence_id"]
    for col in expected_cols_index_levels:
        assert col in data
    sequence_id = int(data['cm_sequence_id'])
    if sequence_id >= 0:
        os.kill(os.getpid(), signal.SIGINT)
    # stream.close()


def on_message_market_trades_test(stream: websocket.WebSocketApp, message: str) -> None:
    """
    Tests that data with the expected keys can be loaded by orjson
    """
    data = orjson.loads(message)
    expected_cols_index_levels = [
        "market",
        "time",
        "coin_metrics_id",
        "amount",
        "price",
        "collect_time",
        "side",
        "cm_sequence_id",
    ]
    for col in expected_cols_index_levels:
        assert col in data
    sequence_id = int(data['cm_sequence_id'])
    if sequence_id >= 0:
        os.kill(os.getpid(), signal.SIGINT)
    # stream.close()


def on_message_market_orderbooks_test(stream: websocket.WebSocketApp, message: str) -> None:
    """
    Tests that data with the expected keys can be loaded by orjson
    """
    data = orjson.loads(message)
    expected_cols_index_levels = [
        "market",
        "time",
        "coin_metrics_id",
        "asks",
        "bids",
        "type",
        "collect_time",
        "cm_sequence_id",
    ]
    for col in expected_cols_index_levels:
        assert col in data
    sequence_id = int(data['cm_sequence_id'])
    if sequence_id >= 0:
        os.kill(os.getpid(), signal.SIGINT)
    # stream.close()


def on_message_market_openinterest(stream: websocket.WebSocketApp, message: str) -> None:
    """
    Tests that data with the expected keys can be loaded by orjson
    """
    data = orjson.loads(message)
    expected_cols_index_levels = [
        "market",
        "time",
        "contract_count",
        "value_usd",
        "cm_sequence_id"
    ]
    for col in expected_cols_index_levels:
        assert col in data
    sequence_id = int(data['cm_sequence_id'])
    if sequence_id >= 0:
        os.kill(os.getpid(), signal.SIGINT)
    # stream.close()


def on_message_market_candles_test(stream: websocket.WebSocketApp, message: str) -> None:
    """
    Tests that data with the expected keys can be loaded by orjson
    """
    data = orjson.loads(message)
    expected_cols_index_levels = [
        "market",
        "time",
        "price_open",
        "price_close",
        "price_high",
        "price_low",
        "vwap",
        "volume",
        "candle_usd_volume",
        "candle_trades_count",
        "cm_sequence_id",
    ]
    for col in expected_cols_index_levels:
        assert col in data
    sequence_id = int(data['cm_sequence_id'])
    if sequence_id >= 0:
        os.kill(os.getpid(), signal.SIGINT)
    # stream.close()


def on_message_market_quotes_test(stream: websocket.WebSocketApp, message: str) -> None:
    """
    Tests that data with the expected keys can be loaded by orjson
    """
    data = orjson.loads(message)
    expected_cols_index_levels = [
        "market",
        "time",
        "coin_metrics_id",
        "ask_price",
        "ask_size",
        "bid_price",
        "bid_size",
        "cm_sequence_id",
    ]
    for col in expected_cols_index_levels:
        assert col in data
    sequence_id = int(data['cm_sequence_id'])
    if sequence_id >= 0:
        os.kill(os.getpid(), signal.SIGINT)
    # stream.close()
    

def on_message_asset_metrics_rr_test(stream: websocket.WebSocketApp, message: str) -> None:
    """
    Tests that data with the expected keys can be loaded by orjson
    """
    data = orjson.loads(message)
    expected_cols_index_levels = ["time", "asset", "ReferenceRateUSD", "cm_sequence_id"]
    for col in expected_cols_index_levels:
        assert col in data
    sequence_id = int(data['cm_sequence_id'])
    if sequence_id >= 0:
        os.kill(os.getpid(), signal.SIGINT)
    # stream.close()


def on_message_pair_quotes_test(stream: websocket.WebSocketApp, message: str) -> None:
    data = orjson.loads(message)
    expected_cols = ["pair", "time", "ask_price", "mid_price"]
    for col in expected_cols:
        assert col in data
    sequence_id = int(data['cm_sequence_id'])
    if sequence_id >= 0:
        os.kill(os.getpid(), signal.SIGINT)
    # stream.close()


def on_message_assets_quotes_test(stream: websocket.WebSocketApp, message: str) -> None:
    data = orjson.loads(message)
    expected_cols = ["pair", "time", "ask_price", "ask_size", "bid_price", "mid_price"]
    for col in expected_cols:
        assert col in data
    sequence_id = int(data['cm_sequence_id'])
    if sequence_id >= 0:
        os.kill(os.getpid(), signal.SIGINT)
        # stream.close()


def on_message_market_liquidations_test(stream: websocket.WebSocketApp, message: str) -> None:
    data = orjson.loads(message)
    expected_cols = [
        "market",
        "time",
        "coin_metrics_id",
        "price",
        "type",
        "side",
        "cm_sequence_id"
    ]
    for col in expected_cols:
        assert col in data
    sequence_id = int(data['cm_sequence_id'])
    if sequence_id >= 0:
        os.kill(os.getpid(), signal.SIGINT)
        # stream.close()


def on_message_sigterm_test(stream: websocket.WebSocketApp, message: str) -> None:
    """
    Tests closing websocket using sigterm
    """
    data = orjson.loads(message)
    sequence_id = int(data['cm_sequence_id'])
    if sequence_id >= 1:
        stream.close()


def on_close_sigterm_test(stream: websocket.WebSocketApp, close_status_code: int, close_msg: str) -> None:
    os.kill(os.getpid(), signal.SIGTERM)


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_index_levels_stream() -> None:
    indexes = ["CMBIBTC", "CMBIETH"]
    stream = client.get_stream_index_levels(indexes=indexes)
    stream.run(on_message=on_message_index_levels_test)


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_market_trades_stream() -> None:
    markets = ["coinbase-btc-usd-spot"]
    stream = client.get_stream_market_trades(markets=markets)
    stream.run(on_message=on_message_market_trades_test)


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_market_orderbooks_stream() -> None:
    markets = ["binance-btc-usdt-spot"]
    stream = client.get_stream_market_orderbooks(markets=markets)
    stream.run(on_message=on_message_market_orderbooks_test)


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_market_quotes_stream() -> None:
    markets = ["*"]
    stream = client.get_stream_market_quotes(markets=markets)
    stream.run(on_message_market_quotes_test)


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_asset_metrics() -> None:
    assets = ["btc"]
    metrics = ["ReferenceRateUSD"]
    stream = client.get_stream_asset_metrics(
        assets=assets, metrics=metrics, frequency="1s"
    )
    stream.run(on_message_asset_metrics_rr_test)


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_market_candles_stream() -> None:
    stream = client.get_stream_market_candles(
        markets=["coinbase-btc-usd-spot"], frequency="1m"
    )
    stream.run(on_message_market_candles_test)


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_get_pair_quotes_stream() -> None:
    stream = client.get_stream_pair_quotes(pairs="btc-usdt")
    stream.run(on_message=on_message_pair_quotes_test)


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_get_asset_quotes_stream() -> None:
    stream = client.get_stream_asset_quotes(assets="btc")
    stream.run(on_message=on_message_assets_quotes_test)

@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_get_market_liquidations() -> None:
    stream = client.get_stream_market_liquidations(markets='binance-LEVERUSDT-future')
    stream.run(on_message=on_message_market_liquidations_test)


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_get_market_openinterest() -> None:
    stream = client.get_stream_market_open_interest(markets='binance-LEVERUSDT-future')
    stream.run(on_message=on_message_market_openinterest)


@pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
def test_on_close() -> None:
    on_close_ran = False
    def on_close(stream: websocket.WebSocketApp, close_status_code: int, close_msg: str) -> None:
        nonlocal on_close_ran
        on_close_ran = True
    stream = client.get_stream_asset_quotes(assets="btc")
    stream.run(on_message=on_message_assets_quotes_test, on_close=on_close)
    assert on_close_ran
    
    
# @pytest.mark.skipif(not cm_api_key_set, reason=REASON_TO_SKIP)
# def test_sigterm() -> None:
#     assets = ["btc"]
#     metrics = ["ReferenceRateUSD"]
#     stream = client.get_stream_asset_metrics(
#         assets=assets, metrics=metrics, frequency="1s"
#     )
#     stream.run(on_message=on_message_sigterm_test, on_close=on_close_sigterm_test)


if __name__ == '__main__':
    pytest.main()