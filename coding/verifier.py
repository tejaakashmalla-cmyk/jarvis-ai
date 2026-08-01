import re

from coding.project_context import ProjectContext
from coding.specs.project_spec import FileSpec


class Verifier:
    """
    Verifies that generated code follows the ProjectSpec.
    """

    def verify(
        self,
        context: ProjectContext,
        file_spec: FileSpec,
        content: str
    ):

        errors = []

        # -----------------------------------------
        # Markdown
        # -----------------------------------------

        if "```" in content:

            errors.append(
                "Markdown fences detected."
            )

        # -----------------------------------------
        # Expected Classes
        # -----------------------------------------

        expected = [

            cls.name

            for cls in context.spec.classes

            if cls.file.replace("\\", "/")
            == file_spec.path.replace("\\", "/")

        ]

        # -----------------------------------------
        # Find ONLY real Python class definitions
        # -----------------------------------------

        found = re.findall(

            r"^\s*class\s+([A-Za-z_][A-Za-z0-9_]*)\s*(?:\(|:)",

            content,

            re.MULTILINE

        )

        # Remove duplicates

        found = list(dict.fromkeys(found))

        # -----------------------------------------
        # Missing Classes
        # -----------------------------------------

        for cls in expected:

            if cls not in found:

                errors.append(

                    f"Missing class: {cls}"

                )

        # -----------------------------------------
        # Unexpected Classes
        # -----------------------------------------

        for cls in found:

            if cls not in expected:

                errors.append(

                    f"Unexpected class: {cls}"

                )

        # -----------------------------------------
        # Markdown Imports (optional sanity check)
        # -----------------------------------------

        if "```" in content:

            errors.append(
                "Markdown code fences detected."
            )

        return errors