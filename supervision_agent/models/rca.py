from dataclasses import dataclass, field
from typing import List, Any
from .anomaly import Anomaly

@dataclass
class RCA:
    anomaly: Anomaly
    failure_localization: str
    failure_category: str
    probable_causes: List[str]
    causal_chain: List[str]
    confidence_score: float
    failure_summary: str
    imputed_metrics: List[Any] = field(default_factory=list)
    p_factor: float = 0.0 # "P" from SOP model requirement
