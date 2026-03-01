#!/bin/bash
# Start script for the AI Market Predictor Web Application

echo "🚀 Starting AI Market Predictor Web Application..."
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

# Start the server
echo ""
echo "🌐 Starting server on http://localhost:8000"
echo "✨ Press Ctrl+C to stop"
echo ""

python serve.py
