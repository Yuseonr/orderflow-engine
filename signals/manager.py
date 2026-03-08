import logging
from core.models import FootprintCandle
from signals.base_signal import BaseSignal

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
        logging.info(f"Registered Signal: {signal.name}")

    def evaluate_all(self, closed_candle: FootprintCandle):
        """
        Passes candle data to every registered signal.
        """
        for signal in self.signals:
            try:
                result = signal.evaluate(closed_candle)
                if result.is_triggered:

                    # Can add other alrt mechanism here like Telegram, Discord. 
                    logging.info(
                        f"[SIGNAL ALERT] {result.timestamp} | {result.signal_name} "
                        f"| {result.direction} | {result.message}"
                    )

            except Exception as e:
                logging.error(f"Error evaluating signal {signal.name}: {e}")