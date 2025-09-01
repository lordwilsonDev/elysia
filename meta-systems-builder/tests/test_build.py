import pytest
from src.build_layer1 import GenesisBuild

def test_build_local():
    """Test the build_local strategy"""
    builder = GenesisBuild()
    result = builder.build_local()
    
    assert isinstance(result, dict)
    assert "success" in result
    assert "strategy" in result
    assert result["strategy"] == "build_local"

def test_build_fallback_strategy():
    """Test that build strategies are attempted in order"""
    builder = GenesisBuild()
    
    # Mock the strategies to force failures
    original_local = builder.build_local
    original_docker = builder.build_docker_in_docker
    
    def failing_local():
        return {"success": False, "error": "Simulated failure"}
    
    def successful_docker():
        return {"success": True, "strategy": "build_docker_in_docker", "time_taken": 3.0}
    
    builder.build_local = failing_local
    builder.build_docker_in_docker = successful_docker
    
    result = builder.execute()
    
    # Should succeed with docker strategy
    assert result["success"] == True
    assert result["strategy"] == "build_docker_in_docker"
    
    # Restore original methods
    builder.build_local = original_local
    builder.build_docker_in_docker = original_docker
