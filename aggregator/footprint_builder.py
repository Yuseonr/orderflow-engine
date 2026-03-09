import os
import json
from utils.logger import ENGINE_LOGGER
from decimal import Decimal
from typing import Callable, Optional
from core.models import Trade, FootprintCandle, FootprintLevel

class FootprintBuilder:
    def __init__(self, tick_size: Decimal, interval_ms: int, on_signal_update: Optional[Callable] = None, on_candle_close: Optional[Callable] = None):
        """
        :param tick_size: The price grouping bracket (e.g., Decimal('5.0'))
        :param interval_ms: Candle length in milliseconds (15m = 900,000 ms)
        :param on_signal_update: A function to call every time the candle updates
        :param on_candle_close: A function to call when a candle is closed
        """
        self.tick_size = tick_size
        self.interval_ms = interval_ms
        self.on_signal_update = on_signal_update
        self.on_candle_close = on_candle_close
        self.current_candle: Optional[FootprintCandle] = None
    
    def get_current_candle(self) -> Optional[FootprintCandle]:
        """Returns the current live candle. """
        return self.current_candle

    def process_trade(self, trade: Trade):
        """Takes a raw trade and integrates it into the footprint."""
        
        # 1. TIME BUCKETING: Calculate exact 15m boundary
        candle_start_time = trade.timestamp - (trade.timestamp % self.interval_ms)
        
        # 2. CANDLE MANAGEMENT: Check if we need a new 15m candle
        if self.current_candle is None or self.current_candle.start_time != candle_start_time:
            if self.current_candle is not None:
                
                # Can add to databsase or perform final calculations on the closed candle here

                """ Save the closed candle to a JSONL file """
                os.makedirs("data", exist_ok=True)
                filename = "data/footprint_history.jsonl"
                with open(filename, "a") as f:
                    json_string = json.dumps(self.current_candle.to_dict())
                    f.write(json_string + "\n")
                
                """ Signal evaluation on closed candle """
                if self.on_candle_close:
                    self.on_candle_close(self.current_candle)

                # Logging 
                ENGINE_LOGGER.info(f"[ARCHIVE] Append closed {self.current_candle.start_time} candle to {filename}")

                print(f"\n[CLOSED] 15m Candle at {self.current_candle.start_time} closed.\n")
            
            # Open the new candle
            self.current_candle = FootprintCandle(
                start_time=candle_start_time,
                open=trade.price,
                high=trade.price,
                low=trade.price,
                close=trade.price
            )

        # 3. UPDATE OHLC (Open, High, Low, Close)
        if trade.price > self.current_candle.high:
            self.current_candle.high = trade.price
        if trade.price < self.current_candle.low:
            self.current_candle.low = trade.price
        self.current_candle.close = trade.price
        
        # 4. UPDATE TOTAL VOLUME
        self.current_candle.total_volume += trade.size
        if trade.is_buy_side:
            self.current_candle.total_buy_volume += trade.size
        else:
            self.current_candle.total_sell_volume += trade.size

        # 5. PRICE GROUPING: Round down to nearest tick size ($5)
        # Example: 85002.50 // 5 = 17000. 17000 * 5 = 85000
        grouped_price = (trade.price // self.tick_size) * self.tick_size

        # 6. UPDATE FOOTPRINT LEVEL
        if grouped_price not in self.current_candle.levels:
            self.current_candle.levels[grouped_price] = FootprintLevel(price=grouped_price)
            
        level = self.current_candle.levels[grouped_price]
        
        if trade.is_buy_side:
            level.buy_volume += trade.size
        else:
            level.sell_volume += trade.size

        # 7. TRIGGER SIGNAL LAYER
        # Pass the live, updating candle to your signal logic if theres any
        if self.on_signal_update:
            self.on_signal_update(self.current_candle)