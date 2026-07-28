import json
import ollama


class Planner:

    def __init__(self):
        self.model = "gemma3:4b"

    def create_plan(self, user_message):

        prompt = f"""
You are Jarvis Planner.

You convert natural language into an execution plan.

Return ONLY valid JSON.

Never explain anything.
Never use markdown.
Never use ```json.

The JSON schema is:

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

Rules:

1. Browser tasks → agent="browser"
2. Desktop tasks → agent="desktop"
3. Normal questions → agent="chat"
4. If there are multiple tasks, create multiple steps.
5. Words like "then", "after that", "next", "finally", "and then" indicate a NEW step.

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
Open calculator then open Notepad then search Google for AI news

Output:
{{
    "steps": [
        {{
            "agent": "desktop",
            "action": "calculator"
        }},
        {{
            "agent": "desktop",
            "action": "notepad"
        }},
        {{
            "agent": "browser",
            "website": "google",
            "action": "search",
            "query": "AI news"
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

        # Remove markdown code fences
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