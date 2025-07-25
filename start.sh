#!/bin/bash

echo "🚀 Starting Data Ghost services..."
echo "Building and starting backend and frontend..."

# Build and start services in detached mode
docker-compose up --build -d

echo "✅ Services started successfully!"
echo ""
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8080"
echo ""
echo "To view logs: docker-compose logs -f"
echo "To stop services: ./stop.sh" 