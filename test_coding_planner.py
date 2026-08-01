from coding.planner import CodingPlanner

planner = CodingPlanner()

plan = planner.create_plan(

    language="python",

    project_name="ExpenseTracker"

)

for step in plan:

    print(step)