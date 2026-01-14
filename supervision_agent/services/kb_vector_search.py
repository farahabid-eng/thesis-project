from typing import List, Dict, Tuple
from dataclasses import dataclass

@dataclass
class KBResult:
    scenario_id: str
    summary: str
    similarity: float

class KBVectorSearch:
    def __init__(self):
        # MVP: Mock vector database with pre-defined scenarios
        self.knowledge_base = [
            {
                "id": "KB-001",
                "vector": [1.0, 0.0, 0.0], # Simplified representation
                "summary": "Edge node offline due to network partition. NodeAvailability dropped to 0.",
                "keywords": ["NodeAvailability", "0", "HardDown"]
            },
            {
                "id": "KB-002",
                "vector": [0.0, 1.0, 0.0],
                "summary": "High latency caused by database lock. ResponseTime > 200ms.",
                "keywords": ["ResponseTime", "Latency"]
            }
        ]
        self.similarity_threshold = 0.7

    def search(self, query_text: str) -> List[KBResult]:
        """
        Simulates vector similarity search.
        In a real system, 'query_text' would be embedded and compared via cosine similarity.
        Here, we use keyword overlap as a deterministic MVP proxy for 'similarity'.
        """
        results = []
        
        # MVP Proxy Logic: Check for keyword presence in query
        # If 'NodeAvailability' and '0' in query => High match for KB-001
        
        # Mock calculation:
        for item in self.knowledge_base:
            score = 0.0
            hits = 0
            for kw in item["keywords"]:
                if kw in query_text:
                    hits += 1
            
            if len(item["keywords"]) > 0:
                score = hits / len(item["keywords"])
            
            # Artificial boost for exact scenario match in MVP
            unique_key = item["keywords"][0] # e.g. NodeAvailability
            if unique_key in query_text:
                if score < 0.8: score = 0.8 # Ensure it passes threshold for relevant metric
                
            if score >= self.similarity_threshold:
                results.append(KBResult(
                    scenario_id=item["id"],
                    summary=item["summary"],
                    similarity=score
                ))
                
        # Sort by similarity desc
        results.sort(key=lambda x: x.similarity, reverse=True)
        return results
