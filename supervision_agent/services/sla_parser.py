import re
import subprocess
import os
from typing import List
from ..models.sla_clause import SLAClause

class SLAParser:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.txt_path = pdf_path.replace(".pdf", ".txt")

    def parse(self) -> List[SLAClause]:
        # Convert PDF to text if text file doesn't exist
        if not os.path.exists(self.txt_path):
            try:
                subprocess.run(["pdftotext", self.pdf_path, self.txt_path], check=True)
            except Exception:
                pass # Fallback to mock if conversion fails

        clauses = []
        if os.path.exists(self.txt_path):
            with open(self.txt_path, "r") as f:
                content = f.read()
                
                # Extract Availability threshold (e.g., 99.9%)
                # Look for "Disponibilité" or similar keywords
                avail_match = re.search(r"(\d+[,.]\d+)%", content)
                threshold = float(avail_match.group(1).replace(",", ".")) if avail_match else 99.0
                
                # Extract Breach Window (e.g., 5 minutes)
                window_match = re.search(r"(\d+)\s+minutes\s+consécutives", content)
                window_seconds = int(window_match.group(1)) * 60 if window_match else 300
                
                # Extract mod_jk error rate threshold (e.g., 10%)
                modjk_match = re.search(r"taux d'erreur mod jk dépasse (\d+)%", content)
                modjk_threshold = float(modjk_match.group(1)) if modjk_match else 10.0
                
                clauses.append(SLAClause(
                    sla_id="SLA-MODJK-EXTRACTED",
                    metric="ModJkErrorRate",
                    threshold=modjk_threshold,
                    operator="<",   # Error rate must be < 10%
                    breach_window_seconds=window_seconds
                ))
        
        # Fallback if parsing failed
        if not clauses:
            clauses.append(SLAClause(
                sla_id="SLA-APACHE-DEFAULT",
                metric="NodeAvailability",
                threshold=99.9,
                operator=">",
                breach_window_seconds=300
            ))
            
        return clauses
