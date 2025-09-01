import pytest
from src.audit_layer2 import InversionAudit

def test_inversion_audit_initialization():
    """Test that inversion audit initializes correctly"""
    audit = InversionAudit()
    assert hasattr(audit, 'inversion_engine')
    assert hasattr(audit, 'resilience_scores')

def test_audit_execution():
    """Test audit execution with mock build result"""
    audit = InversionAudit()
    mock_build_result = {"success": True, "strategy": "build_local"}
    
    result = audit.execute(mock_build_result)
    
    assert isinstance(result, dict)
    assert "total_vectors_tested" in result
    assert "passed_vectors" in result
    assert "resilience_score" in result
    assert "details" in result
