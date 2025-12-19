@echo off
echo Starting Car Rental Management System...
echo.

REM Check if MongoDB is running
net start MongoDB 2>nul
if errorlevel 1 (
    echo Starting MongoDB service...
    net start MongoDB
)

echo MongoDB is running!
echo.
echo Starting Flask application...
echo.
echo Application will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

python app_new.py
