import json
import ollama

from config.models import CODING_MODEL


class ProjectPlanner:

    def __init__(self):

        self.model = CODING_MODEL

    # ----------------------------------------
    # Plan Project Architecture
    # ----------------------------------------

    def plan(

        self,

        language,

        project_name,

        description

    ):

        system_prompt = """
You are Jarvis Project Architect.

You are NOT writing code.

Your ONLY job is to design the project.

Return ONLY valid JSON.

Schema:

{
    "entry_point":"",
    "classes":[
        {
            "name":"",
            "file":"",
            "purpose":""
        }
    ]
}

Rules:

1. Every class must belong to ONE file.

2. Every file may contain multiple classes.

3. main.py MUST import existing classes.

4. Never write code.

Return ONLY JSON.
"""

        user_prompt = f"""
Language:

{language}

Project:

{project_name}

Description:

{description}
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

                    "content": user_prompt

                }

            ]

        )

        text = response["message"]["content"].strip()

        if text.startswith("```json"):
            text = text.replace("```json", "", 1)

        if text.startswith("```"):
            text = text.replace("```", "", 1)

        if text.endswith("```"):
            text = text[:-3]

        return json.loads(text)