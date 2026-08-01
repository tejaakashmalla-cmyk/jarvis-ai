import json
import ollama

from config.models import CODING_MODEL

from coding.tasks.coding_task import CodingTask

from coding.specs.project_spec import (
    ProjectSpec,
    FolderSpec,
    FileSpec,
    ClassSpec,
    DependencySpec
)


class SoftwareArchitect:

    def __init__(self):

        self.model = CODING_MODEL

    # --------------------------------------------------
    # Design Project
    # --------------------------------------------------

    def design(self, task: CodingTask) -> ProjectSpec:

        system_prompt = """
You are Jarvis Software Architect.

You are a senior software architect.

You NEVER write code.

You ONLY design software.

Return ONLY valid JSON.

Schema:

{
    "framework":"",
    "entry_point":"",
    "folders":[
        "..."
    ],
    "files":[
        {
            "path":"",
            "purpose":""
        }
    ],
    "classes":[
        {
            "name":"",
            "file":"",
            "purpose":""
        }
    ],
    "dependencies":[
        "..."
    ],
    "install_command":"",
    "run_command":"",
    "build_command":"",
    "test_command":""
}

Rules:

1. Return ONLY JSON.

2. Never explain.

3. Never write code.

4. Respect ALL constraints.

5. Never invent frameworks.

6. If framework == "" then DO NOT use Flask/FastAPI/Django.

7. If platform == "cli" then create a console application.

8. If storage == "json" then use JSON.

9. If testing == false then DO NOT generate test dependencies.

10. Every class belongs to exactly one file.

11. Entry point must reference existing files.

"""

        user_prompt = f"""
Project Name:
{task.project_name}

Language:
{task.language}

Framework:
{task.framework}

Platform:
{task.platform}

UI:
{task.ui}

Storage:
{task.storage}

Architecture:
{task.architecture}

Testing:
{task.testing}

Description:
{task.description}
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

            ],

            options={
                "temperature": 0
            }

        )

        text = response["message"]["content"].strip()

        if text.startswith("```json"):
            text = text.replace("```json", "", 1)

        if text.startswith("```"):
            text = text.replace("```", "", 1)

        if text.endswith("```"):
            text = text[:-3]

        architecture = json.loads(text)

        return self._build_spec(task, architecture)

    # --------------------------------------------------
    # Convert JSON -> ProjectSpec
    # --------------------------------------------------

    def _build_spec(
        self,
        task: CodingTask,
        architecture: dict
    ) -> ProjectSpec:

        spec = ProjectSpec(

            project_name=task.project_name,

            language=task.language,

            framework=architecture.get(
                "framework",
                task.framework
            ),

            description=task.description,

            entry_point=architecture.get(
                "entry_point",
                ""
            ),

            install_command=architecture.get(
                "install_command",
                ""
            ),

            run_command=architecture.get(
                "run_command",
                ""
            ),

            build_command=architecture.get(
                "build_command",
                ""
            ),

            test_command=architecture.get(
                "test_command",
                ""
            )

        )

        # -------------------------
        # Folders
        # -------------------------

        for folder in architecture.get("folders", []):

            spec.folders.append(

                FolderSpec(folder)

            )

        # -------------------------
        # Files
        # -------------------------

        for file in architecture.get("files", []):

            spec.files.append(

                FileSpec(

                    file["path"],

                    file["purpose"]

                )

            )

        # -------------------------
        # Classes
        # -------------------------

        for cls in architecture.get("classes", []):

            spec.classes.append(

                ClassSpec(

                    cls["name"],

                    cls["file"],

                    cls["purpose"]

                )

            )

        # -------------------------
        # Dependencies
        # -------------------------

        for dep in architecture.get("dependencies", []):

            spec.dependencies.append(

                DependencySpec(dep)

            )

        return spec