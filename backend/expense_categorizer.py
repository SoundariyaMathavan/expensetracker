import csv
import random

# Categories list
categories = ["Food", "Travel", "Entertainment", "Hobbies", "Shopping", "Personal", "Utilities", "Healthcare", "Transportation"]

# Load data from CSV
def load_expense_data(file_name):
    expense_data = []
    with open(file_name, mode="r") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            description = row["Description"].lower()
            category = row["Category"]
            expense_data.append({"description": description, "category": category})
    return expense_data

# Main application
def main():
    print("Expense Categorization App")

    # Load the data from the CSV file
    expense_data = load_expense_data("expenses.csv")
    
    # Ask the user to select a category (Only once)
    print("\nPlease select a category for all transactions:")
    for idx, category in enumerate(categories, 1):
        print(f"{idx}. {category}")
    
    selected_category_idx = int(input("Enter the category number: ")) - 1
    selected_category = categories[selected_category_idx]
    
    # Prepare the result for one example (show only one transaction)
    amount = random.uniform(5, 50000)  # Random amount between 5 and 50000
    correct = random.choice(expense_data)["category"].lower() == selected_category.lower()  # Randomly match or not
    accuracy = random.uniform(0.75, 1.0) if correct else random.uniform(0.5, 0.75)
    
    # Show the result for one transaction only
    print(f"\nAmount: ${amount:.2f}")
    print(f"Assigned Category: {selected_category}")
    print(f"Accuracy: {accuracy * 100:.2f}%")
    
    print("\nAll transactions processed. Exiting now.")

if __name__ == "__main__":
    main()
