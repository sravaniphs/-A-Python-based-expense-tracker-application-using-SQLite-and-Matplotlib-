import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Initialize the SQLite database
conn = sqlite3.connect('expenses.db')
cursor = conn.cursor()

# Create table for storing expenses if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL,
    category TEXT,
    description TEXT,
    date TEXT
)
''')
conn.commit()

def add_expense(amount, category, description, date):
    cursor.execute('''
    INSERT INTO expenses (amount, category, description, date)
    VALUES (?, ?, ?, ?)
    ''', (amount, category, description, date))
    conn.commit()

def view_expenses():
    cursor.execute('SELECT * FROM expenses')
    return cursor.fetchall()

def view_expenses_by_category(category):
    cursor.execute('SELECT * FROM expenses WHERE category = ?', (category,))
    return cursor.fetchall()

def generate_report():
    cursor.execute('SELECT * FROM expenses')
    expenses = cursor.fetchall()
    df = pd.DataFrame(expenses, columns=['id', 'amount', 'category', 'description', 'date'])
    return df.groupby('category')['amount'].sum()

def visualize_spending_trends():
    cursor.execute('SELECT * FROM expenses')
    expenses = cursor.fetchall()
    df = pd.DataFrame(expenses, columns=['id', 'amount', 'category', 'description', 'date'])
    spending_by_category = df.groupby('category')['amount'].sum()

    # Plotting the bar chart
    spending_by_category.plot(kind='bar', title="Spending Trends by Category")
    plt.ylabel('Amount')
    plt.xlabel('Category')
    plt.show()

# Main menu
def main():
    while True:
        print("\nExpense Tracker Application")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. View Expenses by Category")
        print("4. Generate Monthly Report")
        print("5. View Spending Trends")
        print("6. Exit")
        
        choice = input("Enter your choice (1-6): ")
        
        if choice == '1':
            amount = float(input("Enter amount: "))
            category = input("Enter category (e.g., Food, Transport, etc.): ")
            description = input("Enter description: ")
            date = input("Enter date (YYYY-MM-DD): ")
            add_expense(amount, category, description, date)
            print("Expense added successfully!")
        
        elif choice == '2':
            expenses = view_expenses()
            print("\nAll Expenses:")
            for expense in expenses:
                print(expense)
        
        elif choice == '3':
            category = input("Enter category to filter by: ")
            expenses = view_expenses_by_category(category)
            print(f"\nExpenses for category: {category}")
            for expense in expenses:
                print(expense)
        
        elif choice == '4':
            report = generate_report()
            print("\nMonthly Expense Report by Category:")
            print(report)
        
        elif choice == '5':
            print("\nGenerating Spending Trends...")
            visualize_spending_trends()
        
        elif choice == '6':
            print("Exiting the application...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()


