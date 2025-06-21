import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import os

def create_expense_visualizations(expense_data, output_dir='./static'):
    """
    Create visualizations for expense data
    
    Parameters:
    -----------
    expense_data : pandas.DataFrame
        DataFrame containing expense data
    output_dir : str
        Directory to save the visualizations
    
    Returns:
    --------
    dict
        Dictionary containing paths to the generated visualizations
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Set the seaborn style correctly
    # Method 1: Use seaborn's set_style function (recommended)
    sns.set_style("darkgrid")  # Valid options: "darkgrid", "whitegrid", "dark", "white", "ticks"
    
    # DO NOT use this - it will cause the error:
    # plt.style.use('seaborn')  # This is incorrect and causes the error
    
    # Instead, if you want to use matplotlib's style system, use one of these:
    # For newer versions of matplotlib/seaborn:
    # plt.style.use('seaborn-v0_8-darkgrid')
    # For older versions:
    # plt.style.use('seaborn-darkgrid')
    
    # Sample data if expense_data is empty
    if expense_data.empty:
        expense_data = pd.DataFrame({
            'date': pd.date_range(start='2023-01-01', periods=30, freq='D'),
            'amount': np.random.uniform(10, 100, 30),
            'category': np.random.choice(['Food', 'Transport', 'Entertainment', 'Utilities'], 30)
        })
    
    # Create time series plot
    plt.figure(figsize=(12, 6))
    time_series = expense_data.groupby('date')['amount'].sum().reset_index()
    sns.lineplot(x='date', y='amount', data=time_series)
    plt.title('Expenses Over Time')
    plt.xlabel('Date')
    plt.ylabel('Amount ($)')
    plt.tight_layout()
    time_series_path = os.path.join(output_dir, 'time_series.png')
    plt.savefig(time_series_path)
    plt.close()
    
    # Create category distribution plot
    plt.figure(figsize=(10, 6))
    category_data = expense_data.groupby('category')['amount'].sum().reset_index()
    sns.barplot(x='category', y='amount', data=category_data)
    plt.title('Expenses by Category')
    plt.xlabel('Category')
    plt.ylabel('Amount ($)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    category_path = os.path.join(output_dir, 'category_distribution.png')
    plt.savefig(category_path)
    plt.close()
    
    # Create a heatmap for weekly patterns
    if 'date' in expense_data.columns:
        expense_data['day_of_week'] = expense_data['date'].dt.day_name()
        expense_data['week'] = expense_data['date'].dt.isocalendar().week
        weekly_pivot = expense_data.pivot_table(
            index='day_of_week', 
            columns='week', 
            values='amount', 
            aggfunc='sum'
        )
        
        plt.figure(figsize=(12, 8))
        sns.heatmap(weekly_pivot, cmap='YlGnBu', annot=True, fmt='.1f')
        plt.title('Weekly Expense Patterns')
        plt.tight_layout()
        weekly_path = os.path.join(output_dir, 'weekly_pattern.png')
        plt.savefig(weekly_path)
        plt.close()
    
    # Return paths to the generated visualizations
    return {
        'time_series': time_series_path,
        'category_distribution': category_path,
        'weekly_pattern': weekly_path if 'date' in expense_data.columns else None
    }

def print_available_styles():
    """Print all available matplotlib styles"""
    print("Available matplotlib styles:")
    print(plt.style.available)

if __name__ == "__main__":
    # Example usage
    sample_data = pd.DataFrame({
        'date': pd.date_range(start='2023-01-01', periods=30, freq='D'),
        'amount': np.random.uniform(10, 100, 30),
        'category': np.random.choice(['Food', 'Transport', 'Entertainment', 'Utilities'], 30)
    })
    
    # Print available styles
    print_available_styles()
    
    # Create visualizations
    viz_paths = create_expense_visualizations(sample_data)
    print("Visualizations created at:")
    for name, path in viz_paths.items():
        if path:
            print(f"- {name}: {path}")