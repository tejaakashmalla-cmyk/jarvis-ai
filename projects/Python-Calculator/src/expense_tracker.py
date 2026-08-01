# src/expense_tracker.py

class ExpenseTracker:
    def __init__(self):
        self.expenses = []

    def add_expense(self, amount, description):
        if amount > 0:
            self.expenses.append({"amount": amount, "description": description})
            return True
        else:
            print("Expense amount must be greater than zero.")
            return False

    def get_total_spent(self):
        total = sum(expense['amount'] for expense in self.expenses)
        return total if total > 0 else 0

    def get_expenses_by_category(self, category=None):
        filtered_expenses = []
        for expense in self.expenses:
            if not category or expense['description'].lower().startswith(category.lower()):
                filtered_expenses.append(expense)
        return filtered_expenses