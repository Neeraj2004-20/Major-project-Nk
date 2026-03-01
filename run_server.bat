@echo off
REM Local Server Startup Script for Windows
REM Starts the AI Market Predictor on http://localhost:8000

echo.
echo ============================================================
echo Starting AI Market Predictor Local Server
echo ============================================================
echo.

REM Activate virtual environment if it exists
if exist ".venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
    echo.
)

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Start the server
echo Starting server on http://localhost:8000
echo.
python run_local_server.py

pause
