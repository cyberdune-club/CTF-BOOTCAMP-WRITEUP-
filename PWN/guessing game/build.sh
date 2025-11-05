#!/bin/bash
# Build script for local testing

echo "Building challenge binary..."
make clean
make vuln

if [ $? -eq 0 ]; then
    echo "✅ Binary built successfully!"
    echo "Run with: ./vuln"
    echo "Analyze with: file vuln && checksec vuln"
else
    echo "❌ Build failed!"
    exit 1
fi
