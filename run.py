"""
Setup and run script for Validation Engine.
Usage: python run.py
"""

import subprocess
import sys
import os
from pathlib import Path

def check_ollama():
    """Check if Ollama is running."""
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        if response.status_code == 200:
            return True
    except:
        pass
    return False

def check_model():
    """Check if llama3.1:8b is available."""
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        if response.status_code == 200:
            models = response.json().get("models", [])
            model_names = [m.get("name") for m in models]
            return any("llama3.1:8b" in name for name in model_names)
    except:
        pass
    return False

def main():
    """Main setup and run function."""
    print("🔍 Validation Engine")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        sys.exit(1)
    
    # Check dependencies
    print("\n📦 Checking dependencies...")
    try:
        import streamlit
        import duckdb
        import sqlglot
        import requests
        print("✓ All dependencies installed")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Run: pip install -r requirements.txt")
        sys.exit(1)
    
    # Check Ollama
    print("\n🤖 Checking Ollama...")
    if not check_ollama():
        print("❌ Ollama is not running")
        print("Run in another terminal: ollama serve")
        sys.exit(1)
    print("✓ Connected to Ollama")
    
    if not check_model():
        print("❌ Model llama3.1:8b not found")
        print("Run: ollama pull llama3.1:8b")
        sys.exit(1)
    print("✓ Model llama3.1:8b available")
    
    # Check data directory
    print("\n📊 Checking data...")
    data_dir = Path(__file__).parent / "data"
    csv_files = list(data_dir.glob("*.csv"))
    if csv_files:
        print(f"✓ Found {len(csv_files)} CSV files:")
        for f in csv_files:
            print(f"  • {f.name}")
    else:
        print("⚠️ No CSV files found in data/ folder")
    
    # Start Streamlit
    print("\n🚀 Starting Streamlit application...")
    print("=" * 50)
    print("Opening http://localhost:8501 in your browser...")
    print("\nTo stop the application, press Ctrl+C")
    print("=" * 50 + "\n")
    
    app_path = Path(__file__).parent / "app.py"
    subprocess.run([sys.executable, "-m", "streamlit", "run", str(app_path)])

if __name__ == "__main__":
    main()
