from typing import Any, Dict
from ..agents.sla_interpretation_agent import SLAInterpretationAgent
from ..agents.anomaly_formalization_agent import AnomalyFormalizationAgent
from ..agents.rca_agent import RCAAgent
from ..services.log_extractor import LogExtractor
from ..services.sla_gate import SLAGate
from ..services.kb_vector_search import KBVectorSearch
from ..models.rca import RCA
# Or use pydantic for structured logging

class Orchestrator:
    """
    Step 10: ORCHESTRATION RULES
    Sequential execution only.
    """
    
    def __init__(self, sla_pdf_path: str):
        print("[Orchestrator] Initializing components...")
        self.sla_agent = SLAInterpretationAgent(sla_pdf_path)
        self.log_extractor = LogExtractor()
        self.anomaly_agent = AnomalyFormalizationAgent()
        self.sla_gate = SLAGate()
        self.kb_search = KBVectorSearch()
        self.rca_agent = RCAAgent()
        
    def run_pipeline(self, raw_input: Any) -> Dict[str, Any]:
        """
        Executes the fixed high-level pipeline.
        """
        print(f"\n--- START PIPELINE ---")
        
        # 1. SLA Interpretation Agent
        # (Realistically cached, but spec says "Pipeline order MUST NOT change")
        clauses = self.sla_agent.interpret()
        print(f"[1] SLA clauses loaded: {len(clauses)}")
        
        # 2. Log Extraction (Deterministic)
        candidate = self.log_extractor.extract(raw_input)
        print(f"[2] Extracted candidate: {candidate['candidate_metric']} = {candidate['value']}")
        
        # 3. Anomaly Formalization Agent
        anomaly = self.anomaly_agent.formalize(candidate, clauses)
        print(f"[3] Anomaly formalized: {anomaly.metric} ({anomaly.anomaly_type})")
        
        # 4. SLA Impact Gate (Deterministic)
        # Assuming duration came from log or is calculated. 
        # For this MVP, we might treat single point as "instant" or assume duration provided in input.
        # If input has no duration, we assume 0 (which might fail validation if window > 0)
        # Spec 11: "Duration > SLA window"
        duration_s = raw_input.get("duration_seconds", 600) if isinstance(raw_input, dict) else 0
        
        impact_clause = next((c for c in clauses if c.metric == anomaly.metric), None)
        
        if not impact_clause:
            print("[4] No matching SLA clause to check impact against.")
            return {"status": "NoSLA", "anomaly": anomaly}
            
        is_breach, reason = self.sla_gate.check_breach(impact_clause, anomaly.observed_value, duration_s)
        print(f"[4] SLA Impact Decision: {is_breach} ({reason})")
        
        if not is_breach:
            return {"status": "NoBreach", "reason": reason}
            
        # 5. Vector KB Search
        kb_context = self.kb_search.search(f"{anomaly.metric} {anomaly.source} {anomaly.anomaly_type}")
        print(f"[5] KB Similarity Search: {len(kb_context)} hits")
        
        # 6. RCA Agent
        rca = self.rca_agent.diagnose(anomaly, kb_context)
        print(f"[6] RCA Generated: {rca.failure_summary} (Conf: {rca.confidence_score})")
        
        return {
            "status": "BreachConfirmed",
            "sla_impact": True,
            "anomaly": anomaly,
            "rca": rca,
            "kb_context": kb_context
        }
