import asyncio
import json
import websocket
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData
import os
from dotenv import load_dotenv

load_dotenv() 


EVENT_HUB_CONNECTION_STR = os.getenv("EVENT_HUB_CONNECTION_STRING")

EVENT_HUB_NAME = "coinbase-raw-trades"


producer = EventHubProducerClient.from_connection_string(
    conn_str=EVENT_HUB_CONNECTION_STR, 
    eventhub_name=EVENT_HUB_NAME
)

async def send_to_eventhub(message):
    """Sends a single message to Azure Event Hubs"""
    try:
        async with producer:
            
            event_data_batch = await producer.create_batch()

            event_data_batch.add(EventData(message))

            await producer.send_batch(event_data_batch)
            

            data = json.loads(message)
            if 'price' in data:
                print(f"Sent to Azure: {data['product_id']} at ${data['price']}")
    except Exception as e:
        print(f"Error sending to Event Hub: {e}")

def on_message(ws, message):
    """This function triggers every time Coinbase sends a trade"""

    asyncio.run(send_to_eventhub(message))

def on_error(ws, error):
    print(f"WebSocket Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("### Closed Connection ###")

def on_open(ws):
    print("### Connection Opened to Coinbase ###")

    subscribe_msg = {
        "type": "subscribe",
        "channels": [
            {
                "name": "ticker",
                "product_ids": ["BTC-USD", "ETH-USD"]
            }
        ]
    }
    ws.send(json.dumps(subscribe_msg))

if __name__ == "__main__":

    ws = websocket.WebSocketApp(
        "wss://ws-feed.exchange.coinbase.com",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    
    print("Starting Producer... Press Ctrl+C to stop.")
    ws.run_forever()