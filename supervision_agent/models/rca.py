from dataclasses import dataclass
from typing import List, Optional
from .anomaly import Anomaly

@dataclass
class RCA:
    A: Anomaly
    FailureLocalization: str
    FailureCategory: str
    ProbableCauses: List[str]
    CausalChain: List[str]
    ConfidenceScore: float
    FailureSummary: str
    ImputedMetrics: List[str]
    P: str  # Probable solution or recommendation (implied by P in the provided list)

    def __repr__(self):
        return (f"RCA<Localization={self.FailureLocalization}, "
                f"Category={self.FailureCategory}, Confidence={self.ConfidenceScore}>")
