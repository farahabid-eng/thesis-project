from dataclasses import dataclass
from typing import Any
from datetime import datetime

@dataclass
class Anomaly:
    metric: str
    observed_value: Any
    expected_value: float
    operator: str
    anomaly_type: str # e.g., "Breach", "Unavailable"
    source: str
    detected_at: datetime
