import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import './dashboard.css';
import './simple-chart.css';

// API base URL - change this if your backend is running on a different port or host
const API_BASE_URL = 'http://localhost:5000';

function SimpleView() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [data, setData] = useState({
    summary: null,
    expenses: {},
    loading: true,
    error: null
  });
  
  const [category, setCategory] = useState(searchParams.get('category') || 'all');
  const [timePeriod, setTimePeriod] = useState(searchParams.get('period') || 'monthly');
  const [refreshCounter, setRefreshCounter] = useState(0);

  // Update URL when filters change
  useEffect(() => {
    if (category === 'all') {
      searchParams.delete('category');
    } else {
      searchParams.set('category', category);
    }
    searchParams.set('period', timePeriod);
    setSearchParams(searchParams);
  }, [category, timePeriod, searchParams, setSearchParams]);

  // Fetch data when component mounts or when filters change
  useEffect(() => {
    const fetchData = async () => {
      try {
        setData(prev => ({ ...prev, loading: true, error: null }));
        
        console.log(`Fetching data with category=${category}, timePeriod=${timePeriod}`);
        
        // Fetch summary data
        const summaryUrl = `${API_BASE_URL}/api/summary${
          category !== 'all' ? `?category=${category}` : ''
        }`;
        console.log('Fetching from:', summaryUrl);
        
        const summaryRes = await fetch(summaryUrl);
        if (!summaryRes.ok) {
          throw new Error(`Summary API returned status: ${summaryRes.status}`);
        }
        const summaryData = await summaryRes.json();
        
        // Fetch expenses data
        const expensesUrl = `${API_BASE_URL}/api/expenses?period=${timePeriod}${
          category !== 'all' ? `&category=${category}` : ''
        }`;
        console.log('Fetching from:', expensesUrl);
        
        const expensesRes = await fetch(expensesUrl);
        if (!expensesRes.ok) {
          throw new Error(`Expenses API returned status: ${expensesRes.status}`);
        }
        const expensesData = await expensesRes.json();
        
        console.log('Summary data:', summaryData);
        console.log('Expenses data:', expensesData);
        
        setData({
          summary: summaryData,
          expenses: expensesData.data || {},
          loading: false,
          error: null
        });
      } catch (err) {
        console.error('Error fetching data:', err);
        setData(prev => ({
          ...prev,
          loading: false,
          error: `Error fetching data: ${err.message}`
        }));
      }
    };
    
    fetchData();
  }, [category, timePeriod, refreshCounter]);
  
  // Handle category change
  const handleCategoryChange = (e) => {
    const newCategory = e.target.value;
    console.log(`Changing category from ${category} to ${newCategory}`);
    setCategory(newCategory);
  };
  
  // Handle time period change
  const handleTimePeriodChange = (e) => {
    const newPeriod = e.target.value;
    console.log(`Changing time period from ${timePeriod} to ${newPeriod}`);
    setTimePeriod(newPeriod);
  };
  
  // Force refresh data
  const handleRefresh = () => {
    console.log('Manually refreshing data...');
    setRefreshCounter(prev => prev + 1);
  };
  
  // Show loading state
  if (data.loading) {
    return (
      <div className="dashboard">
        <h1>Financial Insights Dashboard</h1>
        <div className="loading">Loading dashboard data...</div>
      </div>
    );
  }
  
  // Show error state
  if (data.error) {
    return (
      <div className="dashboard">
        <h1>Financial Insights Dashboard</h1>
        <div className="error">
          <h3>Error</h3>
          <p>{data.error}</p>
          <div className="error-help">
            <h4>Troubleshooting Steps:</h4>
            <ol>
              <li>Make sure the backend server is running at {API_BASE_URL}</li>
              <li>Check if you have the required Python packages installed:
                <pre>pip install flask flask-cors pandas numpy matplotlib seaborn</pre>
              </li>
              <li>Try running the backend with:
                <pre>python backend/expense_tracker.py</pre>
              </li>
              <li>Check if there are any error messages in the backend console</li>
            </ol>
          </div>
          <button onClick={handleRefresh} className="refresh-btn">Try Again</button>
        </div>
      </div>
    );
  }
  
  // Prepare data for rendering
  const totalSpending = data.summary?.stats?.total || 0;
  const avgDaily = data.summary?.stats?.avg_daily || 0;
  const maxWeekly = data.summary?.stats?.max_weekly || 0;
  const categories = data.summary?.categories || {};
  const recommendations = data.summary?.recommendations || [];
  const expensesData = data.expenses || {};
  
  return (
    <div className="dashboard">
      <h1>Financial Insights Dashboard</h1>
      
      <div className="filters">
        <select 
          value={timePeriod}
          onChange={handleTimePeriodChange}
          aria-label="Select time period"
        >
          <option value="daily">Daily View</option>
          <option value="weekly">Weekly View</option>
          <option value="monthly">Monthly View</option>
        </select>
        
        <select
          value={category}
          onChange={handleCategoryChange}
          aria-label="Select expense category"
        >
          <option value="all">All Categories</option>
          {Object.keys(categories).map(cat => (
            <option key={cat} value={cat}>{cat}</option>
          ))}
        </select>
      </div>
      
      <div className="stats-grid">
        <div className="stat-card">
          <h3>Total Spending</h3>
          <p>${totalSpending.toFixed(2)}</p>
          <span className="stat-period">
            {category !== 'all' ? `${category} category` : 'all categories'}
          </span>
        </div>
        <div className="stat-card">
          <h3>Daily Average</h3>
          <p>${avgDaily.toFixed(2)}</p>
          <span className="stat-period">per day</span>
        </div>
        <div className="stat-card">
          <h3>Max Weekly</h3>
          <p>${maxWeekly.toFixed(2)}</p>
          <span className="stat-period">highest week</span>
        </div>
      </div>
      
      <div className="charts-container">
        <div className="chart">
          <h2>
            {category !== 'all' 
              ? `${category} Spending Analysis` 
              : 'Category Breakdown'}
          </h2>
          {data.summary?.plot ? (
            <img 
              src={`data:image/png;base64,${data.summary.plot}`} 
              alt="Spending analysis" 
              className="analysis-plot"
            />
          ) : (
            <div className="no-data">No chart data available</div>
          )}
        </div>
        
        <div className="chart">
          <h2>
            {category !== 'all' 
              ? `${category} Trend Over Time` 
              : 'Expense Trend Over Time'}
          </h2>
          <div className="simple-chart">
            {Object.keys(expensesData).length > 0 ? (
              <div className="chart-container">
                <div className="chart-bars">
                  {Object.entries(expensesData).map(([period, amount]) => {
                    const maxAmount = Math.max(...Object.values(expensesData).map(val => parseFloat(val)));
                    const height = (parseFloat(amount) / maxAmount) * 100;
                    return (
                      <div key={period} className="chart-bar-container">
                        <div 
                          className="chart-bar" 
                          style={{ height: `${height}%` }}
                          title={`${period}: $${parseFloat(amount).toFixed(2)}`}
                        ></div>
                        <div className="chart-label">{period}</div>
                      </div>
                    );
                  })}
                </div>
              </div>
            ) : (
              <div className="no-data">No data available</div>
            )}
          </div>
        </div>
      </div>
      
      <div className="recommendations">
        <h2>Personalized Financial Insights</h2>
        {recommendations.length > 0 ? (
          <ul>
            {recommendations.map((rec, i) => (
              <li key={i} className={`priority-${rec.priority === 1 ? 'high' : rec.priority === 2 ? 'medium' : 'low'}`}>
                {rec.message}
              </li>
            ))}
          </ul>
        ) : (
          <p>No recommendations available</p>
        )}
      </div>
      
      <div className="debug-info">
        <h3>Debug Information</h3>
        <p><strong>Backend URL:</strong> {API_BASE_URL}</p>
        <p><strong>Selected Category:</strong> {category}</p>
        <p><strong>Selected Time Period:</strong> {timePeriod}</p>
        <p><strong>Total Spending:</strong> ${totalSpending.toFixed(2)}</p>
        <p><strong>Daily Average:</strong> ${avgDaily.toFixed(2)}</p>
        <p><strong>Max Weekly:</strong> ${maxWeekly.toFixed(2)}</p>
        <button onClick={handleRefresh} className="refresh-btn">Refresh Data</button>
      </div>
    </div>
  );
}

export default SimpleView;