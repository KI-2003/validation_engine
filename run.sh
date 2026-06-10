#!/bin/bash
# Validation Engine - Unix/Linux/macOS Quick Start Script

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║          🔍 VALIDATION ENGINE - STARTING                       ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    echo ""
    echo "Please install Python 3 from: https://www.python.org/downloads/"
    exit 1
fi

echo "✓ Python found"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo ""
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment"
        exit 1
    fi
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "🔧 Activating virtual environment..."
source .venv/bin/activate
if [ $? -ne 0 ]; then
    echo "❌ Failed to activate virtual environment"
    exit 1
fi
echo "✓ Virtual environment activated"

# Check if requirements are installed
echo ""
echo "📚 Checking dependencies..."
pip list | grep streamlit > /dev/null
if [ $? -ne 0 ]; then
    echo "📥 Installing requirements..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install requirements"
        exit 1
    fi
fi
echo "✓ Dependencies ready"

# Run the application
echo ""
echo "🚀 Starting application..."
echo ""
python run.py
if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Application failed to start"
    echo ""
    echo "Common issues:"
    echo "- Ollama not running (run 'ollama serve' in another terminal)"
    echo "- Model not available (run 'ollama pull llama3.1:8b')"
    echo ""
    exit 1
fi
