from services.llm_service import LLMService


class ModelRouter:

    def __init__(self):

        self.chat_model = LLMService()

    def get_model(self, intent):

        if intent == "coding":
            return self.chat_model

        if intent == "memory":
            return self.chat_model

        if intent == "tool":
            return self.chat_model

        return self.chat_model