from coding.tasks.coding_task import CodingTask


class TaskBuilder:

    """
    Converts Planner JSON into a strongly typed CodingTask.
    """

    def build(self, plan):

        if not plan:
            raise ValueError("Plan cannot be empty.")

        steps = plan.get("steps", [])

        if not steps:
            raise ValueError("No execution steps found.")

        step = steps[0]

        if step.get("skill") != "coding.create_project":
            raise ValueError("Not a coding task.")

        return CodingTask(

            project_name=step.get(
                "name",
                "MyProject"
            ),

            language=step.get(
                "language",
                "python"
            ),

            framework=step.get(
                "framework",
                ""
            ),

            platform=step.get(
                "platform",
                "cli"
            ),

            ui=step.get(
                "ui",
                "console"
            ),

            storage=step.get(
                "storage",
                "json"
            ),

            architecture=step.get(
                "architecture",
                "oop"
            ),

            testing=step.get(
                "testing",
                False
            ),

            description=step.get(
                "query",
                ""
            )

        )