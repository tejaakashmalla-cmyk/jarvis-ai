from pathlib import Path
from coding.verifier import Verifier
from coding.tasks.coding_task import CodingTask
from coding.debugger.runtime_debugger import RuntimeDebugger
from coding.software_architect import SoftwareArchitect
from coding.spec_validator import SpecValidator
from coding.code_planner import CodePlanner
from coding.project_context import ProjectContext
from coding.code_generator import CodeGenerator

from coding.project_manager import ProjectManager
from coding.file_editor import FileEditor
from coding.terminal import Terminal

from automation.vscode import VSCodeAutomation


class CodingAgent:

    def __init__(self):

        self.architect = SoftwareArchitect()

        self.validator = SpecValidator()

        self.planner = CodePlanner()

        self.generator = CodeGenerator()
        self.debugger = RuntimeDebugger()
        self.verifier = Verifier()

        self.project_manager = ProjectManager()

        self.file_editor = FileEditor()

        self.terminal = Terminal()

        self.vscode = VSCodeAutomation()

    # ===================================================
    # Execute
    # ===================================================

    def execute(
        self,
        task: CodingTask
    ):

        print()

        print("=" * 60)

        print(f"Creating {task.project_name}")

        print("=" * 60)

        print()

        # -----------------------------------------------
        # Software Architecture
        # -----------------------------------------------

        print("[1/8] Designing Project...")

        spec = self.architect.design(task)

        # -----------------------------------------------
        # Validate
        # -----------------------------------------------

        print("[2/8] Validating Specification...")

        spec = self.validator.validate(spec)

        # -----------------------------------------------
        # Generation Order
        # -----------------------------------------------

        print("[3/8] Planning Generation Order...")

        ordered_files = self.planner.create_plan(spec)

        # -----------------------------------------------
        # Project Context
        # -----------------------------------------------

        print("[4/8] Building Project Context...")

        context = ProjectContext(spec)

        context.set_remaining_files(

            [

                file.path

                for file in ordered_files

            ]

        )

        # -----------------------------------------------
        # Create Structure
        # -----------------------------------------------

        print("[5/8] Creating Project Structure...")

        project_path = self.project_manager.create_structure(

            spec

        )

        print()

        print("Project:")

        print(project_path)

        print()

        # ---------- CONTINUE WITH PART 2 ----------
        # -----------------------------------------------
        # Generate Files
        # -----------------------------------------------

        print("[6/8] Generating Files...\n")

        total = len(ordered_files)

        for index, file_spec in enumerate(ordered_files, start=1):

            print(f"[{index}/{total}] {file_spec.path}")

            # Current file

            context.set_current_file(

                file_spec.path

            )

            # Remaining files

            context.set_remaining_files(

                [

                    f.path

                    for f in ordered_files[index:]

                ]

            )

            # ------------------------------
            # AI Generation
            # ------------------------------

            content = self.generator.generate_verified(

                context,

                file_spec,

                self.verifier

            )

            # ------------------------------
            # Save File
            # ------------------------------

            destination = (

                Path(project_path)

                / file_spec.path

            )

            self.file_editor.write_file(

                destination,

                content

            )

            # ------------------------------
            # Register Generated Classes
            # ------------------------------

            for cls in spec.classes:

                if cls.file == file_spec.path:

                    context.add_class(

                        cls.name,

                        cls.file

                    )

            context.add_step(

                f"Generated {file_spec.path}"

            )

            print("   ✓ Saved")

            print()

        print()

        print("[✓] All Files Generated")

        print()

        # -----------------------------------------------
        # Open VS Code
        # -----------------------------------------------

        print("[7/8] Opening VS Code...\n")

        try:

            self.vscode.open_project(

                str(project_path)

            )

            print("[✓] VS Code Opened\n")

        except Exception as e:

            print(e)

            print()

        # ---------- CONTINUE WITH PART 3 ----------
        # -----------------------------------------------
        # Install Dependencies
        # -----------------------------------------------

        print("[8/8] Installing Dependencies...\n")

        if spec.install_command:

            result = self.terminal.run(

                spec.install_command,

                cwd=project_path

            )

            if result["success"]:

                print("[✓] Dependencies Installed")

            else:

                print(result["stderr"])

        else:

            print("No installation required.")

        print()

        # -----------------------------------------------
        # Runtime Debugger
        # -----------------------------------------------

        process = None

        if spec.run_command:

            print()

            print("[9/9] Runtime Debugger")

            print()

            result = self.debugger.debug(

    context=context,

    verifier=self.verifier,

    terminal=self.terminal,

    file_editor=self.file_editor,

    project_path=project_path,

    run_command=spec.run_command

)

            print()

            print(result)

        else:

            print()

            print("No run command defined.")

            print()

        print()

        print("=" * 60)
        print("JARVIS FINISHED SUCCESSFULLY")
        print("=" * 60)
        print()

        context.summary()

        return {

            "success": True,

            "project_name": spec.project_name,

            "project_path": str(project_path),

            "project_spec": spec,

            "context": context,

            "process": process

        }

    # ===================================================
    # Convenience API
    # ===================================================

    def execute_from_spec(

        self,

        task: CodingTask

    ):

        return self.execute(task)

    # ===================================================
    # Project Summary
    # ===================================================

    def summary(

        self,

        context: ProjectContext

    ):

        context.summary()