from core.models import FootprintCandle
from signals.base_signal import BaseSignal, SignalResult

class CheckPocLocation(BaseSignal):
    """ 
    Add target wick : **UPPER**, **LOWER**, or **BODY**\n
    Add cal_poc : **CalculatePoc()** , **CalculatePocProminance()**\n
    POC is in the upper wick if poc_price > max(open, close)\n
    POC is in the lower wick if poc_price < min(open, close)\n
    Otherwise, POC is in the body
    """
    def __init__(self, target_wick: str, cal_poc: BaseSignal):
        self.target_wick = target_wick.upper()
        self.cal_poc = cal_poc
        super().__init__(name=f"CheckPocLocation")

    def evaluate(self, candle: FootprintCandle) -> SignalResult:

        self.cal_poc.evaluate_with_cache(candle)

        poc_price = candle.cache[self.cal_poc.cache_key]
        upper_bound = max(candle.open, candle.close)
        lower_bound = min(candle.open, candle.close)

        if poc_price > upper_bound:
            actual_location = "UPPER"
        elif poc_price < lower_bound:
            actual_location = "LOWER"
        else:
            actual_location = "BODY"

        return SignalResult(
            signal_name=self.name,
            timestamp=candle.start_time,
            is_triggered=(actual_location == self.target_wick),
            direction=None,
            message=f"POC is in the {actual_location} wick."
        )
