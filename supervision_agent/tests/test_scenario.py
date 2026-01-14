import unittest
from datetime import datetime
from supervision_agent.main import run_supervision_pipeline

class TestSupervisionScenario(unittest.TestCase):
    def test_end_to_end_node_availability_failure(self):
        # Scenario requirements:
        # Metric: NodeAvailability
        # Observed value: 0%
        # Source: EdgeNode-12
        # Duration > SLA breach window
        
        alert_data = {
            "metric": "NodeAvailability",
            "observed_value": 0,
            "source": "EdgeNode-12",
            "duration_seconds": 600 # 10 minutes
        }
        
        rca = run_supervision_pipeline(alert_data)
        
        # Validation
        self.assertIsNotNone(rca, "Pipeline should return an RCA for SLA impact")
        self.assertEqual(rca.FailureLocalization, "EdgeNode", "Should localize to EdgeNode (from KB match SCN-001)")
        self.assertEqual(rca.FailureCategory, "INFRASTRUCTURE")
        self.assertGreaterEqual(rca.ConfidenceScore, 0.9, "Should have high confidence due to KB match")
        self.assertIn("NodeAvailability", rca.ImputedMetrics)

if __name__ == "__main__":
    unittest.main()
