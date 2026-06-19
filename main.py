import os
from datetime import datetime

FILE_NAME = "expenses.txt"


def add_expense():
    amount = input("Enter the amount spent: ")
    category = input("Enter the category (Food, Transport, Entertainment): ")
    date = input("Enter the date (YYYY-MM-DD): ")

    if not amount or not category or not date:
        print("❌ Amount, category, and date are required.\n")
        return

    try:
        amount = float(amount)

        # Validate date format
        datetime.strptime(date, "%Y-%m-%d")

        with open(FILE_NAME, "a") as file:
            file.write(f"{amount},{category},{date}\n")

        print("✅ Expense added successfully.\n")

    except ValueError:
        print("❌ Invalid amount or date format.\n")

    except Exception as e:
        print(f"❌ Error: {e}\n")


def view_expenses():
    if not os.path.exists(FILE_NAME):
        print("No expenses recorded yet.\n")
        return

    try:
        with open(FILE_NAME, "r") as file:
            expenses = file.readlines()

        if not expenses:
            print("No expenses recorded yet.\n")
            return

        print("\n📊 Expense Report:")
        for expense in expenses:
            amount, category, date = expense.strip().split(",")
            print(f"Amount: Rs.{amount} | Category: {category} | Date: {date}")

        print()

    except Exception as e:
        print(f"❌ Error: {e}\n")


def view_total_spent():
    if not os.path.exists(FILE_NAME):
        print("No expenses recorded yet.\n")
        return

    total_spent = 0

    try:
        with open(FILE_NAME, "r") as file:
            expenses = file.readlines()

        for expense in expenses:
            amount, _, _ = expense.strip().split(",")
            total_spent += float(amount)

        print(f"\n💰 Total Amount Spent: Rs.{total_spent:.2f}\n")

    except Exception as e:
        print(f"❌ Error: {e}\n")


def view_by_category():
    if not os.path.exists(FILE_NAME):
        print("No expenses recorded yet.\n")
        return

    category_totals = {}

    try:
        with open(FILE_NAME, "r") as file:
            expenses = file.readlines()

        for expense in expenses:
            amount, category, _ = expense.strip().split(",")

            if category in category_totals:
                category_totals[category] += float(amount)
            else:
                category_totals[category] = float(amount)

        print("\n📊 Expenses by Category:")
        for category, total in category_totals.items():
            print(f"{category}: Rs.{total:.2f}")

        print()

    except Exception as e:
        print(f"❌ Error: {e}\n")


def main():
    while True:
        print("💰 Personal Expense Tracker")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. View Total Spent")
        print("4. View Expenses by Category")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            view_total_spent()
        elif choice == "4":
            view_by_category()
        elif choice == "5":
            print("Goodbye! 👋")
            break
        else:
            print("❌ Invalid choice. Please enter a number between 1 and 5.\n")


if __name__ == "__main__":
    main()