from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import io
import json
from datetime import datetime
import os

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Path to the predefined expenses file
EXPENSES_FILE = os.path.join(os.path.dirname(__file__), 'expenses.csv')

@app.post("/api/analyze-expenses")
async def analyze_expenses():
    try:
        # Load and preprocess dataset
        data = pd.read_csv(EXPENSES_FILE)

        # Convert 'amount' column to numeric
        data['amount'] = pd.to_numeric(data['amount'], errors='coerce')
        data = data.dropna(subset=['amount'])

        # Convert 'date' column to datetime
        data['date'] = pd.to_datetime(data['date'], errors='coerce')
        data = data.dropna(subset=['date'])

        # Extract date-related features
        data['day_of_week'] = data['date'].dt.day_name()
        data['month'] = data['date'].dt.month
        data['day'] = data['date'].dt.day
        data['year'] = data['date'].dt.year
        data['year_month'] = data['date'].dt.to_period('M').astype(str)
        data['week'] = data['date'].dt.isocalendar().week

        # Encode category
        data['category_encoded'] = LabelEncoder().fit_transform(data['category'])

        # Calculate metrics
        total_by_category = data.groupby('category')['amount'].sum().sort_values(ascending=False)
        top_category = total_by_category.idxmax()
        total_spend = data['amount'].sum()

        # Weekly pattern
        spend_by_dayofweek = data.groupby('day_of_week')['amount'].sum().sort_values(ascending=False)
        highest_day = spend_by_dayofweek.idxmax()

        # Monthly pattern
        monthly_avg = data.groupby('month')['amount'].mean()
        peak_month = monthly_avg.idxmax()

        # Generate recommendations
        recommendations = []
        if total_by_category[top_category] > 0.4 * total_spend:
            recommendations.append(f"Try reducing expenses in {top_category} as it dominates your spending.")
        recommendations.append(f"You spend the most on {highest_day}. Consider reviewing expenses on that day.")
        recommendations.append(f"Your peak spending is in month {peak_month}. Try budgeting better for that period.")

        # Prepare aggregated data
        daily_spend = data.groupby(['date', 'category'])['amount'].sum().unstack(fill_value=0).reset_index()
        daily_spend['date'] = daily_spend['date'].dt.strftime('%Y-%m-%d')
        
        weekly_spend = data.groupby(['year', 'week', 'category'])['amount'].sum().unstack(fill_value=0).reset_index()
        monthly_spend = data.groupby(['year_month', 'category'])['amount'].sum().unstack(fill_value=0).reset_index()
        yearly_spend = data.groupby(['year', 'category'])['amount'].sum().unstack(fill_value=0).reset_index()

        # Convert to JSON-serializable format
        response = {
            "totalByCategory": total_by_category.to_dict(),
            "topCategory": top_category,
            "totalSpend": float(total_spend),
            "spendByDayOfWeek": spend_by_dayofweek.to_dict(),
            "monthlyAvg": monthly_avg.to_dict(),
            "recommendations": recommendations,
            "dailySpend": daily_spend.to_dict(orient='records'),
            "weeklySpend": weekly_spend.to_dict(orient='records'),
            "monthlySpend": monthly_spend.to_dict(orient='records'),
            "yearlySpend": yearly_spend.to_dict(orient='records')
        }
        return response

    except Exception as e:
        return {"error": str(e)}
