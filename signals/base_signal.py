from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
from core.models import FootprintCandle

@dataclass
class SignalResult:
    """
    Standardized output for all trading signals.
    """
    signal_name: str             # Name of the signal (e.g., "Bullish Engulfing")
    timestamp: int               # Start_time
    is_triggered: bool           # True if the setup is found, False otherwise
    direction: Optional[str]     # 'BULLISH', 'BEARISH', or None
    message: str = ""            # String to log or display when the signal is triggered

class BaseSignal(ABC):
    """
    Every new signal must inherit from this class.
    """
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def evaluate(self, candle: FootprintCandle) -> SignalResult:
        """
        :param candle: The fully closed 15m FootprintCandle object.
        :return: A standardized SignalResult object.
        """
        pass