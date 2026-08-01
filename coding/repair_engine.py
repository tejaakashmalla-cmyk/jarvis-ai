import ollama

from config.models import CODING_MODEL


class RepairEngine:
    """
    Repairs an existing file using runtime errors.
    """

    def __init__(self):

        self.model = CODING_MODEL

    # =====================================================
    # Repair File
    # =====================================================

    def repair(

        self,

        context,

        file_spec,

        repair_prompt,

        verifier,

        max_attempts=3

    ):

        last_errors = []

        for attempt in range(1, max_attempts + 1):

            print(f"      Repair Attempt {attempt}")

            response = ollama.chat(

                model=self.model,

                messages=[

                    {

                        "role": "system",

                        "content": repair_prompt

                    }

                ],

                options={

                    "temperature": 0

                }

            )

            content = self._clean(

                response["message"]["content"]

            )

            errors = verifier.verify(

                context,

                file_spec,

                content

            )

            if not errors:

                print(

                    "      ✓ Repair Verified"

                )

                context.add_file(

                    file_spec.path,

                    content

                )

                return content

            last_errors = errors

            print(

                "      Repair Failed"

            )

            for error in errors:

                print(

                    "       -",

                    error

                )

            repair_prompt += "\n\n"

            repair_prompt += "Previous repair failed.\n"

            repair_prompt += "Problems:\n"

            repair_prompt += "\n".join(

                errors

            )

            repair_prompt += "\nRewrite ONLY this file."

        raise Exception(

            "\n".join(last_errors)

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