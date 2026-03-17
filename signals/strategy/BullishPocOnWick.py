from signals.base_strategy import BaseStrategy
from signals.atomic import (CalculatePoc, 
                            CheckCandleColor, 
                            CheckPocLocation ,
                            IsNewYorkSession)

class BullishPocOnWick(BaseStrategy):
    def __init__(self):
        super().__init__(name="BULLISH_POC_ON_WICK", direction="BULLISH")

        poc_calc = CalculatePoc()
        self.anchor_conditions = [
            CheckCandleColor(target_color="GREEN"),
            CheckPocLocation(target_wick="LOWER", cal_poc=poc_calc)
        ]

        self.context_checks = [
            IsNewYorkSession()
        ]