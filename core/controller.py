from brain.brain import JarvisBrain
from agents.browser_agent import BrowserAgent

from core.tool_router import ToolRouter
from core.model_router import ModelRouter
from core.planner import Planner
from core.response_pipeline import ResponsePipeline
from core.performance_monitor import PerformanceMonitor
from core.memory_engine import MemoryEngine


class JarvisController:

    def __init__(self):

        self.brain = JarvisBrain()

        self.router = ModelRouter()

        self.browser = BrowserAgent()

        self.tools = ToolRouter()

        self.memory = MemoryEngine()

        self.planner = Planner()

        self.pipeline = ResponsePipeline()

    def process(self, history, user_message):

        # ---------------------------------
        # Start Performance Monitor
        # ---------------------------------

        monitor = PerformanceMonitor()

        # ---------------------------------
        # Ask Planner for Execution Plan
        # ---------------------------------

        plan = self.planner.create_plan(user_message)

        steps = plan.get("steps", [])

        # ---------------------------------
        # Execute Planned Steps
        # ---------------------------------

        if steps:

            for step in steps:

                agent = step.get("agent", "").lower()

                # ---------------- Browser ----------------

                if agent == "browser":

                    website = step.get("website", "").lower()

                    action = step.get("action", "").lower()

                    query = step.get("query", "")

                    command = ""

                    if website == "youtube":

                        command = f"open youtube and play {query}"

                    elif website == "google":

                        command = f"search google {query}"

                    elif website == "github":

                        command = "open github"

                    elif website == "chatgpt":

                        command = "open chatgpt"

                    result = self.browser.execute(command)

                    if result:
                        yield result

                    elapsed = monitor.stop()

                    print(f"[Planner] Browser Task ({elapsed:.2f}s)")

                    return

                # ---------------- Desktop ----------------

                elif agent == "desktop":

                    action = step.get("action", "")

                    result = self.tools.execute(action)

                    if result:
                        yield result

                    elapsed = monitor.stop()

                    print(f"[Planner] Desktop Task ({elapsed:.2f}s)")

                    return

        # ---------------------------------
        # Normal AI Conversation
        # ---------------------------------

        llm = self.router.get_model("chat")

        messages = self.brain.create_messages(
            history=history,
            user_message=user_message
        )

        full_response = ""

        for token in llm.stream_chat(messages):

            token = self.pipeline.process_token(token)

            full_response += token

            yield token

        self.pipeline.finalize(full_response)

        elapsed = monitor.stop()

        print(f"[Planner] Chat Task ({elapsed:.2f}s)")