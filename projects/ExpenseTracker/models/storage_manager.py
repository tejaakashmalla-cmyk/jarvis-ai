from typing import List, Dict
import json


class StorageManager:
    def __init__(self):
        self._data: Dict[str, Dict] = {}
    
    def load_data(self, file_path: str) -> None:
        with open(file_path, 'r') as file:
            self._data = json.load(file)
    
    def save_data(self, file_path: str) -> None:
        with open(file_path, 'w') as file:
            json.dump(self._data, file, indent=4)
    
    def add_expense(self, expense_id: str, expense_details: Dict[str, str]) -> None:
        if expense_id not in self._data:
            self._data[expense_id] = expense_details
        else:
            raise ValueError("Expense ID already exists.")
    
    def delete_expense(self, expense_id: str) -> None:
        if expense_id in self._data:
            del self._data[expense_id]
        else:
            raise KeyError("Expense not found.")
    
    def edit_expense(self, expense_id: str, new_details: Dict[str, str]) -> None:
        if expense_id in self._data:
            self._data[expense_id].update(new_details)
        else:
            raise ValueError("Expense ID does not exist.")
    
    def get_all_expenses(self) -> List[Dict]:
        return list(self._data.values())