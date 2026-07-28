from skills.setup import build_registry


class TaskExecutor:

    def __init__(self):

        self.registry = build_registry()

    def execute(self, plan):

        results = []

        steps = plan.get("steps", [])

        for step in steps:

            skill = self._convert_to_skill(step)

            if skill is None:
                continue

            result = self.registry.execute(
                skill,
                **self._build_arguments(step)
            )

            results.append(result)

        return results

    def _convert_to_skill(self, step):

        agent = step.get("agent", "")
        website = step.get("website", "")
        action = step.get("action", "")

        if agent == "browser":

            if website == "youtube" and action == "play":
                return "browser.youtube.play"

            if website == "google" and action == "search":
                return "browser.google.search"

        elif agent == "desktop":

            return "desktop.open"

        return None

    def _build_arguments(self, step):

        agent = step.get("agent", "")

        if agent == "browser":

            return {
                "query": step.get("query", "")
            }

        elif agent == "desktop":

            return {
                "action": step.get("action", "")
            }

        return {}