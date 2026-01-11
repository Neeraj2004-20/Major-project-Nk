#!/bin/bash
# Linux/Mac startup script for Market Predictor API

echo "========================================"
echo "  Market Predictor API - Startup"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

echo "Activating virtual environment..."
source .venv/bin/activate

echo ""
echo "Installing/updating dependencies..."
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet

echo ""
echo "Checking for trained model..."
if ls outputs/*.pt 1> /dev/null 2>&1 || ls model_*.pt 1> /dev/null 2>&1; then
    echo "✓ Model found"
else
    echo "⚠ No trained model found!"
    echo ""
    read -p "Do you want to train a model now? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo ""
        echo "Training model (this may take a while)..."
        python main.py
    else
        echo ""
        echo "Skipping training. API will start without a model."
        echo "You can train later with: python main.py"
    fi
fi

echo ""
echo "========================================"
echo "Starting API server..."
echo "========================================"
echo ""
echo "API will be available at:"
echo "  - Local:   http://localhost:8000"
echo "  - Docs:    http://localhost:8000/docs"
echo "  - Health:  http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python serve.py
