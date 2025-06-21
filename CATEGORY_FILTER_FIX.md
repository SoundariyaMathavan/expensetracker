# Fixing Category Filter Issue

If you're experiencing an issue where only the "Trend Over Time" chart updates when changing categories, but other visualizations don't change, follow these steps to fix it:

## 1. Check Frontend API Calls

Make sure your frontend is passing the category parameter to the summary endpoint:

```javascript
// In dashboard.js
const [summaryRes, expensesRes] = await Promise.all([
  fetch(`http://localhost:5000/api/summary${
    filters.category !== 'all' ? `?category=${filters.category}` : ''
  }`).then(res => res.json()),
  fetch(`http://localhost:5000/api/expenses?period=${filters.timePeriod}${
    filters.category !== 'all' ? `&category=${filters.category}` : ''
  }`).then(res => res.json())
]);
```

## 2. Check Backend API Implementation

Ensure your backend is properly handling the category parameter:

```python
# In app.py
@app.route('/api/summary', methods=['GET'])
def get_summary():
    # Get category filter from request parameters
    category = request.args.get('category', 'all')
    
    # Convert sample data to DataFrame
    df = pd.DataFrame(SAMPLE_DATA)
    df['date'] = pd.to_datetime(df['date'])
    df['amount'] = df['amount'].astype(float)
    
    # Filter by category if specified
    original_df = df.copy()  # Keep a copy of the original data for category breakdown
    if category != 'all':
        df = df[df['category'] == category]
    
    # Rest of the function...
```

## 3. Test the API Directly

Run the test_api.py script to verify that the backend is working correctly:

```
python backend/test_api.py
```

Check that the responses change when different category parameters are provided.

## 4. Check Browser Network Requests

1. Open your browser's developer tools (F12 or right-click > Inspect)
2. Go to the Network tab
3. Change the category filter in the dashboard
4. Look for requests to `/api/summary` and verify that:
   - The category parameter is being included in the URL
   - The response data changes based on the selected category

## 5. Clear Browser Cache

Sometimes browser caching can cause issues:

1. Open developer tools (F12)
2. Right-click on the refresh button
3. Select "Empty Cache and Hard Reload"

## 6. Restart Servers

1. Stop both the frontend and backend servers
2. Start the backend server:
   ```
   cd backend
   python app.py
   ```
3. Start the frontend server (in a separate terminal):
   ```
   npm start
   ```

## 7. Check for CORS Issues

Make sure CORS is properly enabled in your Flask app:

```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
```

And install the required package:
```
pip install flask-cors
```

## 8. Debug Mode

If the issue persists, add console logs to debug:

```javascript
// In dashboard.js
useEffect(() => {
  const fetchData = async () => {
    try {
      console.log('Fetching data with filters:', filters);
      // Rest of the function...
      
      console.log('Summary response:', summaryRes);
      console.log('Expenses response:', expensesRes);
      
      // Rest of the function...
    } catch (err) {
      console.error('Error fetching data:', err);
      // Rest of the function...
    }
  };

  fetchData();
}, [filters]);
```

Check the browser console for these logs to see if the data is changing correctly.