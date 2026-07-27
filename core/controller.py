from brain.brain import JarvisBrain
from agents.browser_agent import BrowserAgent

from core.tool_router import ToolRouter
from core.intent_analyzer import IntentAnalyzer
from core.model_router import ModelRouter
from core.planner import Planner
from core.response_pipeline import ResponsePipeline
from core.performance_monitor import PerformanceMonitor
from core.memory_engine import MemoryEngine


class JarvisController:

    def __init__(self):

        self.brain = JarvisBrain()

        self.intent = IntentAnalyzer()

        self.router = ModelRouter()

        self.tools = ToolRouter()

        self.browser = BrowserAgent()

        self.memory = MemoryEngine()

        self.planner = Planner()

        self.pipeline = ResponsePipeline()

    def process(self, history, user_message):

        # --------------------------------
        # Performance Monitor
        # --------------------------------

        monitor = PerformanceMonitor()

        # --------------------------------
        # Detect Intent
        # --------------------------------

        intent_data = self.intent.detect(user_message)
        intent = intent_data["intent"]

        # --------------------------------
        # Planner
        # --------------------------------

        self.planner.create_plan(
            intent,
            user_message
        )

        # --------------------------------
        # Tool Execution
        # --------------------------------

        if intent == "tool":

            command = user_message.lower()

            # Browser Commands
            if "youtube" in command or "google" in command:

                result = self.browser.execute(command)

                if result:
                    yield result
                    return

            # Desktop Commands
            result = self.tools.execute(command)

            if result:
                yield result
                return

        # --------------------------------
        # AI Chat
        # --------------------------------

        llm = self.router.get_model(intent)

        messages = self.brain.create_messages(
            history=history,
            user_message=user_message
        )

        full_response = ""

        for token in llm.stream_chat(messages):

            token = self.pipeline.process_token(token)

            full_response += token

            yield token

        # --------------------------------
        # Finalize Response
        # --------------------------------

        self.pipeline.finalize(full_response)

        # --------------------------------
        # Performance Logging
        # --------------------------------

        elapsed = monitor.stop()

        print(f"[Jarvis] Intent: {intent}")
        print(f"[Jarvis] Time: {elapsed:.2f}s")