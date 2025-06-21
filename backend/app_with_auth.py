from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
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

# Import our models and auth blueprint
from models import db, User, Expense
from auth import auth_bp

# Filter out UserWarnings
warnings.filterwarnings("ignore", category=UserWarning)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expense_tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string-change-this-in-production'

# Initialize extensions
db.init_app(app)
jwt = JWTManager(app)
CORS(app)  # Enable CORS for all routes

# Register auth blueprint
app.register_blueprint(auth_bp, url_prefix='/api/auth')

# Create tables
with app.app_context():
    db.create_all()

def get_user_expenses(user_id, category='all'):
    """Get expenses for a specific user, optionally filtered by category"""
    query = Expense.query.filter_by(user_id=user_id)
    
    if category != 'all':
        query = query.filter_by(category=category)
    
    expenses = query.all()
    return [expense.to_dict() for expense in expenses]

@app.route('/api/summary', methods=['GET'])
@jwt_required()
def get_summary():
    try:
        user_id = get_jwt_identity()
        print(f"Summary endpoint called for user {user_id} with args:", request.args)
        
        # Get category from request args
        category = request.args.get('category', 'all')
        
        # Get user expenses
        expenses_data = get_user_expenses(user_id, category)
        
        if not expenses_data:
            # Return empty data structure if no expenses
            return jsonify({
                "success": True,
                "stats": {
                    "total": 0.0,
                    "avg_daily": 0.0,
                    "max_weekly": 0.0
                },
                "categories": {},
                "weekly_data": {},
                "plot": "",
                "recommendations": [
                    {"message": "Start tracking your expenses to get insights", "priority": 1}
                ],
                "selected_category": category
            })
        
        # Convert to DataFrame
        df = pd.DataFrame(expenses_data)
        df['date'] = pd.to_datetime(df['date'])
        df['amount'] = df['amount'].astype(float)
        
        # Calculate statistics
        total = df['amount'].sum()
        print(f"Total amount: {total}")
        
        # Calculate daily average
        avg_daily = df.groupby(df['date'].dt.date)['amount'].sum().mean()
        print(f"Daily average: {avg_daily}")
        
        # Calculate category totals (from all user expenses, not filtered)
        all_expenses = get_user_expenses(user_id, 'all')
        if all_expenses:
            category_df = pd.DataFrame(all_expenses)
            category_totals = category_df.groupby('category')['amount'].sum().to_dict()
        else:
            category_totals = {}
        
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
        
        # Generate recommendations based on user data
        recommendations = []
        if category_totals:
            max_category = max(category_totals, key=category_totals.get)
            max_amount = category_totals[max_category]
            recommendations.append({
                "message": f"Your highest spending is on {max_category} (${max_amount:.2f})",
                "priority": 1
            })
            
            if len(category_totals) > 1:
                sorted_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
                if len(sorted_categories) >= 2:
                    second_highest = sorted_categories[1]
                    recommendations.append({
                        "message": f"Consider budgeting for {second_highest[0]} expenses",
                        "priority": 2
                    })
        else:
            recommendations.append({
                "message": "Start adding expenses to get personalized insights",
                "priority": 1
            })
        
        response = {
            "success": True,
            "stats": {
                "total": float(total),
                "avg_daily": float(avg_daily),
                "max_weekly": float(max_weekly)
            },
            "categories": {k: float(v) for k, v in category_totals.items()},
            "weekly_data": {k: float(v) for k, v in weekly_data.items()},
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
@jwt_required()
def get_expenses():
    try:
        user_id = get_jwt_identity()
        period = request.args.get('period', 'monthly')
        category = request.args.get('category', 'all')
        
        # Get user expenses
        expenses_data = get_user_expenses(user_id, category)
        
        if not expenses_data:
            return jsonify({
                "success": True,
                "data": {},
                "selected_category": category,
                "selected_period": period
            })
        
        # Convert to DataFrame
        df = pd.DataFrame(expenses_data)
        df['date'] = pd.to_datetime(df['date'])
        df['amount'] = df['amount'].astype(float)
        
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
            "data": {k: float(v) for k, v in period_totals.items()},
            "selected_category": category,
            "selected_period": period
        }
        
        print(f"Expenses endpoint called for user {user_id} with period={period}, category={category}")
        return jsonify(response)
    
    except Exception as e:
        print(f"Error in expenses endpoint: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/expenses', methods=['POST'])
@jwt_required()
def add_expense():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['amount', 'category', 'date']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'{field} is required'
                }), 400
        
        # Create new expense
        expense = Expense(
            user_id=user_id,
            amount=float(data['amount']),
            category=data['category'],
            description=data.get('description', ''),
            date=datetime.strptime(data['date'], '%Y-%m-%d').date()
        )
        
        db.session.add(expense)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Expense added successfully',
            'expense': expense.to_dict()
        }), 201
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'message': 'Invalid date format. Use YYYY-MM-DD'
        }), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'An error occurred while adding expense',
            'error': str(e)
        }), 500

@app.route('/api/expenses/<int:expense_id>', methods=['DELETE'])
@jwt_required()
def delete_expense(expense_id):
    try:
        user_id = get_jwt_identity()
        
        # Find expense belonging to the user
        expense = Expense.query.filter_by(id=expense_id, user_id=user_id).first()
        
        if not expense:
            return jsonify({
                'success': False,
                'message': 'Expense not found'
            }), 404
        
        db.session.delete(expense)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Expense deleted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'An error occurred while deleting expense',
            'error': str(e)
        }), 500

@app.route('/api/test', methods=['GET'])
def test_api():
    return jsonify({
        "success": True,
        "message": "API is working correctly",
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

if __name__ == '__main__':
    print("Starting Flask server with authentication...")
    print("API endpoints:")
    print("  Authentication:")
    print("    - POST /api/auth/signup - Create new account")
    print("    - POST /api/auth/login - Login to account")
    print("    - GET /api/auth/profile - Get user profile")
    print("    - GET /api/auth/verify-token - Verify JWT token")
    print("  Expenses (require authentication):")
    print("    - GET /api/summary - Get summary statistics and visualizations")
    print("    - GET /api/expenses - Get expense data by period")
    print("    - POST /api/expenses - Add new expense")
    print("    - DELETE /api/expenses/<id> - Delete expense")
    print("  General:")
    print("    - GET /api/test - Test if the API is working")
    app.run(debug=True, host='0.0.0.0', port=5000)