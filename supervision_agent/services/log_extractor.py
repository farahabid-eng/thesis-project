import re
from typing import Dict, Any, Optional

class LogExtractor:
    """
    Step 1: Deterministic Log Extraction (NO AGENT)
    Parses raw logs/inputs to extract candidate signals.
    """
    
    def extract(self, log_input: Any) -> Dict[str, Any]:
        """
        Extract structured candidates from raw string or dict.
        """
        if isinstance(log_input, dict):
            # Already structured, just normalize
            return {
                "candidate_metric": log_input.get("metric"),
                "value": log_input.get("value", log_input.get("observed_value")),
                "source": log_input.get("source"),
                "timestamp": log_input.get("timestamp"),
                "raw_context": str(log_input)
            }
            
        if isinstance(log_input, str):
            # Regex extraction for demo purposes (e.g. Apache logs)
            # "[error] mod_jk child workerEnv in error state 6"
            
            error_pattern = r"\[error\]\s+(.*?)\s+in error state\s+(\d+)"
            match = re.search(error_pattern, log_input)
            
            if match:
                return {
                    "candidate_metric": "ErrorRate",
                    "value": 100,  # Proxy for presence of error
                    "source": match.group(1),
                    "timestamp": None, # Should extract from date part
                    "raw_context": log_input
                }
                
        return {"raw_context": str(log_input), "parsed": False}
