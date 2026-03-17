import datetime
from core.models import FootprintCandle
from signals.base_signal import BaseSignal, SignalResult

class IsNewYorkSession(BaseSignal):
    def __init__(self):
        super().__init__(name="IsNewYorkSession")

    def evaluate(self, candle: FootprintCandle) -> SignalResult:
        dt_utc = datetime.datetime.fromtimestamp(candle.start_time / 1000, tz=datetime.timezone.utc)
        current_hour = dt_utc.hour
        is_ny = 13 <= current_hour < 22
        time_str = dt_utc.strftime('%H:%M UTC')
        if is_ny:
            msg = f"Candle time ({time_str}) is inside the NY Session."
        else:
            msg = f"Candle time ({time_str}) is outside the NY Session."

        return SignalResult(
            signal_name=self.name,
            timestamp=candle.start_time,
            is_triggered=is_ny,
            direction=None,
            message=msg
        )