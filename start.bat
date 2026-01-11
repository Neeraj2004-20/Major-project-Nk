@echo off
REM Windows startup script for Market Predictor API

echo ========================================
echo   Market Predictor API - Startup
echo ========================================
echo.

REM Check if virtual environment exists
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo.
echo Installing/updating dependencies...
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet

echo.
echo Checking for trained model...
if exist "outputs\*.pt" (
    echo ✓ Model found in outputs folder
) else if exist "model_*.pt" (
    echo ✓ Model found in root folder
) else (
    echo ⚠ No trained model found!
    echo.
    choice /C YN /M "Do you want to train a model now"
    if errorlevel 2 goto skip_training
    if errorlevel 1 goto train_model
    
    :train_model
    echo.
    echo Training model (this may take a while)...
    python main.py
    goto after_training
    
    :skip_training
    echo.
    echo Skipping training. API will start without a model.
    echo You can train later with: python main.py
)

:after_training
echo.
echo ========================================
echo Starting API server...
echo ========================================
echo.
echo API will be available at:
echo   - Local:   http://localhost:8000
echo   - Docs:    http://localhost:8000/docs
echo   - Health:  http://localhost:8000/health
echo.
echo Press Ctrl+C to stop the server
echo.

python serve.py

pause
