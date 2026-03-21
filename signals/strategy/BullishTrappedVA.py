from signals.base_strategy import BaseStrategy
from signals.atomic import (CalculatePocGaussian, 
                            CalculateValueArea, 
                            CheckCandleColor, 
                            CheckTrappedValueArea,
                            IsNewYorkSession)

class BullishTrappedVA(BaseStrategy):
    def __init__(self):
        super().__init__(name="BULLISH_TRAPPED_VA", direction="BULLISH")
        poc_calc = CalculatePocGaussian()
        cal_va = CalculateValueArea(cal_poc=poc_calc, value_area_pct='0.70')
        self.anchor_conditions = [
            CheckTrappedValueArea(target_wick="LOWER", cal_va=cal_va)
        ]

        self.context_checks = [
            IsNewYorkSession(),
            CheckCandleColor(target_color="GREEN"),
        ]