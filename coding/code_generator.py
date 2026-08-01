import ollama

from config.models import CODING_MODEL

from coding.project_context import ProjectContext
from coding.specs.project_spec import FileSpec


class CodeGenerator:

    def __init__(self):

        self.model = CODING_MODEL

    # =====================================================
    # Context-Aware Generation
    # =====================================================

    def generate(

        self,

        context: ProjectContext,

        file_spec: FileSpec,

        feedback: str = ""

    ):

        spec = context.spec

        classes = "\n".join(

            f"- {cls.name} -> {cls.file}"

            for cls in spec.classes

        )

        files = "\n".join(

            f"- {file.path}"

            for file in spec.files

        )

        generated = "\n".join(

            context.generated_files.keys()

        )

        remaining = "\n".join(

            context.remaining_files

        )

        system_prompt = f"""
You are Jarvis Coding Engine.

You are an elite senior software engineer.

Generate ONLY ONE FILE.

Return ONLY the contents of that file.

NEVER explain.

NEVER use markdown.

NEVER use ```.

PROJECT

Name:
{spec.project_name}

Language:
{spec.language}

Framework:
{spec.framework}

Description:
{spec.description}

ENTRY POINT

{spec.entry_point}

ALL FILES

{files}

ALL CLASSES

{classes}

CURRENT FILE

{context.current_file}

REMAINING FILES

{remaining}

ALREADY GENERATED FILES

{generated}

Rules

1. Generate ONLY the requested file.

2. Never generate another file.

3. Never invent class names.

4. Every class must belong to its assigned file.

5. Respect the architecture.

6. Generate production-quality code.
"""

        user_prompt = f"""
Generate ONLY

{file_spec.path}

Purpose

{file_spec.purpose}
"""

        if feedback:

            user_prompt += f"""

Previous attempt failed.

Fix the following problems ONLY.

{feedback}
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

        content = self._clean(

            response["message"]["content"]

        )

        context.add_file(

            file_spec.path,

            content

        )

        return content

    # =====================================================
    # Verified Generation
    # =====================================================

    def generate_verified(

        self,

        context: ProjectContext,

        file_spec: FileSpec,

        verifier,

        max_attempts=3

    ):

        feedback = ""

        last_errors = []

        for attempt in range(

            1,

            max_attempts + 1

        ):

            print(

                f"      Attempt {attempt}"

            )

            content = self.generate(

                context,

                file_spec,

                feedback

            )

            errors = verifier.verify(

                context,

                file_spec,

                content

            )

            if not errors:

                print(

                    "      ✓ Verification Passed"

                )

                return content

            last_errors = errors

            print(

                "      Verification Failed"

            )

            for error in errors:

                print(

                    "       -",

                    error

                )

            feedback = "\n".join(

                errors

            )

        raise Exception(

            "\n".join(last_errors)

        )

    # =====================================================
    # Legacy Wrapper
    # =====================================================

    def generate_file(

        self,

        task

    ):

        system_prompt = f"""
You are Jarvis Coding Engine.

Generate ONLY ONE FILE.

Return ONLY code.

Project

{task["project_name"]}

Language

{task["language"]}

Description

{task["project_description"]}

Existing Files

{", ".join(task["existing_files"])}
"""

        user_prompt = f"""
Generate ONLY

{task["file_path"]}

Purpose

{task["file_description"]}
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

        return self._clean(

            response["message"]["content"]

        )

    # =====================================================
    # Markdown Cleaner
    # =====================================================

    def _clean(

        self,

        content

    ):

        content = content.strip()

        if content.startswith("```"):

            lines = content.splitlines()

            lines = lines[1:]

            if lines and lines[-1].strip() == "```":

                lines = lines[:-1]

            content = "\n".join(

                lines

            )

        return content.strip()