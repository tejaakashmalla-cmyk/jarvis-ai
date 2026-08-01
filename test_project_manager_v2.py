from coding.software_architect import SoftwareArchitect
from coding.spec_validator import SpecValidator
from coding.project_manager import ProjectManager
from coding.tasks.coding_task import CodingTask

task = CodingTask(

    project_name="ExpenseTracker",

    language="python",

    framework="",

    platform="cli",

    ui="console",

    storage="json",

    architecture="oop",

    testing=False,

    description="Professional Expense Tracker"

)

architect = SoftwareArchitect()

spec = architect.design(task)

validator = SpecValidator()

spec = validator.validate(spec)

manager = ProjectManager()

project = manager.create_structure(spec)

manager.summary(spec)

print(project)