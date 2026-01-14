from datetime import datetime
from typing import Dict, Any, List
from ..models.anomaly import Anomaly
from ..models.sla_clause import SLAClause
from ..utils.time_utils import get_now

class AnomalyFormalizationAgent:
    """
    Step 2: ANOMALY FORMALIZATION AGENT
    Infer impacts, consolidate signals, formalize anomaly.
    """
    
    def formalize(self, 
                  candidate_signal: Dict[str, Any], 
                  sla_clauses: List[SLAClause]) -> Anomaly:
        """
        Agents interpret semantically which SLA applies and formalize the anomaly.
        """
        metric_name = candidate_signal.get("candidate_metric")
        source = candidate_signal.get("source")
        
        # Agent Logic: Match signal metric to SLA definition
        matched_clause = next((c for c in sla_clauses if c.metric == metric_name), None)
        
        if not matched_clause:
            # Fallback
            return Anomaly(
                metric=metric_name or "Unknown",
                observed_value=candidate_signal.get("value", 0),
                expected_value=0.0,
                operator="??",
                anomaly_type="Unknown",
                source=source or "Unknown",
                detected_at=get_now(),
                confidence=0.1,
                evidence="No matching SLA found."
            )
            
        # Agent Formalization
        return Anomaly(
            metric=matched_clause.metric,
            observed_value=candidate_signal.get("value"),
            expected_value=matched_clause.threshold,
            operator=matched_clause.operator,
            anomaly_type="Breach",
            source=source,
            detected_at=get_now(),
            confidence=0.95,
            evidence=f"Observed {candidate_signal.get('value')} violates {matched_clause.operator} {matched_clause.threshold}"
        )
