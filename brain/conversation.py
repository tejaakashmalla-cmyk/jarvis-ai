class ConversationManager:

    def build_messages(self, system_prompt, history, user_message):

        messages = []

        messages.append({
            "role": "system",
            "content": system_prompt
        })

        for msg in history:

            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })

        messages.append({
            "role": "user",
            "content": user_message
        })

        return messages