import React, { useState, useEffect } from 'react';
import { Chart } from 'react-google-charts';
import './dashboard.css';

function Dashboard() {
  const [data, setData] = useState({
    summary: null,
    expenses: {},
    loading: true,
    error: null
  });
  const [filters, setFilters] = useState({
    timePeriod: 'monthly',
    category: 'all'
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        console.log('Fetching data with filters:', filters);
        setData(prev => ({ ...prev, loading: true, error: null }));
        
        // Log the URLs being fetched
        const summaryUrl = `http://localhost:5000/api/summary${
          filters.category !== 'all' ? `?category=${filters.category}` : ''
        }`;
        const expensesUrl = `http://localhost:5000/api/expenses?period=${filters.timePeriod}${
          filters.category !== 'all' ? `&category=${filters.category}` : ''
        }`;
        
        console.log('Fetching summary from:', summaryUrl);
        console.log('Fetching expenses from:', expensesUrl);
        
        const [summaryRes, expensesRes] = await Promise.all([
          fetch(summaryUrl).then(res => res.json()),
          fetch(expensesUrl).then(res => res.json())
        ]);

        console.log('Summary response:', summaryRes);
        console.log('Expenses response:', expensesRes);

        if (!summaryRes.success || !expensesRes.success) {
          throw new Error(summaryRes.error || expensesRes.error || 'Unknown error');
        }

        setData({
          summary: summaryRes,
          expenses: expensesRes.data,
          loading: false,
          error: null
        });
        
        console.log('Updated state data:', {
          summary: summaryRes,
          expenses: expensesRes.data
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
  }, [filters]);

  const prepareTimeChartData = () => {
    if (!data.expenses || Object.keys(data.expenses).length === 0) return null;
    
    return [
      ['Period', 'Amount'],
      ...Object.entries(data.expenses).map(([period, amount]) => [
        period, 
        parseFloat(amount)
      ])
    ];
  };

  const prepareGaugeData = () => {
    if (!data.summary) return null;
    
    const total = data.summary.stats.total;
    const avgDaily = data.summary.stats.avg_daily;
    const maxCategory = Math.max(...Object.values(data.summary.categories));
    
    return [
      ['Label', 'Value'],
      ['Total', total],
      ['Daily Avg', avgDaily],
      ['Max Category', maxCategory]
    ];
  };

  if (data.loading) return <div className="loading">Loading dashboard...</div>;
  if (data.error) return <div className="error">Error: {data.error}</div>;

  return (
    <div className="dashboard">
      <h1>Expense Tracker Dashboard</h1>
      
      <div className="filters">
        <select 
          value={filters.timePeriod}
          onChange={(e) => setFilters({...filters, timePeriod: e.target.value})}
        >
          <option value="daily">Daily</option>
          <option value="weekly">Weekly</option>
          <option value="monthly">Monthly</option>
        </select>
        
        <select
          value={filters.category}
          onChange={(e) => setFilters({...filters, category: e.target.value})}
        >
          <option value="all">All Categories</option>
          {data.summary?.categories && Object.keys(data.summary.categories).map(category => (
            <option key={category} value={category}>{category}</option>
          ))}
        </select>
      </div>
      
      <div className="stats-grid">
        <div className="stat-card">
          <h3>Total Spending</h3>
          <p>${data.summary?.stats?.total?.toFixed(2) || '0.00'}</p>
        </div>
        <div className="stat-card">
          <h3>Daily Average</h3>
          <p>${data.summary?.stats?.avg_daily?.toFixed(2) || '0.00'}</p>
        </div>
        <div className="stat-card">
          <h3>Max Weekly</h3>
          <p>${Math.max(...Object.values(data.summary?.weekly_data || {}).map(parseFloat)).toFixed(2) || '0.00'}</p>
        </div>
      </div>
      
      <div className="charts-container">
        <div className="chart">
          <h2>Spending Analysis</h2>
          {data.summary?.plot && (
            <img 
              src={`data:image/png;base64,${data.summary.plot}`} 
              alt="Spending analysis" 
              className="analysis-plot"
            />
          )}
        </div>
        
        <div className="chart">
          <h2>Trend Over Time</h2>
          <Chart
            width={'100%'}
            height={'300px'}
            chartType="LineChart"
            loader={<div>Loading chart...</div>}
            data={prepareTimeChartData()}
            options={{
              hAxis: { title: filters.timePeriod.toUpperCase() },
              vAxis: { title: 'Amount ($)' },
              legend: 'none'
            }}
          />
        </div>
        
        <div className="chart">
          <h2>Spending Metrics</h2>
          <Chart
            width={'100%'}
            height={'300px'}
            chartType="Gauge"
            loader={<div>Loading gauge...</div>}
            data={prepareGaugeData()}
            options={{
              redFrom: 90,
              redTo: 100,
              yellowFrom: 75,
              yellowTo: 90,
              minorTicks: 5
            }}
          />
        </div>
      </div>
      
      <div className="recommendations">
        <h2>Personalized Recommendations</h2>
        <ul>
          {data.summary?.recommendations?.map((rec, i) => (
            <li key={i} className={`priority-${rec.priority}`}>
              {rec.message}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default Dashboard;
