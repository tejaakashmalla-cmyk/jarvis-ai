import ollama


class LLMService:

    def __init__(self, model="llama3.1:8b"):
        self.model = model

    def chat(self, messages):

        response = ollama.chat(
            model=self.model,
            messages=messages
        )

        return response["message"]["content"]