import math
import re
from typing import List, Dict, Tuple, Optional
from ..models.rca import RCA
from ..models.anomaly import Anomaly

class KBVectorSearch:
    def __init__(self):
        # A small set of predefined incident scenarios (MVP KB)
        self.scenarios = [
            {
                "id": "SCN-001",
                "description": "Critical Node failure due to edge power loss",
                "category": "INFRASTRUCTURE",
                "localization": "EdgeNode",
                "probable_causes": ["Power supply failure", "UPS battery depletion"],
                "causal_chain": ["Power loss -> Node shutdown"],
                "imputed_metrics": ["NodeAvailability", "PowerStatus"],
                "keywords": {"availability", "node", "power", "shutdown", "0%"}
            },
            {
                "id": "SCN-003",
                "description": "Critical mod_jk worker error (State 6-9)",
                "category": "APPLICATION",
                "localization": "workerEnv",
                "probable_causes": ["Backend timeout", "Max connections reached", "Circuit breaker open"],
                "causal_chain": ["Connection failure -> mod_jk Error State 6"],
                "imputed_metrics": ["ModJkErrorRate", "BackendResponseTime"],
                "keywords": {"mod_jk", "workerenv", "state", "6", "error", "backend"}
            },
            {
                "id": "SCN-002",
                "description": "Network congestion on edge gateway",
                "category": "NETWORK",
                "localization": "Gateway",
                "probable_causes": ["High traffic volume", "DDoS attack"],
                "causal_chain": ["Congestion -> Packet loss -> Timeout"],
                "imputed_metrics": ["Latency", "PacketLoss"],
                "keywords": {"latency", "network", "slow", "packet", "timeout"}
            }
        ]

    def _get_similarity(self, query_keywords: set, scenario_keywords: set) -> float:
        intersection = query_keywords.intersection(scenario_keywords)
        union = query_keywords.union(scenario_keywords)
        return len(intersection) / len(union) if union else 0

    def lookup(self, anomaly: Anomaly, threshold: float = 0.2) -> Optional[Dict]:
        # Extract keywords from anomaly for simple vector-ish search
        query = {str(anomaly.observedValue)}
        
        # Split metric and source into component words
        for item in [anomaly.metric, anomaly.source, anomaly.type]:
            if item:
                # Better splitting for CamelCase and underscores
                words = re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z][a-z]|\b)|[0-9]+', item)
                words = [w.lower() for w in words]
                query.update(words)
                query.add(item.lower())

        # Specific mappings to align with KB
        if "modjk" in query or "mod_jk" in query:
            query.add("mod_jk")
            query.add("error")
        
        if "6" in query: query.add("state")

        best_match = None
        max_score = 0
        
        for scenario in self.scenarios:
            score = self._get_similarity(query, scenario["keywords"])
            if score > max_score:
                max_score = score
                best_match = scenario

        if max_score >= threshold:
            print(f"[KB] Found match with score {max_score:.2f}: {best_match['id']}")
            return best_match
        return None
