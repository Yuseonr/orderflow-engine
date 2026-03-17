from signals.base_strategy import BaseStrategy
from signals.atomic.CalculatePoc import CalculatePoc
from signals.atomic.CheckCandleColor import CheckCandleColor
from signals.atomic.CheckPocLocation import CheckPocLocation
from signals.atomic.IsNewYorkSession import IsNewYorkSession

class BullishPocOnWick(BaseStrategy):
    def __init__(self):
        super().__init__(name="BULLISH_TRAPPED_POC", direction="BULLISH")

        poc_calc = CalculatePoc()
        self.anchor_conditions = [
            CheckCandleColor(target_color="GREEN"),
            CheckPocLocation(target_wick="LOWER", cal_poc=poc_calc)
        ]

        self.context_checks = [
            IsNewYorkSession()
        ]