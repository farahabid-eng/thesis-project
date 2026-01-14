import unittest
from supervision_agent.main import SupervisionAgent

class TestSupervisionAgent(unittest.TestCase):
    def test_mandatory_scenario(self):
        """
        MANDATORY TEST SCENARIO:
        - Metric: NodeAvailability
        - Observed value: 0%
        - Source: EdgeNode-12
        - Duration > SLA breach window
        """
        # Setup
        agent = SupervisionAgent("supervision_agent/config/apache_sla.pdf")
        
        # Test Data
        alert = {
            "metric": "NodeAvailability",
            "value": 0,
            "source": "EdgeNode-12",
            "duration_seconds": 600 # 10 minutes (SLA window is 5 min)
        }
        
        # Action
        result = agent.run_pipeline(alert)
        
        # Verification
        # 1. SLA Impact Detected
        self.assertTrue(result["sla_impact"], "SLA Impact should be True")
        
        # 2. Anomaly Correctly Built
        anomaly = result["anomaly"]
        self.assertEqual(anomaly.metric, "NodeAvailability")
        self.assertEqual(anomaly.observed_value, 0)
        self.assertEqual(anomaly.source, "EdgeNode-12")
        self.assertEqual(anomaly.anomaly_type, "HardDown") # Inferred type
        
        # 3. Vector KB Queried (Indirectly verified by RCA confidence boost or logs)
        # We check kb_hits in result which main.py returns
        self.assertTrue(len(result["kb_hits"]) > 0, "Should find similar scenarios in KB")
        self.assertEqual(result["kb_hits"][0].scenario_id, "KB-001", "Should match KB-001 (NodeOffline)")
        
        # 4. RCA Generated
        rca = result["rca"]
        self.assertIsNotNone(rca)
        self.assertEqual(rca.failure_localization, "EdgeNode-12")
        self.assertEqual(rca.failure_category, "Infrastructure")
        self.assertIn("Network Partition", rca.probable_causes)
        
        # 5. Confidence Score Reasonable
        # Since KB match is high (keywords match), confidence should be high (> 0.8)
        self.assertGreater(rca.confidence_score, 0.8, "Confidence should be high due to KB match")
        
        print("\nTest passed successfully with RCA:", rca)

if __name__ == "__main__":
    unittest.main()
