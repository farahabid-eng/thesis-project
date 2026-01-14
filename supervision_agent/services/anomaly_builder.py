from datetime import datetime
from typing import Any, List
from ..models.anomaly import Anomaly
from ..models.sla_clause import SLAClause

class AnomalyBuilder:
    def build_anomaly(self, metric: str, value: Any, source: str, clauses: List[SLAClause]) -> Anomaly:
        """
        Builds an Anomaly object deterministically based on SLA violation.
        """
        relevant_clause = next((c for c in clauses if c.metric == metric), None)
        
        # Default fallback if no clause found (should not happen if filtered correctly)
        expected = relevant_clause.threshold if relevant_clause else 0.0
        operator = relevant_clause.operator if relevant_clause else "?"
        
        # Simple heuristic for type
        # If availability is 0, it's a "HardDown", else "PerformanceBreach"
        anomaly_type = "PerformanceBreach"
        try:
            val_float = float(value)
            if "Availability" in metric and val_float == 0.0:
                anomaly_type = "HardDown"
        except (ValueError, TypeError):
            pass

        return Anomaly(
            metric=metric,
            observed_value=value,
            expected_value=expected,
            operator=operator,
            anomaly_type=anomaly_type,
            source=source,
            detected_at=datetime.now()
        )
