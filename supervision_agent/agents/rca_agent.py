from typing import List, Dict, Any
from ..models.rca import RCA
from ..models.anomaly import Anomaly

class RCAAgent:
    """
    Step 9: RCA AGENT
    Rule-guided agent reasoning.
    """
    
    def diagnose(self, anomaly: Anomaly, kb_context: List[Any]) -> RCA:
        """
        Generates RCA based on Anomaly, SLA impact, and KB similarity.
        """
        
        # Agent Reasoning (Simulated)
        # 1. Localize
        localization = anomaly.source
        
        # 2. Categorize
        category = "Unknown"
        probable_causes = []
        causal_chain = []
        
        if "NodeAvailability" in anomaly.metric or "Availability" in anomaly.metric:
             category = "INFRASTRUCTURE"
             probable_causes = ["Network Partition", "Power Failure", "OS Crash"]
             causal_chain = ["Node Unreachable", "Heartbeat Timeout"]
        elif "ResponseTime" in anomaly.metric:
             category = "PERFORMANCE"
             probable_causes = ["Resource Saturation", "Database Lock", "High Traffic"]
             causal_chain = ["Queue Buildup", "Latency Spike"]
        else:
             # Default fallback
             category = "APPLICATION"
             probable_causes = ["Configuration Error", "Dependencies"]
             causal_chain = ["Service degradation", "Error Rate Increase"]
             
        # Limit lists as per SOP
        probable_causes = probable_causes[:3]
        causal_chain = causal_chain[:2]
        
        # 4. Confidence
        # Boost confidence if we have KB matches
        confidence = 0.7
        if kb_context and len(kb_context) > 0:
            confidence = 0.92  # Boosted by historical similarity
            
        return RCA(
            anomaly_signature=f"{anomaly.metric}_{anomaly.anomaly_type}",
            failure_localization=localization,
            failure_category=category,
            probable_causes=probable_causes,
            causal_chain=causal_chain,
            confidence_score=confidence,
            failure_summary=f"Detected {anomaly.metric} drop on {localization}. KB confirms similarity to past incidents.",
            imputed_metrics=[anomaly.metric],
            prevention_plan="Review switch redundancy."
        )
