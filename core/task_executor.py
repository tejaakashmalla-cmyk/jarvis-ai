from skills.setup import build_registry
from coding.agent import CodingAgent


class TaskExecutor:

    def __init__(self):

        self.registry = build_registry()

        self.coding = CodingAgent()

    # -------------------------------------------------
    # Execute Plan
    # -------------------------------------------------

    def execute(self, plan):

        results = []

        steps = plan.get("steps", [])

        for step in steps:

            skill = step.get("skill", "")

            # -----------------------------------------
            # Coding Tasks
            # -----------------------------------------

            if skill == "coding.create_project":

                task = {

                    "language": step.get("language", "python"),

                    "project_name": step.get("name", "MyProject"),

                    "project_description": step.get(
                        "query",
                        "Create a complete software project."
                    )

                }

                result = self.coding.execute(task)

                results.append(result)

                continue

            # -----------------------------------------
            # Browser/Desktop Skills
            # -----------------------------------------

            if skill:

                result = self.registry.execute(

                    skill,

                    **self._build_arguments(step)

                )

                results.append(result)

        return results

    # -------------------------------------------------
    # Build Arguments
    # -------------------------------------------------

    def _build_arguments(self, step):

        skill = step.get("skill", "")

        if skill.startswith("browser"):

            return {

                "query": step.get("query", "")

            }

        if skill == "desktop.open":

            return {

                "action": step.get("action", "")

            }

        return {}