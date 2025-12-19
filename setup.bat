@echo off
echo ====================================
echo Car Rental System - Quick Setup
echo ====================================
echo.

echo Step 1: Checking setup...
python check_setup.py
echo.

echo ====================================
echo Would you like to continue with installation?
echo ====================================
pause

echo.
echo Step 2: Installing dependencies...
pip install -r requirements.txt
echo.

echo Step 3: Checking MongoDB...
net start MongoDB 2>nul
if errorlevel 1 (
    echo MongoDB service not found. Please install MongoDB first.
    echo Download from: https://www.mongodb.com/try/download/community
    pause
    exit /b
)
echo MongoDB is running!
echo.

echo Step 4: Running migration...
python migrate.py
echo.

echo ====================================
echo Setup Complete!
echo ====================================
echo.
echo To start the application, run:
echo   python app_new.py
echo.
echo Then open browser: http://localhost:5000
echo.
pause
