from core.models import FootprintCandle
from signals.base_signal import BaseSignal, SignalResult

class PocWickSignal(BaseSignal):
    """
    This signal identifies when the Point of Control (POC) is on a candle's wick.\n
    Bullish : Green candle with POC on the lower wick (POC price < Open)
    Bearish : Red candle with POC on the upper wick (POC price > Open)
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

        # candle color
        is_green = candle.close > candle.open
        is_red = candle.close < candle.open

        # Bullish
        if is_green and poc_price < candle.open:
            msg = f"Bullish: POC at {poc_price} wick below Open {candle.open}. Delta: {poc_level.delta}"
            return SignalResult(
                signal_name=self.name,
                timestamp=candle.start_time,
                is_triggered=True,
                direction="BULLISH",
                message=msg
            )

        # Bearish
        elif is_red and poc_price > candle.open:
            msg = f"Bearish: POC at {poc_price} wick above Open {candle.open}. Delta: {poc_level.delta}"
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
            message="POC inside body or Doji candle"
        )