from coding.agent import CodingAgent
from coding.tasks.coding_task import CodingTask


def main():

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
- Edit expenses
- Monthly reports
- Budget tracking
- PrettyTable interface
"""

    )

    agent = CodingAgent()

    result = agent.execute(task)

    print("\n========== RESULT ==========\n")

    print(result)

    print("\n============================\n")


if __name__ == "__main__":

    main()