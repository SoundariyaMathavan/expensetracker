# Troubleshooting Guide

## Common Errors and Solutions

### 1. "Failed to fetch" Error

This error occurs when your React frontend cannot connect to the Flask backend.

**Possible causes and solutions:**

#### Backend Server Not Running
- Make sure your Flask backend is running on http://localhost:5000
- Run the backend server: `cd backend && python app.py`
- Check if the server is running by opening http://localhost:5000/api/summary in your browser

#### CORS Issues
- Install Flask-CORS: `pip install flask-cors`
- Make sure CORS is enabled in your Flask app:
  ```python
  from flask_cors import CORS
  app = Flask(__name__)
  CORS(app)  # Enable CORS for all routes
  ```

#### Network/Firewall Issues
- Check if port 5000 is blocked by your firewall
- Try changing the port in your Flask app:
  ```python
  app.run(debug=True, host='0.0.0.0', port=8000)
  ```
  And update the frontend fetch URLs accordingly:
  ```javascript
  fetch('http://localhost:8000/api/summary')
  ```

### 2. Seaborn Style Error

If you encounter: `'seaborn' is not a valid package style...`

**Solution:**
- Replace `plt.style.use('seaborn')` with `sns.set_style("darkgrid")`
- Or use a valid style name: `plt.style.use('seaborn-v0_8-darkgrid')`

### 3. Missing Dependencies

If you're missing dependencies:

**Solution:**
- Activate your virtual environment:
  ```
  venv\Scripts\activate  # Windows
  source venv/bin/activate  # Mac/Linux
  ```
- Install all requirements:
  ```
  pip install -r requirements.txt
  ```
- Install additional packages if needed:
  ```
  pip install flask-cors
  ```

## Starting the Application

For convenience, you can use the `start.bat` script (Windows) to start both the backend and frontend:

```
start.bat
```

Or start them manually:

1. Start the backend:
   ```
   cd backend
   python app.py
   ```

2. Start the frontend (in a separate terminal):
   ```
   npm start
   ```

## Testing the API

You can test the backend API directly using your browser or tools like Postman:

- Summary endpoint: http://localhost:5000/api/summary
- Expenses endpoint: http://localhost:5000/api/expenses?period=monthly&category=all