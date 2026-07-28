import ollama


class CodeGenerator:

    def __init__(self):

        self.model = "gemma3:4b"

    def generate_python(self, prompt):

        system = """
You are an expert Python developer.

Return ONLY Python code.

Do not explain.

Do not use markdown.

Do not use ```.

Only output the file contents.
"""

        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": system
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]