from core.models import FootprintCandle
from signals.base_signal import BaseSignal, SignalResult

class BaseStrategy(BaseSignal):
    def __init__(self, name: str, direction: str):
        super().__init__(name=name)
        self.direction = direction.upper()
        self.anchor_conditions: list[BaseSignal] = []
        self.context_checks: list[BaseSignal] = []

    def evaluate(self, candle: FootprintCandle) -> SignalResult:
        triggers_dict = {}
        context_dict = {}

        for atom in self.anchor_conditions:
            result = atom.evaluate_with_cache(candle)
            if not result.is_triggered:
                return SignalResult(
                    signal_name=self.name,
                    timestamp=candle.start_time,
                    is_triggered=False,
                    direction=None,
                    message=f"Strategy aborted: {atom.name} failed."
                )
            
            triggers_dict[atom.name] = f"[TRUE] {result.message}"

        for atom in self.context_checks:
            result = atom.evaluate_with_cache(candle)
            icon = "[TRUE]" if result.is_triggered else "[FALSE]"
            context_dict[atom.name] = f"{icon} {result.message}"

        return SignalResult(
            signal_name=self.name,
            timestamp=candle.start_time,
            is_triggered=True,
            direction=self.direction,
            message=f"{self.name} triggered with {len(self.anchor_conditions)} anchor conditions and {len(self.context_checks)} context checks.",
            Anchor_trigger=triggers_dict,
            Data_Context=context_dict
        )