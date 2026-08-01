from models.expense_model import ExpenseModel
from prettytable import PrettyTable

class ReportGenerator:
    def __init__(self, storage_manager):
        self.storage_manager = storage_manager

    def generate_monthly_report(self, month, year):
        expenses = self.storage_manager.get_expenses_by_date(month, year)
        
        if not expenses:
            print(f"No expenses found for {month}/{year}.")
            return
        
        table = PrettyTable(["Date", "Description", "Amount"])
        total_spent = 0
        for expense in expenses:
            table.add_row([expense.date, expense.description, expense.amount])
            total_spent += expense.amount

        print(f"Monthly Report for {month}/{year}")
        print(table)
        print(f"\nTotal Spent: ${total_spent:.2f}")

    def generate_budget_report(self):
        expenses = self.storage_manager.get_all_expenses()
        
        if not expenses:
            print("No expenses found. Budget report is empty.")
            return

        total_spent = sum(expense.amount for expense in expenses)
        budget_limit = 1000  # Example budget limit
        remaining_budget = budget_limit - total_spent
        
        table = PrettyTable(["Category", "Amount"])
        table.add_row(["Total Spent", f"${total_spent:.2f}"])
        table.add_row(["Remaining Budget", f"${remaining_budget:.2f}"])

        print("Budget Report")
        print(table)