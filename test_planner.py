from core.planner import Planner
import json

planner = Planner()

while True:

    command = input("You: ")

    if command.lower() == "exit":
        break

    plan = planner.create_plan(command)

    print("\nExecution Plan:\n")

    print(json.dumps(plan, indent=4))