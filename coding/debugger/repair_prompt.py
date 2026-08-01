from coding.project_context import ProjectContext


class RepairPrompt:
    """
    Builds a repair prompt for regenerating a broken file.
    """

    # --------------------------------------------------
    # Build Repair Prompt
    # --------------------------------------------------

    def build(

        self,

        context: ProjectContext,

        error: dict

    ):

        spec = context.spec

        file_path = error["file"]

        # ------------------------------------------
        # Find Expected Classes
        # ------------------------------------------

        expected = [

            cls

            for cls in spec.classes

            if cls.file.replace("\\", "/") == file_path.replace("\\", "/")

        ]

        class_text = ""

        for cls in expected:

            class_text += (

                f"- {cls.name}: {cls.purpose}\n"

            )

        generated = context.get_file(

            file_path

        )

        prompt = f"""
You are Jarvis Repair Engine.

You are fixing ONE broken file.

PROJECT

Name:
{spec.project_name}

Language:
{spec.language}

Framework:
{spec.framework}

Description:
{spec.description}

------------------------------------------------

BROKEN FILE

{file_path}

------------------------------------------------

RUNTIME ERROR

Type:
{error['error_type']}

Message:
{error['message']}

Line:
{error['line']}

------------------------------------------------

EXPECTED CLASSES

{class_text}

------------------------------------------------

PREVIOUS IMPLEMENTATION

{generated}

------------------------------------------------

RULES

1. Rewrite ONLY this file.

2. Do NOT generate any other file.

3. Keep the architecture unchanged.

4. Fix the runtime error.

5. Do not invent extra classes.

6. Return ONLY code.

"""

        return prompt

    # --------------------------------------------------
    # Pretty Print
    # --------------------------------------------------

    def summary(

        self,

        prompt

    ):

        print("\n========== REPAIR PROMPT ==========\n")

        print(prompt)

        print("\n===================================\n")