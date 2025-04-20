#!/bin/bash

# Exit on error
set -e

echo "Setting up SlideSage..."

# Create necessary directories
mkdir -p input output examples/input examples/output

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Build and start the containers
echo "Building and starting containers..."
cd docker
docker-compose up -d

# Wait for Ollama to be ready
echo "Waiting for Ollama to be ready..."
sleep 10

# Pull the required model
echo "Pulling the required model..."
docker-compose exec ollama ollama pull gemma3:4b

echo "Setup complete!"
echo "You can now place your PPTX files in the 'input' directory and run the processing."
echo "To process files, run: docker-compose exec slidesage python main.py"
echo "To stop the services, run: docker-compose down" 