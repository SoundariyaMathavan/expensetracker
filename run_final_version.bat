@echo off
echo ===================================================
echo RUNNING FINAL VERSION (NO GOOGLE CHARTS)
echo ===================================================
echo.
echo This script will:
echo 1. Copy the final fixed backend file to app.py
echo 2. Copy the final frontend files
echo 3. Start the backend server
echo 4. Start the frontend
echo.
echo ===================================================

echo.
echo Step 1: Copying the final fixed backend file...
copy /Y backend\app_final_fix.py backend\app.py

echo.
echo Step 2: Copying the final frontend files...
copy /Y frontend\src\FinalDashboard.js frontend\src\dashboard.js
copy /Y frontend\src\App_final.js frontend\src\App.js
copy /Y frontend\src\simple-chart.css frontend\src\simple-chart.css

echo.
echo Step 3: Starting the backend server...
start cmd /k "cd backend && python app.py"

echo.
echo Step 4: Waiting for the backend to start...
timeout /t 5

echo.
echo Step 5: Starting the frontend...
start cmd /k "npm start"

echo.
echo ===================================================
echo Both servers should now be starting.
echo.
echo Backend: http://localhost:5000
echo Frontend: http://localhost:3000
echo.
echo This version uses a simple HTML/CSS chart instead of Google Charts
echo to avoid the "Cannot read properties of undefined" error.
echo ===================================================