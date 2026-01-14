from dataclasses import dataclass
from typing import Any

@dataclass
class SLAClause:
    sla_id: str
    metric: str
    threshold: Any
    operator: str
    breach_window_seconds: int

    def is_breached(self, value: Any) -> bool:
        if self.operator == "<":
            return value < self.threshold
        elif self.operator == ">":
            return value > self.threshold
        elif self.operator == "<=":
            return value <= self.threshold
        elif self.operator == ">=":
            return value >= self.threshold
        elif self.operator == "==":
            return value == self.threshold
        return False
