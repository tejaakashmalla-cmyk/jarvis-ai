from pathlib import Path

from coding.debugger.error_parser import ErrorParser
from coding.debugger.repair_prompt import RepairPrompt
from coding.repair_engine import RepairEngine


class RuntimeDebugger:
    """
    Automatically repairs runtime errors.

    Pipeline

    Run
        ↓
    Parse Error
        ↓
    Build Repair Prompt
        ↓
    Repair Broken File
        ↓
    Verify
        ↓
    Save
        ↓
    Run Again
    """

    def __init__(self):

        self.parser = ErrorParser()

        self.repair_prompt = RepairPrompt()

        self.repair_engine = RepairEngine()

    # ==================================================
    # Debug Project
    # ==================================================

    def debug(

        self,

        context,

        verifier,

        terminal,

        file_editor,

        project_path,

        run_command,

        max_repairs=3

    ):

        print("\n========== RUNTIME DEBUGGER ==========\n")

        for attempt in range(1, max_repairs + 1):

            print(f"Repair Attempt {attempt}")

            result = terminal.run(

                run_command,

                cwd=project_path

            )

            # -----------------------------------------
            # Success
            # -----------------------------------------

            if result["success"]:

                print("\n✓ Project runs successfully.\n")

                return {

                    "success": True,

                    "attempts": attempt

                }

            # -----------------------------------------
            # Parse Runtime Error
            # -----------------------------------------

            error = self.parser.parse(

                result["stderr"]

            )

            self.parser.summary(error)

            if error.get("success", False):

                return {

                    "success": True

                }

            broken_file = error.get("file")

            if not broken_file:

                return {

                    "success": False,

                    "reason": "unable_to_parse_error"

                }

            # -----------------------------------------
            # Locate FileSpec
            # -----------------------------------------

            file_spec = None

            for file in context.spec.files:

                if (

                    file.path.replace("\\", "/")

                    ==

                    broken_file.replace("\\", "/")

                ):

                    file_spec = file

                    break

            if file_spec is None:

                print()

                print(

                    "Cannot locate file:",

                    broken_file

                )

                print()

                return {

                    "success": False,

                    "reason": "missing_file"

                }

            # -----------------------------------------
            # Build Repair Prompt
            # -----------------------------------------

            prompt = self.repair_prompt.build(

                context,

                error

            )

            self.repair_prompt.summary(

                prompt

            )

            # -----------------------------------------
            # Repair File
            # -----------------------------------------

            print()

            print(

                f"Repairing {broken_file}"

            )

            print()

            context.set_current_file(

                broken_file

            )

            content = self.repair_engine.repair(

                context=context,

                file_spec=file_spec,

                repair_prompt=prompt,

                verifier=verifier

            )

            destination = (

                Path(project_path)

                / broken_file

            )

            file_editor.write_file(

                destination,

                content

            )

            context.add_file(

                broken_file,

                content

            )

            print()

            print(

                "✓ File repaired"

            )

            print()

        print()

        print(

            "Maximum repair attempts reached."

        )

        print()

        return {

            "success": False,

            "reason": "max_repairs"

        }