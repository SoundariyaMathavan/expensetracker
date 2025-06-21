import pandas as pd
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import seaborn as sns
import calendar

# ----------------------------
# 📥 Load and Preprocess Data
# ----------------------------
data = pd.read_csv("expenses.csv")

# Convert 'amount' to numeric
data['amount'] = pd.to_numeric(data['amount'], errors='coerce')
data = data.dropna(subset=['amount'])

# Convert 'date' to datetime
data['date'] = pd.to_datetime(data['date'], errors='coerce')
data = data.dropna(subset=['date'])

# Extract date features
data['day_of_week'] = data['date'].dt.day_name()
data['month'] = data['date'].dt.month
data['month_name'] = data['date'].dt.month_name()
data['day'] = data['date'].dt.day
data['year'] = data['date'].dt.year
data['year_month'] = data['date'].dt.to_period('M')
data['week'] = data['date'].dt.isocalendar().week

# Encode category
data['category_encoded'] = LabelEncoder().fit_transform(data['category'])

# ----------------------------
# 📊 Daily Spend by Category (Vertical Format)
# ----------------------------
daily_spend = data.groupby(['date', 'category'])['amount'].sum().unstack(fill_value=0)

# Transform to vertical format
vertical_daily_spend = daily_spend.stack().reset_index()
vertical_daily_spend.columns = ['date', 'category', 'amount']

# Add recommendations column
def generate_recommendation(amount, avg):
    if amount > avg * 1.5:
        return "⚠️ High spending. Consider reducing."
    elif amount < avg * 0.5 and amount > 0:
        return "✅ Low spending. Great job!"
    else:
        return "Normal spending."

# Calculate average spending for each category
category_avg = vertical_daily_spend.groupby('category')['amount'].mean()

# Apply recommendations
vertical_daily_spend['recommendation'] = vertical_daily_spend.apply(
    lambda row: generate_recommendation(row['amount'], category_avg[row['category']]), axis=1
)

# Display the vertical format with recommendations
print("\n📊 Daily Spend by Category (Vertical Format with Recommendations):")
print(vertical_daily_spend.tail())

# ----------------------------
# 📊 Monthly Spend by Category (Vertical Format)
# ----------------------------
monthly_spend = data.groupby(['year_month', 'category'])['amount'].sum().unstack(fill_value=0)

# Transform to vertical format
vertical_monthly_spend = monthly_spend.stack().reset_index()
vertical_monthly_spend.columns = ['year_month', 'category', 'amount']

# Apply recommendations
category_month_avg = vertical_monthly_spend.groupby('category')['amount'].mean()
vertical_monthly_spend['recommendation'] = vertical_monthly_spend.apply(
    lambda row: generate_recommendation(row['amount'], category_month_avg[row['category']]), axis=1
)

# Display the vertical format with recommendations
print("\n📅 Monthly Spend by Category (Vertical Format with Recommendations):")
print(vertical_monthly_spend.tail())

# ----------------------------
# 📊 Yearly Spend by Category (Vertical Format)
# ----------------------------
yearly_spend = data.groupby(['year', 'category'])['amount'].sum().unstack(fill_value=0)

# Transform to vertical format
vertical_yearly_spend = yearly_spend.stack().reset_index()
vertical_yearly_spend.columns = ['year', 'category', 'amount']

# Apply recommendations
category_year_avg = vertical_yearly_spend.groupby('category')['amount'].mean()
vertical_yearly_spend['recommendation'] = vertical_yearly_spend.apply(
    lambda row: generate_recommendation(row['amount'], category_year_avg[row['category']]), axis=1
)

# Display the vertical format with recommendations
print("\n📈 Yearly Spend by Category (Vertical Format with Recommendations):")
print(vertical_yearly_spend.tail())

# ----------------------------
# 📈 Visualization
# ----------------------------
plt.figure(figsize=(10, 5))
sns.barplot(x=vertical_daily_spend['category'], y=vertical_daily_spend['amount'], palette="viridis")
plt.title("Daily Spend by Category")
plt.ylabel("Amount")
plt.xlabel("Category")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# ----------------------------
# 🔁 User-Prompted Comparison Function
# ----------------------------
def compare_periods(df, level):
    """
    Ask user for two values (e.g., months, years, days) to compare category expenses.
    """
    available = df[level].unique()
    print(f"\n📅 Available {level.title()}s in your data: {sorted(available)}")

    period1 = input(f"🔎 Enter the first {level} to compare (e.g., 'March' or '3'): ").strip()
    period2 = input(f"🔍 Enter the second {level} to compare (e.g., 'April' or '4'): ").strip()

    # Handle month names or numbers
    if level == 'month':
        try:
            period1 = int(period1) if period1.isdigit() else list(calendar.month_name).index(period1.capitalize())
            period2 = int(period2) if period2.isdigit() else list(calendar.month_name).index(period2.capitalize())
        except ValueError:
            print("⚠️ Invalid month input. Please enter a valid month name or number.")
            return

    grouped = df.groupby([level, 'category'])['amount'].sum().unstack(fill_value=0)

    if period1 not in grouped.index or period2 not in grouped.index:
        print(f"⚠️ One of the periods ({period1}, {period2}) not found in data.")
        return

    diff = grouped.loc[period2] - grouped.loc[period1]
    print(f"\n🔁 Comparison: {period2} vs {period1}")
    print(diff.sort_values(ascending=False))

    # Recommendations based on comparison
    print("\n📊 Recommendations Based on Comparison:")
    for category, change in diff.items():
        if change > 0:
            print(f"📈 You spent more on **{category}** in {period2} compared to {period1}. Consider reducing.")
        elif change < 0:
            print(f"📉 You spent less on **{category}** in {period2} compared to {period1}. Keep it up!")

# Prompt user for level of comparison
comparison_level = input("\n📊 Compare by 'month', 'year', or 'day_of_week'? ").strip().lower()

if comparison_level in ['month', 'year', 'day_of_week']:
    compare_periods(data, comparison_level)
else:
    print("⚠️ Invalid input. Please choose 'month', 'year', or 'day_of_week'.")

# ----------------------------
# 🧠 Add Suggestions Below Tables
# ----------------------------
print("\n📊 Suggestions for Each Category:")
for category, avg in category_avg.items():
    print(f"Category: {category}")
    print(f"  - Average Spending: {avg:.2f}")
    print(f"  - Suggestion: {generate_recommendation(avg, avg)}")