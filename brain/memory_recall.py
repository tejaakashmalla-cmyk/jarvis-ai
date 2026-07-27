from memory.memory_manager import MemoryManager


class MemoryRecall:

    def __init__(self):

        self.memory = MemoryManager()

    def get_context(self):

        data = self.memory.get_all()

        if not data:
            return ""

        context = "Known information about the user:\n\n"

        for key, value in data.items():

            context += f"{key}: {value}\n"

        return context