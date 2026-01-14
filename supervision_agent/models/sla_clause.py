from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class SLAClause:
    sla_clause_id: str
    metric: str
    operator: str
    threshold: float
    window_minutes: int
    exclusions: List[str] = field(default_factory=list)
    confidence: float = 0.0
    justification: str = ""
