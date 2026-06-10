"""Configuration module."""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

# Data directory
DATA_DIR = BASE_DIR / "data"

# Ollama configuration
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Streamlit configuration
STREAMLIT_THEME = "light"
MAX_RESULTS_DISPLAY = 1000
