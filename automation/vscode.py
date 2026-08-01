import os
import subprocess
from pathlib import Path


class VSCodeAutomation:

    def __init__(self):

        self.code_command = "code"

    # ------------------------------------
    # Open VS Code
    # ------------------------------------

    def open_vscode(self):

        try:

            subprocess.Popen([self.code_command])

            return "VS Code opened."

        except Exception as e:

            return f"VS Code Error: {e}"

    # ------------------------------------
    # Open Folder
    # ------------------------------------

    def open_folder(self, folder_path):

        folder = Path(folder_path).resolve()

        if not folder.exists():

            folder.mkdir(parents=True)

        subprocess.Popen(
            [self.code_command, str(folder)]
        )

        return f"Opened {folder.name} in VS Code."

    # ------------------------------------
    # Create Folder + Open
    # ------------------------------------

    def create_project(self, project_name):

        workspace = Path.cwd()

        project = workspace / project_name

        project.mkdir(
            parents=True,
            exist_ok=True
        )

        subprocess.Popen(
            [self.code_command, str(project)]
        )

        return str(project)

    # ------------------------------------
    # Open Existing Project
    # ------------------------------------

    def open_project(self, project_path):

        subprocess.Popen(
            [self.code_command, project_path]
        )

        return "Project opened."

    # ------------------------------------
    # Open Current Folder
    # ------------------------------------

    def open_current_folder(self):

        subprocess.Popen(
            [self.code_command, "."]
        )

        return "Current folder opened."