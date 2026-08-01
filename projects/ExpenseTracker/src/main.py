import sys
from src.expense_tracker import ExpenseTrackerCLI


def main():
    tracker = ExpenseTrackerCLI()
    while True:
        print("\nExpense Tracker CLI")
        print("1. Add expense")
        print("2. Delete expense")
        print("3. List expenses")
        print("4. Exit")
        choice = input("Choose an option: ")
        
        if choice == '1':
            amount = float(input("Enter the expense amount: "))
            category = input("Enter the category: ")
            tracker.add_expense(amount, category)
        elif choice == '2':
            id_to_delete = int(input("Enter the ID of the expense to delete: "))
            tracker.delete_expense(id_to_delete)
        elif choice == '3':
            tracker.list_expenses()
        elif choice == '4':
            sys.exit(0)
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()