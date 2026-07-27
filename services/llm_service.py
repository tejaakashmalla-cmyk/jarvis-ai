import ollama


class LLMService:

    def __init__(self, model="gemma3:4b"):
        self.model = model

    def stream_chat(self, messages):

        stream = ollama.chat(
            model=self.model,
            messages=messages,
            stream=True,
            options={
                "temperature": 0.7,
                "num_predict": 150,
                "num_ctx": 4096,
                "num_thread": 8
            }
        )

        for chunk in stream:

            if "message" in chunk:

                token = chunk["message"]["content"]

                if token:
                    yield token

    def chat(self, messages):

        full_response = ""

        for token in self.stream_chat(messages):
            full_response += token

        return full_response