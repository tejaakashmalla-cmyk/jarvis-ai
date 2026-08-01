from coding.template_loader import TemplateLoader


class CodingPlanner:

    def __init__(self):

        self.loader = TemplateLoader()

    # -------------------------------------------------
    # Create Execution Plan
    # -------------------------------------------------

    def create_plan(
        self,
        language,
        project_name
    ):

        template = self.loader.load(language)

        plan = []

        # -----------------------------------------
        # Create Project
        # -----------------------------------------

        plan.append({

            "action": "create_project",

            "project_name": project_name

        })

        # -----------------------------------------
        # Create Folder Structure
        # -----------------------------------------

        plan.append({

            "action": "create_structure",

            "folders": template["folders"]

        })

        # -----------------------------------------
        # Generate Every File
        # -----------------------------------------

        for file in template["files"]:

            plan.append({

                "action": "generate_file",

                "path": file["path"],

                "description": file["description"]

            })

        # -----------------------------------------
        # Install Dependencies
        # -----------------------------------------

        if template["install"]:

            plan.append({

                "action": "install",

                "command": template["install"]

            })

        # -----------------------------------------
        # Run Project
        # -----------------------------------------

        if template["run"]:

            plan.append({

                "action": "run",

                "command": template["run"]

            })

        # -----------------------------------------
        # Open VS Code
        # -----------------------------------------

        plan.append({

            "action": "open_vscode"

        })

        return plan