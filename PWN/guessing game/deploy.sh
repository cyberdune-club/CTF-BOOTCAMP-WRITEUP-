#!/bin/bash
# Deployment script for Guessing Game PWN Challenge

echo "Building Docker container for Guessing Game PWN..."

# Build the Docker image
docker build -t guessing-game-pwn .

# Check if build was successful
if [ $? -eq 0 ]; then
    echo "✅ Docker image built successfully!"
    echo ""
    echo "To run the challenge:"
    echo "docker run -d -p 1337:1337 --name guessing-game-instance guessing-game-pwn"
    echo ""
    echo "To connect to the challenge:"
    echo "nc localhost 1337"
    echo ""
    echo "To stop the challenge:"
    echo "docker stop guessing-game-instance && docker rm guessing-game-instance"
else
    echo "❌ Docker build failed!"
    exit 1
fi
