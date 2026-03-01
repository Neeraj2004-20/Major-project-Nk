@echo off
REM Start script for the AI Market Predictor Web Application (Windows)

echo 🚀 Starting AI Market Predictor Web Application...
echo.

REM Check if virtual environment exists
if not exist ".venv" (
    echo 📦 Creating virtual environment...
    python -m venv .venv
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Installing dependencies...
pip install -q -r requirements.txt

REM Start the server
echo.
echo 🌐 Starting server on http://localhost:8000
echo ✨ Press Ctrl+C to stop
echo.

python serve.py
