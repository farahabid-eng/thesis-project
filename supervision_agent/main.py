import sys
import os
from datetime import datetime, timedelta
from typing import Any, Union

# Add current directory to path for imports
sys.path.append(os.getcwd())

from supervision_agent.services.sla_parser import SLAParser
from supervision_agent.services.sla_filter import SLAFilter
from supervision_agent.services.anomaly_builder import AnomalyBuilder
from supervision_agent.services.kb_vector_search import KBVectorSearch
from supervision_agent.services.rca_engine import RCAEngine
from supervision_agent.utils.time_utils import get_now

def run_supervision_pipeline(alert_input: Any):
    print("--- Supervision Agent Pipeline Start ---")
    
    # 0. Ingestion & Normalization
    if isinstance(alert_input, str):
        print(f"[0] Ingesting raw log: {alert_input}")
        alert_data = log_to_alert(alert_input)
        if not alert_data:
            print("[0] Error: Failed to parse log string into alert data.")
            return None
    else:
        alert_data = alert_input

    # 1. Load and Parse SLA
    sla_path = "config/apache_sla.pdf"
    parser = SLAParser(sla_path)
    clauses = parser.parse()
    print(f"[1] SLA Parsed: {len(clauses)} clauses loaded.")
    
    # 2. SLA Impact Filter
    sla_filter = SLAFilter(clauses)
    impact_clause = sla_filter.check_impact(
        metric=alert_data["metric"],
        observed_value=alert_data["observed_value"],
        duration_seconds=alert_data["duration_seconds"]
    )
    
    if not impact_clause:
        print("[2] No SLA impact detected (or duration below threshold). Pipeline terminated.")
        return None
    
    print(f"[2] SLA Impact detected! Clause breached: {impact_clause.sla_id}")
    
    # 3. Anomaly Builder
    builder = AnomalyBuilder()
    anomaly = builder.build(
        metric=alert_data["metric"],
        observed_value=alert_data["observed_value"],
        source=alert_data["source"],
        clause=impact_clause,
        detected_at=get_now()
    )
    print(f"[3] Anomaly object formalized: {anomaly}")
    
    # 4. KB Vector Search
    kb_search = KBVectorSearch()
    kb_match = kb_search.lookup(anomaly)
    
    # 5. RCA Engine
    rca_engine = RCAEngine()
    rca = rca_engine.generate(anomaly, kb_match)
    print(f"[5] RCA Generated. Confidence: {rca.ConfidenceScore}")
    
    print("\n--- STRUCTURED DECISION OUTPUT ---")
    print(f"Outcome: {'KB Match' if kb_match else 'New RCA'}")
    print(f"Summary: {rca.FailureSummary}")
    print(f"Category: {rca.FailureCategory}")
    print(f"Localization: {rca.FailureLocalization}")
    print(f"Probable Causes: {', '.join(rca.ProbableCauses)}")
    print(f"Chain: {' -> '.join(rca.CausalChain)}")
    print(f"Confidence: {rca.ConfidenceScore*100}%")
    print("----------------------------------")
    
    return rca

def log_to_alert(log_line: str) -> dict:
    import re
    # Match mod_jk errors
    if "mod_jk" in log_line.lower():
        # Match error state
        state_match = re.search(r"state (\d+)", log_line)
        source_match = re.search(r"child (\w+)", log_line)
        
        source = source_match.group(1) if source_match else "mod_jk"
        state = state_match.group(1) if state_match else "unknown"
        
        # Determine metric based on the error
        metric = "ModJkErrorRate"
        
        return {
            "metric": metric,
            "observed_value": 100, # Single events are treated as 100% error in that window
            "source": source,
            "duration_seconds": 600 # Static assumption for MVP
        }
    return {}

if __name__ == "__main__":
    # 1. Test with Structured Data (Original Scenario)
    print("=== SCENARIO 1: Node Availability (Structured) ===")
    example_alert = {
        "metric": "NodeAvailability",
        "observed_value": 0,
        "source": "EdgeNode-12",
        "duration_seconds": 600 
    }
    run_supervision_pipeline(example_alert)
    
    # 2. Test with User's Log (Raw String)
    print("\n=== SCENARIO 2: mod_jk Log Error (Raw String) ===")
    user_log = "[Mon Dec 05 19:15:57 2005] [error] mod_jk child workerEnv in error state 6"
    run_supervision_pipeline(user_log)
