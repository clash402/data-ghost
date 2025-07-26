#!/bin/bash

echo "🚀 Starting Data Ghost Backend..."
echo "Installing dependencies and starting FastAPI server..."

# Check if uv is installed, if not install it
if ! command -v uv &> /dev/null; then
    echo "📦 Installing uv..."
    pip install uv
fi

# Install dependencies using uv
echo "📦 Installing Python dependencies..."
uv pip sync pyproject.toml

# Start the FastAPI server
echo "🔥 Starting FastAPI server on http://localhost:8080"
echo "Press Ctrl+C to stop"
echo ""

# python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
uv run python -m uvicorn src.main:app --host 0.0.0.0 --port ${PORT:-8000}