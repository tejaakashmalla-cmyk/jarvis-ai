import json
from models.storage_manager import StorageManager
from views.report_generator import ReportGenerator
from controllers.main import ExpenseTrackerApp

def main():
    storage = StorageManager()
    
    while True:
        print("\nExpense Tracker Menu")
        print("1. Add Expense")
        print("2. Delete Expense")
        print("3. Edit Expense")
        print("4. Generate Monthly Report")
        print("5. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            amount = float(input("Enter expense amount: "))
            description = input("Enter expense description: ")
            date = input("Enter expense date (YYYY-MM-DD): ")
            storage.add_expense(amount, description, date)
        elif choice == "2":
            id_to_delete = int(input("Enter the ID of the expense to delete: "))
            storage.delete_expense(id_to_delete)
        elif choice == "3":
            id_to_edit = int(input("Enter the ID of the expense to edit: "))
            amount = float(input("Enter new expense amount (leave blank if no change): "))
            description = input("Enter new expense description (leave blank if no change): ")
            date = input("Enter new expense date (YYYY-MM-DD) (leave blank if no change): ")
            storage.edit_expense(id_to_edit, amount, description, date)
        elif choice == "4":
            ReportGenerator().generate_report(storage.get_all_expenses())
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")
        
    storage.save_data()

if __name__ == "__main__":
    main()