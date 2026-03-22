from decimal import Decimal
from core.models import FootprintCandle
from signals.base_signal import BaseSignal, SignalResult

class CalculateValueArea(BaseSignal):
    """
    Calculates the Value Area High (VAH) and Value Area Low (VAL)\n
    based on a specified percentage of total volume around the Point of Control (POC).
    """
    def __init__(self, cal_poc: BaseSignal, value_area_pct: str):
        self.cal_poc = cal_poc
        super().__init__(name=f"CalculateValueArea_{self.cal_poc.name}")
        self.value_area_pct = Decimal(value_area_pct)
        self.cache_key_vah = "value_area_high"
        self.cache_key_val = "value_area_low"

    def evaluate(self, candle: FootprintCandle) -> SignalResult:
        if not candle.levels:
            return SignalResult(self.name, candle.start_time, False, None, "Empty candle")

        self.cal_poc.evaluate_with_cache(candle)
        poc_price = candle.cache.get(self.cal_poc.cache_key)

        if not poc_price:
            return SignalResult(self.name, candle.start_time, False, None, "Missing POC")

        if self.cache_key_vah not in candle.cache or self.cache_key_val not in candle.cache:
            tick_size = getattr(candle, 'tick_size', None)
            if tick_size is None:
                return SignalResult(self.name, candle.start_time, False, None, "Missing tick size for Value Area calculation")
            
            if not isinstance(tick_size, Decimal):
                tick_size = Decimal(str(tick_size))

            target_volume = candle.total_volume * self.value_area_pct
            max_price = max(candle.levels.keys())
            min_price = min(candle.levels.keys())

            vah = poc_price
            val = poc_price
            
            poc_level = candle.levels.get(poc_price)
            current_volume = getattr(poc_level, 'volume', poc_level) if poc_level else Decimal('0')

            while current_volume < target_volume:
                price_up = vah + tick_size
                price_down = val - tick_size

                if price_up > max_price and price_down < min_price:
                    break

                level_up = candle.levels.get(price_up)
                vol_up = getattr(level_up, 'volume', level_up) if level_up else Decimal('0')

                level_down = candle.levels.get(price_down)
                vol_down = getattr(level_down, 'volume', level_down) if level_down else Decimal('0')

                if vol_up > vol_down:
                    vah = price_up
                    current_volume += vol_up
                elif vol_down > vol_up:
                    val = price_down
                    current_volume += vol_down
                else:
                    vah = price_up
                    val = price_down
                    current_volume += (vol_up + vol_down)

            candle.cache[self.cache_key_vah] = vah
            candle.cache[self.cache_key_val] = val

        vah = candle.cache[self.cache_key_vah]
        val = candle.cache[self.cache_key_val]

        return SignalResult(
            signal_name=self.name,
            timestamp=candle.start_time,
            is_triggered=True,
            direction=None,
            message=f"VAH: {vah}, VAL: {val}"
        )