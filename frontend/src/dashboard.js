import React, { useState, useEffect } from 'react';
import { Chart } from 'react-google-charts';
import { useSearchParams } from 'react-router-dom';
import './dashboard.css';

function Dashboard() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [data, setData] = useState({
    summary: null,
    expenses: {},
    loading: true,
    error: null
  });
  
  // Initialize filters from URL parameters or defaults
  const [filters, setFilters] = useState({
    timePeriod: searchParams.get('period') || 'monthly',
    category: searchParams.get('category') || 'all'
  });

  // Update filters when URL parameters change
  useEffect(() => {
    const periodParam = searchParams.get('period');
    const categoryParam = searchParams.get('category');
    
    const newFilters = { ...filters };
    if (periodParam) newFilters.timePeriod = periodParam;
    if (categoryParam) newFilters.category = categoryParam;
    
    setFilters(newFilters);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [searchParams]);

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

  // Removed gauge data preparation function

  if (data.loading) return <div className="loading">Loading dashboard...</div>;
  if (data.error) return <div className="error">Error: {data.error}</div>;

  return (
    <div className="dashboard">
      <h1>Expense Tracker Dashboard</h1>
      
      <div className="filters">
        <select 
          value={filters.timePeriod}
          onChange={(e) => {
            const newTimePeriod = e.target.value;
            setFilters({...filters, timePeriod: newTimePeriod});
            
            // Update URL parameters
            searchParams.set('period', newTimePeriod);
            setSearchParams(searchParams);
          }}
        >
          <option value="daily">Daily</option>
          <option value="weekly">Weekly</option>
          <option value="monthly">Monthly</option>
        </select>
        
        <select
          value={filters.category}
          onChange={(e) => {
            const newCategory = e.target.value;
            setFilters({...filters, category: newCategory});
            
            // Update URL parameters
            if (newCategory === 'all') {
              searchParams.delete('category');
            } else {
              searchParams.set('category', newCategory);
            }
            setSearchParams(searchParams);
          }}
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
        <div className="chart big-chart">
          <h2>Spending Analysis</h2>
          {data.summary?.plot && (
            <img 
              src={`data:image/png;base64,${data.summary.plot}`} 
              alt="Spending analysis" 
              className="analysis-plot semi-circle-chart"
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
