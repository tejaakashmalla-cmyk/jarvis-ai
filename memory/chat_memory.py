import json
import os


class ChatMemory:

    def __init__(self, file_path="memory/memory.json"):

        self.file_path = file_path

        if not os.path.exists(file_path):

            with open(file_path, "w") as f:
                json.dump({}, f)

    def load(self):

        with open(self.file_path, "r") as f:
            return json.load(f)

    def save(self, data):

        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=4)

    def remember(self, key, value):

        memory = self.load()

        memory[key] = value

        self.save(memory)

    def recall(self, key):

        memory = self.load()

        return memory.get(key)

    def all_memory(self):

        return self.load()