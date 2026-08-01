from coding.code_generator import CodeGenerator

generator = CodeGenerator()

task = {

    "language": "python",

    "project_name": "ExpenseTracker",

    "project_description":
        "CLI expense tracker using JSON.",

    "file_path": "src/main.py",

    "file_description":
        "Application entry point.",

    "existing_files": [

        "README.md",

        ".gitignore",

        "requirements.txt",

        "src/expense_tracker.py"

    ]

}

content = generator.generate_file(task)

print(content)  