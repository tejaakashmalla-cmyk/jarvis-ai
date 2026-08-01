from coding.debugger.repair_prompt import RepairPrompt

from coding.project_context import ProjectContext

from coding.specs.project_spec import (

    ProjectSpec,

    FileSpec,

    ClassSpec

)

spec = ProjectSpec(

    project_name="ExpenseTracker",

    language="python",

    framework="",

    description="Expense Tracker"

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

context.add_file(

    "models/user.py",

    """
class WrongClass:

    pass
"""

)

error = {

    "success": False,

    "file": "models/user.py",

    "line": 2,

    "error_type": "NameError",

    "message": "UserModel not defined"

}

repair = RepairPrompt()

prompt = repair.build(

    context,

    error

)

repair.summary(prompt)