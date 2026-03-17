from core.models import FootprintCandle
from signals.base_signal import BaseSignal, SignalResult

class CheckCandleColor(BaseSignal):
    """ 
    Add target color : **RED**, **GREEN**, or **DOJI** (if open and close are equal)
    """
    def __init__(self, target_color: str):
        self.target_color = target_color.upper()
        super().__init__(name=f"CheckCandleColor")

    def evaluate(self, candle: FootprintCandle) -> SignalResult:
        is_green = candle.close > candle.open
        is_red = candle.close < candle.open
        
        if not is_green and not is_red:
            actual_color = "DOJI"
        elif is_green:
            actual_color = "GREEN"
        else:
            actual_color = "RED"

        return SignalResult(
            signal_name=self.name,
            timestamp=candle.start_time,
            is_triggered=(actual_color == self.target_color),
            direction=None,
            message=f"Candle closed {actual_color}."
        )
