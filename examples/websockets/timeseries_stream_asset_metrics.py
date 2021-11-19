from coinmetrics.api_client import CoinMetricsClient, CmStream
import orjson

api_key = "<api_key>"
client = CoinMetricsClient(api_key)

stream = client.get_stream_asset_metrics(
    assets=['btc', 'eth'], frequency='1s',
    metrics=['ReferenceRateUSD', 'ReferenceRateBTC', 'ReferenceRateETH']
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
stream.run(on_message=on_message)