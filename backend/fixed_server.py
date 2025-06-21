from flask import Flask, jsonify, request
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import base64
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from flask_cors import CORS

app = Flask(__name__)
# Enable CORS for all routes and all origins
CORS(app, resources={r"/*": {"origins": "*"}})

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

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "ok",
        "message": "Expense Tracker API is running"
    })

@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({
        "success": True,
        "message": "API is working correctly",
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

@app.route('/api/summary', methods=['GET'])
def get_summary():
    # Get category filter from request parameters
    category = request.args.get('category', 'all')
    print(f"Summary API called with category: {category}")
    
    # Convert sample data to DataFrame
    df = pd.DataFrame(SAMPLE_DATA)
    df['date'] = pd.to_datetime(df['date'])
    df['amount'] = df['amount'].astype(float)
    
    # Keep a copy of the original data
    original_df = df.copy()
    
    # Filter by category if specified
    if category != 'all':
        df = df[df['category'] == category]
        print(f"Filtered to {len(df)} rows for category: {category}")
    
    # Calculate statistics based on filtered data
    total = df['amount'].sum()
    avg_daily = df.groupby(df['date'].dt.date)['amount'].sum().mean()
    
    # Calculate weekly data from filtered data
    df['week'] = df['date'].dt.strftime('%U')
    weekly_data = df.groupby('week')['amount'].sum().to_dict()
    max_weekly = max(weekly_data.values()) if weekly_data else 0
    
    # Calculate category totals (from original data)
    category_totals = original_df.groupby('category')['amount'].sum().to_dict()
    
    # Generate plot
    plt.figure(figsize=(10, 6))
    sns.set_style("darkgrid")
    
    if category != 'all':
        # If a category is selected, show time trend for that category
        time_data = df.groupby(df['date'].dt.to_period('M'))['amount'].sum().reset_index()
        time_data['date'] = time_data['date'].astype(str)
        sns.barplot(x='date', y='amount', data=time_data)
        plt.title(f'{category} Expenses Over Time')
    else:
        # If no category is selected, show category breakdown
        category_data = original_df.groupby('category')['amount'].sum().reset_index()
        sns.barplot(x='category', y='amount', data=category_data)
        plt.title('Expenses by Category')
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Save plot to a base64 string
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()
    
    # Generate recommendations
    recommendations = []
    if category != 'all':
        cat_total = df['amount'].sum()
        total_expenses = original_df['amount'].sum()
        cat_pct = (cat_total / total_expenses) * 100 if total_expenses > 0 else 0
        
        if cat_pct > 30:
            recommendations.append({
                "message": f"Your {category} spending is {cat_pct:.1f}% of total expenses. Consider reducing this category.",
                "priority": 1
            })
        elif cat_pct < 10:
            recommendations.append({
                "message": f"You're doing well controlling {category} expenses ({cat_pct:.1f}% of total).",
                "priority": 3
            })
        else:
            recommendations.append({
                "message": f"{category} spending is {cat_pct:.1f}% of your total budget.",
                "priority": 2
            })
    else:
        top_category = max(category_totals.items(), key=lambda x: x[1]) if category_totals else ('None', 0)
        top_pct = (top_category[1] / total) * 100 if total > 0 else 0
        
        if top_pct > 40:
            recommendations.append({
                "message": f"Your spending on {top_category[0]} is {top_pct:.1f}% of total expenses. Consider reducing this category.",
                "priority": 1
            })
        
        recommendations.append({
            "message": "Try to keep individual categories under 30% of your total budget.",
            "priority": 2
        })
        
        recommendations.append({
            "message": "Consider setting up automatic savings for 20% of your income.",
            "priority": 3
        })
    
    # Prepare response
    response = {
        "success": True,
        "stats": {
            "total": total,
            "avg_daily": avg_daily,
            "max_weekly": max_weekly
        },
        "categories": category_totals,
        "weekly_data": weekly_data,
        "plot": plot_data,
        "recommendations": recommendations,
        "selected_category": category
    }
    
    print(f"Summary response stats: total={total}, avg_daily={avg_daily}, max_weekly={max_weekly}")
    return jsonify(response)

@app.route('/api/expenses', methods=['GET'])
def get_expenses():
    period = request.args.get('period', 'monthly')
    category = request.args.get('category', 'all')
    
    print(f"Expenses API called with period={period}, category={category}")
    
    # Convert sample data to DataFrame
    df = pd.DataFrame(SAMPLE_DATA)
    df['date'] = pd.to_datetime(df['date'])
    
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
    
    response = {
        "success": True,
        "data": period_totals,
        "selected_category": category,
        "selected_period": period
    }
    
    return jsonify(response)

if __name__ == '__main__':
    print("="*50)
    print("Starting Expense Tracker API Server")
    print("="*50)
    print("API Endpoints:")
    print("  - /api/test - Test if the API is working")
    print("  - /api/summary - Get summary statistics and visualizations")
    print("  - /api/expenses - Get expense data by period")
    print("="*50)
    print("Server will be available at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print("="*50)
    app.run(debug=True, host='0.0.0.0', port=5000)from flask import Flask, jsonify, request
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import base64
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from flask_cors import CORS

app = Flask(__name__)
# Enable CORS for all routes and all origins
CORS(app, resources={r"/*": {"origins": "*"}})

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

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "ok",
        "message": "Expense Tracker API is running"
    })

@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({
        "success": True,
        "message": "API is working correctly",
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

@app.route('/api/summary', methods=['GET'])
def get_summary():
    # Get category filter from request parameters
    category = request.args.get('category', 'all')
    print(f"Summary API called with category: {category}")
    
    # Convert sample data to DataFrame
    df = pd.DataFrame(SAMPLE_DATA)
    df['date'] = pd.to_datetime(df['date'])
    df['amount'] = df['amount'].astype(float)
    
    # Keep a copy of the original data
    original_df = df.copy()
    
    # Filter by category if specified
    if category != 'all':
        df = df[df['category'] == category]
        print(f"Filtered to {len(df)} rows for category: {category}")
    
    # Calculate statistics based on filtered data
    total = df['amount'].sum()
    avg_daily = df.groupby(df['date'].dt.date)['amount'].sum().mean()
    
    # Calculate weekly data from filtered data
    df['week'] = df['date'].dt.strftime('%U')
    weekly_data = df.groupby('week')['amount'].sum().to_dict()
    max_weekly = max(weekly_data.values()) if weekly_data else 0
    
    # Calculate category totals (from original data)
    category_totals = original_df.groupby('category')['amount'].sum().to_dict()
    
    # Generate plot
    plt.figure(figsize=(10, 6))
    sns.set_style("darkgrid")
    
    if category != 'all':
        # If a category is selected, show time trend for that category
        time_data = df.groupby(df['date'].dt.to_period('M'))['amount'].sum().reset_index()
        time_data['date'] = time_data['date'].astype(str)
        sns.barplot(x='date', y='amount', data=time_data)
        plt.title(f'{category} Expenses Over Time')
    else:
        # If no category is selected, show category breakdown
        category_data = original_df.groupby('category')['amount'].sum().reset_index()
        sns.barplot(x='category', y='amount', data=category_data)
        plt.title('Expenses by Category')
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Save plot to a base64 string
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()
    
    # Generate recommendations
    recommendations = []
    if category != 'all':
        cat_total = df['amount'].sum()
        total_expenses = original_df['amount'].sum()
        cat_pct = (cat_total / total_expenses) * 100 if total_expenses > 0 else 0
        
        if cat_pct > 30:
            recommendations.append({
                "message": f"Your {category} spending is {cat_pct:.1f}% of total expenses. Consider reducing this category.",
                "priority": 1
            })
        elif cat_pct < 10:
            recommendations.append({
                "message": f"You're doing well controlling {category} expenses ({cat_pct:.1f}% of total).",
                "priority": 3
            })
        else:
            recommendations.append({
                "message": f"{category} spending is {cat_pct:.1f}% of your total budget.",
                "priority": 2
            })
    else:
        top_category = max(category_totals.items(), key=lambda x: x[1]) if category_totals else ('None', 0)
        top_pct = (top_category[1] / total) * 100 if total > 0 else 0
        
        if top_pct > 40:
            recommendations.append({
                "message": f"Your spending on {top_category[0]} is {top_pct:.1f}% of total expenses. Consider reducing this category.",
                "priority": 1
            })
        
        recommendations.append({
            "message": "Try to keep individual categories under 30% of your total budget.",
            "priority": 2
        })
        
        recommendations.append({
            "message": "Consider setting up automatic savings for 20% of your income.",
            "priority": 3
        })
    
    # Prepare response
    response = {
        "success": True,
        "stats": {
            "total": total,
            "avg_daily": avg_daily,
            "max_weekly": max_weekly
        },
        "categories": category_totals,
        "weekly_data": weekly_data,
        "plot": plot_data,
        "recommendations": recommendations,
        "selected_category": category
    }
    
    print(f"Summary response stats: total={total}, avg_daily={avg_daily}, max_weekly={max_weekly}")
    return jsonify(response)

@app.route('/api/expenses', methods=['GET'])
def get_expenses():
    period = request.args.get('period', 'monthly')
    category = request.args.get('category', 'all')
    
    print(f"Expenses API called with period={period}, category={category}")
    
    # Convert sample data to DataFrame
    df = pd.DataFrame(SAMPLE_DATA)
    df['date'] = pd.to_datetime(df['date'])
    
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
    
    response = {
        "success": True,
        "data": period_totals,
        "selected_category": category,
        "selected_period": period
    }
    
    return jsonify(response)

if __name__ == '__main__':
    print("="*50)
    print("Starting Expense Tracker API Server")
    print("="*50)
    print("API Endpoints:")
    print("  - /api/test - Test if the API is working")
    print("  - /api/summary - Get summary statistics and visualizations")
    print("  - /api/expenses - Get expense data by period")
    print("="*50)
    print("Server will be available at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print("="*50)
    app.run(debug=True, host='0.0.0.0', port=5000)