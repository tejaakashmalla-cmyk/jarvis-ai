from coding.software_architect import SoftwareArchitect
from coding.spec_validator import SpecValidator
from coding.code_planner import CodePlanner
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

planner = CodePlanner()

order = planner.create_plan(spec)

planner.summary(order)