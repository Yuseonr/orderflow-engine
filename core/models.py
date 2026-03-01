from dataclasses import dataclass, field
from decimal import Decimal
from typing import Dict

@dataclass(slots=True)
class Trade:
    """
    1. RAW TRADE DATA
    Represents a single, atomic transaction sent by the Binance websocket.
    Process these instantly and discard them to keep memory usage low.
    """
    timestamp: int       # Unix timestamp in milliseconds from the exchange
    price: Decimal       # The exact execution price
    size: Decimal        # The quantity traded (e.g., amount of BTC or ETH)
    is_buyer_maker: bool # Binance specific: True = Market Sell, False = Market Buy

    @property
    def is_buy_side(self) -> bool:
        """
        Helper property. If the buyer was the 'maker' (sitting on the limit book), 
        it means the aggressor who crossed the spread was a Market Seller.
        """
        return not self.is_buyer_maker


@dataclass(slots=True)
class FootprintLevel:
    """
    2. PRICE ROW
    Represents a single horizontal row on footprint chart (e.g., the $85,000 level).
    It acts as a tally counter for all trades that happen at this specific price.
    """
    price: Decimal
    buy_volume: Decimal = Decimal('0')
    sell_volume: Decimal = Decimal('0')

    @property
    def delta(self) -> Decimal:
        """The net difference between aggressive buyers and sellers at this specific price."""
        return self.buy_volume - self.sell_volume

    @property
    def total_volume(self) -> Decimal:
        """Total volume traded at this specific price level."""
        return self.buy_volume + self.sell_volume


@dataclass(slots=True)
class FootprintCandle:
    """
    3. CANDLE CONTAINER
    Master object for a specific time window. It holds standard OHLC data 
    and contains all the individual FootprintLevels inside a dictionary.
    """
    start_time: int  # Millisecond timestamp marking the exact start of this 15m window
    
    # Standard Candlestick Data
    open: Decimal = Decimal('0')
    high: Decimal = Decimal('0')
    low: Decimal = Decimal('0')
    close: Decimal = Decimal('0')
    
    # Aggregated Volume Data
    total_volume: Decimal = Decimal('0')
    total_buy_volume: Decimal = Decimal('0')
    total_sell_volume: Decimal = Decimal('0')
    
    # The Orderflow Dictionary: Maps a Price (Decimal) to its FootprintLevel.
    # Use a dictionary because checking if a price exists is an O(1) operation,
    # which is incredibly fast for high-frequency data.
    levels: Dict[Decimal, FootprintLevel] = field(default_factory=dict)

    @property
    def delta(self) -> Decimal:
        """The overall delta (Buy Volume - Sell Volume) for the entire candle."""
        return self.total_buy_volume - self.total_sell_volume
    
    # Convertion method to make it JSON serializable for storage 
    def to_dict(self) -> dict:
        """Converts the candle into a JSON dictionary."""
        return {
            "start_time": self.start_time,
            "open": str(self.open),
            "high": str(self.high),
            "low": str(self.low),
            "close": str(self.close),
            "total_volume": str(self.total_volume),
            "total_buy_volume": str(self.total_buy_volume),
            "total_sell_volume": str(self.total_sell_volume),
            "delta": str(self.delta),
            "levels": {
                str(price): {
                    "buy_volume": str(level.buy_volume),
                    "sell_volume": str(level.sell_volume),
                    "total_volume": str(level.total_volume),
                    "delta": str(level.delta)
                }
                for price, level in self.levels.items()
            }
        }