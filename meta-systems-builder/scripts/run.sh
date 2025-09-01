#!/bin/bash

# Meta Systems Builder - Run Script

echo "🚀 Starting Meta Systems Builder v1.0"

# Check if Docker is available
if command -v docker &> /dev/null; then
    echo "🐳 Docker is available, building container..."
    docker build -f docker/Dockerfile -t meta-systems-builder .
    
    echo "🏃 Running container..."
    docker run -p 8000:8000 meta-systems-builder
else
    echo "⚠️ Docker not available, running directly with Python..."
    python src/core_engine.py
fi
