from dataclasses import dataclass, field
from typing import List

@dataclass
class RCA:
    anomaly_signature: str  # A
    failure_localization: str
    failure_category: str
    probable_causes: List[str]
    causal_chain: List[str]
    confidence_score: float
    failure_summary: str
    imputed_metrics: List[str]
    prevention_plan: str = "" # P
