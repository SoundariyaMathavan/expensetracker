@echo off
echo ===================================================
echo RUNNING FINAL FIXED VERSION
echo ===================================================
echo.
echo This script will:
echo 1. Copy the final fixed backend file to app.py
echo 2. Start the backend server
echo 3. Start the frontend
echo.
echo ===================================================

echo.
echo Step 1: Copying the final fixed backend file...
copy /Y backend\app_final_fix.py backend\app.py

echo.
echo Step 2: Starting the backend server...
start cmd /k "cd backend && python app.py"

echo.
echo Step 3: Waiting for the backend to start...
timeout /t 5

echo.
echo Step 4: Starting the frontend...
start cmd /k "npm start"

echo.
echo ===================================================
echo Both servers should now be starting.
echo.
echo Backend: http://localhost:5000
echo Frontend: http://localhost:3000
echo.
echo If you encounter any issues, please check the console output
echo for error messages.
echo ===================================================