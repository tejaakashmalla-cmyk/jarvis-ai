from coding.file_editor import FileEditor
from coding.project_manager import ProjectManager

pm = ProjectManager()

project = pm.create_project("ExpenseTracker")

editor = FileEditor()

editor.write_file(

    project / "main.py",

    """
print("Hello Jarvis")
"""
)

print(

    editor.read_file(

        project / "main.py"

    )

)