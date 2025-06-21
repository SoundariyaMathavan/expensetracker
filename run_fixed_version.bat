@echo off
echo ===================================================
echo FIXED EXPENSE TRACKER DASHBOARD
echo ===================================================
echo.
echo This script will:
echo 1. Install required Python packages
echo 2. Copy the fixed files to the main files
echo 3. Start the backend server
echo 4. Start the frontend
echo.
echo ===================================================

echo.
echo Step 1: Installing required Python packages...
pip install flask flask-cors pandas numpy matplotlib seaborn requests

echo.
echo Step 2: Copying the fixed files...
copy /Y frontend\src\FixedDashboard.js frontend\src\dashboard.js
copy /Y frontend\src\App_fixed.js frontend\src\App.js
copy /Y backend\fixed_server.py backend\app.py

echo.
echo Step 3: Testing if backend server is already running...
python backend\check_server.py
if %ERRORLEVEL% NEQ 0 (
    echo Backend server is not running. Starting it now...
    start cmd /k "cd backend && python fixed_server.py"
) else (
    echo Backend server is already running.
)

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
echo If you encounter the "Failed to fetch" error:
echo 1. Make sure the backend server is running
echo 2. Check if there are any error messages in the backend console
echo 3. Try restarting both servers
echo ===================================================@echo off
echo ===================================================
echo FIXED EXPENSE TRACKER DASHBOARD
echo ===================================================
echo.
echo This script will:
echo 1. Install required Python packages
echo 2. Copy the fixed files to the main files
echo 3. Start the backend server
echo 4. Start the frontend
echo.
echo ===================================================

echo.
echo Step 1: Installing required Python packages...
pip install flask flask-cors pandas numpy matplotlib seaborn requests

echo.
echo Step 2: Copying the fixed files...
copy /Y frontend\src\FixedDashboard.js frontend\src\dashboard.js
copy /Y frontend\src\App_fixed.js frontend\src\App.js
copy /Y backend\fixed_server.py backend\app.py

echo.
echo Step 3: Testing if backend server is already running...
python backend\check_server.py
if %ERRORLEVEL% NEQ 0 (
    echo Backend server is not running. Starting it now...
    start cmd /k "cd backend && python fixed_server.py"
) else (
    echo Backend server is already running.
)

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
echo If you encounter the "Failed to fetch" error:
echo 1. Make sure the backend server is running
echo 2. Check if there are any error messages in the backend console
echo 3. Try restarting both servers
echo ===================================================