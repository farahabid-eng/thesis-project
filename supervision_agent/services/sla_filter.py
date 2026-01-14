from typing import Any, List
from ..models.sla_clause import SLAClause

class SLAFilter:
    def check_impact(self, metric: str, value: Any, duration_seconds: int, clauses: List[SLAClause]) -> bool:
        """
        Determines if an anomaly impacts the SLA based on strict contract rules.
        """
        # 1. Is the metric governed by the SLA?
        relevant_clause = next((c for c in clauses if c.metric == metric), None)
        if not relevant_clause:
            return False

        # 2. Is the threshold violated?
        is_violated = False
        if relevant_clause.operator == ">":
            is_violated = value <= relevant_clause.threshold # Violation if value is LOWER/EQUAL when it must be GREATER
        elif relevant_clause.operator == "<":
            is_violated = value >= relevant_clause.threshold
        elif relevant_clause.operator == ">=":
             is_violated = value < relevant_clause.threshold
        elif relevant_clause.operator == "<=":
             is_violated = value > relevant_clause.threshold
        
        # Note: Handled STRICT inequality violation based on operator. 
        # e.g. operator ">" (Expect > 99.9), so if Value <= 99.9 it IS a violation.

        if not is_violated:
            return False

        # 3. Is the breach duration exceeded?
        if duration_seconds < relevant_clause.breach_window_seconds:
            return False

        return True
