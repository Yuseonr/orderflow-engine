from core.models import FootprintCandle
from signals.base_signal import BaseSignal, SignalResult

class CheckTrappedValueArea(BaseSignal):
    """
    Evaluates if the entire Value Area (VAH to VAL) is 
    trapped inside a specific wick (UPPER or LOWER).
    """
    def __init__(self, target_wick: str, cal_va: BaseSignal):
        self.target_wick = target_wick.upper()
        self.cal_va = cal_va
        super().__init__(name=f"TrappedVA_{self.target_wick}_with_{self.cal_va.name}")

    def evaluate(self, candle: FootprintCandle) -> SignalResult:
        self.cal_va.evaluate_with_cache(candle)
        vah = candle.cache.get(self.cal_va.cache_key_vah)
        val = candle.cache.get(self.cal_va.cache_key_val)

        if vah is None or val is None:
            return SignalResult(self.name, candle.start_time, False, None, "Missing Value Area data")

        upper_bound = max(candle.open, candle.close)
        lower_bound = min(candle.open, candle.close)

        is_trapped = False

        if self.target_wick == "UPPER":
            if val > upper_bound:
                is_trapped = True
                
        elif self.target_wick == "LOWER":
            if vah < lower_bound:
                is_trapped = True

        if is_trapped:
            msg = f"TRAP CONFIRMED: VA ({val} - {vah}) trapped in {self.target_wick} wick."
        else:
            msg = f"No trap. VA ({val} - {vah}) intersects body."

        return SignalResult(
            signal_name=self.name,
            timestamp=candle.start_time,
            is_triggered=is_trapped,
            direction=None,
            message=msg
        )