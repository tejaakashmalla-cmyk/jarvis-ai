from coding.verifier import Verifier
from coding.project_context import ProjectContext
from coding.specs.project_spec import (
    ProjectSpec,
    FileSpec,
    ClassSpec
)

spec = ProjectSpec(
    project_name="Demo",
    language="python"
)

spec.files.append(
    FileSpec(
        "models/user.py",
        "User model"
    )
)

spec.classes.append(
    ClassSpec(
        "User",
        "models/user.py",
        "Represents a user"
    )
)

context = ProjectContext(spec)

verifier = Verifier()

content = """
class WrongClass:
    pass
"""

errors = verifier.verify(
    context,
    spec.files[0],
    content
)

print(errors)