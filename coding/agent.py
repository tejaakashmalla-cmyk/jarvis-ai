from coding.project_manager import ProjectManager
from coding.file_editor import FileEditor
from coding.templates import Templates
from coding.terminal import Terminal


class CodingAgent:

    def __init__(self):

        self.projects = ProjectManager()

        self.editor = FileEditor()

        self.templates = Templates()

        self.terminal = Terminal()

    def create_python_project(self, name):

        root = self.projects.create_project(name)

        files = self.templates.python_project()

        for filename, content in files.items():

            self.editor.create_file(
                root / filename,
                content
            )

        return f"Python project '{name}' created successfully."