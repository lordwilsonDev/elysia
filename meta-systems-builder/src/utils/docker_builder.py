import docker
from typing import Dict, Optional
import time

class DockerManager:
    """Manages Docker operations for MSB"""
    
    def __init__(self):
        try:
            self.client = docker.from_env()
            self.available = True
        except Exception:
            self.available = False
    
    def check_daemon(self) -> Dict:
        """Check if Docker daemon is available"""
        if not self.available:
            return {"available": False, "error": "Docker not available"}
        
        try:
            info = self.client.info()
            return {
                "available": True,
                "version": info.get("ServerVersion", "unknown"),
                "containers": info.get("ContainersRunning", 0)
            }
        except Exception as e:
            return {"available": False, "error": str(e)}
    
    def build_image(self, tag: str = "meta-systems-builder") -> Dict:
        """Build Docker image"""
        if not self.available:
            return {"success": False, "error": "Docker not available"}
        
        try:
            image, logs = self.client.images.build(
                path=".",
                tag=tag,
                dockerfile="docker/Dockerfile"
            )
            return {"success": True, "image_id": image.id}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def run_container(self, image: str, ports: Dict) -> Dict:
        """Run Docker container"""
        if not self.available:
            return {"success": False, "error": "Docker not available"}
        
        try:
            container = self.client.containers.run(
                image,
                ports=ports,
                detach=True
            )
            return {"success": True, "container_id": container.id}
        except Exception as e:
            return {"success": False, "error": str(e)}