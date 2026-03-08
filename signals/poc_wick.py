from core.models import FootprintCandle
from signals.base_signal import BaseSignal, SignalResult

class PocWickSignal(BaseSignal):
    """
    This signal identifies when the Point of Control (POC) is on a candle's wick.\n
    Bullish : POC on the lower wick (POC < body_low)
    Bearish : POC on the upper wick (POC > body_high)
    """
    def __init__(self):
        super().__init__(name="POC_ON_WICK")

    def evaluate(self, candle: FootprintCandle) -> SignalResult:
        # safety check 
        if not candle.levels:
            return SignalResult(self.name, candle.start_time, False, None, "Empty candle")

        # poc level 
        poc_level = max(candle.levels.values(), key=lambda lvl: lvl.total_volume)
        poc_price = poc_level.price

        # candle body
        body_low = min(candle.open, candle.close)
        body_high = max(candle.open, candle.close)

        # Bullish
        if poc_price < body_low:
            msg = f"Bullish: POC at {poc_price} wick below body_low {body_low}. Delta: {poc_level.delta}"
            return SignalResult(
                signal_name=self.name,
                timestamp=candle.start_time,
                is_triggered=True,
                direction="BULLISH",
                message=msg
            )

        # Bearish
        elif poc_price > body_high:
            msg = f"Bearish: POC at {poc_price} wick above body_high {body_high}. Delta: {poc_level.delta}"
            return SignalResult(
                signal_name=self.name,
                timestamp=candle.start_time,
                is_triggered=True,
                direction="BEARISH",
                message=msg
            )

        # No signal
        return SignalResult(
            signal_name=self.name,
            timestamp=candle.start_time,
            is_triggered=False,
            direction=None,
            message="POC inside body"
        )