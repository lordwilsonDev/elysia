from typing import Dict, List
import subprocess
import time
from .utils.logger import logger
from .utils.docker_builder import DockerManager
from .utils.port_scanner import find_free_port

class GenesisBuild:
    """Implements Layer 1: Genesis Build with triple redundancy"""
    
    def __init__(self):
        self.docker_manager = DockerManager()
        self.build_strategies = [
            self.build_local,
            self.build_docker_in_docker,
            self.build_from_template
        ]
    
    def execute(self) -> Dict:
        """Execute the build process with fallback strategy"""
        logger.info("Starting Genesis Build process")
        
        # Check preconditions
        context = self._assess_context()
        logger.info("Context assessment completed", context=context)
        
        # Try each build strategy in order
        for strategy in self.build_strategies:
            result = strategy()
            if result["success"]:
                logger.info("Build strategy succeeded", 
                           strategy=strategy.__name__, result=result)
                return result
            
            logger.warning("Build strategy failed", 
                          strategy=strategy.__name__, error=result.get("error"))
        
        # All strategies failed
        error_msg = "All build strategies failed"
        logger.error(error_msg)
        return {"success": False, "error": error_msg}
    
    def _assess_context(self) -> Dict:
        """Assess the current context for build decisions"""
        docker_status = self.docker_manager.check_daemon()
        free_port = find_free_port()
        
        return {
            "docker_available": docker_status["available"],
            "free_port_available": free_port is not None,
            "free_port": free_port,
            "timestamp": time.time()
        }
    
    def build_local(self) -> Dict:
        """Build strategy 1: Local execution"""
        logger.info("Attempting build_local strategy")
        
        try:
            # Chain-of-Thought reasoning
            thought_process = [
                "Choosing build_local because:",
                "- Direct execution is fastest path",
                "- Historical success rate: ~70%",
                "- No container overhead"
            ]
            
            # Simulate build process
            time.sleep(2)  # Simulate build time
            
            # Check if build was successful (simulated)
            success = True  # In real implementation, this would be determined by actual build result
            
            if success:
                return {
                    "success": True,
                    "strategy": "build_local",
                    "time_taken": 2.1,
                    "thought_process": thought_process
                }
            else:
                return {
                    "success": False,
                    "error": "Build failed during local execution"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Exception in build_local: {str(e)}"
            }
    
    def build_docker_in_docker(self) -> Dict:
        """Build strategy 2: Docker-in-Docker approach"""
        logger.info("Attempting build_docker_in_docker strategy")
        
        try:
            # Chain-of-Thought reasoning
            thought_process = [
                "Falling back to build_docker_in_docker because:",
                "- Local build failed",
                "- Docker daemon is available",
                "- Provides better isolation"
            ]
            
            # Simulate Docker build
            time.sleep(3)  # Simulate longer build time
            
            # Check if build was successful (simulated)
            success = True
            
            if success:
                return {
                    "success": True,
                    "strategy": "build_docker_in_docker",
                    "time_taken": 3.2,
                    "thought_process": thought_process
                }
            else:
                return {
                    "success": False,
                    "error": "Docker build failed"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Exception in build_docker_in_docker: {str(e)}"
            }
    
    def build_from_template(self) -> Dict:
        """Build strategy 3: Template-based recovery"""
        logger.info("Attempting build_from_template strategy")
        
        try:
            # Chain-of-Thought reasoning
            thought_process = [
                "Falling back to build_from_template because:",
                "- Previous strategies failed",
                "- Using golden snapshot for recovery",
                "- Most reliable but slowest approach"
            ]
            
            # Simulate template-based build
            time.sleep(5)  # Simulate longest build time
            
            # Check if build was successful (simulated)
            success = True
            
            if success:
                return {
                    "success": True,
                    "strategy": "build_from_template",
                    "time_taken": 5.3,
                    "thought_process": thought_process
                }
            else:
                return {
                    "success": False,
                    "error": "Template build failed"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Exception in build_from_template: {str(e)}"
            }
    
    def rebuild_from_scratch(self) -> Dict:
        """Nuclear option: Complete rebuild from scratch"""
        logger.warning("Initiating rebuild_from_scratch")
        
        try:
            # This would implement a complete clean rebuild
            time.sleep(8)  # Simulate extensive rebuild process
            
            return {
                "success": True,
                "strategy": "rebuild_from_scratch",
                "time_taken": 8.5,
                "thought_process": ["Nuclear rebuild initiated due to complete failure"]
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Rebuild from scratch failed: {str(e)}"
            }