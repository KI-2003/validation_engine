@echo off
REM Validation Engine - Windows Quick Start Script

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║          🔍 VALIDATION ENGINE - STARTING                       ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo ✓ Python found

REM Check if virtual environment exists
if not exist ".venv" (
    echo.
    echo 📦 Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✓ Virtual environment created
)

REM Activate virtual environment
echo.
echo 🔧 Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Failed to activate virtual environment
    pause
    exit /b 1
)
echo ✓ Virtual environment activated

REM Check if requirements are installed
echo.
echo 📚 Checking dependencies...
pip list | findstr streamlit >nul
if errorlevel 1 (
    echo 📥 Installing requirements...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Failed to install requirements
        pause
        exit /b 1
    )
)
echo ✓ Dependencies ready

REM Run the application
echo.
echo 🚀 Starting application...
echo.
python run.py
if errorlevel 1 (
    echo.
    echo ❌ Application failed to start
    echo.
    echo Common issues:
    echo - Ollama not running (run "ollama serve" in another terminal)
    echo - Model not available (run "ollama pull llama3.1:8b")
    echo.
    pause
    exit /b 1
)

pause
