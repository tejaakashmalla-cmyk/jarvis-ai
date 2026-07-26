from .personality import PersonalityEngine
from .conversation import ConversationManager


class JarvisBrain:

    def __init__(self):

        self.personality = PersonalityEngine()

        self.conversation = ConversationManager()

    def create_messages(self, history, user_message):

        prompt = self.personality.get_system_prompt()

        return self.conversation.build_messages(
            prompt,
            history,
            user_message
        )