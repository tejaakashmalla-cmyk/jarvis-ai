from coding.project_manager import ProjectManager

pm = ProjectManager()

project = pm.create_structure(

    project_name="ExpenseTracker",

    folders=[
        "src",
        "data",
        "assets"
    ],

    files=[
        "README.md",
        ".gitignore",
        "requirements.txt",
        "src/main.py",
        "src/utils.py"
    ]

)

print("Project Created At:")

print(project)

print("\nProjects:")

print(pm.list_projects())