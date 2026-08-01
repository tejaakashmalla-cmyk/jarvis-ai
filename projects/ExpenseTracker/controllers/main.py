from controllers.storage_manager import StorageManager
from controllers.expense_model import ExpenseModel
from views.report_generator import ReportGenerator

class ExpenseTrackerApp:
    def __init__(self):
        self.storage = StorageManager()
        self.model = ExpenseModel(self.storage)
        self.generator = ReportGenerator()

    def add_expense(self, amount, category, description):
        expense_id = self.model.add_expense(amount, category, description)
        print(f"Expense added with ID: {expense_id}")

    def delete_expense(self, expense_id):
        if not self.model.delete_expense(expense_id):
            print("Expense not found.")
        else:
            print("Expense deleted successfully.")

    def edit_expense(self, expense_id, amount=None, category=None, description=None):
        if amount is None and category is None and description is None:
            return
        edited = self.model.edit_expense(expense_id, amount, category, description)
        if not edited:
            print("Expense not found.")
        else:
            print("Expense updated successfully.")

    def generate_monthly_report(self):
        report = self.generator.generate_monthly_report()
        print(report)

    def run(self):
        while True:
            print("\nChoose an option:")
            print("1. Add Expense")
            print("2. Delete Expense")
            print("3. Edit Expense")
            print("4. Generate Monthly Report")
            choice = input("Enter your choice: ")
            if choice == "1":
                amount = float(input("Amount: "))
                category = input("Category: ")
                description = input("Description: ")
                self.add_expense(amount, category, description)
            elif choice == "2":
                expense_id = int(input("Expense ID to delete: "))
                self.delete_expense(expense_id)
            elif choice == "3":
                expense_id = int(input("Expense ID to edit: "))
                amount = float(input("New Amount (leave blank if no change): ") or None)
                category = input("New Category (leave blank if no change): ") or None
                description = input("New Description (leave blank if no change): ") or None
                self.edit_expense(expense_id, amount, category, description)
            elif choice == "4":
                self.generate_monthly_report()
            else:
                print("Invalid choice. Please try again.")