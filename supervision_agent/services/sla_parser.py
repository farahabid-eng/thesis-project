from typing import List
from ..models.sla_clause import SLAClause

class SLAParser:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path

    def parse(self) -> List[SLAClause]:
        # MVP: Rule-based extraction (Mocking the PDF parsing for deterministic behavior)
        # In a real scenario, this would read self.pdf_path and use regex/NLP.
        # Contract-first: We define the rules expected from 'apache_sla.pdf'.
        
        clauses = [
            # Clause 1: Availability must be > 99.9%
            SLAClause(
                sla_id="SLA-001",
                metric="NodeAvailability",
                operator=">",
                threshold=99.9,
                breach_window_seconds=300  # 5 minutes
            ),
            # Clause 2: Response Time must be < 200ms
            SLAClause(
                sla_id="SLA-002",
                metric="ResponseTime",
                operator="<",
                threshold=200.0,
                breach_window_seconds=60  # 1 minute
            )
        ]
        return clauses
