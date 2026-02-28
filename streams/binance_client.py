import json
import logging
from decimal import Decimal
from typing import Callable
from core.models import Trade
from streams.base_client import BaseWebsocketClient

class BinanceWebsocketClient(BaseWebsocketClient):
    def __init__(self, symbol: str, on_trade_callback: Callable):
        """
        :param symbol: The trading pair (e.g., 'BTCUSDT')
        :param on_trade_callback: The function to pass the parsed Trade object to.
        """
        # Formatted for Binance USD-M Futures raw stream endpoint
        stream_url = f"wss://fstream.binance.com/ws/{symbol.lower()}@trade"

        super().__init__(url=stream_url, on_trade_callback=on_trade_callback)
        self.symbol = symbol.upper()

    async def process_message(self, message: str):
        """
        Parses the raw Binance Futures JSON string into standard Trade object.
        """
        try:
            data = json.loads(message)

            # safety check to ensure we are parsing the correct message type and that price/quantity are valid
            if data.get('e') != 'trade' or Decimal(data.get('p')) <= 0 or Decimal(data.get('q')) <= 0:
                return
            
            # Pass the string values directly into Decimal() 
            trade = Trade(
                timestamp=data['T'],           # Trade Execution Time
                price=Decimal(data['p']),      # Price
                size=Decimal(data['q']),       # Quantity / Volume
                is_buyer_maker=data['m']       # Maker side (True = Market Sell, False = Market Buy)
            )
            self.on_trade_callback(trade)
        except KeyError as e:
            logging.error(f"Missing expected key in Binance message: {e} - Message: {message}")
        except Exception as e:
            logging.error(f"Error processing Binance message: {e} - Message: {message}")