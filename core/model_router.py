from services.llm_service import LLMService

from config.models import (
    CHAT_MODEL,
    PLANNER_MODEL,
    CODING_MODEL,
)


class ModelRouter:

    def __init__(self):

        self.chat = LLMService(CHAT_MODEL)

        self.coding = LLMService(CODING_MODEL)

        self.planner = LLMService(PLANNER_MODEL)

    def get_model(self, intent):

        if intent == "coding":
            return self.coding

        if intent == "planner":
            return self.planner

        return self.chat