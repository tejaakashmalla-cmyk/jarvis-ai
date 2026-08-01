from automation.vscode import VSCodeAutomation

vs = VSCodeAutomation()

print(
    vs.create_project(
        "ExpenseTracker"
    )
)