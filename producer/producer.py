import asyncio
import json
import websocket
import os
from dotenv import load_dotenv
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData
import threading
from datetime import datetime, timezone


# --- Configuration ---
load_dotenv()
EVENT_HUB_CONNECTION_STR = os.getenv("EVENT_HUB_CONNECTION_STRING")
EVENT_HUB_NAME = "coinbase-raw-trades"
WEBSOCKET_URL = "wss://ws-feed.exchange.coinbase.com"

# --- Main Application Logic ---

async def main():
    """Main function to run the producer and websocket client."""
    
    # Get the current running event loop to schedule tasks from another thread
    loop = asyncio.get_running_loop()
    
    # Create the producer client that will stay open for the life of the app
    producer = EventHubProducerClient.from_connection_string(
        conn_str=EVENT_HUB_CONNECTION_STR, 
        eventhub_name=EVENT_HUB_NAME
    )
    
# The same async function, but with a timeout added

    async def send_to_eventhub(message):
        """Coroutine to send a single message with a timeout."""
        try:
            event_data_batch = await producer.create_batch()
            event_data_batch.add(EventData(message))
            
            # --- THIS IS THE KEY CHANGE ---
            # Add a timeout of 15 seconds to the send operation.
            # If it takes longer than 15s, it will raise a TimeoutError.
            await producer.send_batch(event_data_batch, timeout=15)
            
            # This print statement now only runs on SUCCESS
            data = json.loads(message)
            if 'price' in data:
                print(f"Sent: {data['product_id']} at ${data['price']}")
                
        except asyncio.TimeoutError:
            # This will be logged if the send_batch call takes too long
            print("ERROR: Sending to Event Hub timed out after 15 seconds. This may cause a container restart.")
            # We will exit with a non-zero code to trigger the OnFailure restart policy
            exit(1)
            
        except Exception as e:
            # This catches other errors from the Event Hub SDK
            print(f"ERROR: An exception occurred while sending to Event Hub: {e}")
            # We also exit here to be safe and trigger a restart
            exit(1)

    # --- WebSocket Callback Functions ---
    # These functions run in a separate thread managed by the websocket client
    
    def on_message(ws, message):
        """Schedules the async send_to_eventhub function to run on the main event loop."""
        
        # --- ADD THIS LOGGING ---
        # 1. Get the current time the moment the message is received
        received_at_utc = datetime.now(timezone.utc)
        
        # 2. Parse the timestamp from the Coinbase message body
        try:
            data = json.loads(message)
            coinbase_time_str = data.get('time')
            if coinbase_time_str:
                # 3. Log both timestamps for comparison
                print(f"DEBUG: Coinbase Time = {coinbase_time_str} | Producer Received Time = {received_at_utc.isoformat()}")
        except Exception as e:
            print(f"DEBUG: Could not parse message body: {e}")
        # --- END OF LOGGING ---

        # This part remains the same
        asyncio.run_coroutine_threadsafe(send_to_eventhub(message), loop)

    def on_error(ws, error):
        print(f"WebSocket Error: {error}")

    def on_close(ws, close_status_code, close_msg):
        print("### WebSocket Closed ###")

    def on_open(ws):
        print("### WebSocket Opened to Coinbase ###")
        subscribe_msg = {
            "type": "subscribe",
            "channels": [{"name": "ticker", "product_ids": ["BTC-USD", "ETH-USD"]}]
        }
        ws.send(json.dumps(subscribe_msg))

    # Create the WebSocketApp instance
    ws = websocket.WebSocketApp(
        WEBSOCKET_URL,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    
    # Run the WebSocket client in a separate thread so it doesn't block the async loop
    wst = threading.Thread(target=ws.run_forever)
    wst.daemon = True
    wst.start()

    print("Producer started. Press Ctrl+C to stop.")
    
    try:
        # Keep the main async function running forever
        while True:
            await asyncio.sleep(3600) # Sleep for a long time; the work is done in callbacks
    finally:
        # Ensure the producer is closed gracefully on exit
        await producer.close()
        ws.close()
        print("Producer and WebSocket clients closed.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Program stopped by user.")