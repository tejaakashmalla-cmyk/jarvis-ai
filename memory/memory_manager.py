from .chat_memory import ChatMemory


class MemoryManager:

    def __init__(self):

        self.memory = ChatMemory()

    def save_items(self, items):

        if not items:
            return

        data = self.memory.load()

        data.update(items)

        self.memory.save(data)

    def get_all(self):

        return self.memory.load()

    def get(self, key):

        return self.memory.recall(key)