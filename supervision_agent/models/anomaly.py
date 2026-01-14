from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Anomaly:
    metric: str
    observed_value: float
    expected_value: float
    operator: str
    anomaly_type: str
    source: str
    detected_at: datetime
    confidence: float = 0.0
    evidence: str = ""
