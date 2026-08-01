from models.expense_model import ExpenseModel
import json
from prettytable import PrettyTable

class ReportGenerator:
    def __init__(self, expense_data_path):
        self.expense_data_path = expense_data_path
        self.expense_model = ExpenseModel()

    def generate_monthly_report(self, month, year):
        with open(self.expense_data_path, 'r') as file:
            data = json.load(file)

        monthly_expenses = {}
        for entry in data['entries']:
            if entry['date'].startswith(f"{month}-{year}-"):
                expense_date = entry['date'][len(month) + 1:]
                if expense_date not in monthly_expenses:
                    monthly_expenses[expense_date] = []
                monthly_expenses[expense_date].append(entry)

        report_table = PrettyTable()
        report_table.field_names = ["Date", "Description", "Amount"]

        for date, entries in sorted(monthly_expenses.items()):
            total_amount = sum(float(entry['amount']) for entry in entries)
            report_table.add_row([date, ", ".join(entry['description'] for entry in entries), f"${total_amount:.2f}"])

        print(report_table)

    def generate_budget_report(self):
        with open(self.expense_data_path, 'r') as file:
            data = json.load(file)

        total_expenses = sum(float(entry['amount']) for entry in data['entries'])
        budget_percentage = (total_expenses / float(data['budget'])) * 100 if data['budget'] else 0
        print(f"Total Expenses: ${total_expenses:.2f}")
        print(f"Budget Percentage: {budget_percentage:.2f}%")