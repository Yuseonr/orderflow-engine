from decimal import Decimal
from core.models import FootprintCandle
from signals.base_signal import BaseSignal, SignalResult

class CalculatePocGaussian(BaseSignal):
    """
    Calculates the Point of Control (POC) using a Gaussian convolution to smooth the volume profile.\n
    Weights :\n
                - Lower price level: 25pct
                - Target price level: 50pct
                - Upper price level: 25pct

    The POC is determined by finding the price level with the highest smoothed volume.
    """
    def __init__(self):
        super().__init__(name="CalculatePocGaussian")
        self.cache_key = "poc_price_gaussian"
        
        # Gaussian Kernel Weights 
        self.weight_lower = Decimal('0.25')
        self.weight_target = Decimal('0.50')
        self.weight_upper = Decimal('0.25')

    def evaluate(self, candle: FootprintCandle) -> SignalResult:
        if not candle.levels:
            return SignalResult(self.name, candle.start_time, False, None, "Empty candle")
       
        if self.cache_key not in candle.cache:
            smoothed_profile = {}
            tick_size = getattr(candle, 'tick_size', None)

            if not tick_size:
                return SignalResult(self.name, candle.start_time, False, None, "Missing tick size for Gaussian smoothing")
            
            if not isinstance(tick_size, Decimal):
                tick_size = Decimal(str(tick_size))

            for target_price, level_data in candle.levels.items():
                
                raw_volume = getattr(level_data, 'volume', level_data)
                price_below = target_price - tick_size
                price_above = target_price + tick_size
                
                level_below = candle.levels.get(price_below)
                vol_below = getattr(level_below, 'volume', level_below) if level_below else Decimal('0')
                
                level_above = candle.levels.get(price_above)
                vol_above = getattr(level_above, 'volume', level_above) if level_above else Decimal('0')

                smoothed_vol = (
                    (vol_below * self.weight_lower) + 
                    (raw_volume * self.weight_target) + 
                    (vol_above * self.weight_upper)
                )

                smoothed_profile[target_price] = smoothed_vol

            best_price = max(smoothed_profile, key=smoothed_profile.get)
            candle.cache[self.cache_key] = best_price

        poc_price = candle.cache[self.cache_key]

        return SignalResult(
            signal_name=self.name,
            timestamp=candle.start_time,
            is_triggered=True,
            direction=None, 
            message=f"Gaussian POC at {poc_price}"
        )