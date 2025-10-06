#!/bin/bash
# Setup script for Politician Trade Tracker

echo "🏛️  Politician Trade Tracker Setup"
echo "=================================="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ Created .env file"
    echo "⚠️  Please edit .env with your email credentials!"
    echo ""
else
    echo "✅ .env file already exists"
fi

# Check if Docker is installed
if command -v docker &> /dev/null; then
    echo "✅ Docker is installed"
else
    echo "⚠️  Docker is not installed. Please install Docker to use this application."
    echo "   Visit: https://docs.docker.com/get-docker/"
fi

# Check if docker-compose is installed
if command -v docker-compose &> /dev/null; then
    echo "✅ Docker Compose is installed"
else
    echo "⚠️  Docker Compose is not installed. Please install it to use this application."
fi

echo ""
echo "📋 Next Steps:"
echo "1. Edit .env with your email credentials"
echo "2. Edit config.yaml to choose politicians to track"
echo "3. Run: docker-compose up -d"
echo "4. View logs: docker-compose logs -f"
echo ""
echo "For detailed instructions, see README.md"
