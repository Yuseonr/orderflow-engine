import asyncio
import logging
from decimal import Decimal

# Import  modules
from streams.binance_client import BinanceWebsocketClient
from aggregator.footprint_builder import FootprintBuilder
from utils.interface import run_interface_loop

# --- CONFIGURATION ---
SYMBOL = "btcusdt"              # symbol to subscribe to (e.g., 'btcusdt' or 'ethusdt')
TICK_SIZE = Decimal("5.0")      # Group trades into $5 buckets
INTERVAL_MS = 15 * 60 * 1000    # 15 minutes in milliseconds (900,000)
FPS = 4

refresh_rate = 1 / FPS

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='engine.log',  
    filemode='a'
)

async def main():
    print(f"Starting Orderflow Engine for {SYMBOL.upper()}...")
    
    # Aggregator
    # We pass our display function as the callback. Every time a trade is 
    # processed, the builder will hand the updated candle to print_live_footprint.
    builder = FootprintBuilder(
        tick_size=TICK_SIZE,
        interval_ms=INTERVAL_MS,
    )
    
    # Initialize the Websocket Client
    # We pass the builder's process_trade function as the callback. 
    # Every time the socket gets a raw JSON trade, it passes the clean Trade object here.
    ws_client = BinanceWebsocketClient(
        symbol=SYMBOL,
        on_trade_callback=builder.process_trade
    )

    # Terminal UI Task 
    # This runs concurrently with the websocket listener. It continuously fetches the latest candle from the builder and prints it.
    interface_task = asyncio.create_task(run_interface_loop(get_candle_func=builder.get_current_candle, refresh_rate=refresh_rate))
    
    # Start the Event Loop
    try:
        # This will run forever, listening to Binance and updating the terminal
        await ws_client.start()
    except KeyboardInterrupt:
        print("\nShutting down engine...")
    finally:
        interface_task.cancel()
        ws_client.stop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass 