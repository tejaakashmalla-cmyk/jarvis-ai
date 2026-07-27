import re


class BasicExtractor:

    def extract(self, text):

        memory = {}

        patterns = [

            (r"my favorite programming language is (.+)", "favorite_language"),

            (r"my best friend is (.+)", "best_friend"),

            (r"my goal is (.+)", "goal"),

            (r"my name is (.+)", "name"),

            (r"i study at (.+)", "college"),

        ]

        text = text.lower()

        for pattern, key in patterns:

            match = re.search(pattern, text)

            if match:

                memory[key] = match.group(1).strip().title()

        return memory