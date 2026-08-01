import json
import ollama

from config.models import PLANNER_MODEL


class Planner:

    def __init__(self):

        self.model = PLANNER_MODEL

    # -------------------------------------------------
    # Create Execution Plan
    # -------------------------------------------------

    def create_plan(self, user_message):

        system_prompt = """
You are Jarvis Planner.

You NEVER answer the user.

You ONLY return JSON.

Return ONLY valid JSON.

Never explain.

Never write code.

Never use markdown.

The schema is:

{
    "steps":[
        {
            "skill":"",
            "language":"",
            "name":"",
            "query":"",
            "action":""
        }
    ]
}

Available skills:

browser.youtube.play
browser.google.search
desktop.open
coding.create_project
chat.reply

RULES

1. Browser requests -> browser skills

2. Desktop apps -> desktop.open

3. Project creation -> coding.create_project

4. General conversation -> chat.reply

5. Always preserve the COMPLETE project description inside "query".

Examples

User:
Create a Python project called ExpenseTracker that stores data in JSON and allows add/delete/list expenses.

Output:

{
    "steps":[
        {
            "skill":"coding.create_project",
            "language":"python",
            "name":"ExpenseTracker",
            "query":"Create a Python project called ExpenseTracker that stores data in JSON and allows add/delete/list expenses."
        }
    ]
}

User:
Create a React portfolio website

Output:

{
    "steps":[
        {
            "skill":"coding.create_project",
            "language":"react",
            "name":"Portfolio",
            "query":"Create a React portfolio website"
        }
    ]
}

User:
Search Google for AI News

Output:

{
    "steps":[
        {
            "skill":"browser.google.search",
            "query":"AI News"
        }
    ]
}

User:
Open calculator

Output:

{
    "steps":[
        {
            "skill":"desktop.open",
            "action":"calculator"
        }
    ]
}

User:
What is Artificial Intelligence?

Output:

{
    "steps":[
        {
            "skill":"chat.reply"
        }
    ]
}
"""

        response = ollama.chat(

            model=self.model,

            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],

            options={
                "temperature": 0,
                "num_predict": 256
            }

        )

        text = response["message"]["content"].strip()

        print("\n========== RAW PLANNER OUTPUT ==========\n")
        print(text)
        print("\n========================================\n")

        # -----------------------------------------
        # Remove Markdown
        # -----------------------------------------

        if text.startswith("```json"):
            text = text.replace("```json", "", 1)

        if text.startswith("```"):
            text = text.replace("```", "", 1)

        if text.endswith("```"):
            text = text[:-3]

        text = text.strip()

        try:

            plan = json.loads(text)

            if "steps" not in plan:
                raise ValueError("Missing steps")

            return plan

        except Exception as e:

            print("Planner JSON Error:", e)

            return {
                "steps": [
                    {
                        "skill": "chat.reply"
                    }
                ]
            }