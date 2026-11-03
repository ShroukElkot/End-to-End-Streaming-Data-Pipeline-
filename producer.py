import json
import websocket
from azure.eventhub import EventHubProducerClient, EventData
import time
# ==========================================
# 1. AZURE EVENT HUBS CONFIGURATION
# ==========================================
# Member 2 needs to provide this connection string and hub name
EVENT_HUB_CONNECTION_STR = ""
EVENT_HUB_NAME = "crypto-raw-stream"

producer = EventHubProducerClient.from_connection_string(
    conn_str=EVENT_HUB_CONNECTION_STR,
    eventhub_name=EVENT_HUB_NAME
)

# ==========================================
# 2. BINANCE WEBSOCKET CONFIGURATION
# ==========================================
coins = ['btcusdt', 'ethusdt', 'bnbusdt', 'solusdt', 'xrpusdt']
streams = '/'.join([f"{coin}@trade" for coin in coins])
socket_url = f"wss://stream.binance.com:9443/stream?streams={streams}"

# ==========================================
# 3. WEBSOCKET EVENT HANDLERS
# ==========================================
def on_message(ws, message):
    try:
        # Create a batch and add the JSON message
        event_data_batch = producer.create_batch()
        event_data_batch.add(EventData(message))
        
        # Send to Event Hubs
        producer.send_batch(event_data_batch)
        print(f"Sent trade data: {json.loads(message)['data']['s']}")
    except Exception as e:
        print(f"Error sending message: {e}")

def on_error(ws, error):
    print(f"WebSocket Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("WebSocket Closed")

def on_open(ws):
    print(f"Connected to Binance! Streaming top 5 coins...")

# ==========================================
# 4. START STREAM
# ==========================================
# if __name__ == "__main__":
#     ws = websocket.WebSocketApp(
#         socket_url,
#         on_open=on_open,
#         on_message=on_message,
#         on_error=on_error,
#         on_close=on_close
#     )
#     # run_forever automatically keeps the connection alive
#     ws.run_forever()

# ==========================================
# 4. START STREAM (WITH AUTO-RECONNECT)
# ==========================================
if __name__ == "__main__":
    while True:
        try:
            print("Connecting to Binance WebSocket...")
            ws = websocket.WebSocketApp(
                socket_url,
                on_open=on_open,
                on_message=on_message,
                on_error=on_error,
                on_close=on_close
            )
            
            # ping_interval forces a heartbeat every 60 seconds so Binance doesn't drop you
            ws.run_forever(ping_interval=60, ping_timeout=10)
            
            # If run_forever() stops (WinError 10054), this code executes
            print("Connection dropped! Reconnecting in 3 seconds...")
            time.sleep(3)
            
        except Exception as e:
            print(f"Critical error: {e}. Reconnecting in 3 seconds...")
            time.sleep(3)