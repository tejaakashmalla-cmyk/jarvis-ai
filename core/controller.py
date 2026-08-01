from brain.brain import JarvisBrain
from core.task_executor import TaskExecutor
from core.model_router import ModelRouter
from core.planner import Planner
from core.response_pipeline import ResponsePipeline
from core.performance_monitor import PerformanceMonitor
from core.memory_engine import MemoryEngine


class JarvisController:

    def __init__(self):

        self.brain = JarvisBrain()

        self.router = ModelRouter()

        self.memory = MemoryEngine()

        self.planner = Planner()

        self.executor = TaskExecutor()

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

        print("\n========== EXECUTION PLAN ==========\n")
        print(plan)
        print("\n====================================\n")

        # ---------------------------------
        # Execute Plan
        # ---------------------------------

        results = self.executor.execute(plan)

        if results:

            for result in results:

                if result:
                    yield result

            elapsed = monitor.stop()

            print(f"[Executor] Finished in {elapsed:.2f}s")

            return

        # ---------------------------------
        # Fallback to Chat
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

        print(f"[Chat] Finished in {elapsed:.2f}s")