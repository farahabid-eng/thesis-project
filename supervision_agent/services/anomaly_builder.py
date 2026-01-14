from datetime import datetime
from ..models.anomaly import Anomaly
from ..models.sla_clause import SLAClause

class AnomalyBuilder:
    @staticmethod
    def build(metric: str, observed_value: float, source: str, clause: SLAClause, detected_at: datetime) -> Anomaly:
        # Infer type using simple heuristics
        anomaly_type = "AVAILABILITY_CRITICAL" if observed_value == 0 else "PERFORMANCE_DEGRADATION"
        
        return Anomaly(
            metric=metric,
            observedValue=observed_value,
            expectedValue=clause.threshold,
            operator=clause.operator,
            type=anomaly_type,
            source=source,
            detectedAt=detected_at
        )
