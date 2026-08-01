from models.storage_manager import StorageManager
from datetime import datetime


class ExpenseModel:
    def __init__(self, id=None, amount=0.0, category="", date=datetime.now()):
        self.id = id
        self.amount = amount
        self.category = category
        self.date = date

    @classmethod
    def from_dict(cls, data):
        return cls(id=data.get("id"), amount=data["amount"], category=data["category"], date=data["date"])

    def to_dict(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "category": self.category,
            "date": self.date.strftime("%Y-%m-%d %H:%M:%S")
        }

    def save_to_storage(self, storage_manager: StorageManager):
        data = self.to_dict()
        storage_manager.save_data(data)

    @classmethod
    def load_from_storage(cls, storage_manager: StorageManager):
        return [cls.from_dict(expense) for expense in storage_manager.load_data()]

    def delete_from_storage(self, storage_manager: StorageManager):
        storage_manager.delete_data_by_id(self.id)