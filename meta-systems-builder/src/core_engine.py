from typing import Dict
import time
from datetime import datetime
from .utils.logger import logger
from .build_layer1 import GenesisBuild
from .audit_layer2 import InversionAudit
from .deploy_layer3 import AutonomousDeployer

class MetaSystemsBuilder:
    """Core engine that orchestrates the MSB framework"""
    
    def __init__(self):
        self.genesis_build = GenesisBuild()
        self.inversion_audit = InversionAudit()
        self.autonomous_deployer = AutonomousDeployer()
        self.cycle_count = 0
    
    def execute_full_cycle(self) -> Dict:
        """Execute a full MSB cycle (all three layers)"""
        self.cycle_count += 1
        cycle_id = f"cycle_{self.cycle_count}_{int(time.time())}"
        
        logger.info("Starting MSB cycle", cycle_id=cycle_id)
        
        # Layer 1: Genesis Build
        build_result = self.genesis_build.execute()
        if not build_result["success"]:
            logger.error("Build failed, attempting rebuild from scratch")
            build_result = self.genesis_build.rebuild_from_scratch()
            
            if not build_result["success"]:
                error_msg = "Complete build failure after rebuild attempt"
                logger.critical(error_msg)
                return {"success": False, "error": error_msg, "cycle_id": cycle_id}
        
        # Layer 2: Inversion Audit
        audit_result = self.inversion_audit.execute(build_result)
        
        # Check if resilience threshold is met
        if audit_result["resilience_score"] < 8.0:  # Configurable threshold
            logger.warning("Resilience score below threshold, triggering rebuild")
            build_result = self.genesis_build.rebuild_from_scratch()
            audit_result = self.inversion_audit.execute(build_result)
        
        # Layer 3: Autonomous Deployment
        deployment_result = self.autonomous_deployer.execute(build_result, audit_result)
        
        # Compile final results
        final_result = {
            "success": deployment_result["success"],
            "cycle_id": cycle_id,
            "timestamp": datetime.now().isoformat(),
            "build": build_result,
            "audit": audit_result,
            "deployment": deployment_result
        }
        
        if deployment_result["success"]:
            logger.info("MSB cycle completed successfully", result=final_result)
        else:
            logger.error("MSB cycle completed with errors", result=final_result)
        
        return final_result

def main():
    """Main entry point for MSB"""
    msb = MetaSystemsBuilder()
    
    # Execute a single cycle
    result = msb.execute_full_cycle()
    
    # Print summary
    if result["success"]:
        print(f"✅ MSB cycle completed successfully!")
        print(f"   Version: {result['deployment'].get('version', 'unknown')}")
        print(f"   Build Strategy: {result['build']['strategy']}")
        print(f"   Resilience Score: {result['audit']['resilience_score']}/10")
    else:
        print(f"❌ MSB cycle failed!")
        print(f"   Error: {result.get('error', 'Unknown error')}")
    
    return result

if __name__ == "__main__":
    main()