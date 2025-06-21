@echo off
echo ===================================================
echo RUNNING FIXED VERSION
echo ===================================================
echo.
echo This script will:
echo 1. Start the backend server with the fixed app.py
echo 2. Start the frontend
echo.
echo ===================================================

echo.
echo Step 1: Starting the backend server...
start cmd /k "cd backend && python app.py"

echo.
echo Step 2: Waiting for the backend to start...
timeout /t 5

echo.
echo Step 3: Starting the frontend...
start cmd /k "npm start"

echo.
echo ===================================================
echo Both servers should now be starting.
echo.
echo Backend: http://localhost:5000
echo Frontend: http://localhost:3000
echo.
echo This version has fixed the syntax errors in app.py
echo and ensures that all data is properly displayed.
echo ===================================================