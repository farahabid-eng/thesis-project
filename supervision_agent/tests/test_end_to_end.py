import unittest
from supervision_agent.services.orchestrator import Orchestrator

class TestEndToEnd(unittest.TestCase):
    """
    Step 11: TEST (MANDATORY)
    Scenario: NodeAvailability 0% -> RCA
    """
    
    def setUp(self):
        # Setup Orchestrator with dummy PDF path (agent mocks it anyway)
        self.orchestrator = Orchestrator("supervision_agent/config/apache_sla.pdf")
        
    def test_node_availability_breach(self):
        # Input
        payload = {
            "metric": "NodeAvailability",
            "value": 0,
            "source": "EdgeNode-12",
            "duration_seconds": 601 # > 5 min window
        }
        
        # Execute
        result = self.orchestrator.run_pipeline(payload)
        
        # Verify 1: SLA Impact Decided
        self.assertEqual(result["status"], "BreachConfirmed")
        self.assertTrue(result["sla_impact"])
        
        # Verify 2: Anomaly Formalized via Agent
        anomaly = result["anomaly"]
        self.assertEqual(anomaly.metric, "NodeAvailability")
        self.assertEqual(anomaly.expected_value, 99.0)
        
        # Verify 3: RCA Generated
        rca = result["rca"]
        self.assertIsNotNone(rca)
        self.assertIn("EdgeNode-12", rca.failure_localization)
        self.assertGreater(rca.confidence_score, 0.9, "Confidence should be high due to KB match")
        self.assertEqual(rca.failure_category, "INFRASTRUCTURE")
        
        print("\nMandatory Test Passed: NodeAvailability -> RCA with high confidence.")

if __name__ == "__main__":
    unittest.main()
