@echo off
echo ========================================
echo StockSense AI - Deployment Script
echo ========================================
echo.

cd "C:\Users\palam\OneDrive\Desktop\empty folder"

echo [1/5] Initializing Git repository...
git init

echo.
echo [2/5] Adding all files...
git add .

echo.
echo [3/5] Committing changes...
git commit -m "StockSense AI v1.0 - Production Ready with 7 AI Features"

echo.
echo [4/5] Setting branch to main...
git branch -M main

echo.
echo ========================================
echo NEXT STEPS:
echo ========================================
echo.
echo 1. Create GitHub repository:
echo    - Go to: https://github.com/new
echo    - Name: stocksense-ai
echo    - Description: Advanced AI Market Intelligence
echo    - Public repository
echo    - Click "Create repository"
echo.
echo 2. Copy the git remote add command from GitHub
echo    Example: git remote add origin https://github.com/YOUR_USERNAME/stocksense-ai.git
echo.
echo 3. Run: git push -u origin main
echo.
echo 4. Deploy on Render.com:
echo    - Go to: https://render.com
echo    - Sign up with GitHub
echo    - New + → Web Service
echo    - Select: stocksense-ai
echo    - Click: Create Web Service
echo.
echo ========================================
echo Your app will be live at:
echo https://stocksense-ai.onrender.com
echo ========================================
pause
