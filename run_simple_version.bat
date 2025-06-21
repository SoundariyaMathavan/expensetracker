@echo off
echo Starting the simplified version of the Expense Tracker...

echo.
echo Step 1: Copying the simplified files to the main files...
copy /Y frontend\src\SimpleDashboard.js frontend\src\dashboard.js
copy /Y frontend\src\App_simple.js frontend\src\App.js
copy /Y backend\simple_app.py backend\app.py

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
echo Both servers should now be starting.
echo.
echo Backend: http://localhost:5000
echo Frontend: http://localhost:3000
echo.
echo IMPORTANT: When testing the dashboard, check that ALL components update when changing categories:
echo - Total Spending
echo - Daily Average
echo - Max Weekly
echo - Spending Analysis chart
echo - Trend Over Time chart
echo - Recommendations
echo.
echo If you encounter any issues, check the debug section at the bottom of the dashboard.
echo.@echo off
echo Starting the simplified version of the Expense Tracker...

echo.
echo Step 1: Copying the simplified files to the main files...
copy /Y frontend\src\SimpleDashboard.js frontend\src\dashboard.js
copy /Y frontend\src\App_simple.js frontend\src\App.js
copy /Y backend\simple_app.py backend\app.py

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
echo Both servers should now be starting.
echo.
echo Backend: http://localhost:5000
echo Frontend: http://localhost:3000
echo.
echo IMPORTANT: When testing the dashboard, check that ALL components update when changing categories:
echo - Total Spending
echo - Daily Average
echo - Max Weekly
echo - Spending Analysis chart
echo - Trend Over Time chart
echo - Recommendations
echo.
echo If you encounter any issues, check the debug section at the bottom of the dashboard.
echo.