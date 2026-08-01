# src/expense_tracker.py

import json
from pathlib import Path


class ExpenseTracker:
    def __init__(self, data_file: str = "expenses.json"):
        self.data_file = Path(data_file)
        if not self.data_file.exists():
            self._initialize_data()

    def _initialize_data(self):
        with open(self.data_file, 'w') as file:
            json.dump({}, file)

    def add_expense(self, description: str, amount: float, category: str) -> None:
        expenses = self.load_expenses()
        expenses[description] = {
            "amount": amount,
            "category": category
        }
        with open(self.data_file, 'w') as file:
            json.dump(expenses, file)

    def delete_expense(self, description: str) -> bool:
        expenses = self.load_expenses()
        if description in expenses:
            del expenses[description]
            with open(self.data_file, 'w') as file:
                json.dump(expenses, file)
            return True
        return False

    def list_expenses(self) -> None:
        expenses = self.load_expenses()
        for description, details in expenses.items():
            print(f"{description}: {details['amount']} ({details['category']})")

    def load_expenses(self) -> dict:
        with open(self.data_file, 'r') as file:
            return json.load(file)