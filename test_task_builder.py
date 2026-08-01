from coding.task_builder import TaskBuilder

plan = {

    "steps": [

        {

            "skill": "coding.create_project",

            "language": "python",

            "name": "ExpenseTracker",

            "framework": "",

            "platform": "cli",

            "ui": "console",

            "storage": "json",

            "architecture": "oop",

            "testing": False,

            "query": "Professional Expense Tracker"

        }

    ]

}

builder = TaskBuilder()

task = builder.build(plan)

print(task)