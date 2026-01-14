from typing import List, Optional
from ..models.sla_clause import SLAClause

class SLAFilter:
    def __init__(self, clauses: List[SLAClause]):
        self.clauses = clauses

    def check_impact(self, metric: str, observed_value: float, duration_seconds: float) -> Optional[SLAClause]:
        for clause in self.clauses:
            if clause.metric == metric:
                # Check if threshold is breached (negation of is_breached logic or direct check)
                # In SLAClause, is_breached returns True if metric < threshold (breach)
                # Here we use the data model logic
                if not clause.is_breached(observed_value):
                    # It's a breach (e.g., current 0% < threshold 99%)
                    if duration_seconds >= clause.breach_window_seconds:
                        return clause
        return None
