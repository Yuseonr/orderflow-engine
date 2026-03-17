from core.models import FootprintCandle
from signals.base_signal import BaseSignal, SignalResult

class CalculatePoc(BaseSignal):
    def __init__(self):
        super().__init__(name="CalculatePoc")
        self.cache_key = "poc_price"

    def evaluate(self, candle: FootprintCandle) -> SignalResult:
        if not candle.levels:
            return SignalResult(self.name, candle.start_time, False, None, "Empty candle")

        if self.cache_key not in candle.cache:
            poc_level = max(candle.levels.values(), key=lambda lvl: lvl.total_volume)
            candle.cache[self.cache_key] = poc_level.price

        poc_price = candle.cache[self.cache_key]

        return SignalResult(
            signal_name=self.name,
            timestamp=candle.start_time,
            is_triggered=True,
            direction=None, 
            message=f"POC at {poc_price}"
        )