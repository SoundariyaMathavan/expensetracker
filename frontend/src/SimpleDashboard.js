import React, { useState, useEffect } from 'react';
import { Chart } from 'react-google-charts';
import './dashboard.css';

function SimpleDashboard() {
  const [data, setData] = useState({
    summary: null,
    expenses: {},
    loading: true,
    error: null
  });
  
  const [category, setCategory] = useState('all');
  const [timePeriod, setTimePeriod] = useState('monthly');
  const [refreshCounter, setRefreshCounter] = useState(0);

  // Fetch data when component mounts or when filters change
  useEffect(() => {
    const fetchData = async () => {
      try {
        setData(prev => ({ ...prev, loading: true, error: null }));
        
        console.log(`Fetching data with category=${category}, timePeriod=${timePeriod}`);
        
        // Fetch summary data
        const summaryUrl = `http://localhost:5000/api/summary${
          category !== 'all' ? `?category=${category}` : ''
        }`;
        console.log('Fetching from:', summaryUrl);
        
        const summaryRes = await fetch(summaryUrl);
        const summaryData = await summaryRes.json();
        
        // Fetch expenses data
        const expensesUrl = `http://localhost:5000/api/expenses?period=${timePeriod}${
          category !== 'all' ? `&category=${category}` : ''
        }`;
        console.log('Fetching from:', expensesUrl);
        
        const expensesRes = await fetch(expensesUrl);
        const expensesData = await expensesRes.json();
        
        console.log('Summary data:', summaryData);
        console.log('Expenses data:', expensesData);
        
        if (!summaryData.success || !expensesData.success) {
          throw new Error('API request failed');
        }
        
        setData({
          summary: summaryData,
          expenses: expensesData.data,
          loading: false,
          error: null
        });
      } catch (err) {
        console.error('Error fetching data:', err);
        setData({
          summary: null,
          expenses: {},
          loading: false,
          error: err.message
        });
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
  
  // Prepare time chart data
  const prepareTimeChartData = () => {
    if (!data.expenses || Object.keys(data.expenses).length === 0) {
      return [['Period', 'Amount'], ['No Data', 0]];
    }
    
    return [
      ['Period', 'Amount'],
      ...Object.entries(data.expenses).map(([period, amount]) => [
        period, 
        parseFloat(amount)
      ])
    ];
  };
  
  // Prepare gauge data
  const prepareGaugeData = () => {
    if (!data.summary) {
      return [['Label', 'Value'], ['No Data', 0]];
    }
    
    const total = data.summary.stats.total;
    const avgDaily = data.summary.stats.avg_daily;
    const maxCategory = Math.max(...Object.values(data.summary.categories || {}));
    
    return [
      ['Label', 'Value'],
      ['Total', total],
      ['Daily Avg', avgDaily],
      ['Max Category', maxCategory]
    ];
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
          Error loading data: {data.error}
          <button onClick={handleRefresh} className="refresh-btn">Try Again</button>
        </div>
      </div>
    );
  }
  
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
          {data.summary?.categories && Object.keys(data.summary.categories).map(cat => (
            <option key={cat} value={cat}>{cat}</option>
          ))}
        </select>
      </div>
      
      <div className="stats-grid">
        <div className="stat-card">
          <h3>Total Spending</h3>
          <p>${data.summary?.stats?.total?.toFixed(2) || '0.00'}</p>
          <span className="stat-period">
            {category !== 'all' ? `${category} category` : 'all categories'}
          </span>
        </div>
        <div className="stat-card">
          <h3>Daily Average</h3>
          <p>${data.summary?.stats?.avg_daily?.toFixed(2) || '0.00'}</p>
          <span className="stat-period">per day</span>
        </div>
        <div className="stat-card">
          <h3>Max Weekly</h3>
          <p>${data.summary?.stats?.max_weekly?.toFixed(2) || '0.00'}</p>
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
          {data.summary?.plot && (
            <img 
              src={`data:image/png;base64,${data.summary.plot}`} 
              alt="Spending analysis" 
              className="analysis-plot"
            />
          )}
        </div>
        
        <div className="chart">
          <h2>
            {category !== 'all' 
              ? `${category} Trend Over Time` 
              : 'Expense Trend Over Time'}
          </h2>
          <Chart
            width={'100%'}
            height={'300px'}
            chartType="LineChart"
            loader={<div className="chart-loading">Loading trend data...</div>}
            data={prepareTimeChartData()}
            options={{
              hAxis: { 
                title: timePeriod === 'daily' ? 'Day' : 
                       timePeriod === 'weekly' ? 'Week' : 'Month'
              },
              vAxis: { title: 'Amount ($)' },
              legend: 'none',
              colors: ['#3a7bd5'],
              lineWidth: 3,
              pointSize: 6,
              animation: {
                startup: true,
                duration: 1000,
                easing: 'out'
              },
              backgroundColor: 'transparent'
            }}
          />
        </div>
        
        <div className="chart">
          <h2>Spending Metrics</h2>
          <Chart
            width={'100%'}
            height={'300px'}
            chartType="Gauge"
            loader={<div className="chart-loading">Loading metrics...</div>}
            data={prepareGaugeData()}
            options={{
              redFrom: 90,
              redTo: 100,
              yellowFrom: 75,
              yellowTo: 90,
              minorTicks: 5,
              animation: {
                duration: 1000,
                easing: 'out'
              }
            }}
          />
        </div>
      </div>
      
      <div className="recommendations">
        <h2>Personalized Financial Insights</h2>
        <ul>
          {data.summary?.recommendations?.map((rec, i) => (
            <li key={i} className={`priority-${rec.priority === 1 ? 'high' : rec.priority === 2 ? 'medium' : 'low'}`}>
              {rec.message}
            </li>
          ))}
        </ul>
      </div>
      
      <div className="debug-info">
        <h3>Debug Information</h3>
        <p><strong>Selected Category:</strong> {category}</p>
        <p><strong>Selected Time Period:</strong> {timePeriod}</p>
        <p><strong>Total Spending:</strong> ${data.summary?.stats?.total?.toFixed(2) || '0.00'}</p>
        <p><strong>Daily Average:</strong> ${data.summary?.stats?.avg_daily?.toFixed(2) || '0.00'}</p>
        <p><strong>Max Weekly:</strong> ${data.summary?.stats?.max_weekly?.toFixed(2) || '0.00'}</p>
        <button onClick={handleRefresh} className="refresh-btn">Refresh Data</button>
      </div>
    </div>
  );
}

export default SimpleDashboard;import React, { useState, useEffect } from 'react';
import { Chart } from 'react-google-charts';
import './dashboard.css';

function SimpleDashboard() {
  const [data, setData] = useState({
    summary: null,
    expenses: {},
    loading: true,
    error: null
  });
  
  const [category, setCategory] = useState('all');
  const [timePeriod, setTimePeriod] = useState('monthly');
  const [refreshCounter, setRefreshCounter] = useState(0);

  // Fetch data when component mounts or when filters change
  useEffect(() => {
    const fetchData = async () => {
      try {
        setData(prev => ({ ...prev, loading: true, error: null }));
        
        console.log(`Fetching data with category=${category}, timePeriod=${timePeriod}`);
        
        // Fetch summary data
        const summaryUrl = `http://localhost:5000/api/summary${
          category !== 'all' ? `?category=${category}` : ''
        }`;
        console.log('Fetching from:', summaryUrl);
        
        const summaryRes = await fetch(summaryUrl);
        const summaryData = await summaryRes.json();
        
        // Fetch expenses data
        const expensesUrl = `http://localhost:5000/api/expenses?period=${timePeriod}${
          category !== 'all' ? `&category=${category}` : ''
        }`;
        console.log('Fetching from:', expensesUrl);
        
        const expensesRes = await fetch(expensesUrl);
        const expensesData = await expensesRes.json();
        
        console.log('Summary data:', summaryData);
        console.log('Expenses data:', expensesData);
        
        if (!summaryData.success || !expensesData.success) {
          throw new Error('API request failed');
        }
        
        setData({
          summary: summaryData,
          expenses: expensesData.data,
          loading: false,
          error: null
        });
      } catch (err) {
        console.error('Error fetching data:', err);
        setData({
          summary: null,
          expenses: {},
          loading: false,
          error: err.message
        });
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
  
  // Prepare time chart data
  const prepareTimeChartData = () => {
    if (!data.expenses || Object.keys(data.expenses).length === 0) {
      return [['Period', 'Amount'], ['No Data', 0]];
    }
    
    return [
      ['Period', 'Amount'],
      ...Object.entries(data.expenses).map(([period, amount]) => [
        period, 
        parseFloat(amount)
      ])
    ];
  };
  
  // Prepare gauge data
  const prepareGaugeData = () => {
    if (!data.summary) {
      return [['Label', 'Value'], ['No Data', 0]];
    }
    
    const total = data.summary.stats.total;
    const avgDaily = data.summary.stats.avg_daily;
    const maxCategory = Math.max(...Object.values(data.summary.categories || {}));
    
    return [
      ['Label', 'Value'],
      ['Total', total],
      ['Daily Avg', avgDaily],
      ['Max Category', maxCategory]
    ];
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
          Error loading data: {data.error}
          <button onClick={handleRefresh} className="refresh-btn">Try Again</button>
        </div>
      </div>
    );
  }
  
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
          {data.summary?.categories && Object.keys(data.summary.categories).map(cat => (
            <option key={cat} value={cat}>{cat}</option>
          ))}
        </select>
      </div>
      
      <div className="stats-grid">
        <div className="stat-card">
          <h3>Total Spending</h3>
          <p>${data.summary?.stats?.total?.toFixed(2) || '0.00'}</p>
          <span className="stat-period">
            {category !== 'all' ? `${category} category` : 'all categories'}
          </span>
        </div>
        <div className="stat-card">
          <h3>Daily Average</h3>
          <p>${data.summary?.stats?.avg_daily?.toFixed(2) || '0.00'}</p>
          <span className="stat-period">per day</span>
        </div>
        <div className="stat-card">
          <h3>Max Weekly</h3>
          <p>${data.summary?.stats?.max_weekly?.toFixed(2) || '0.00'}</p>
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
          {data.summary?.plot && (
            <img 
              src={`data:image/png;base64,${data.summary.plot}`} 
              alt="Spending analysis" 
              className="analysis-plot"
            />
          )}
        </div>
        
        <div className="chart">
          <h2>
            {category !== 'all' 
              ? `${category} Trend Over Time` 
              : 'Expense Trend Over Time'}
          </h2>
          <Chart
            width={'100%'}
            height={'300px'}
            chartType="LineChart"
            loader={<div className="chart-loading">Loading trend data...</div>}
            data={prepareTimeChartData()}
            options={{
              hAxis: { 
                title: timePeriod === 'daily' ? 'Day' : 
                       timePeriod === 'weekly' ? 'Week' : 'Month'
              },
              vAxis: { title: 'Amount ($)' },
              legend: 'none',
              colors: ['#3a7bd5'],
              lineWidth: 3,
              pointSize: 6,
              animation: {
                startup: true,
                duration: 1000,
                easing: 'out'
              },
              backgroundColor: 'transparent'
            }}
          />
        </div>
        
        <div className="chart">
          <h2>Spending Metrics</h2>
          <Chart
            width={'100%'}
            height={'300px'}
            chartType="Gauge"
            loader={<div className="chart-loading">Loading metrics...</div>}
            data={prepareGaugeData()}
            options={{
              redFrom: 90,
              redTo: 100,
              yellowFrom: 75,
              yellowTo: 90,
              minorTicks: 5,
              animation: {
                duration: 1000,
                easing: 'out'
              }
            }}
          />
        </div>
      </div>
      
      <div className="recommendations">
        <h2>Personalized Financial Insights</h2>
        <ul>
          {data.summary?.recommendations?.map((rec, i) => (
            <li key={i} className={`priority-${rec.priority === 1 ? 'high' : rec.priority === 2 ? 'medium' : 'low'}`}>
              {rec.message}
            </li>
          ))}
        </ul>
      </div>
      
      <div className="debug-info">
        <h3>Debug Information</h3>
        <p><strong>Selected Category:</strong> {category}</p>
        <p><strong>Selected Time Period:</strong> {timePeriod}</p>
        <p><strong>Total Spending:</strong> ${data.summary?.stats?.total?.toFixed(2) || '0.00'}</p>
        <p><strong>Daily Average:</strong> ${data.summary?.stats?.avg_daily?.toFixed(2) || '0.00'}</p>
        <p><strong>Max Weekly:</strong> ${data.summary?.stats?.max_weekly?.toFixed(2) || '0.00'}</p>
        <button onClick={handleRefresh} className="refresh-btn">Refresh Data</button>
      </div>
    </div>
  );
}

export default SimpleDashboard;