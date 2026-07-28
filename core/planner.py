import json
import ollama


class Planner:

    def __init__(self):

        self.model = "gemma3:4b"

    def create_plan(self, user_message):

        prompt = f"""
You are Jarvis Planner.

Convert the user's request into JSON.

IMPORTANT:
Return ONLY valid JSON.
Do NOT use markdown.
Do NOT use ```json.
Do NOT explain anything.

Schema:

{{
    "steps": [
        {{
            "agent": "browser|desktop|chat",
            "website": "",
            "action": "",
            "query": ""
        }}
    ]
}}

Examples:

User:
Open YouTube and play Telugu songs

Output:

{{
    "steps": [
        {{
            "agent": "browser",
            "website": "youtube",
            "action": "play",
            "query": "Telugu songs"
        }}
    ]
}}

User:
Search Google for Python tutorials

Output:

{{
    "steps": [
        {{
            "agent": "browser",
            "website": "google",
            "action": "search",
            "query": "Python tutorials"
        }}
    ]
}}

User:
Open calculator

Output:

{{
    "steps": [
        {{
            "agent": "desktop",
            "action": "calculator"
        }}
    ]
}}

User:

{user_message}
"""

        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        text = response["message"]["content"]

        print("\n========== RAW GEMMA OUTPUT ==========\n")
        print(text)
        print("\n======================================\n")

        # -----------------------------
        # Remove markdown code fences
        # -----------------------------

        text = text.strip()

        if text.startswith("```json"):
            text = text.replace("```json", "", 1)

        if text.startswith("```"):
            text = text.replace("```", "", 1)

        if text.endswith("```"):
            text = text[:-3]

        text = text.strip()

        try:

            return json.loads(text)

        except Exception as e:

            print("Planner JSON Error:", e)

            return {
                "steps": [
                    {
                        "agent": "chat"
                    }
                ]
            }