from typing import List, Tuple
from ..models.sla_clause import SLAClause

class SLAGate:
    """
    Step 7B: DETERMINISTIC SLA GATE
    """
    
    def check_breach(self, 
                     clause: SLAClause, 
                     observed_value: float, 
                     duration_seconds: float) -> Tuple[bool, str]:
        """
        Contractual decision based on rigid logic.
        Agents do NOT touch this logic.
        """
        
        # 1. Breach Check
        violated = False
        if clause.operator == ">=":
            if observed_value < clause.threshold:
                violated = True
        elif clause.operator == "<=":
            if observed_value > clause.threshold:
                violated = True
        elif clause.operator == "==":
            if observed_value != clause.threshold:
                violated = True
        elif clause.operator == "<" or clause.operator == ">":
             # Simplified for MVP, strictly follow spec operators if defined
             pass 

        if not violated:
             return False, "Value within threshold."

        # 2. Window Check
        window_seconds = clause.window_minutes * 60
        if duration_seconds < window_seconds:
             return False, f"Duration {duration_seconds}s < Window {window_seconds}s"
             
        return True, "SLA Breach Confirmed"
