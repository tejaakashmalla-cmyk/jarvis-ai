from coding.software_architect import SoftwareArchitect
from coding.tasks.coding_task import CodingTask

architect = SoftwareArchitect()

task = CodingTask(

    project_name="ExpenseTracker",

    language="python",

    framework="",

    platform="cli",

    ui="console",

    storage="json",

    architecture="oop",

    testing=False,

    description="""
Professional Expense Tracker.

Features:

- JSON storage
- Add expenses
- Delete expenses
- Reports
- Budget
"""

)

spec = architect.design(task)

print(spec)