from core.planner import Planner
from core.task_executor import TaskExecutor

planner = Planner()
executor = TaskExecutor()

while True:

    command = input("You: ")

    if command.lower() == "exit":
        break

    plan = planner.create_plan(command)

    print()

    print(plan)

    print()

    result = executor.execute(plan)

    print(result)

    print()