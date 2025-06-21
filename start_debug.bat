@echo off
echo Starting Expense Tracker Application in Debug Mode...

REM Install required packages
echo Installing required packages...
cd backend
pip install -r requirements.txt
cd ..

REM Start the Flask backend in a new window
echo Starting backend server...
start cmd /k "cd backend && python app.py"

REM Wait for backend to start
echo Waiting for backend to start...
timeout /t 5

REM Test the API
echo Testing API endpoints...
start cmd /k "cd backend && python test_api.py"

REM Wait for API test to complete
timeout /t 2

REM Start the React frontend in a new window
echo Starting frontend server...
start cmd /k "npm start"

echo Both backend and frontend servers are starting...
echo Backend: http://localhost:5000
echo Frontend: http://localhost:3000
echo.
echo DEBUGGING INSTRUCTIONS:
echo 1. Open browser developer tools (F12)
echo 2. Check the console for API request logs
echo 3. Verify that category filter is being passed correctly
echo 4. If issues persist, refer to CATEGORY_FILTER_FIX.md