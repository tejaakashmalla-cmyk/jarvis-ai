import ollama
from config.models import CHAT_MODEL


class LLMService:

    def __init__(self, model=None):

        self.model = model if model else CHAT_MODEL

    def stream_chat(self, messages):

        stream = ollama.chat(
            model=self.model,
            messages=messages,
            stream=True,
            options={
                # Lower temperature = faster & more stable
                "temperature": 0.4,

                # Larger context for future memory
                "num_ctx": 8192,

                # Let the model generate naturally
                "num_predict": -1,

                # Utilize CPU efficiently alongside GPU
                "num_thread": 8,

                # Keep model loaded in VRAM
                "keep_alive": "30m"
            }
        )

        for chunk in stream:

            if "message" not in chunk:
                continue

            token = chunk["message"].get("content", "")

            if token:
                yield token

    def chat(self, messages):

        return "".join(self.stream_chat(messages))