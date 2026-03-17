import asyncio
from core.models import FootprintCandle
from signals.base_signal import BaseSignal
from utils.convert_time import convert_time
from utils.AsukaWebhook import send_to_asuka
from utils.logger import ENGINE_LOGGER, SIGNAL_LOGGER

class SignalManager:
    """
    1. Register signals 
    2. Evaluate all registered signals against newly closed candle.
    3. Alert logic when any signal finds a valid setup.
    """
    def __init__(self):
        self.signals: list[BaseSignal] = []

    def register(self, signal: BaseSignal):
        """
        Adds an instantiated signal to the manager's signal list.
        """
        self.signals.append(signal)
        ENGINE_LOGGER.info(f"Registered Signal: {signal.name}")

    def evaluate_all(self, candle: FootprintCandle):
        """
        Passes candle data to every registered Strategy.
        """
        for strategy in self.signals:
            try:
                result = strategy.evaluate_with_cache(candle)
                
                if result.is_triggered:
            
                    SIGNAL_LOGGER.info(
                        f"[SIGNAL ALERT] {convert_time(result.timestamp, 7)} | {result.signal_name} "
                        f"| {result.direction} | {result.message}"
                    )

                    payload = {
                        "pair": "BTCUSDT", 
                        "timeframe": "15m",
                        "signal": {
                            "name": result.signal_name,
                            "direction": result.direction,
                            "timestamp": result.timestamp
                        },
                        "triggers_met": result.Anchor_trigger,
                        "market_context": result.Data_Context,
                        "candle": candle.to_dict()
                    }

                    asyncio.create_task(send_to_asuka(payload))

            except Exception as e:
                ENGINE_LOGGER.error(f"Error evaluating strategy {strategy.name}: {e}")