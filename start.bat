@echo off
echo Starting Expense Tracker Application...

REM Activate virtual environment
call venv\Scripts\activate

REM Install Flask-CORS if not already installed
pip install flask-cors

REM Start the Flask backend in a new window
start cmd /k "cd backend && python app.py"

REM Wait for backend to start
timeout /t 5

REM Start the React frontend in a new window
start cmd /k "npm start"

echo Both backend and frontend servers are starting...
echo Backend: http://localhost:5000
echo Frontend: http://localhost:3000