from pathlib import Path
import shutil

from coding.specs.project_spec import ProjectSpec


class ProjectManager:

    def __init__(self, workspace=None):

        if workspace is None:

            workspace = Path.cwd() / "projects"

        self.workspace = Path(workspace)

        self.workspace.mkdir(

            parents=True,

            exist_ok=True

        )

    # ===================================================
    # Create Project
    # ===================================================

    def create_project(

        self,

        spec: ProjectSpec

    ):

        project_path = self.workspace / spec.project_name

        project_path.mkdir(

            parents=True,

            exist_ok=True

        )

        return project_path

    # ===================================================
    # Create Complete Structure
    # ===================================================

    def create_structure(

        self,

        spec: ProjectSpec

    ):

        project_path = self.create_project(spec)

        # -----------------------------------------

        # Create Folders

        # -----------------------------------------

        for folder in spec.folders:

            folder_path = project_path / folder.path

            folder_path.mkdir(

                parents=True,

                exist_ok=True

            )

        # -----------------------------------------

        # Create Empty Files

        # -----------------------------------------

        for file in spec.files:

            path = project_path / file.path

            path.parent.mkdir(

                parents=True,

                exist_ok=True

            )

            path.touch(

                exist_ok=True

            )

        return project_path

    # ===================================================
    # Delete Project
    # ===================================================

    def delete_project(

        self,

        project_name

    ):

        project = self.workspace / project_name

        if project.exists():

            shutil.rmtree(project)

            return True

        return False

    # ===================================================
    # Exists
    # ===================================================

    def exists(

        self,

        project_name

    ):

        return (

            self.workspace / project_name

        ).exists()

    # ===================================================
    # Path
    # ===================================================

    def get_path(

        self,

        project_name

    ):

        return self.workspace / project_name

    # ===================================================
    # List
    # ===================================================

    def list_projects(self):

        return [

            p.name

            for p in self.workspace.iterdir()

            if p.is_dir()

        ]

    # ===================================================
    # Summary
    # ===================================================

    def summary(

        self,

        spec: ProjectSpec

    ):

        print("\n========== PROJECT ==========\n")

        print(spec.project_name)

        print()

        print("Folders")

        for folder in spec.folders:

            print(

                "📁",

                folder.path

            )

        print()

        print("Files")

        for file in spec.files:

            print(

                "📄",

                file.path

            )

        print()

        print("Entry")

        print(

            spec.entry_point

        )

        print()

        print("=============================\n")