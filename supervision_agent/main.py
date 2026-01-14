import sys
from datetime import datetime
from typing import Dict, Any

from .services.sla_parser import SLAParser
from .services.sla_filter import SLAFilter
from .services.anomaly_builder import AnomalyBuilder
from .services.kb_vector_search import KBVectorSearch
from .services.rca_engine import RCAEngine

class SupervisionAgent:
    def __init__(self, sla_pdf_path: str):
        self.sla_parser = SLAParser(sla_pdf_path)
        self.sla_filter = SLAFilter()
        self.anomaly_builder = AnomalyBuilder()
        self.kb_search = KBVectorSearch()
        self.rca_engine = RCAEngine()
        
        # Load SLA rules into memory
        self.sla_clauses = self.sla_parser.parse()
        print(f"Loaded {len(self.sla_clauses)} SLA clauses.")

    def run_pipeline(self, alert_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes the sequential pipeline:
        Parse SLA (done in init) -> Receive Alert -> SLA Filter -> Anomaly Builder -> KB Search -> RCA -> Output
        """
        metric = alert_data.get("metric")
        value = alert_data.get("value")
        source = alert_data.get("source")
        duration = alert_data.get("duration_seconds", 0)
        
        print(f"Processing Alert: {metric} = {value} from {source} (Duration: {duration}s)")

        # 1. SLA Impact Filter
        is_impacted = self.sla_filter.check_impact(metric, value, duration, self.sla_clauses)
        if not is_impacted:
            return {"status": "ignored", "reason": "No SLA impact detected"}
        
        print(">> SLA Impact Confirmed.")

        # 2. Anomaly Builder
        anomaly = self.anomaly_builder.build_anomaly(metric, value, source, self.sla_clauses)
        print(f">> Anomaly Formally Built: {anomaly}")

        # 3. Vector KB Search
        # Create a query summary from the anomaly
        query = f"{anomaly.metric} {anomaly.observed_value} {anomaly.anomaly_type} {anomaly.source}"
        kb_results = self.kb_search.search(query)
        print(f">> KB Search Found {len(kb_results)} similar scenarios.")

        # 4. RCA Engine
        rca = self.rca_engine.diagnose(anomaly, kb_results)
        print(f">> RCA Generated with Confidence: {rca.confidence_score}")

        # Structured Output
        output = {
            "status": "processed",
            "sla_impact": True,
            "anomaly": anomaly,
            "rca": rca,
            "kb_hits": kb_results
        }
        return output

if __name__ == "__main__":
    # Example usage for quick check
    agent = SupervisionAgent("config/apache_sla.pdf")
    test_alert = {
        "metric": "NodeAvailability",
        "value": 0,
        "source": "EdgeNode-12",
        "duration_seconds": 600
    }
    result = agent.run_pipeline(test_alert)
    print("\nFinal Result:", result)
