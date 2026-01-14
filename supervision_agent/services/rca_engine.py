from typing import List, Dict, Optional
from ..models.rca import RCA
from ..models.anomaly import Anomaly

class RCAEngine:
    def generate(self, anomaly: Anomaly, kb_match: Optional[Dict] = None) -> RCA:
        if kb_match:
            # Reuse scenario data if match found
            return RCA(
                A=anomaly,
                FailureLocalization=kb_match["localization"],
                FailureCategory=kb_match["category"],
                ProbableCauses=kb_match["probable_causes"],
                CausalChain=kb_match["causal_chain"],
                ConfidenceScore=0.9, # High confidence for KB match
                FailureSummary=f"Known issue identified: {kb_match['description']}",
                ImputedMetrics=kb_match["imputed_metrics"],
                P="Follow established recovery procedures for " + kb_match["id"]
            )
        
        # Rule-based fallback if no KB match
        return RCA(
            A=anomaly,
            FailureLocalization=anomaly.source,
            FailureCategory=self._infer_category(anomaly),
            ProbableCauses=["Unspecified system error", "Component timeout"],
            CausalChain=[f"{anomaly.metric} violation -> System anomaly"],
            ConfidenceScore=0.5,
            FailureSummary=f"Anomaly detected in {anomaly.metric} on {anomaly.source}",
            ImputedMetrics=[anomaly.metric],
            P="Investigate logs for " + anomaly.source
        )

    def _infer_category(self, anomaly: Anomaly) -> str:
        if "Availability" in anomaly.metric or "Power" in anomaly.metric:
            return "INFRASTRUCTURE"
        if "Latency" in anomaly.metric or "Network" in anomaly.metric:
            return "NETWORK"
        return "GENERAL"
