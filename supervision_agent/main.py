import sys
import os
from supervision_agent.services.orchestrator import Orchestrator

# Ensure we can import from local
sys.path.append(os.getcwd())

def main():
    print("=== SUPERVISION AGENT MVP (AGENT-AUGMENTED) ===")
    
    # Path to SLA
    sla_path = "supervision_agent/config/apache_sla.pdf"
    
    # Initialize Orchestrator
    orchestrator = Orchestrator(sla_path)

    # SCENARIO 1: Node Availability (Structured Input)
    # Spec 11: Metric: NodeAvailability, Value: 0%, Source: EdgeNode-12, Duration > Window
    print("\n\n>>> RUNNING SCENARIO 1: Hard Down Event")
    scenario_input = {
        "metric": "NodeAvailability",
        "value": 0,
        "source": "EdgeNode-12",
        "duration_seconds": 600
    }
    result = orchestrator.run_pipeline(scenario_input)
    
    print("\n=== FINAL RESULT ===")
    print(f"Status: {result.get('status')}")
    if result.get("rca"):
        rca = result["rca"]
        print(f"RCA Summary: {rca.failure_summary}")
        print(f"Confidence: {rca.confidence_score}")
        print(f"Causes: {rca.probable_causes}")

if __name__ == "__main__":
    main()
