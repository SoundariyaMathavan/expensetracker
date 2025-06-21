from flask import Flask, jsonify, request
import pandas as pd
import numpy as np
import os
import json
from datetime import datetime, timedelta
import base64
import matplotlib
matplotlib.use('Agg')  # Must be before other matplotlib imports
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from flask_cors import CORS
import warnings

# Filter out UserWarnings
warnings.filterwarnings("ignore", category=UserWarning)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Sample data for demonstration
def generate_sample_data():
    # Generate dates for the last 30 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Categories
    categories = ['Food', 'Transport', 'Entertainment', 'Utilities', 'Shopping']
    
    # Generate random expenses
    expenses = []
    for date in dates:
        # Generate 1-3 expenses per day
        num_expenses = np.random.randint(1, 4)
        for _ in range(num_expenses):
            category = np.random.choice(categories)
            amount = round(np.random.uniform(10, 100), 2)
            expenses.append({
                'date': date.strftime('%Y-%m-%d'),
                'category': category,
                'amount': amount,
                'description': f"{category} expense"
            })
    
    return expenses

# Sample data
SAMPLE_DATA = generate_sample_data()

@app.route('/api/summary', methods=['GET'])
def get_summary():
    try:
        print("Summary endpoint called with args:", request.args)
        # Convert sample data to DataFrame
        df = pd.DataFrame(SAMPLE_DATA)
        df['date'] = pd.to_datetime(df['date'])
        df['amount'] = df['amount'].astype(float)
        
        # Get category from request args
        category = request.args.get('category', 'all')
        
        # Filter by category if specified
        if category != 'all':
            print(f"Filtering data for category: {category}")
            df = df[df['category'] == category]
            print(f"Filtered data has {len(df)} rows")
        
        # Calculate statistics
        total = df['amount'].sum()
        print(f"Total amount: {total}")
        
        # Calculate daily average
        avg_daily = df.groupby(df['date'].dt.date)['amount'].sum().mean()
        print(f"Daily average: {avg_daily}")
        
        # Calculate category totals (from unfiltered data)
        category_totals = pd.DataFrame(SAMPLE_DATA).groupby('category')['amount'].sum().to_dict()
        
        # Calculate weekly data from filtered data
        df['week'] = df['date'].dt.strftime('%U')
        weekly_data = df.groupby('week')['amount'].sum().to_dict()
        max_weekly = max(weekly_data.values()) if weekly_data else 0
        
        # Generate plot
        plt.figure(figsize=(10, 6))
        sns.set_style("darkgrid")
        
        if not df.empty:
            plot_df = df.groupby('category')['amount'].sum().reset_index()
            if not plot_df.empty:
                sns.barplot(x='category', y='amount', data=plot_df)
            else:
                plt.text(0.5, 0.5, 'No data available', 
                         ha='center', va='center', fontsize=12)
        else:
            plt.text(0.5, 0.5, 'No data available', 
                     ha='center', va='center', fontsize=12)
        
        plt.title('Expenses by Category')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Save plot to buffer
        buffer = BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        plot_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
        plt.close()
        
        # Generate recommendations
        recommendations = [
            {"message": "You're spending too much on Entertainment", "priority": 1},
            {"message": "Your Food expenses are within budget", "priority": 3},
            {"message": "Consider reducing Shopping expenses", "priority": 2}
        ]
        
        response = {
            "success": True,
            "stats": {
                "total": float(total),  # Convert numpy types to native Python
                "avg_daily": float(avg_daily),
                "max_weekly": float(max_weekly)
            },
            "categories": category_totals,
            "weekly_data": weekly_data,
            "plot": plot_data,
            "recommendations": recommendations,
            "selected_category": category
        }
        
        print(f"Response stats: {response['stats']}")
        return jsonify(response)
    
    except Exception as e:
        print(f"Error in summary endpoint: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/expenses', methods=['GET'])
def get_expenses():
    try:
        period = request.args.get('period', 'monthly')
        category = request.args.get('category', 'all')
        
        # Convert sample data to DataFrame
        df = pd.DataFrame(SAMPLE_DATA)
        df['date'] = pd.to_datetime(df['date'])
        df['amount'] = df['amount'].astype(float)
        
        # Filter by category if specified
        if category != 'all':
            df = df[df['category'] == category]
        
        # Group by period
        if period == 'daily':
            df['period'] = df['date'].dt.strftime('%Y-%m-%d')
        elif period == 'weekly':
            df['period'] = df['date'].dt.strftime('%Y-W%U')
        else:  # monthly
            df['period'] = df['date'].dt.strftime('%Y-%m')
        
        # Calculate totals by period
        period_totals = df.groupby('period')['amount'].sum().to_dict()
        
        # Prepare the response
        response = {
            "success": True,
            "data": {k: float(v) for k, v in period_totals.items()},  # Convert numpy types
            "selected_category": category,
            "selected_period": period
        }
        
        print(f"Expenses endpoint called with period={period}, category={category}")
        print(f"Expenses response: {response}")
        return jsonify(response)
    
    except Exception as e:
        print(f"Error in expenses endpoint: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/test', methods=['GET'])
def test_api():
    return jsonify({
        "success": True,
        "message": "API is working correctly",
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

if __name__ == '__main__':
    print("Starting Flask server...")
    print("API endpoints:")
    print("  - /api/summary - Get summary statistics and visualizations")
    print("  - /api/expenses - Get expense data by period")
    print("  - /api/test - Test if the API is working")
    app.run(debug=True, host='0.0.0.0', port=5000)