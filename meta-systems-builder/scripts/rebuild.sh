#!/bin/bash

# Nuclear rebuild script for MSB

echo "💥 Initiating nuclear rebuild..."

# Clean up any existing containers
docker ps -aq --filter "name=meta-systems-builder" | xargs docker rm -f 2>/dev/null

# Clean up images
docker images -q "meta-systems-builder" | xargs docker rmi -f 2>/dev/null

# Remove any temporary files
rm -rf __pycache__ .pytest_cache

echo "✅ Cleanup complete. Run ./scripts/run.sh to start fresh."
