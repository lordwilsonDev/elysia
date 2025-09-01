import joblib
from typing import Dict, List
import json
from pathlib import Path

class FailurePredictor:
    """Predicts potential failures based on historical patterns"""
    
    def __init__(self):
        self.risk_patterns = self._load_risk_patterns()
        
    def _load_risk_patterns(self) -> Dict:
        """Load risk patterns from knowledge base"""
        patterns = {
            "dependency_conflicts": {
                "probability": 0.5,
                "mitigation": "Use cached layers, fallback mirrors, and dependency scanning"
            },
            "configuration_errors": {
                "probability": 0.45,
                "mitigation": "Pre-validation of configs and fail-fast checks"
            },
            "docker_daemon_issues": {
                "probability": 0.4,
                "mitigation": "Pre-check docker info, clear cache with 'docker builder prune'"
            },
            "network_timeouts": {
                "probability": 0.35,
                "mitigation": "Cached dependencies + retry mechanisms"
            },
            "test_flakiness": {
                "probability": 0.3,
                "mitigation": "Rerun flaky tests, environment consistency checks"
            }
        }
        return patterns
    
    def predict_risks(self, context: Dict) -> List[Dict]:
        """Predict risks based on current context"""
        predicted_risks = []
        
        for risk_name, risk_data in self.risk_patterns.items():
            # Simple heuristic-based prediction
            if self._is_risk_likely(risk_name, context):
                predicted_risks.append({
                    "risk": risk_name,
                    "probability": risk_data["probability"],
                    "mitigation": risk_data["mitigation"]
                })
        
        return sorted(predicted_risks, key=lambda x: x["probability"], reverse=True)
    
    def _is_risk_likely(self, risk_name: str, context: Dict) -> bool:
        """Determine if a risk is likely based on context"""
        if risk_name == "docker_daemon_issues":
            return not context.get("docker_available", False)
        
        elif risk_name == "network_timeouts":
            return context.get("network_latency", 0) > 100
        
        elif risk_name == "dependency_conflicts":
            return context.get("has_complex_dependencies", False)
        
        # Default: assume risk is possible
        return True
