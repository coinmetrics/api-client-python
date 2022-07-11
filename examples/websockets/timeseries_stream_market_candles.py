import sys
from os import environ

import orjson

from coinmetrics.api_client import CoinMetricsClient, CmStream

api_key = (
        environ.get("CM_API_KEY") or sys.argv[1]
)  # sys.argv[1] is executed only if CM_API_KEY is not found

client = CoinMetricsClient(api_key)

stream = client.get_stream_market_candles(
    markets=['coinbase-btc-usd-spot'],
    frequency="1m"
)

def on_message(
        stream: CmStream, message: str
) -> None:
    """
    Custom message callable to be passed in the streaming object
    :param stream: CmStream, WebSocketApp connection
    :param message: str, The message relayed by the API
    :return: None
    """
    data = orjson.loads(message)
    print(data)
    sequence_id = int(data['cm_sequence_id'])
    max_cm_sequence_id = 10
    if sequence_id >= max_cm_sequence_id:
        print(f"Closing the connection after {max_cm_sequence_id} messages...")
        stream.close()

# blocks until connection is closed or interrupted
if __name__ == "__main__":
    stream.run(on_message=on_message)