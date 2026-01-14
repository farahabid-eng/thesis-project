from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Any

@dataclass
class Anomaly:
    metric: str
    observedValue: Any
    expectedValue: Any
    operator: str
    type: str
    source: str
    detectedAt: datetime

    def __repr__(self):
        return (f"Anomaly<metric={self.metric}, observed={self.observedValue}, "
                f"expected={self.expectedValue}, operator={self.operator}, "
                f"type={self.type}, source={self.source}, at={self.detectedAt}>")
