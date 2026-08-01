from coding.specs.project_spec import (
    ProjectSpec,
    FolderSpec,
    FileSpec,
    ClassSpec,
    DependencySpec
)

spec = ProjectSpec(

    project_name="ExpenseTracker",

    language="python",

    framework="",

    description="Professional Expense Tracker",

    entry_point="src/main.py",

    folders=[
        FolderSpec("src"),
        FolderSpec("src/models"),
        FolderSpec("src/services")
    ],

    files=[
        FileSpec(
            "src/main.py",
            "Application Entry Point"
        ),
        FileSpec(
            "src/services/expense_manager.py",
            "Business Logic"
        )
    ],

    classes=[
        ClassSpec(
            "ExpenseManager",
            "src/services/expense_manager.py",
            "Handles all expense operations."
        )
    ],

    dependencies=[
        DependencySpec(
            "prettytable"
        )
    ],

    install_command="pip install -r requirements.txt",

    run_command="python -m src.main"

)

print(spec)