from memory.memory_manager import MemoryManager


class MemoryEngine:

    def __init__(self):

        self.memory = MemoryManager()

    def save(self, items):

        if items:
            self.memory.save_items(items)

    def recall(self, query):

        """
        Placeholder for future semantic search.
        """

        return []