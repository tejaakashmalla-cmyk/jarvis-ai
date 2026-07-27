from .personality import PersonalityEngine
from .conversation import ConversationManager
from .memory_recall import MemoryRecall


class JarvisBrain:

    def __init__(self):

        self.personality = PersonalityEngine()

        self.conversation = ConversationManager()

        self.memory = MemoryRecall()

    def create_messages(self, history, user_message):

        system_prompt = self.personality.get_system_prompt()

        memory_context = self.memory.get_context()

        full_prompt = system_prompt

        if memory_context:

            full_prompt += "\n\n"

            full_prompt += memory_context

        return self.conversation.build_messages(

            full_prompt,

            history,

            user_message

        )