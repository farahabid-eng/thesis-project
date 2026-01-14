from dataclasses import dataclass
from typing import Any

@dataclass
class SLAClause:
    metric: str
    operator: str  # ">", "<", ">=", "<="
    threshold: float
    breach_window_seconds: int
    sla_id: str = "SLA-GENERIC"
