from brain.brain import JarvisBrain

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

        self.memory = MemoryEngine()

        self.planner = Planner()

        self.pipeline = ResponsePipeline()

    def process(self, history, user_message):

        # Start performance timer
        monitor = PerformanceMonitor()

        # Detect intent
        intent_data = self.intent.detect(user_message)
        intent = intent_data["intent"]

        # Create execution plan
        self.planner.create_plan(
            intent,
            user_message
        )

        # Execute tools directly
        if intent == "tool":

            result = self.tools.execute(user_message)

            if result:
                yield result
                return

        # Select model
        llm = self.router.get_model(intent)

        # Build prompt
        messages = self.brain.create_messages(
            history=history,
            user_message=user_message
        )

        # Stream response
        full_response = ""

        for token in llm.stream_chat(messages):

            token = self.pipeline.process_token(token)

            full_response += token

            yield token

        # Final processing
        self.pipeline.finalize(full_response)

        # Performance logging
        elapsed = monitor.stop()

        print(f"[Jarvis] Intent: {intent}")
        print(f"[Jarvis] Time: {elapsed}s")