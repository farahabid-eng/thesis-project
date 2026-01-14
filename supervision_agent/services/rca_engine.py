from typing import List
from ..models.anomaly import Anomaly
from ..models.rca import RCA
from .kb_vector_search import KBResult

class RCAEngine:
    def diagnose(self, anomaly: Anomaly, kb_results: List[KBResult]) -> RCA:
        """
        Produce a rule-based Root Cause Analysis.
        """
        # 1. Failure Localization
        localization = anomaly.source
        
        # 2. Failure Category (Simple Mapping)
        category = "Unknown"
        probable_causes = []
        causal_chain = []
        
        if anomaly.metric == "NodeAvailability":
             category = "Infrastructure"
             probable_causes = ["Network Partition", "Power Failure", "OS Crash"]
             causal_chain = ["Node Unreachable", "Heartbeat Timeout"]
        elif anomaly.metric == "ResponseTime":
             category = "Performance"
             probable_causes = ["Resource Saturation", "Database Lock", "High Traffic"]
             causal_chain = ["Queue Buildup", "Latency Spike"]
        elif anomaly.metric == "ModJkErrorRate":
             category = "Application"
             probable_causes = ["Worker Thread Starvation", "Backend Unreachable"]
             causal_chain = ["Connection Refused", "Error Rate Increase"]
             
        # Limit lists as per SOP
        probable_causes = probable_causes[:3]
        causal_chain = causal_chain[:2]
        
        # 3. Confidence Score calculation
        # Baseline confidence
        confidence = 0.5
        # Boost if KB results found similar scenarios
        if kb_results:
             # Take top match
             top_match = kb_results[0]
             if top_match.similarity > 0.8:
                 confidence = 0.95
             elif top_match.similarity > 0.6:
                 confidence = 0.8
        
        # 4. Failure Summary
        summary = f"Detected {anomaly.anomaly_type} on {anomaly.metric} at {anomaly.source}. \
Value {anomaly.observed_value} violated (Expect {anomaly.operator} {anomaly.expected_value})."

        return RCA(
            anomaly=anomaly,
            failure_localization=localization,
            failure_category=category,
            probable_causes=probable_causes,
            causal_chain=causal_chain,
            confidence_score=confidence,
            failure_summary=summary,
            imputed_metrics=[],
            p_factor=confidence # Assuming P corresponds to probability/confidence or similar factor
        )
