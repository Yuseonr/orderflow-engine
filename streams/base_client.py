import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Callable
import websockets
from websockets.exceptions import ConnectionClosed

class BaseWebsocketClient(ABC):
    def __init__(self, url: str, on_trade_callback: Callable):
        """
        :param url: The websocket endpoint for the exchange.
        :param on_trade_callback: The function to pass the parsed Trade object to Aggregator.
        """
        self.url = url
        self.on_trade_callback = on_trade_callback
        self.is_running = False

    @abstractmethod
    async def process_message(self, message: str):
        """
        CHILD CLASSES MUST IMPLEMENT THIS.
        It takes the raw JSON string from the exchange, converts it to a standardized
        core.models.Trade object, and passes it to self.on_trade_callback().
        """
        pass

    async def start(self):
        """The main loop that maintains the connection and auto-reconnects on failure."""
        self.is_running = True
        
        while self.is_running:
            try:
                # The 'async with' block ensures the socket is cleanly closed if errors occur
                async with websockets.connect(self.url) as ws:
                    logging.info(f"Successfully connected to {self.url}")
                    
                    # Listen for messages until the connection is closed or an error occurs
                    while self.is_running:
                        message = await ws.recv()
                        # Pass the raw text to the exchange-specific parser
                        await self.process_message(message)
                        
            except ConnectionClosed as e:
                logging.warning(f"Websocket connection closed: {e}. Reconnecting in 3 seconds...")
                await asyncio.sleep(3)
            except Exception as e:
                logging.error(f"Unexpected error in websocket loop: {e}. Reconnecting in 5 seconds...")
                await asyncio.sleep(5)

    def stop(self):
        """Gracefully signals the loop to shut down."""
        logging.info("Initiating websocket shutdown...")
        self.is_running = False